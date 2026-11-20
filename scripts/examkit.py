"""Exam typesetting kit: Hebrew RTL A4 exams and answer sheets as HTML, printed to PDF with headless Chrome.

Copy this file into the exam's source folder (new_exam.py does it) and import it from build.py:

    import examkit as K
    body = K.header("מבחן בפיזיקה - אופטיקה", K.subtitle(...)) + K.notes(...) + K.section(1, "...", "...")
    K.build_pdf(body, title="מבחן ...", out_dir=..., html_dir=..., name="exam")

Everything inline-math goes through m(): it isolates the left-to-right run inside the Hebrew paragraph, so formulas,
numbers and units never get reordered by the bidi algorithm.
"""
import os
import platform
import shutil
import subprocess
from pathlib import Path


# ------------------------------------------------------------------ inline helpers
def m(s):
    """Inline LTR math (numbers, units, symbols). Never put . , : ; ? right after an m() that starts with a digit."""
    return f'<span class="m" dir="ltr">{s}</span>'


def frac(a, b):
    return f'<span class="frac"><span>{a}</span><span>{b}</span></span>'


def th(sub):
    """θ with a Hebrew subscript, e.g. th("אוויר")."""
    return f"<i>θ</i><sub><bdi>{sub}</bdi></sub>"


def part(label, html):
    """A lettered section: part("א", "...")."""
    return f'<div class="part"><span class="lbl">{label}.</span><div class="body">{html}</div></div>'


def sub(n, html):
    """A numbered sub-section inside a part: sub(1, "...")."""
    return f'<div class="sub"><span class="lbl">({n})</span><div>{html}</div></div>'


def eq(*lines):
    """Centered display equations (one per line), used in the answer sheets."""
    return '<div class="eq" dir="ltr">' + "".join(f"<div>{ln}</div>" for ln in lines) + "</div>"


def res(html):
    """Highlighted final result in the answer sheet."""
    return f'<span class="res">{html}</span>'


def fig(svg, width_cm, cls="fig"):
    return f'<figure class="{cls}" style="width:{width_cm}cm">{svg}</figure>'


def side_by_side(text_html, svg, width_cm):
    """Text on the right, figure on the left (RTL), kept on one page."""
    return f'<div class="row"><div class="txt">{text_html}</div><figure class="side" style="width:{width_cm}cm">{svg}</figure></div>'


def keep(html):
    """Keep a block (e.g. a part and its figure) on one page."""
    return f'<div style="break-inside: avoid">{html}</div>'


def table(rows, header_col=True):
    """rows = [[th, td, td, ...], ...]; the first cell of each row is a header cell when header_col."""
    out = ['<table class="tbl">']
    for r in rows:
        cells = [f"<th>{r[0]}</th>" if header_col else f"<td>{r[0]}</td>"] + [f"<td>{c}</td>" for c in r[1:]]
        out.append("<tr>" + "".join(cells) + "</tr>")
    return "".join(out) + "</table>"


IMP = " ⟹ "
NBSP = "&nbsp;"


# ------------------------------------------------------------------ formula sheets (book conventions)
FORMULAS = {
    "optics": [
        f"מהירות האור: {m('<i>c</i> = 3 · 10<sup>8</sup> m/s = 300,000 km/s')}",
        f"תנועה במהירות קבועה: {m('<i>s</i> = <i>v</i> · <i>t</i>')}",
        f"חוק סנל: {m(frac('sin' + th('אוויר'), 'sin' + th('חומר')) + ' = <i>n</i>')}",
        f'<span style="font-size:9pt">{m("<i>n</i>")}{NBSP}הוא מקדם השבירה של החומר ביחס לאוויר</span>',
    ],
    "mechanics": [
        m("<i>g</i> = 10 m/s<sup>2</sup>"),
        f"{m('sin37° = 0.6')}{NBSP}{NBSP} {m('cos37° = 0.8')}",
        f"{m('sin53° = 0.8')}{NBSP}{NBSP} {m('cos53° = 0.6')}",
    ],
    "electricity": [
        m("<i>k</i> = 9 · 10<sup>9</sup> N·m<sup>2</sup>/C<sup>2</sup>"),
        m("<i>ε</i><sub>0</sub> = 8.85 · 10<sup>−12</sup> C<sup>2</sup>/(N·m<sup>2</sup>)"),
        m("<i>e</i> = 1.6 · 10<sup>−19</sup> C"),
        m("<i>g</i> = 10 m/s<sup>2</sup>"),
    ],
}


