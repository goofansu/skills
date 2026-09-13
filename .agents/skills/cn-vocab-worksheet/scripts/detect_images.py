#!/usr/bin/env python3
"""
Detect and extract embedded images in a PDF, then emit HTML snippets
that can be pasted into the worksheet.

Usage:
  python3 detect_images.py <input.pdf>
  python3 detect_images.py <input.pdf> --extract-dir ./images --html-path-prefix ./images
  python3 detect_images.py <input.pdf> --extract-dir ./images --html-snippets ./image-snippets.html
"""

from __future__ import annotations

import argparse
import base64
import os
import re
import struct
import sys
import zlib
from typing import Iterable


OBJECT_RE = re.compile(rb"(\d+)\s+(\d+)\s+obj(.*?)endobj", re.DOTALL)
STREAM_RE = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.DOTALL)
CM_DO_RE = re.compile(
    r"([\d.]+)\s+0\s+0\s+(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)\s+cm\s*/(\w+)\s+Do"
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Detect/extract PDF embedded images")
    p.add_argument("pdf", help="Input PDF path")
    p.add_argument(
        "--extract-dir",
        help="Directory to write extracted images (jpg/png/jp2). If omitted, detection only.",
    )
    p.add_argument(
        "--html-snippets",
        help="Optional output file for generated HTML image snippets.",
    )
    p.add_argument(
        "--html-path-prefix",
        default="",
        help="Prefix prepended to image src paths in HTML snippets (e.g. ./images)",
    )
    return p.parse_args()


def parse_int(dictionary: bytes, key: bytes) -> int | None:
    m = re.search(rb"/" + key + rb"\s+(\d+)", dictionary)
    return int(m.group(1)) if m else None


def parse_colorspace(dictionary: bytes) -> str | None:
    m = re.search(rb"/ColorSpace\s*/([A-Za-z0-9]+)", dictionary)
    return m.group(1).decode("ascii", errors="ignore") if m else None


def parse_filter_chain(dictionary: bytes) -> list[str]:
    arr = re.search(rb"/Filter\s*\[(.*?)\]", dictionary, re.DOTALL)
    if arr:
        return [x.decode("ascii", errors="ignore") for x in re.findall(rb"/([A-Za-z0-9]+)", arr.group(1))]
    single = re.search(rb"/Filter\s*/([A-Za-z0-9]+)", dictionary)
    return [single.group(1).decode("ascii", errors="ignore")] if single else []


def apply_filters(data: bytes, filters: Iterable[str]) -> bytes:
    out = data
    for f in filters:
        if f == "ASCII85Decode":
            cleaned = re.sub(rb"\s+", b"", out)
            if not cleaned.endswith(b"~>"):
                cleaned += b"~>"
            out = base64.a85decode(cleaned, adobe=True)
        elif f == "FlateDecode":
            out = zlib.decompress(out)
        elif f in ("DCTDecode", "JPXDecode"):
            # Binary container format already suitable for output file.
            pass
        else:
            raise ValueError(f"Unsupported filter: {f}")
    return out


def png_chunk(tag: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(tag)
    crc = zlib.crc32(payload, crc) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", crc)


def raw_to_png(width: int, height: int, channels: int, raw: bytes) -> bytes:
    if channels not in (1, 3):
        raise ValueError("Only grayscale (1) and RGB (3) are supported for PNG conversion")
    row = width * channels
    expected = row * height
    if len(raw) != expected:
        raise ValueError(f"Raw image size mismatch: got {len(raw)}, expected {expected}")

    scanlines = bytearray()
    for y in range(height):
        scanlines.append(0)  # filter type 0
        start = y * row
        scanlines.extend(raw[start : start + row])

    color_type = 0 if channels == 1 else 2
    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    compressed = zlib.compress(bytes(scanlines), level=9)

    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", compressed)
        + png_chunk(b"IEND", b"")
    )


def detect_positions(pdf_bytes: bytes) -> list[tuple[float, float, float, float, float, str]]:
    placed = []
    for stream in re.findall(rb"stream\r?\n(.*?)\r?\nendstream", pdf_bytes, re.DOTALL):
        for decoded in decode_text_stream_candidates(stream):
            hits = CM_DO_RE.findall(decoded)
            for w, h, x, y, name in hits:
                y_mm = float(y) * 25.4 / 72
                placed.append((float(x), float(y), abs(float(w)), abs(float(h)), y_mm, name))
    return placed


def decode_text_stream_candidates(stream: bytes) -> list[str]:
    out: list[str] = []
    # Try plain latin-1 decode directly first.
    try:
        out.append(stream.decode("latin-1", errors="replace"))
    except Exception:
        pass

    # Try Flate decode.
    try:
        out.append(zlib.decompress(stream).decode("latin-1", errors="replace"))
    except Exception:
        pass

    # Try ASCII85 + Flate.
    try:
        cleaned = re.sub(rb"\s+", b"", stream)
        if not cleaned.endswith(b"~>"):
            cleaned += b"~>"
        a85 = base64.a85decode(cleaned, adobe=True)
        out.append(zlib.decompress(a85).decode("latin-1", errors="replace"))
    except Exception:
        pass

    return out


def extract_images(pdf_bytes: bytes, out_dir: str) -> list[dict]:
    os.makedirs(out_dir, exist_ok=True)

    results = []
    image_index = 0

    for obj_match in OBJECT_RE.finditer(pdf_bytes):
        obj_num = int(obj_match.group(1))
        body = obj_match.group(3)

        if b"/Subtype" not in body or b"/Image" not in body:
            continue

        stream_match = STREAM_RE.search(body)
        if not stream_match:
            continue

        dictionary = body[: stream_match.start()]
        stream_data = stream_match.group(1)
        filters = parse_filter_chain(dictionary)

        width = parse_int(dictionary, b"Width")
        height = parse_int(dictionary, b"Height")
        bpc = parse_int(dictionary, b"BitsPerComponent")
        cs = parse_colorspace(dictionary)

        image_index += 1
        stem = f"image-{image_index:02d}-obj{obj_num}"

        try:
            if "DCTDecode" in filters:
                path = os.path.join(out_dir, stem + ".jpg")
                with open(path, "wb") as f:
                    f.write(stream_data)
                results.append({"path": path, "width": width, "height": height, "object": obj_num, "filters": filters})
                continue

            if "JPXDecode" in filters:
                path = os.path.join(out_dir, stem + ".jp2")
                with open(path, "wb") as f:
                    f.write(stream_data)
                results.append({"path": path, "width": width, "height": height, "object": obj_num, "filters": filters})
                continue

            decoded = apply_filters(stream_data, filters)

            if bpc != 8 or not width or not height:
                raise ValueError("Need Width/Height and 8-bit samples for Flate image conversion")

            if cs == "DeviceGray":
                channels = 1
            elif cs == "DeviceRGB":
                channels = 3
            else:
                raise ValueError(f"Unsupported ColorSpace for PNG conversion: {cs!r}")

            png = raw_to_png(width, height, channels, decoded)
            path = os.path.join(out_dir, stem + ".png")
            with open(path, "wb") as f:
                f.write(png)
            results.append({"path": path, "width": width, "height": height, "object": obj_num, "filters": filters})

        except Exception as e:
            results.append({
                "path": None,
                "width": width,
                "height": height,
                "object": obj_num,
                "filters": filters,
                "error": str(e),
            })

    return results


def build_html_snippets(images: list[dict], prefix: str = "") -> str:
    rows = []
    for i, img in enumerate(images, 1):
        if not img.get("path"):
            rows.append(
                f"<!-- Image {i} (obj {img['object']}) not extracted: {img.get('error', 'unknown error')} -->"
            )
            continue

        rel = os.path.basename(img["path"])
        src = f"{prefix.rstrip('/')}/{rel}" if prefix else rel
        w = img.get("width") or ""
        h = img.get("height") or ""
        rows.append(
            "\n".join(
                [
                    f"<!-- Image {i} from PDF object {img['object']} ({w}x{h}) -->",
                    '<div class="pdf-image-block no-break">',
                    f'  <img src="{src}" alt="PDF embedded image {i}" class="pdf-image" />',
                    "</div>",
                ]
            )
        )
    return "\n\n".join(rows)


def main() -> int:
    args = parse_args()

    with open(args.pdf, "rb") as f:
        pdf = f.read()

    positions = detect_positions(pdf)
    if positions:
        print(f"Found {len(positions)} image placement marker(s):\n")
        for i, (x, y, w, h, y_mm, name) in enumerate(positions, 1):
            print(f"  Placement {i}: /{name}")
            print(f"    Position : x={x:.1f}pt, y={y:.1f}pt  (~{y_mm:.0f}mm from top)")
            print(f"    Size     : {w:.0f} x {h:.0f} pt  ({w*25.4/72:.0f} x {h*25.4/72:.0f} mm)")
            print()
    else:
        print("No image placement markers found.")

    if not args.extract_dir:
        return 0

    extracted = extract_images(pdf, args.extract_dir)
    ok = [x for x in extracted if x.get("path")]
    fail = [x for x in extracted if not x.get("path")]

    print(f"Extracted {len(ok)} image(s) to: {args.extract_dir}")
    if fail:
        print(f"Skipped/failed {len(fail)} image(s):")
        for f in fail:
            print(f"  - obj {f['object']}: {f.get('error', 'unknown error')}")

    snippets = build_html_snippets(ok + fail, prefix=args.html_path_prefix)
    if snippets:
        print("\nHTML snippets:\n")
        print(snippets)

    if args.html_snippets:
        with open(args.html_snippets, "w", encoding="utf-8") as out:
            out.write(snippets + "\n")
        print(f"\nSaved snippets to {args.html_snippets}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
