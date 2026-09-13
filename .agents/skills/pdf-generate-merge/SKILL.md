---
name: pdf-generate-merge
description: Convert local HTML files to PDF and merge multiple PDFs into a final document. Use when the user asks to print worksheet HTML to PDF (Chrome headless), combine PDFs in a specific order, or run an end-to-end HTML→PDF→merge pipeline.
disable-model-invocation: true
---

# PDF Generate Merge

Unified PDF skill with two focused references.

## Task routing

- **HTML to PDF**: read [HTML_TO_PDF_CHROME.md](./references/HTML_TO_PDF_CHROME.md)
- **Merge PDFs**: read [PDFUNITE_MERGE.md](./references/PDFUNITE_MERGE.md)

## Typical pipeline

1. Convert each unit HTML to PDF via `chrome_print_nohf.sh`.
2. Merge outputs via `pdfunite_merge.sh` (optionally with cover).

## Bundled scripts

- `./scripts/chrome_print_nohf.sh`
- `./scripts/pdfunite_merge.sh`

Always return clear output file paths in the handoff.
