# The blind solve

After the exam builds and passes verify.py, give it to an independent subagent that sees only the exam PDF. It solves
the exam as a strong student would and reports problems. Matching answers confirm the exam; a mismatch means either a
bug in the data or a question that can be read another way. Past blind solves caught a ball that would hit a balcony
in the drawing, ambiguous wording, punctuation that made "2." look like "0.2", and an unrealistic setup.

Do one blind solve per document that students receive (the exam and, if built, the review exam). Run them in the
background while you do other checks.

## Prompt template

```
You are checking a <grade> physics exam (Hebrew, RTL) before a teacher gives it to students. Solve it blind, as a
strong student would, using only the exam PDF. Do NOT open any other file in that folder or its source subfolder
(no answer sheet, no source code, no other exams), so your solution stays independent.

Exam PDF: "<absolute path>" (<n> pages). Read it with the Read tool. For figure detail, render pages with
`pdftoppm -r 150 -png <pdf> <prefix>` into <a scratch folder> and read the PNGs. Count grid squares carefully.

Deliverable (plain text, concise):
1. For every question and sub-part: your final answer with a one-line justification, numbers with units; for grid
   questions give positions and lengths in squares.
2. Problems noticed: ambiguous or under-specified wording, missing data, a figure that contradicts the text, physics
   errors, unrealistic data, knowledge needed that the course does not teach, and RTL typesetting glitches (a formula
   or number in the wrong order, punctuation touching a number so it looks like a decimal). Say "none" if none.
Do not edit any files.
```

## Acting on the report

* Compare every answer with the answer sheet. Fix the data or the wording for every mismatch, rebuild, and rerun
  verify.py and rtl_scan.py.
* Fix every real problem in the list. Small rounding differences (64.1° against 64.2°) are not errors: state the
  answer with the precision the data justify ("≈ 64°").
* Tell the teacher in one short list what the blind solve found and what you changed.
