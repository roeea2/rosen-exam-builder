---
name: rosen-exam-builder
description: Builds Hebrew high-school physics exams as print-ready A4 PDFs (RTL) from Adi Rosen's textbooks (אופטיקה גאומטרית of קרינה וחומר, מכניקה ניוטונית volumes א-ב, the electricity book), with an optional review exam (מבחן חזרה / מועד ב׳) and full answer sheets. It interviews the teacher first (subject, chapters, duration, difficulty, number of questions, review exam, answer sheet), reads the chapters, writes original bagrut-style questions with computed figures, verifies every number in code and has a blind solver check the exam. Use it whenever someone asks for a physics מבחן, בוחן, מבחן חזרה, מועד ב׳, דף תשובות or פתרון for grades 10-12 on optics, kinematics, dynamics, energy, momentum, electric force or fields, even if the book is not named, and also when they ask for an exam made of specific book exercises.
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

Ask only what the request does not already answer, with the AskUserQuestion tool, in at most two rounds. Write the
questions in Hebrew, since the teacher works in Hebrew.

Round 1 (one call, up to four questions):
1. מקצוע: אופטיקה / מכניקה / חשמל.
2. כיתה ורמה: כיתה י׳ / כיתה יא׳ 5 יח״ל / כיתה יב׳ 5 יח״ל.
3. משך המבחן: שעה / שעה וחצי / שעתיים.
4. רמת קושי: קל ("שאלות לא קשות") / בינוני / ברמת בגרות.

Round 2, after you know the subject and have looked at the book's table of contents:
1. נושאים: multiSelect, with the book's chapters as options (the four most likely; the teacher can type others).
   Example for optics: פרק א אור וראייה / פרק ב החזרת אור / פרק ג שבירת אור / פרק ד עדשות.
2. כמות שאלות: 2 / 3 / 4 / 5 (the usual exam is 3).
3. מבחן חזרה: כן, מבחן חזרה דומה עם הקשרים אחרים / לא.
4. דף תשובות: כן, לכל מבחן / רק למבחן הראשי / לא.

If the teacher names specific book exercises, switch to the "specific book questions" mode
(`references/exam-design.md` section 1) and skip the questions that no longer apply.

## 2. Find and read the book

1. Locate the PDF: `python3 scripts/find_books.py <workspace>`. If nothing is found, ask for the path. Never copy the
   book into the skill or the repository: it is copyrighted.
2. Read `references/books.md` for the chapter map, page numbers and the book's conventions.
3. Read the chosen chapters: table of contents, section headings, the chapter summary and the exercise pages.
   Scanned books: `python3 scripts/render_pages.py BOOK.pdf --pages 38-43 --dpi 75 --sheet 3 --out <scratch>`.
   Text-layer books: `pdftotext -layout -f N -l M BOOK.pdf -`.
4. Note the notation, constants and terms the book uses, and which exercises practise each skill. Ask only about
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
3. `verify.py`: assert every number printed in the answer sheet, every designed "nice number", and every geometric
   fact a figure relies on. Run it until it passes.
4. `figs.py`: one function per figure with `answer=False/True`, drawn with svgkit from data.py.
5. `build.py`: the Hebrew text with examkit helpers (`part`, `sub`, `m`, `eq`, `res`, `fig`, `keep`, `side_by_side`,
   `table`); read `references/typesetting.md` first, the RTL rules matter.
6. Run `python3 verify.py && python3 build.py && python3 rtl_scan.py *.html`.

## 5. Check

1. Page counts, then render every page (`render_pages.py <pdf> --dpi 80 --sheet 2 --out <scratch>`) and look at
   each one; zoom into crowded figures. Fix collisions, separated figures, orphan headers.
2. Blind solve: follow `references/blind-solve.md` (one subagent per student document, run in the background).
3. Fix what the blind solve finds, rebuild, rerun verify.py and rtl_scan.py.

## 6. Deliver

Tell the teacher, in Hebrew, briefly:
* what the exam contains: a small table with the question, the topic, what it asks and the key answers;
* how it was checked (code verification, blind solve and what it changed);
* links to the PDFs (relative paths from the workspace).

Keep everything inside the teacher's workspace (PDFs next to the `מקור/` folder). If the teacher later asks for
changes, edit `data.py` / `build.py`, rerun verify and build, and check the changed pages again.

## Files in this skill

* `scripts/examkit.py`: page layout, header, instructions and formula boxes, inline-math and section helpers, PDF printing.
* `scripts/svgkit.py`: figure primitives (rays, arcs, mirrors, lamps, eyes, people, half disk, grids, motion-graph axes).
* `scripts/new_exam.py`: scaffolds an exam folder from `templates/`.
* `scripts/find_books.py`, `scripts/render_pages.py`: find the textbooks, render book pages and exam pages.
* `scripts/rtl_scan.py`: flags right-to-left punctuation and number-order traps in the built HTML.
* `references/books.md`, `references/exam-design.md`, `references/typesetting.md`, `references/blind-solve.md`.
