---
name: rosen-exam-builder
description: Builds Hebrew high-school physics exams as print-ready A4 PDFs (RTL) from Adi Rosen's textbooks (אופטיקה גאומטרית of קרינה וחומר, מכניקה ניוטונית volumes א-ב, the electricity book), with an optional review exam (מבחן חזרה / מועד ב׳) and full answer sheets. It interviews the teacher first (subject, chapters, duration, difficulty, number of questions, review exam, answer sheet), asks for the teacher's own copy of the book (PDF or chapter scans), reads the chapters, writes original bagrut-style questions with computed figures, verifies every number in code, has a blind solver check the exam and an auditor check the answer sheet. Use it whenever someone asks for a physics מבחן, בוחן, מבחן חזרה, מועד ב׳, דף תשובות or פתרון for grades 10-12 on optics, kinematics, dynamics, energy, momentum, electric force or fields, even if the book is not named, and also when they ask for an exam made of specific book exercises.
---

# Rosen exam builder

Build a physics exam the way a careful teacher would: questions rooted in the book's chapters and notation, data
chosen so the answers come out clean and realistic, figures computed from the same numbers as the answers, every
answer recomputed in code, and an independent blind solve before handing anything over.

The output is a folder with the exam PDF, optionally an answer sheet PDF, a review exam PDF and its answer sheet,
plus a `מקור/` source folder that rebuilds them.

Requirements: Python 3.12+, Google Chrome or Chromium (headless PDF printing), poppler (`pdftoppm`, `pdftotext`,
`pdfinfo`); Pillow is optional (contact sheets). Building loads the Heebo and STIX fonts from Google Fonts.

## 1. Interview the teacher

Ask only what the request does not already answer, with the AskUserQuestion tool: two rounds, with the book question
(section 2) between them. Write the questions in Hebrew, since the teacher works in Hebrew.

Round 1 (one call, up to four questions):
1. מקצוע: אופטיקה / מכניקה / חשמל.
2. כיתה ורמה: כיתה י׳ / כיתה יא׳ 5 יח״ל / כיתה יב׳ 5 יח״ל.
3. משך המבחן: שעה / שעה וחצי / שעתיים.
4. רמת קושי: קל ("שאלות לא קשות") / בינוני / ברמת בגרות.

Then get the teacher's own copy of the book (section 2) before round 2, because the topics come from its table of
contents.

Round 2, after you have the book and have looked at its table of contents:
1. נושאים: multiSelect, with the book's chapters as options (the four most likely; the teacher can type others).
   Example for optics: פרק א אור וראייה / פרק ב החזרת אור / פרק ג שבירת אור / פרק ד עדשות.
2. כמות שאלות: 2 / 3 / 4 / 5 (the usual exam is 3).
3. מבחן חזרה: כן, מבחן חזרה דומה עם הקשרים אחרים / לא.
4. דף תשובות: כן, לכל מבחן / רק למבחן הראשי / לא.

If the teacher names specific book exercises, switch to the "specific book questions" mode
(`references/exam-design.md` section 1) and skip the questions that no longer apply.

## 2. Get the teacher's own book

The books are copyrighted, so the skill ships without them and every teacher works from their own copy: a PDF of the
book, or scans or photos of the chapters. Always ask which copy to use, even when one is lying in the workspace.
Never download a book, and never copy one into the skill or into any repository.

1. Look for candidates: `python3 scripts/find_books.py <workspace> --subject <optics|mechanics|electricity>`.
2. Ask with AskUserQuestion, in Hebrew (header "הספר"): "מאיזה עותק של הספר לבנות את המבחן?"
   * one option per candidate found (file name and page count), the most likely first;
   * "אעלה את הספר שלי": the teacher drags the PDF into this window or types its full path;
   * "אין לי את הספר": build from the chapter map in `references/books.md`; say that the answer sheet will not cite
     pages or exercises.
   If no candidate was found, ask in plain text instead and wait: "כדי לבנות את המבחן מהפרקים שלמדתם אני צריך את
   הספר שלכם: גררו לכאן את קובץ ה-PDF (או סריקות של הפרקים), או כתבו את הנתיב המלא אליו."
3. Check the file: `python3 scripts/find_books.py "<path>"` prints the subject guess, the pages and whether it has a
   text layer. If it is not the right subject, say so and ask again. If it is outside the workspace, copy it into
   `<workspace>/ספרים/` so the next exam finds it (if the workspace is a git repository, add `ספרים/` to its
   .gitignore first) and tell the teacher where it is.
4. Read `references/books.md` for the chapter map and the book's conventions, then the teacher's table of contents.
   If its page numbers differ from the map (another edition), use the teacher's pages everywhere.
