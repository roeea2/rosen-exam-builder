# The books

This file maps Adi Rosen's physics textbooks (Weizmann Institute, Department of Science Teaching), the skill's
built-in reference. Teachers may also give any other physics textbook or their own material; for those, build the
chapter map from the material itself (SKILL.md section 2). No book is ever copied into this skill or its repository:
books are copyrighted, and every teacher gives their own copy. The map below is from one edition: when the teacher's
copy numbers its pages differently, follow the teacher's copy.

Page numbers below are printed page numbers. Check the offset in the teacher's copy on the first page you open
(in a scanned copy the PDF page usually equals the printed page; in the text-layer mechanics volume it does not).

## Contents
1. Optics: "אופטיקה גאומטרית" (קרינה וחומר, כרך א)
2. Mechanics: "מכניקה ניוטונית" כרך א and כרך ב
3. Electricity
4. How to read a chapter quickly

## 1. Optics: "אופטיקה גאומטרית" (קרינה וחומר, כרך א)

Usually a scanned PDF with no text layer (about 276 pages). Read pages as images (`render_pages.py`, 3 pages per sheet at 75 dpi).

| Chapter | Starts | Exercises ("שאלות, תרגילים ובעיות") | Topics that exercises cover |
|---|---|---|---|
| א אור וראייה | 9 | 38-43 | light and vision, sources vs reflectors, straight-line propagation, shadow and partial shadow (two sources, extended source), the ray, speed of light, light year (ex. 17), interaction with matter, Moon phases (5.4), eclipses (5.5, pp. 36-37) |
| ב החזרת אור | 45 | 77-90 | law of reflection, diffuse reflection, image in a plane mirror, ray paths to the eye on a grid, orientation / mirror writing (6, ex. 23), field of view (7, ex. 26-29), multiple images in two mirrors (8, ex. 31), periscope (10.1, p. 75), corner reflector (10.2, ex. 32, p. 83) |
| ג שבירת אור | 91 | 149-162 | air-glass and back, Snell's law, critical angle and total internal reflection, semicircular disk (ex. 9-10, n = 1.6), prisms (13-15), dispersion, table of measurements (ex. 21), apparent depth (4.1, ex. 22-23), lamp at the bottom of a pool (ex. 24), optical fibres (5.2, ex. 27), two transparent media (6), refraction in the atmosphere (7) |
| ד עדשות דקות | 163 | 201+ | thin lenses (not covered by the exams built so far) |
| ה העין וליקויי ראייה | 213 | 226+ | the eye and vision defects |

Conventions of the book: Snell's law written as sin θ_אוויר / sin θ_חומר = n (n relative to air); glass n = 1.5,
water n = 1.33; c = 3 · 10⁸ m/s = 300,000 km/s; terms "זווית הגבול" (θc), "החזרה פנימית מלאה", "צל מלא",
"צל חלקי", "מקור אור", "מחזיר אור". The relation n = c/v does not appear in the chapter-ג exercises; use it only
if the teacher confirms it was taught.

## 2. Mechanics: "מכניקה ניוטונית"

כרך א has a text layer (about 355 pages): extract with `pdftotext -layout -f N -l M`. The PDF page is ahead of the
printed page (check the offset on the first page you read).

| Volume | Chapter | Starts | Exercises |
|---|---|---|---|
| א | א קינמטיקה, תנועה לאורך קו ישר | 9 | 82-104 |
| א | ב וקטורים | 105 | 134 |
| א | ג כוחות ומצבי התמדה | 145 | 200 |
| א | ד החוק השני של ניוטון | see the table of contents (p. 6) | |
| א | ה תנועה במישור (projectiles, circular motion) | see the table of contents | |
| ב | ו תנע ושימורו | 9 | 39 |
| ב | ז אנרגיה מכנית ושימורה | 49 | 112 |
| ב | ח תנועה הרמונית פשוטה | 129 | 158 |
| ב | ט כבידה | 173 | 217 |

Each exercise collection has three parts: exercises matched to the chapter sections, summary exercises
("תרגילי סיכום", the right pool for an exam), and enrichment ("תרגילי העמקה", too hard for a regular exam).
Conventions: g = 10 m/s², sin37° = 0.6, cos37° = 0.8 (and the 53° pair), neglect air resistance unless stated.
Bagrut style for 5 units: graphs (x-t, v-t), a strobe photo, a two-body chase, a vertical or oblique throw.

## 3. Electricity

Adi Rosen's electricity book, chapter א "כוח חשמלי ושדה חשמלי" (Coulomb's law, electric field, field lines,
charged plane and capacitor, motion of charges). Teachers often have only scanned chapters, sometimes upside down:
render one page first and rotate if needed (`pdftoppm` then rotate with Pillow, or read the image upside down).
Conventions: k = 9 · 10⁹ N·m²/C², ε0 = 8.85 · 10⁻¹² C²/(N·m²), g = 10 m/s², e = 1.6 · 10⁻¹⁹ C.
Field-line drawings: the number of lines leaving a charge is proportional to the charge. Typical 12th-grade
exam: 3 book questions, שעה וחצי.

Books contain occasional errata (for example a stated charge ratio that contradicts the book's own figure).
When the text and a figure disagree, make the exam physically consistent and tell the teacher what you changed.

## 4. How to read a chapter quickly

1. Table of contents first (pages 3-8), then the chapter's section headings, then its exercise pages.
2. For scanned pages: `render_pages.py BOOK.pdf --pages 38-43 --dpi 75 --sheet 3 --out <scratch>` and read the
   sheets. Chapter summaries ("עיקרי הדברים", end-of-chapter sections) list every concept the chapter teaches.
3. Keep a short list of the concepts and the exercise numbers you base each question on: they go into the
   teacher's note at the top of the answer sheet.
4. Only ask about what the chapter teaches. Background that a physics course does not teach (for example the
   Hebrew calendar dates of eclipses) must not be needed to answer.
