# DICTATION mode (hide English worksheet)

Use this mode when the user asks for a dictation/practice version that hides English prompts.

Typical user requests:
- "Create hide-English HTML based on <unit>.html"
- "Hide English words and sentences"
- "Remove 其他"

## Command

```bash
python3 ./.agents/skills/cn-vocab-worksheet/scripts/make_hide_english_html.py "M1U1 What a mess.html"
```

Optional output filename:

```bash
python3 ./.agents/skills/cn-vocab-worksheet/scripts/make_hide_english_html.py \
  "M1U1 What a mess.html" \
  "M1U1 What a mess (hide English).html"
```

Keep the `其他` block:

```bash
python3 ./.agents/skills/cn-vocab-worksheet/scripts/make_hide_english_html.py \
  "M1U1 What a mess.html" \
  --keep-other
```

## Behavior guarantees

The script should:
- append `(默写)` to `<title>` and `<h1>`, and remove footer block
- hide `.english` and `.sentence-english` with transparent text + underline
- preserve Chinese text and original layout
- remove `<div class="grammar-section">` by default (unless `--keep-other`)
