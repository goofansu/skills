#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <input.html>" >&2
  exit 1
fi

infile="$1"
if [ ! -f "$infile" ]; then
  echo "Input file not found: $infile" >&2
  exit 1
fi

base="${infile%.html}"
outfile="${base}.chrome-nohf.pdf"
if [ -e "$outfile" ]; then
  i=2
  while [ -e "${base}.chrome-nohf-${i}.pdf" ]; do i=$((i+1)); done
  outfile="${base}.chrome-nohf-${i}.pdf"
fi

abs_in="$(pwd)/$infile"
log_file="/tmp/chrome_print_nohf.log"

# Prefer macOS Google Chrome if present.
if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless=new \
    --disable-gpu \
    --no-pdf-header-footer \
    --print-to-pdf="$outfile" \
    "file://$abs_in" >"$log_file" 2>&1 || {
      cat "$log_file"
      exit 1
    }
  echo "$outfile"
  exit 0
fi

# Alpine/Linux fallback: use project-local chromium-headless-shell under .apkroot.
CHROMIUM_BIN="$(pwd)/.apkroot/usr/bin/chromium-headless-shell"
if [ ! -x "$CHROMIUM_BIN" ]; then
  echo "No supported Chrome/Chromium binary found." >&2
  echo "Expected one of:" >&2
  echo "  - /Applications/Google Chrome.app/Contents/MacOS/Google Chrome" >&2
  echo "  - $(pwd)/.apkroot/usr/bin/chromium-headless-shell" >&2
  exit 1
fi

LD_LIBRARY_PATH="$(pwd)/.apkroot/usr/lib/pulseaudio:$(pwd)/.apkroot/usr/lib:$(pwd)/.apkroot/lib:$(pwd)/.apkroot/usr/lib/chromium"
export LD_LIBRARY_PATH

"$CHROMIUM_BIN" \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$outfile" \
  "file://$abs_in" >"$log_file" 2>&1 || {
    cat "$log_file"
    exit 1
  }

echo "$outfile"
