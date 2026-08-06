# LEARNING mode (normal worksheet from PDF)

Use this mode when the user wants the standard study worksheet from a unit PDF.

## Must-follow rules

1. Build HTML from source PDF layout/content.
2. HTML-only output (no screenshot/OCR render pipeline).
3. Use `pdftotext` as the text extractor.
4. Always run `pdfimages -list` and preserve image blocks if present.

## Dependency check

```bash
command -v pdftotext
command -v pdfimages
```

If either is missing, stop and report which one is missing.

## Workflow

### 1) Extract layout text

```bash
bash ./.agents/skills/cn-vocab-worksheet/scripts/extract_text.sh "path/to/unit.pdf" > ./.tmp_<unit-slug>_layout.txt
```

### 2) Discover/extract embedded images

```bash
pdfimages -list "path/to/unit.pdf"
mkdir -p "images/<unit-slug>"
pdfimages -j "path/to/unit.pdf" "images/<unit-slug>/image"
```

If images exist, refresh snippet file:
- `./.tmp_<unit-slug>_image-snippets.html`

### 3) Build HTML using template

Read:
- `./.agents/skills/cn-vocab-worksheet/assets/base-template.html`

Section order:
1. 重点单词
2. 单词
3. 词组
4. 句型
5. 其他 (omit if truly empty)

Mapping:
- 重点单词 → `word-item` (3 columns, add spacers if row incomplete)
- 单词/词组 → `phrase-item` (natural width, no spacers)
- 句型 → `sentence-item`
- 其他 → notes/tables/text and preserved image blocks

## Output rules

- Save as `<UnitName>.html` next to source PDF.
- Replace `{{TITLE}}` correctly.
- Keep `.english { white-space: nowrap; }`.
- Do not add non-source explanatory text in HTML body.
- If image blocks exist, keep them semantically near related content in `其他`.
