# Designing the questions

## Contents
1. Two modes
2. Structure of an exam
3. Difficulty levels
4. Choosing the data
5. The review exam (מבחן חזרה / מועד ב׳)
6. The answer sheet
7. Lessons from teachers' corrections

## 1. Two modes

* **New questions from the chapters (default).** The teacher names chapters or topics. Write original questions in
  the book's style, using its notation and constants, built on what its exercises practise. Do not copy exercises.
* **Specific book questions.** The teacher names exercises ("שאלה 3, 8 ו-10"). Keep the text and data verbatim,
  renumber them 1..n, redraw the figures cleanly and consistently with the data. If the stem contains a task with no
  section letter (e.g. "קבעו את סימן המטען של הטיפה. נמקו."), it becomes section א and the book's sections shift
  down. Report any book error you corrected.

## 2. Structure of an exam

* One question per chapter or topic when possible, in the order of the book.
* Each question: a short stem with a figure, then sections א, ב, ג... with sub-items (1), (2), (3). Four or five
  sections per question is typical for a 2-hour exam with 3 questions.
* Inside a question go from the concept to the calculation: an "explain why" section, a drawing section, one or two
  calculations, then a short application or a "what happens if" section.
* Mix skills across the exam: reading a figure or a grid, drawing rays or vectors, a calculation, a qualitative
  explanation with the book's terms, a table of measurements.
* Points: equal per question (3 questions: 33⅓ each) unless the teacher asks otherwise.
* Every question starts on a new page; the formula box lists only constants and relations the book gives.

## 3. Difficulty levels

| Level | What it means |
|---|---|
| קל / "לא קשות" | One idea per section, guided steps, data that give round answers, a drawing on a grid, no algebra with symbols. |
| בינוני | Two steps per calculation, one section that combines two ideas, one "explain" section that needs a careful argument. |
| בגרות (5 יח״ל) | Bagrut-style multi-step questions, symbolic derivations ("פתחו ביטוי"), graphs to read and to draw, a section that tests a misconception. |

Match the time: about 30-40 minutes of work per question at the chosen level for an average student.

## 4. Choosing the data

* Design the numbers backwards from clean answers (integers, one decimal, angles like 30°, 45°, 53°) and assert them
  in verify.py.
* Keep the data realistic: grades never above 100, a person can only hold a coin at arm's length (put it on a window
  instead), lamps and plates fit in the room, shadows land on the drawn floor, rays hit the drawn mirror.
* Grid figures: put every given point, every image and every answer point on a grid node; avoid cases on the edge
  (a ray that just touches the end of a mirror, an angle 45.0° against a critical angle of 45.6°).
* Avoid coincidences that make a figure confusing: one object directly under another object's reflection point, two
  rays meeting by accident, a label sitting on a ray.
* A table of measurements should look measured: integer degrees and a small spread (1.39, 1.42, 1.39), and say how
  to round ("עגלו כל תוצאה לשתי ספרות אחרי הנקודה").
* When a section uses a result of an earlier one, say which value to use ("השתמשו בממוצע שמצאתם בסעיף ב׳").

## 5. The review exam (מבחן חזרה / מועד ב׳)

* Same chapters, same skills, same structure and similar difficulty, but **different contexts and different numbers**.
  Changing only the numbers is not enough: teachers notice and ask for questions that are "קצת שונות". Swap the
  scenario (a street lamp becomes two lamps over a plate, a horizontal mirror becomes a wall mirror, light entering
  a block becomes light leaving it, a solar eclipse becomes a lunar eclipse).
* A מועד ב׳ must also differ from the original exam and from its review exam. A review exam built for a מועד ב׳
  should be "similar but not identical" to that מועד ב׳.
* Keep a table: question, skill, context in the exam, context in the review. Check that no context repeats.

## 6. The answer sheet

* A separate document with the same header style (no grade box) and a short teacher's note: that every number was
  computed in code, and which chapters and exercises each question is based on.
* Full solutions: the reasoning in sentences with the book's terms, the calculation in an equation box, the final
  result highlighted, and the completed drawing for every drawing section.
* For open questions, write what a full-credit answer must contain and accept equivalent correct answers (say so when
  a question can be read two ways).

## 7. Lessons from teachers' corrections

* "השאלות צריכות להיות קצת שונות": a new exam on the same material must change the questions, not only the numbers.
* Students do not learn the Hebrew calendar in physics: no question may ask for the Hebrew date of an eclipse or a
  phase. Ask about the order of the Sun, the Moon and the Earth, the shadow, or source versus reflector instead.
* "איך יכול להיות ציון מעל 100?": check every range the data imply (normal-distribution axes, heights, speeds).
* Wording that let students read a question two ways ("איזו יד מרימה הדמות, כפי שנועה רואה אותה?") was rewritten
  to one meaning ("אילו הדמות הייתה אדם אמיתי שעומד מול נועה, איזו יד שלו הייתה מורמת?").
* If a sketch has no figure in the questionnaire, say "סרטטו במחברת"; if it does, the instructions say to draw on it.
* If the teacher asks for a figure detail (e.g. "שיהיה נח לראות את המשבצות למטה בריצפה"), make that detail clearly
  visible and keep it in later versions.
