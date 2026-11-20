# Independent checks: the blind solve and the answer-sheet audit

verify.py proves that the numbers agree with the data you chose. It cannot tell whether a question can be read
another way, whether the figure shows what the text says, or whether an explanation in the answer sheet is wrong
physics. Two independent subagents cover that, and nothing is delivered until both reports are handled.

| Check | Sees | Run |
|---|---|---|
| Blind solve | only the student document (exam PDF, review exam PDF) | one subagent per student document |
| Answer-sheet audit | the student document and its answer sheet, never the source folder | one subagent for all answer sheets |

Start them together in the background, after the documents build and pass rtl_scan, while you do the visual checks.
Past blind solves caught a ball that would hit a balcony in the drawing, ambiguous wording, punctuation that made
"2." look like "0.2", and an unrealistic setup.

## Blind solve prompt

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

## Answer-sheet audit prompt

```
You are auditing the answer sheets of a <grade> physics exam (Hebrew, RTL) before a teacher uses them for grading.
For each pair below, read the student document and its answer sheet with the Read tool (render pages with
`pdftoppm -r 150 -png <pdf> <prefix>` into <a scratch folder> for figure detail). Do NOT open the source folder or
any other file: judge only what the teacher will hold.

Pairs: "<exam PDF>" with "<exam answers PDF>"; "<review PDF>" with "<review answers PDF>".

For every sub-part, first solve it yourself from the student document, then compare with the answer sheet. Check:
1. the final answer is correct, with the right units and a precision the given data justify;
2. it answers what the sub-part actually asks (the quantity, the object, the units requested);
3. the reasoning is correct physics, uses only course material, and every given value it uses appears in the
   student document with the same value;
4. every completed drawing matches the question's figure and the computed answer;
5. nothing is missing: every sub-part of the student document has an answer, and for open questions the answer
   sheet says what a full-credit answer must contain and accepts other correct readings.

Deliverable (plain text, concise): a table per document with one row per sub-part: sub-part | your answer | answer
sheet | OK or the problem. Then a list of every problem with the exact fix. Say "none" if none. Do not edit files.
```

## Acting on the reports

1. Build the match table yourself, one row per sub-part of every student document: blind-solve answer, answer sheet,
   audit verdict. Every row must match. A small rounding difference (64.1° against 64.2°) is not an error, but state
   the answer with the precision the data justify ("≈ 64°") so the row matches.
2. For every mismatch, decide which side is wrong: a bug in data.py, an answer-sheet error, or a question that can be
   read another way. Fix the data, the wording or the answer sheet, never only the side that is easier to change.
3. Fix every other real problem in both reports.
4. Rebuild (build.py reruns verify.py), rerun rtl_scan.py and look at the changed pages again. If a question's data or
   wording changed in substance, run the blind solve again on that document.
5. Tell the teacher in one short list what the checks found and what you changed, and how many sub-parts matched
   (for example "28 מתוך 28 סעיפים תואמים").
