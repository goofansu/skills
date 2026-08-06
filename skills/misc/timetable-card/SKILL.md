---
name: timetable-card
description: Generate a compact, printable HTML timetable card from a school schedule image. Produces 3 identical cut-out cards on one A4 page — sized to fit in a pencil box. Use this skill whenever the user provides a school timetable photo/image and wants to print a small card version, make a pocket schedule, create a pencil-box card, or print multiple copies of a class timetable on one sheet.
disable-model-invocation: true
---

# Timetable Card Skill

Turn a school timetable photo into a **print-ready A4 HTML file** containing **3 identical pocket-sized cards** — one cut line each, ready to slip into a pencil box or folder.

## What the output looks like

- **3 stacked cards** on one A4 page, separated by a dashed cut line
- Each card is **~9 cm wide × ~8.5 cm tall** — pencil-box size
- Shows **weekdays only** (周一–周五 or Mon–Fri)
- Shows **subject names only** — no teacher names
- **Color-coded subjects** for quick scanning
- Break / activity rows shown as slim tinted rows
- Works for both Chinese and English timetables

---

## Step 1 — Read and extract the timetable

Read the provided image carefully. Extract:

1. **Class name & term** (e.g. 五(4)班, 2025学年度第二学期) — shown in card header
2. **Period rows** — for each period capture:
   - Period label (第一节 / Period 1 / etc.)
   - Time range (e.g. 8:20–9:00)
   - Subject for each weekday — **strip teacher names entirely**
3. **Break / activity rows** between periods (课间大活动, 眼保健操, 午间活动, etc.) — keep these as slim rows showing label + time, they help the child orient themselves in the day
4. **After-school rows** if present (课后服务, etc.)

If a cell is empty or has a dash, render it as `—`.

> Why strip teacher names? The card is meant to be a quick at-a-glance reference for the student. Teacher names add clutter without helping the child know what lesson is next.

---

## Step 2 — Abbreviate long subject names

Long subject names must be shortened to fit the compact cell. Use judgment — abbreviate only when clearly unambiguous:

| Full name | Abbreviation |
|---|---|
| 体育与健康 | 体育 |
| 道德与法治 | 道法 |
| 艺术（音乐）| 音乐 |
| 艺术（美术）| 美术 |
| 综合实践活动 | 综合实践 |
| 兴趣活动1/2 | 兴趣1 / 兴趣2 |
| Physical Education | PE |
| Religious Education | RE |

For English timetables, apply the same principle — shorten to what students actually call the subject.

---

## Step 3 — Generate the HTML

Use the template in `references/card-template.md` as your starting point. Key rules:

### Layout & print
- **Page**: A4 portrait, 8 mm margins (`@page { size: A4 portrait; margin: 8mm }`)
- **3 cards** stacked vertically in `.sheet`, separated by `.cut-line` divs
- Each card: `width: 9cm`, no fixed height (let content flow naturally)
- Force backgrounds and colors in print: `* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }`
- Each card: `page-break-inside: avoid; break-inside: avoid`

### Table
- `border-collapse: collapse`, all borders `1px solid #999` (not thinner — they disappear in print)
- Header row: dark navy background `#1a3a6b` with white text, `!important` so print doesn't strip it
- Period label cells: light blue tint `#e8eef8 !important`
- Break rows: warm cream tint `#f0ece0 !important`, italic, slim (`height: 12px`, `padding: 2px`)
- Subject cells: `font-size: 7pt`, `font-weight: 500`
- Period label column: `font-size: 6pt`, time sub-label `5.5pt` in a `<span class="time">`

### Subject color coding
Pick readable, distinct colors. Suggested palette for Chinese primary subjects:

```css
.语文  { color: #c0392b; }   /* red */
.数学  { color: #1a5276; }   /* dark blue */
.外语  { color: #1e8449; }   /* green */
.体育  { color: #6c3483; }   /* purple */
.道法  { color: #784212; }   /* brown */
.音乐  { color: #1a6b5a; }   /* teal */
.美术  { color: #b7770d; }   /* amber */
.科学  { color: #117a65; }   /* dark teal */
.写字  { color: #555;    }   /* grey */
.劳动  { color: #7d6608; }   /* olive */
.班会  { color: #922b21; }   /* deep red */
.综合  { color: #1b4f72; }   /* navy */
.兴趣  { color: #5b2c6f; }   /* violet */
```

For English timetables, assign similar distinct colors to each subject.

Apply the color class to a `<span>` wrapping the subject text inside the `<td>`.

### Cut line between cards
```html
<div class="cut-line">✂︎ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
```
```css
.cut-line {
  border-top: 1px dashed #aaa;
  color: #aaa;
  font-size: 8pt;
  text-align: left;
  margin: 3mm 0;
  padding-top: 1px;
}
```

---

## Step 4 — Save and open

- Save the HTML file **in the same directory as the source image**, named after the class:
  e.g. `5b-card.html`, `3a-card.html`, `year4-card.html`
- Run `open <filename>` so the user can immediately preview and print
- Tell the user: **File → Print → "No margins" or set to 8mm → Print**

---

## Reference

- `references/card-template.md` — Full boilerplate HTML to copy and adapt (saves time, ensures correct print CSS)
