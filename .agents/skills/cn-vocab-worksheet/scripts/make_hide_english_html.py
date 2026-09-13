#!/usr/bin/env python3
import argparse
import pathlib
import re


def ensure_hide_style(html: str, class_name: str) -> str:
    pattern = rf"(\n\s*\.{re.escape(class_name)}\s*\{{.*?\n\s*\}}\n)"
    m = re.search(pattern, html, flags=re.DOTALL)
    if not m:
        return html

    block = m.group(1)
    if "color: transparent;" in block and "border-bottom: 1px solid #000;" in block:
        return html

    block = re.sub(r"\n\s*\}\n$", "\n            color: transparent;\n            text-shadow: none;\n            border-bottom: 1px solid #000;\n        }\n", block)
    return html[: m.start(1)] + block + html[m.end(1) :]


def append_hide_suffix(text: str) -> str:
    if "(默写)" in text:
        return text
    if "(Hide English)" in text:
        return text.replace("(Hide English)", "(默写)")
    return f"{text} (默写)"


def update_title_h1_and_remove_footer(html: str) -> str:
    html = re.sub(
        r"(<title>)(.*?)(</title>)",
        lambda m: f"{m.group(1)}{append_hide_suffix(m.group(2))}{m.group(3)}",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"(<h1>)(.*?)(</h1>)",
        lambda m: f"{m.group(1)}{append_hide_suffix(m.group(2))}{m.group(3)}",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(r"\n\s*<div class=\"footer\">.*?</div>\s*\n", "\n", html, count=1, flags=re.DOTALL)
    return html


def find_matching_div_end(html: str, start: int) -> int:
    """Return index just after the matching </div> for a <div ...> at `start`, else -1."""
    token_re = re.compile(r"<div\b|</div>", flags=re.IGNORECASE)
    depth = 0
    for m in token_re.finditer(html, start):
        token = m.group(0).lower()
        if token.startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return m.end()
    return -1


def remove_other_section(html: str) -> str:
    # Remove only the actual "其他" block (not template comments/examples).
    h2_match = re.search(r"<h2>\s*其他\s*</h2>", html)
    if not h2_match:
        return html

    start = html.rfind('<div class="grammar-section">', 0, h2_match.start())
    if start == -1:
        return html

    end = find_matching_div_end(html, start)
    if end == -1:
        return html

    return html[:start] + html[end:]


def default_output_name(input_path: pathlib.Path) -> pathlib.Path:
    stem = input_path.stem
    if "(hide English)" in stem:
        out_stem = stem
    else:
        out_stem = f"{stem} (hide English)"
    return input_path.with_name(out_stem + input_path.suffix)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create hide-English worksheet HTML from existing unit HTML.")
    parser.add_argument("input_html", help="Source worksheet HTML file")
    parser.add_argument("output_html", nargs="?", help="Output path (default: <input> (hide English).html)")
    parser.add_argument("--keep-other", action="store_true", help="Keep the '其他' block.")
    args = parser.parse_args()

    in_path = pathlib.Path(args.input_html)
    if not in_path.exists():
        raise SystemExit(f"Input file not found: {in_path}")

    out_path = pathlib.Path(args.output_html) if args.output_html else default_output_name(in_path)

    html = in_path.read_text(encoding="utf-8")
    html = update_title_h1_and_remove_footer(html)
    html = ensure_hide_style(html, "english")
    html = ensure_hide_style(html, "sentence-english")
    if not args.keep_other:
        html = remove_other_section(html)

    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))


if __name__ == "__main__":
    main()
