# Card HTML Template

Copy this boilerplate and adapt it. Replace the placeholder rows with real data extracted from the timetable image.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box;
      -webkit-print-color-adjust: exact; print-color-adjust: exact; }

  body {
    font-family: sans-serif;
    background: #f0f0f0;
    display: flex;
    justify-content: center;
    padding: 20px;
  }

  .sheet { display: flex; flex-direction: column; width: 9cm; }

  .card {
    width: 9cm;
    background: #fff;
    border-radius: 6px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15);
    padding: 5px 6px 6px;
  }

  .card-title {
    text-align: center;
    font-size: 11pt;
    font-weight: bold;
    color: #1a3a6b;
    border-bottom: 1.5px solid #1a3a6b;
    margin-bottom: 2px;
    padding-bottom: 3px;
  }

  .card-subtitle { text-align: center; font-size: 6pt; color: #666; margin-bottom: 4px; }

  table { width: 100%; border-collapse: collapse; font-size: 7pt; }

  th, td { border: 1px solid #999; text-align: center; vertical-align: middle;
           padding: 1.5px 1px; line-height: 1.3; }

  thead th { background: #1a3a6b !important; color: #fff !important;
             font-weight: bold; font-size: 7.5pt; padding: 2px 1px; }

  td.period { background: #e8eef8 !important; color: #1a3a6b; font-weight: bold;
              font-size: 6pt; white-space: nowrap; min-width: 1.2cm; padding: 1px 2px; }

  td.period .time { font-weight: normal; font-size: 5.5pt; color: #555; display: block; }

  /* Break / activity rows — slim tinted rows between periods */
  tr.break td { background: #f0ece0 !important; color: #555; font-size: 6pt;
                font-style: italic; padding: 2px 1px; height: 12px; }

  td.subj { font-size: 7pt; font-weight: 500; }

  /* Assign a distinct color to each subject */
  .subj-1 { color: #c0392b; }
  .subj-2 { color: #1a5276; }
  .subj-3 { color: #1e8449; }
  .subj-4 { color: #6c3483; }
  .subj-5 { color: #784212; }
  .subj-6 { color: #1a6b5a; }
  .subj-7 { color: #b7770d; }
  /* Add more as needed */

  .cut-line { border-top: 1px dashed #aaa; color: #aaa; font-size: 8pt;
              margin: 3mm 0; padding-top: 1px; }

  @media print {
    @page { size: A4 portrait; margin: 8mm; }
    body { background: white; display: block; padding: 0; }
    .sheet { width: 9cm; margin: 0 auto; }
    .card { box-shadow: none; border: 1px solid #999; border-radius: 4px;
            page-break-inside: avoid; break-inside: avoid; }
    .cut-line { margin: 2mm 0; }
  }
</style>
</head>
<body>
<div class="sheet">

  <div class="card">
    <div class="card-title">Class Name</div>
    <div class="card-subtitle">Term / Year</div>
    <table>
      <thead>
        <tr>
          <th style="width:1.3cm"></th>
          <th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="period">Period 1<span class="time">8:20–9:00</span></td>
          <td class="subj"><span class="subj-1">Maths</span></td>
          <td class="subj"><span class="subj-2">English</span></td>
          <!-- ... -->
        </tr>
        <tr class="break"><td colspan="6">Break 9:00–9:30</td></tr>
        <!-- more period and break rows -->
      </tbody>
    </table>
  </div>

  <div class="cut-line">✂︎</div>

  <!-- Repeat card block for cards 2 and 3 (identical content) -->

</div>
</body>
</html>
```

Map each unique subject to a `subj-N` class and pick a distinct, readable color for each. The exact colors don't matter — just make sure no two subjects share a color.
