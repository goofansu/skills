---
name: english-word-exercise
description: Create paired printable English↔Chinese word-exercise HTML from a photographed worksheet.
disable-model-invocation: true
---

# English Word Exercise

Turn a photographed bilingual vocabulary sheet into two print-ready worksheets:

1. **English → Chinese**: show only the English prompt on the left and a blank underline for Chinese.
2. **Chinese → English**: show only the Chinese prompt on the left and a blank underline for English.

## 1. Transcribe the source

Read the image and capture:

- the lesson title exactly as printed;
- every section heading, numbered row, word, phrase, part of speech, transformation arrow, note, and parenthetical;
- handwritten entries and user-supplied corrections or additions;
- the requested position of additions, such as immediately before a named entry.

Treat the lesson title as a proper name: use the exact same title in both worksheets rather than translating it.

Ask the user about genuinely ambiguous text. Do not silently invent missing content.

Completion criterion: every printed and requested handwritten entry is accounted for in source order.

## 2. Build the two prompt sets

Keep both worksheets aligned row-for-row and section-for-section.

### English → Chinese

- Keep the English word or phrase, English part-of-speech labels, and English transformation chain.
- Remove its Chinese answer.

### Chinese → English

- Keep the Chinese meaning and Chinese transformation chain.
- Remove its English answer.
- Express grammatical labels in Chinese, such as `名词`, `动词`, and `形容词`, so the prompt remains Chinese-only.

Preserve meaningful hints needed to produce the complete answer. For example, keep a Chinese plural cue when the expected English answer includes both singular and plural forms.

Completion criterion: the two prompt sets have identical entry counts and ordering, with no answer-language leakage except the unchanged lesson title.

## 3. Populate the bundled templates

Copy these files beside the source image:

- [`templates/english-to-chinese.html`](templates/english-to-chinese.html) → `<source-stem>-english-to-chinese.html`
- [`templates/chinese-to-english.html`](templates/chinese-to-english.html) → `<source-stem>-chinese-to-english.html`

Reuse the templates rather than writing HTML or CSS from scratch. In each copy, replace only the `const SHEET = { ... };` data block with the exact title, section headings, numbering, and prompts. Keep the renderer and print styles unchanged unless the user requests a layout change.

The templates already provide A4 margins, name/date fields, natural-width prompts, right-filling underlines, `9mm` handwriting rows, `8mm` section spacing, intact rows, and continuous pagination.

Completion criterion: both output files are copied from the matching template and their `SHEET` blocks contain every prompt.

## 4. Verify and hand off

Check both files for:

1. exact title preservation;
2. complete transcription, including handwriting and additions;
3. matching row counts and order;
4. correct one-language prompts;
5. underlines beginning immediately after each prompt and reaching the right margin;
6. continuous pagination without avoidable blank space, clipping, or horizontal overflow.

Open or render the files for print preview when browser tooling is available. Return both absolute output paths.
