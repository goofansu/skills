# HTML → PDF (Chrome headless)

Use when converting local `.html` files to PDF.

## Requirements

- macOS Google Chrome at:
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- or project-local Linux fallback:
  `./.apkroot/usr/bin/chromium-headless-shell`

## Preferred command

```bash
bash ./.agents/skills/pdf/scripts/chrome_print_nohf.sh "M1U1 What a mess.html"
```

## Behavior

- Input must exist.
- Output naming:
  - default `<base>.chrome-nohf.pdf`
  - collision-safe increment: `<base>.chrome-nohf-2.pdf`, `<base>.chrome-nohf-3.pdf`, ...
- Prints with no header/footer.
- On failure, prints log and exits non-zero.
- On success, prints only generated PDF filename.
