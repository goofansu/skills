# Timetable Card HTML Template

Copy this boilerplate, replace the placeholder header and `<tbody>` rows, and add subject color classes as needed. The script renders two identical cards from one template.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Class timetable cards</title>
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  body {
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #f0f0f0;
    display: flex;
    justify-content: center;
    padding: 20px;
  }

  .sheet {
    display: flex;
    flex-direction: column;
    width: 13cm;
  }

  .card {
    width: 13cm;
    background: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
    padding: 7px 9px 8px;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .card-title {
    color: #1a3a6b;
    text-align: center;
    font-size: 13pt;
    font-weight: 700;
    border-bottom: 1.5px solid #1a3a6b;
    margin-bottom: 2px;
    padding-bottom: 4px;
  }

  .card-subtitle {
    color: #666;
    text-align: center;
    font-size: 7pt;
    margin-bottom: 5px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 8pt;
  }

  th, td {
    border: 1px solid #999;
    text-align: center;
    vertical-align: middle;
    padding: 2px 1.5px;
    line-height: 1.1;
  }

  thead th {
    background: #1a3a6b !important;
    color: #fff !important;
    font-size: 9pt;
    font-weight: 700;
    padding: 3px 1px;
  }

  th:first-child { width: 1.7cm; }

  td.period {
    background: #e8eef8 !important;
    color: #1a3a6b;
    font-size: 7.5pt;
    font-weight: 700;
    white-space: nowrap;
    padding: 2px 1px;
  }

  td.period .time {
    display: block;
    color: #555;
    font-size: 6.5pt;
    font-weight: 400;
  }

  td.subj {
    padding: 2px 1px;
    font-weight: 500;
    white-space: nowrap;
  }

  .course {
    display: block;
    font-size: 8pt;
    font-weight: 600;
    line-height: 1.05;
  }

  .course.long { font-size: 7.5pt; letter-spacing: -0.1px; }
  .course.xlong { font-size: 7pt; letter-spacing: -0.15px; }

  .teacher {
    display: block;
    color: #555;
    font-size: 6.3pt;
    font-weight: 400;
    line-height: 1.05;
    margin-top: 2px;
  }

  .teacher.team { font-size: 5.3pt; letter-spacing: -0.1px; }
  .teacher-only { color: #34495e; font-size: 8pt; }
  .empty { color: #999; }

  tr.break td {
    height: 16px;
    background: #f0ece0 !important;
    color: #555;
    font-size: 7pt;
    font-style: italic;
    line-height: 1.1;
    padding: 2px 1px;
  }

  /* Replace or extend these classes for the timetable's subjects. */
  .subj-1 { color: #c0392b; }
  .subj-2 { color: #1a5276; }
  .subj-3 { color: #1e8449; }
  .subj-4 { color: #6c3483; }
  .subj-5 { color: #784212; }
  .subj-6 { color: #1a6b5a; }
  .subj-7 { color: #b7770d; }
  .subj-8 { color: #117a65; }

  .cut-line {
    height: 4mm;
    border-top: 1px dashed #aaa;
    color: #aaa;
    font-size: 8pt;
    text-align: left;
    margin: 3mm 0;
    padding-top: 1px;
  }

  @media print {
    @page { size: A4 portrait; margin: 8mm; }

    body {
      background: #fff;
      display: block;
      padding: 0;
    }

    .sheet {
      width: 13cm;
      margin: 0 auto;
    }

    .card {
      box-shadow: none;
      border: 1px solid #999;
      border-radius: 4px;
    }

    .cut-line { margin: 2mm 0; }
  }
</style>
</head>
<body>
<div class="sheet" id="sheet"></div>

<template id="card-template">
  <section class="card">
    <div class="card-title">Class Name</div>
    <div class="card-subtitle">Term / Year</div>
    <table aria-label="Class timetable">
      <thead>
        <tr>
          <th>Period</th>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="period">Period 1<span class="time">8:20–9:00</span></td>
          <td class="subj"><span class="course subj-2">Maths</span><span class="teacher">Teacher A</span></td>
          <td class="subj"><span class="course subj-3">English</span><span class="teacher">Teacher B</span></td>
          <td class="subj"><span class="course subj-1">Language</span><span class="teacher">Teacher C</span></td>
          <td class="subj"><span class="course long subj-4">Physical Education</span><span class="teacher">Teacher D</span></td>
          <td class="subj"><span class="course subj-8">Science</span><span class="teacher">Teacher E</span></td>
        </tr>

        <tr class="break"><td colspan="6">Break · 9:00–9:20</td></tr>

        <tr>
          <td class="period">Period 2<span class="time">9:20–10:00</span></td>
          <td class="subj"><span class="course xlong subj-5">Full long subject name</span><span class="teacher">Teacher F</span></td>
          <td class="subj"><span class="course subj-2">Maths</span></td>
          <td class="subj teacher-only">Teacher C</td>
          <td class="subj"><span class="course subj-3">English</span><span class="teacher">Teacher B</span></td>
          <td class="subj empty">—</td>
        </tr>

        <!-- Replace with all remaining period, break, and after-school rows. -->
        <tr class="break"><td colspan="6">After-school service · 16:50–17:30</td></tr>
      </tbody>
    </table>
  </section>
</template>

<script>
  const sheet = document.getElementById('sheet');
  const card = document.getElementById('card-template');

  for (let index = 0; index < 2; index += 1) {
    sheet.appendChild(card.content.cloneNode(true));
    if (index < 1) {
      const cutLine = document.createElement('div');
      cutLine.className = 'cut-line';
      cutLine.textContent = '✂︎';
      sheet.appendChild(cutLine);
    }
  }
</script>
</body>
</html>
```
