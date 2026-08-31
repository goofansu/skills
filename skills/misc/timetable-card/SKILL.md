---
name: timetable-card
description: Generate two readable, cut-out timetable cards on one printable A4 page from a school schedule image.
disable-model-invocation: true
---

# Timetable Card

Turn a school timetable image into a print-ready A4 HTML file containing **2 identical, comfortably spaced cards** separated by a cut line.

## Step 1 — Extract the timetable

Read the image carefully and capture:

1. **Class name and term** for the card header.
2. **Period rows**, including the period label, time, full subject name, and teacher when explicitly assigned in the source.
3. **Break and activity rows** with their labels and times.
4. **After-school rows** that belong on the timetable.

Apply these transcription rules:

- Render the **full subject name above the teacher name**.
- Omit the teacher line when the source does not explicitly assign one; do not infer it from another occurrence of the subject.
- Preserve a teacher-only cell as a teacher name without inventing a subject.
- Render an empty cell as `—`.
- Confirm uncertain handwriting with the user before finalizing.

Completion criterion: every visible row and weekday cell is accounted for, including handwritten additions and user corrections.

## Step 2 — Fit full names legibly

Keep full subject names. Use the template's `.long` or `.xlong` course classes for unusually long labels rather than abbreviating them. Abbreviate only when the user requests it or the full label remains unreadable at the template's minimum long-label size.

Wrap each ordinary cell like this:

```html
<td class="subj">
  <span class="course subj-2">数学</span>
  <span class="teacher">张仲炎</span>
</td>
```

For a subject with no stated teacher, omit the teacher span. For a teacher-only cell:

```html
<td class="subj teacher-only">张仲炎</td>
```

## Step 3 — Generate the HTML

Start from [`references/card-template.md`](references/card-template.md) and replace its placeholder timetable rows.

### Layout and print

- A4 portrait with 8 mm page margins.
- **2 cards** stacked vertically with one dashed cut line between them.
- Each card and `.sheet` are **13 cm wide**.
- Cards have natural height, `page-break-inside: avoid`, and `break-inside: avoid`.
- Use exact print colors via `-webkit-print-color-adjust: exact` and `print-color-adjust: exact`.
- Render the two cards from one `<template>` so their content stays identical.

### Readability

- Table borders: `1px solid #999` with `border-collapse: collapse`.
- Header: 9 pt, navy `#1a3a6b`, white text.
- Subject: 8 pt; long labels 7.5 pt; extra-long labels 7 pt.
- Teacher: 6.3 pt with visible spacing beneath the subject.
- Period label: 7.5 pt; time: 6.5 pt.
- Break row: 7 pt, warm cream `#f0ece0`, 16 px minimum height.
- Use comfortable cell padding; preserve clear separation between subject and teacher.

### Subject colors

Assign readable, consistent colors by subject category. Apply the color class to the `.course` span, leaving teacher names neutral. Suggested palette:

```css
.语文 { color: #c0392b; }
.数学 { color: #1a5276; }
.英语 { color: #1e8449; }
.体育 { color: #6c3483; }
.道法 { color: #784212; }
.音乐 { color: #1a6b5a; }
.美术 { color: #b7770d; }
.科学 { color: #117a65; }
.信息 { color: #2471a3; }
.劳动 { color: #7d6608; }
.综合 { color: #1b4f72; }
```

For English timetables, assign equivalent distinct classes such as `.maths`, `.english`, and `.science`.

## Step 4 — Verify, save, and open

1. Save beside the source image, named after the class, such as `6-5-card.html`, `5b-card.html`, or `year4-card.html`.
2. Render or print-preview the HTML and verify that both complete cards fit on **one A4 page** without clipping or overflow. Tighten spacing slightly if needed while preserving readable type.
3. Run `open <filename>` for immediate preview.
4. Tell the user: **File → Print → use the document's 8 mm page margins → Print**.