# ------------------------------------------------------------------ page parts
CSS = """
  @page {
    size: A4;
    margin: 14mm 15mm 16mm 15mm;
    @bottom-center {
      content: "עמוד " counter(page) " מתוך " counter(pages);
      font-family: Heebo, Arial, sans-serif; font-size: 8.5pt; color: #8a8a8a;
    }
  }
  :root { --accent: #4a2a7f; --accent-soft: #f3eefb; --rule: #d9d2e6; --ink: #1c1b1f; --good: #2b8a3e; }
  * { box-sizing: border-box; }
  html, body { margin: 0; background: #fff; }
  body { font-family: Heebo, Arial, sans-serif; font-size: 11.4pt; line-height: 1.55; color: var(--ink); }
  p { margin: 0 0 6pt; }
  .m { font-family: 'STIX Two Text', 'Times New Roman', serif; font-size: 1.08em; unicode-bidi: isolate; white-space: nowrap; }
  .m sub, .eq sub { font-size: 0.68em; vertical-align: -0.28em; line-height: 0; }
  .m sup, .eq sup { font-size: 0.7em; vertical-align: 0.42em; line-height: 0; }
  .frac { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; line-height: 1.05; font-size: 0.86em; margin: 0 0.1em; }
  .frac > span:first-child { border-bottom: 1px solid currentColor; padding: 0 0.15em 0.05em; }
  .frac > span:last-child { padding-top: 0.05em; }

  .head { border: 1.4px solid var(--accent); border-radius: 10px; padding: 7pt 14pt 7pt; margin-bottom: 7pt; }
  .head-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 12pt; }
  .title { font-size: 20pt; font-weight: 800; color: var(--accent); line-height: 1.15; margin: 0; }
  .subtitle { font-size: 11pt; color: #555; margin-top: 2pt; }
  .grade { border: 1.2px solid var(--accent); border-radius: 8px; width: 70pt; height: 40pt; text-align: center; font-size: 9.5pt; color: var(--accent); font-weight: 600; padding-top: 3pt; flex: none; }
  .fields { display: flex; gap: 16pt; margin-top: 6pt; font-size: 10.5pt; }
  .field { display: flex; align-items: flex-end; gap: 5pt; }
  .field .line { border-bottom: 1px solid #777; height: 1.2em; }
  .notes { display: flex; gap: 10pt; margin-bottom: 9pt; font-size: 9.8pt; line-height: 1.42; }
  .box { background: var(--accent-soft); border-radius: 8px; padding: 6pt 11pt; }
  .box b { color: var(--accent); }
  .notes .box:first-child { flex: 1.3; }
  .notes .box:last-child { flex: 1; }
  .consts { display: grid; grid-template-columns: auto; gap: 2pt; margin-top: 2pt; }
  .consts .frac { font-size: 1.05em; }
  .consts .m sub { font-size: 0.8em; }

  .q { break-before: page; }
  .q.first { break-before: auto; }
  .qhead { display: flex; align-items: center; gap: 8pt; margin: 0 0 7pt; break-after: avoid; }
  .qhead span { background: var(--accent); color: #fff; font-weight: 700; font-size: 12.5pt; padding: 1pt 12pt 2pt; border-radius: 6px; }
  .qhead em { font-style: normal; color: var(--accent); font-weight: 600; font-size: 10.5pt; }
  .qhead::after { content: ""; flex: 1; height: 1.4px; background: var(--rule); }
  .part { display: grid; grid-template-columns: 1.55em 1fr; margin: 4pt 0 5pt; break-inside: avoid; }
  .part .lbl { font-weight: 700; color: var(--accent); }
  .sub { display: grid; grid-template-columns: 1.9em 1fr; }
  .sub .lbl { font-weight: 500; }
  figure { margin: 0; }
  svg { direction: ltr; }
  .fig { display: block; margin: 4pt auto 8pt; break-inside: avoid; }
  .fig svg { display: block; width: 100%; height: auto; }
  .row { display: flex; align-items: center; gap: 14pt; break-inside: avoid; }
  .row .txt { flex: 1; }
  .row .side { flex: none; }
  .row .side svg { display: block; width: 100%; height: auto; }
  .end { text-align: center; margin-top: 18pt; font-weight: 700; color: var(--accent); letter-spacing: 0.5pt; }
  .tbl { border-collapse: collapse; margin: 5pt auto 7pt; font-size: 10.8pt; }
  .tbl th, .tbl td { border: 1px solid var(--rule); padding: 3pt 13pt; text-align: center; }
  .tbl th { background: var(--accent-soft); color: var(--accent); font-weight: 600; text-align: right; }

  .teacher { background: #fff4e6; border: 1px solid #f5c48a; border-radius: 8px; padding: 5pt 11pt; font-size: 9.8pt; margin-bottom: 9pt; }
  .ans .part { margin: 3pt 0 6pt; break-inside: auto; }
  .ans .sub, .eq { break-inside: avoid; }
  .eq { font-family: 'STIX Two Text', 'Times New Roman', serif; font-size: 11.6pt; text-align: center; background: #faf8fd; border: 1px dashed #d9d2e6; border-radius: 6px; padding: 2pt 10pt; margin: 3pt auto 3pt; width: fit-content; min-width: 50%; line-height: 1.65; }
  .res { background: #e9f6ec; border: 1px solid #9fd3ad; color: #1d5e2d; border-radius: 5px; padding: 0 5pt; font-weight: 600; white-space: nowrap; }
  .ans { font-size: 11pt; }
  .ans .eq { font-size: 11.2pt; }
  .ans .q { break-before: auto; margin-top: 12pt; }
  .ans .q.first { margin-top: 0; }
  .ans .fig { margin: 3pt auto 6pt; }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800'
         '&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400;1,600&display=swap" rel="stylesheet">')


def page(title, body, cls="", extra_css=""):
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head><meta charset="utf-8"><title>{title}</title>{FONTS}<style>{CSS}{extra_css}</style></head>
<body class="{cls}">{body}</body></html>"""


