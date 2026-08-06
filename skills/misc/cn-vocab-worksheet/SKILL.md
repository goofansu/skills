---
name: cn-vocab-worksheet
description: Create printable A4 vocabulary worksheet HTML for Chinese primary school English units, including both normal learning sheets (from PDF) and dictation sheets that hide English prompts (from existing HTML). Use when the user asks to generate/update unit worksheet HTML, create hide-English practice versions, or remove/keep the “其他” section.
disable-model-invocation: true
---

# CN Vocab Worksheet

This skill has two modes. Read only the relevant partial:

1. **LEARNING mode** (build normal worksheet HTML from PDF):
   - [LEARNING.md](./references/LEARNING.md)
2. **DICTATION mode** (hide-English worksheet from existing HTML):
   - [DICTATION.md](./references/DICTATION.md)

## Quick mode selection

- If input is a **unit PDF** and user wants a standard worksheet → use **LEARNING**.
- If input is an **existing unit HTML** and user wants “hide English / dictation / 默写” → use **DICTATION**.

## Shared constraints

- Keep output printable A4 style and preserve source-derived structure.
- Do not fabricate worksheet body content not present in source material.
- Keep file paths explicit in handoff.
