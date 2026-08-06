#!/usr/bin/env bash
# Extract layout-preserving text from a PDF using pdftotext.
# Usage: extract_text.sh <input.pdf>
# Output: prints to stdout; pipe to a file as needed.
set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <input.pdf>" >&2
    exit 1
fi

if ! command -v pdftotext >/dev/null 2>&1; then
    echo "Error: pdftotext not found. Install poppler (pdftotext) first." >&2
    exit 1
fi

pdftotext -layout "$1" -
