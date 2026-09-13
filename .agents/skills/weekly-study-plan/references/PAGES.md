# Reading a Pages study plan

Use the document preview for layout and a temporary Word export for exact run text and colors.

## Inspect the preview

A `.pages` file is normally a ZIP archive. List it, then extract only the preview into a temporary directory:

```bash
unzip -l <plan.pages>
tmp=$(mktemp -d)
unzip -q <plan.pages> preview.jpg -d "$tmp"
```

Read `preview.jpg` to recover headings, visual grouping, and item order.

## Extract exact text and colors

When Pages is installed, export a temporary `.docx` without changing the source:

```applescript
tell application "Pages"
  set d to open POSIX file "/absolute/path/to/plan.pages"
  export d to POSIX file "/tmp/plan.docx" as Microsoft Word
  close d saving no
end tell
```

Read `word/document.xml` from the DOCX archive. Each Word run contains its text in `w:t` and may contain an RGB value in `w:rPr/w:color/@w:val`. Runs without an explicit color inherit the default, usually black.

Use the preview to join split runs back into visible lines. Record each distinct RGB value and every item using it. Treat exported values as evidence of source color, while using the weekly-plan template's darker semantic colors for readable printing.

Completion criterion: the reconstructed lines match the preview, and every colored run is mapped to blue, purple, green, orange, or the actual source category before recurrence is assigned.
