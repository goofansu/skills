---
name: weekly-study-plan
description: Turn a color-coded weekly study plan into a clear, one-page printable A4 HTML checklist.
disable-model-invocation: true
---

# Weekly Study Plan

Turn a color-coded study plan into a print-ready weekly checklist that tells a student what to do each day.

## 1. Transcribe the source

For a `.pages` source, read [`references/PAGES.md`](references/PAGES.md) before transcribing.

Capture:

- the title and start time;
- every subject, task, quantity, duration, and frequency;
- which items are daily;
- each weekday heading and every item governed by it;
- the source color of every item.

Treat a weekday heading as governing all following items in that subject block until another heading or subject begins. Confirm genuinely ambiguous text with the user.

Completion criterion: every visible item is accounted for in source order, with its color and recurrence recorded.

## 2. Build the recurrence model

Classify items into the template's three groups:

- `dailyGroups`: items required every day. The template renders one checkbox per weekday, Monday through Sunday.
- `purple`: scheduled practice for a stated weekday pair.
- `green`: the second scheduled group for the same weekday pair.

Put **every purple and green item in both stated weekday cards**. A pair such as `周一、周四` produces separate `周一` and `周四` cards containing the same complete task list. Keep frequency text such as `一周一次` on both cards; it remains a weekly frequency, not an instruction to split or rewrite the item.

Render Monday through Saturday as six separate cards. Sunday contains only daily work unless the source explicitly assigns more.

Normalize time units to Chinese:

- `10min` → `10分钟`
- `10～20` when it denotes time → `10～20分钟`
- a bare time value such as `20` → `20分钟`

Preserve non-time quantities and weekly frequencies verbatim.

Completion criterion: every scheduled group is attached to its full weekday pair, both cards contain the same items, and every time value has an explicit `分钟` unit.

## 3. Populate the template

Copy [`templates/weekly-study-plan.html`](templates/weekly-study-plan.html) beside the source as `<source-stem>-weekly-study-plan.html`.

Replace only the `const PLAN = { ... };` data block:

- `dailyGroups` holds subject groups and daily tasks.
- `scheduledGroups` holds a subject, its weekday pair, and the complete purple/green task list.
- Use `tone: "purple"` or `tone: "green"` on every scheduled task.
- Keep task numbers when the source provides them.

The renderer duplicates each `scheduledGroups` task list into every day named by `days`. Keep the renderer and print CSS unchanged unless the user requests a layout change.

The template applies corresponding colors to the full task text, duration, number badge, and checkbox border. Its darker screen/print colors intentionally preserve readability rather than reproducing faint source colors exactly.

## 4. Verify and hand off

Render or print-preview the result and verify:

1. all daily tasks appear in the daily table with seven checkboxes;
2. Monday through Saturday each have a visible card;
3. every paired-day card contains the complete purple and green lists;
4. all durations use `分钟`;
5. task text uses its corresponding blue, purple, or green;
6. the complete plan fits on one unclipped A4 landscape page.

Save a PDF beside the HTML when Chrome or another browser print tool is available. Return both absolute output paths.
