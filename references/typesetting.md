# Typesetting Hebrew exams (RTL)

## Inline math and punctuation

* Every number, unit, symbol and formula inside Hebrew text goes through `m()` (examkit). It isolates the
  left-to-right run, so "4.5 m", "sin30°" and "A′" keep their order.
* In an RTL paragraph a punctuation mark after an LTR run is drawn on its left side, next to its first character.
  "בזווית של {m('30°')}." prints ".30°", which reads like a decimal. End such sentences with a Hebrew word:
  "בזווית של 30° ביחס לאנך.", "... 150,000,000 km בקירוב.". The same applies to commas and colons. A comma after a
  Latin letter (M, N) is fine.
* A calculation typed as plain text ("2 · 4 = 8") can be reversed by the bidi algorithm: wrap it in `m()` and do not
  put punctuation right after it.
* Page references in a teacher's note: "(עמ' 39)", not "בעמ' 39;".
* Hebrew subscripts in math: `th("אוויר")` or `<sub><bdi>חומר</bdi></sub>`.
* Bind words that must not break apart with `&nbsp;`: "מראה&nbsp;1", "מכונית&nbsp;א", "4.2&nbsp;שנות אור".
* A lone Hebrew letter used as a name (גוף א) can wrap to the start of a line and look like a section label: bind it.
* Use Latin capital letters for points and objects in figures (A, B, K, L, R, M, N, O, P), primes for images (A′).
* Run `rtl_scan.py *.html` after every build; it flags the cases above.

## Layout

* A4, Heebo for text, STIX Two Text for math (loaded from Google Fonts, so building needs internet access).
* The first page: header (title, subtitle "chapters · class", name/class/date fields, grade box), then the
  instructions box (duration, number of questions, points, drawing instructions, calculator) and the formula box.
* Each question starts on a new page (`K.section`). Keep a part and its figure together with `K.keep(...)`, and a
  short part next to a small figure with `K.side_by_side(...)`.
* Answer sheets use `cls="ans"`: no page break per question, equations in boxes, results highlighted.

## Figures

* SVG built in figs.py with svgkit; every coordinate comes from data.py.
* Grids: 26 px squares; points on nodes; images behind a mirror inside the grid (extend the grid if needed).
* Labels must not touch rays or other labels: put angle labels inside the angle at a radius where it is wide enough,
  or outside with clear space; put object labels on the side away from the rays.
* Mirrors: hatching on the back side. Rays: arrows show the direction. Normals dashed. Shadows dark, partial shadows
  light. Add "(האיור אינו בקנה מידה)" to astronomical drawings.
* A drawn object must be physically right: a straw is straight above and below the water (only its image bends),
  mirror orientations reflect the ray where the text says, a ray leaving a half disk along a radius does not bend.

## Checking the PDFs

1. Page counts (`pdfinfo`): the exam should not end with a nearly empty page caused by one stray line.
2. Render every page (`render_pages.py exam.pdf --dpi 80 --sheet 2 --out <scratch>`) and look at each one: label
   collisions, a figure separated from its text, a header left alone at the bottom of a page, numbers in the wrong
   order.
3. Zoom into every figure that has many labels (render the SVG alone at a larger size with headless Chrome).
