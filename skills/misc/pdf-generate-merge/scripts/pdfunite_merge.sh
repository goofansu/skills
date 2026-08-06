#!/usr/bin/env bash
set -euo pipefail

cover=""
pattern="*.pdf"
out="merged.pdf"
dir="."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cover)
      cover="${2:-}"
      shift 2
      ;;
    --pattern)
      pattern="${2:-}"
      shift 2
      ;;
    --output)
      out="${2:-}"
      shift 2
      ;;
    --dir)
      dir="${2:-}"
      shift 2
      ;;
    -h|--help)
      cat <<'EOF'
Usage:
  pdfunite_merge.sh [--cover FILE] [--pattern GLOB] [--output FILE] [--dir DIR]

Examples:
  pdfunite_merge.sh --cover "封面.pdf" --pattern "*.chrome-nohf.pdf" --output "all.pdf"
  pdfunite_merge.sh --pattern "*.pdf" --output "merged.pdf"
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

command -v pdfunite >/dev/null 2>&1 || { echo "pdfunite not found in PATH" >&2; exit 127; }
[[ -d "$dir" ]] || { echo "Directory not found: $dir" >&2; exit 1; }

inputs=()

if [[ -n "$cover" ]]; then
  [[ -f "$dir/$cover" ]] || { echo "Cover PDF not found: $dir/$cover" >&2; exit 1; }
  inputs+=("$dir/$cover")
fi

while IFS= read -r -d '' f; do
  b="$(basename "$f")"
  [[ -n "$cover" && "$b" == "$cover" ]] && continue
  [[ "$b" == "$out" ]] && continue
  inputs+=("$f")
done < <(find "$dir" -maxdepth 1 -type f -name "$pattern" -print0 | sort -z)

if [[ ${#inputs[@]} -eq 0 ]]; then
  echo "No input PDFs found (pattern: $pattern in $dir)" >&2
  exit 1
fi

base="$out"
if [[ "$out" == *.pdf ]]; then
  stem="${out%.pdf}"
  ext=".pdf"
else
  stem="$out"
  ext=""
fi

outfile="$dir/$base"
if [[ -e "$outfile" ]]; then
  i=2
  while [[ -e "$dir/${stem}-${i}${ext}" ]]; do
    i=$((i+1))
  done
  outfile="$dir/${stem}-${i}${ext}"
fi

pdfunite "${inputs[@]}" "$outfile"

echo "$(basename "$outfile")"