5. Read the chosen chapters: section headings, the chapter summary and the exercise pages.
   Scanned books: `python3 scripts/render_pages.py BOOK.pdf --pages 38-43 --dpi 75 --sheet 3 --out <scratch>`.
   Text-layer books: `pdftotext -layout -f N -l M BOOK.pdf -`.
6. Note the notation, constants and terms the book uses, and which exercises practise each skill. Ask only about
   what the chapters teach.

## 3. Design the exam

Read `references/exam-design.md` before writing questions. In short:

* One question per chapter or topic, 4-5 sections each, from concept to calculation, mixing drawing, calculation,
  explanation and figure reading.
* Choose the data backwards from clean, realistic answers; keep grid points on nodes; avoid edge cases and visual
  coincidences.
* For a review exam: same chapters, skills and difficulty, but different contexts and different numbers.

Write down, for yourself, a short plan table: question, chapter, skill per section, context, key answers (and the
review exam's context for each question). Check it against the difficulty level and the time.

## 4. Build

1. Scaffold the folder inside the teacher's workspace, in the subject's folder (for example
   `<workspace>/אופטיקה/מבחן אופטיקה י/`):
   ```
   python3 scripts/new_exam.py "<exam folder>" --subject optics --questions 3 --duration "שעתיים" \
     --title "מבחן בפיזיקה - אופטיקה גאומטרית" --file "מבחן באופטיקה גאומטרית - כיתה י" \
     --topics "פרקים א-ג: אור וראייה, החזרת אור, שבירת אור" --grade "כיתה י׳" [--answers] [--review ...]
   ```
   It creates `מקור/` with `data.py`, `verify.py`, `figs.py`, `build.py` (TODO placeholders that already build) and
   copies of `examkit.py`, `svgkit.py`, `rtl_scan.py`.
2. `data.py`: every given value and every answer, computed. Nothing in the questions or the answers is typed by hand.
3. `verify.py`: `close()` every number printed in the answer sheet and every designed "nice number", and `check()`
   every geometric fact a figure relies on. build.py imports it first, so a failed check stops the build.
4. `figs.py`: one function per figure with `answer=False/True`, drawn with svgkit from data.py.
5. `build.py`: the Hebrew text with examkit helpers (`part`, `sub`, `m`, `eq`, `res`, `fig`, `keep`, `side_by_side`,
   `table`); read `references/typesetting.md` first, the RTL rules matter.
6. Run `python3 build.py && python3 rtl_scan.py *.html` (build.py runs every verify.py check first; rtl_scan also
   fails on any TODO left from the scaffold).

## 5. Check (the gate: deliver nothing until every item passes)

Exams go to students and answer sheets are used for grading, so an error in either one is costly. Each check below
catches something the others miss.

1. Code: verify.py passes (it runs on every build) and rtl_scan.py reports 0 issues.
2. Visual: page counts, then render every page (`render_pages.py <pdf> --dpi 80 --sheet 2 --out <scratch>`) and look
   at each one; zoom into crowded figures. Fix collisions, separated figures, orphan headers.
3. Independent: follow `references/blind-solve.md`. Start a blind solve for each student document and one audit of
   all answer sheets, together, in the background.
4. Match: build the table from both reports, one row per sub-part. Every row must match; fix every mismatch and every
   real problem, rebuild, and repeat the checks on what changed.

## 6. Deliver

Tell the teacher, in Hebrew, briefly:
* what the exam contains: a small table with the question, the topic, what it asks and the key answers;
* how it was checked: the number of verify.py checks, how many sub-parts the blind solve and the audit matched, and
  what they found and you changed;
* links to the PDFs (relative paths from the workspace).

Keep everything inside the teacher's workspace (PDFs next to the `מקור/` folder). If the teacher later asks for
changes, edit `data.py` / `build.py`, rerun verify and build, and check the changed pages again.

## Files in this skill

* `scripts/examkit.py`: page layout, header, instructions and formula boxes, inline-math and section helpers, PDF printing.
* `scripts/svgkit.py`: figure primitives (rays, arcs, mirrors, lamps, eyes, people, half disk, grids, motion-graph axes).
* `scripts/new_exam.py`: scaffolds an exam folder from `templates/`.
* `scripts/find_books.py`: list candidate textbooks in a folder, or check one file the teacher gave.
* `scripts/render_pages.py`: render book pages and exam pages (contact sheets).
* `scripts/rtl_scan.py`: flags right-to-left punctuation and number-order traps, and leftover TODOs, in the built HTML.
* `references/books.md`, `references/exam-design.md`, `references/typesetting.md`,
  `references/blind-solve.md` (blind solve, answer-sheet audit, match table).