def subtitle(topics, grade):
    """e.g. subtitle("פרקים א-ג: אור וראייה, החזרת אור, שבירת אור", "כיתה י׳")."""
    return f"{topics} · {grade}"


def header(title, sub_title, grade_box=True):
    """Exam header with name/class/date fields and a grade box; grade_box=False for answer sheets."""
    g = '<div class="grade">ציון</div>' if grade_box else ""
    fields = """<div class="fields">
    <div class="field" style="flex:2.2">שם התלמיד/ה:<span class="line" style="flex:1"></span></div>
    <div class="field" style="flex:1">כיתה:<span class="line" style="flex:1"></span></div>
    <div class="field" style="flex:1.3">תאריך:<span class="line" style="flex:1"></span></div>
  </div>""" if grade_box else ""
    return f"""<header class="head">
  <div class="head-top"><div><h1 class="title">{title}</h1><div class="subtitle">{sub_title}</div></div>{g}</div>
  {fields}
</header>"""


def points_text(n_questions, choose=None):
    """Instruction text for the points split. choose = how many to answer when there is a choice."""
    k = choose or n_questions
    pts = 100 / k
    p = f"{pts:g}" if pts == int(pts) else {3: "33⅓", 6: "16⅔"}.get(k, f"{pts:.1f}")
    words = {2: "שתי", 3: "שלוש", 4: "ארבע", 5: "חמש", 6: "שש"}
    total = words.get(n_questions, str(n_questions))
    if choose and choose < n_questions:
        return f"במבחן {total} שאלות. ענו על {words.get(k, k)} מהן (לכל{NBSP}שאלה{NBSP}<bdi dir=\"ltr\">{p}</bdi>{NBSP}נקודות)."
    return f"במבחן {total} שאלות. ענו על כל השאלות (לכל{NBSP}שאלה{NBSP}<bdi dir=\"ltr\">{p}</bdi>{NBSP}נקודות)."


def notes(duration, n_questions, subject=None, formulas=None, choose=None, draw_on_figures=True, extra=""):
    """Instructions box + data/formula box. duration e.g. "שעתיים"; formulas overrides FORMULAS[subject]."""
    lines = formulas if formulas is not None else FORMULAS.get(subject, [])
    draw = ("את הסרטוטים שיש להם איור בצעו על גבי האיורים שבשאלון, בעיפרון ובסרגל, ושאר הסרטוטים במחברת. הגישו את השאלון יחד עם המחברת. "
            if draw_on_figures else "יש לכתוב את התשובות במחברת הבחינה. ")
    consts = "".join(f"<span>{ln}</span>" for ln in lines)
    right = f"""<div class="box"><b>משך המבחן:</b> {duration}.<br><b>הנחיות:</b> {points_text(n_questions, choose)}
  בכל סעיף נמקו את תשובותיכם ופרטו את החישובים. {draw}מותר להשתמש במחשבון.{(' ' + extra) if extra else ''}</div>"""
    left = f'<div class="box"><b>נתונים ונוסחאות:</b><div class="consts">{consts}</div></div>' if lines else ""
    return f'<div class="notes">{right}{left}</div>'


def qhead(n, topic=""):
    em = f"<em>{topic}</em>" if topic else ""
    return f'<div class="qhead"><span>שאלה {n}</span>{em}</div>'


def section(n, topic, html, first=False):
    """One question; every question after the first starts on a new page in the exam."""
    return f'<section class="q{" first" if first else ""}">{qhead(n, topic)}{html}</section>'


def teacher_note(html):
    return f'<div class="teacher"><b>למורה.</b> {html}</div>'


END = '<div class="end">בהצלחה!</div>'


# ------------------------------------------------------------------ printing
def find_chrome():
    env = os.environ.get("CHROME")
    if env:
        return env
    candidates = {
        "Darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                   "/Applications/Chromium.app/Contents/MacOS/Chromium"],
        "Windows": [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"],
    }.get(platform.system(), [])
    for c in candidates:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    raise SystemExit("Google Chrome / Chromium not found. Install it or set the CHROME environment variable.")


def build_pdf(body, title, out_dir, html_dir, name, cls="", extra_css=""):
    """Write <html_dir>/<name>.html and print it to <out_dir>/<title>.pdf. cls="ans" for answer sheets."""
    html_dir, out_dir = Path(html_dir), Path(out_dir)
    html_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = html_dir / f"{name}.html"
    html_path.write_text(page(title, body, cls, extra_css), encoding="utf-8")
    pdf = out_dir / f"{title}.pdf"
    subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={pdf}", html_path.as_uri()], check=True, capture_output=True)
    print("wrote", pdf)
    return pdf
