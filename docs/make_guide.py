"""Builds docs/rosen-exam-builder-guide.pdf: a one-page Hebrew install and usage guide.

    python3 docs/make_guide.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from examkit import find_chrome  # noqa: E402

REPO = "https://github.com/roeea2/rosen-exam-builder"

LOGO = r"""   _______
  /       \      ____                             _      ___
 /  \ | /  \    |  _ \    ___     ___    ___     / \    |_ _|
|  -- O --  |   | |_) |  / _ \   / _ \  / _ \   / _ \    | |
 \  / | \  /    |  _ &lt;  | (_) | |  __/ |  __/  / ___ \   | |
  \_______/     |_| \_\  \___/   \___|  \___| /_/   \_\ |___|"""

CSS = """
@page { size: A4; margin: 10mm 12mm 9mm 12mm; }
* { box-sizing: border-box; }
html, body { margin: 0; background: #fff; }
body { font-family: Heebo, Arial, sans-serif; font-size: 10.2pt; line-height: 1.42; color: #1c1b1f; }
.top { background: linear-gradient(135deg, #2a1650, #4a2a7f 60%, #6a3fb0); color: #fff; border-radius: 12px; padding: 7pt 14pt 8pt; text-align: center; }
.logo { font-family: 'JetBrains Mono', Menlo, Consolas, monospace; font-size: 6.6pt; line-height: 1.1; margin: 0 auto 3pt; display: inline-block; text-align: left; direction: ltr; color: #e9dcff; }
h1 { margin: 0; font-size: 18pt; letter-spacing: 0.4pt; direction: ltr; }
.tag { font-size: 10.3pt; color: #e9dcff; margin-top: 1pt; }
h2 { font-size: 11.4pt; color: #4a2a7f; margin: 0 0 3pt; }
.card { border: 1px solid #ddd3ee; border-radius: 10px; padding: 6pt 11pt 7pt; margin-top: 6pt; }
.main { border: 2px solid #4a2a7f; background: #fcfaff; padding: 8pt 12pt 9pt; }
.main h2 { font-size: 15pt; margin-bottom: 6pt; }
.steps { display: grid; grid-template-columns: 1.15fr 1fr; gap: 12pt; align-items: start; }
.steps > *, .row2 > * { min-width: 0; }
.step { display: flex; gap: 8pt; margin: 0 0 9pt; font-size: 11.6pt; line-height: 1.48; }
.step:last-child { margin-bottom: 0; }
.step .n { background: #4a2a7f; color: #fff; border-radius: 50%; width: 21pt; height: 21pt; display: inline-flex; align-items: center; justify-content: center; font-size: 11.5pt; font-weight: 700; flex: none; margin-top: 1pt; }
.step b.h { color: #4a2a7f; }
.small { font-size: 9.6pt; color: #555; }
.tree { background: #fff; border: 1px solid #ddd3ee; border-radius: 8px; padding: 8pt 10pt; font-size: 10.8pt; }
.tree .cap { font-weight: 700; color: #4a2a7f; margin-bottom: 4pt; font-size: 10.4pt; }
.row { display: flex; align-items: center; gap: 5pt; margin: 5pt 0; white-space: nowrap; }
.row svg { flex: none; }
.in1 { padding-right: 16pt; } .in2 { padding-right: 34pt; }
.hl { background: #fff3b0; border-radius: 5px; padding: 1pt 5pt; font-weight: 700; }
.pill { background: #4a2a7f; color: #fff; border-radius: 9px; padding: 0 6pt; font-size: 8.6pt; font-weight: 600; }
.mute { color: #8a8494; font-size: 8.8pt; }
.prompt { background: #f3eefb; border-right: 4px solid #4a2a7f; border-radius: 6px; padding: 5pt 9pt; margin: 3pt 0; font-weight: 500; }
.cmd { font-family: 'JetBrains Mono', Menlo, Consolas, Heebo, monospace; font-size: 8.6pt; direction: ltr; text-align: left; background: #1f1b2e; color: #e9e3ff; border-radius: 6px; padding: 4pt 8pt; margin: 3pt 0 0; white-space: pre; }
.ltr { direction: ltr; unicode-bidi: isolate; font-family: 'JetBrains Mono', Menlo, monospace; font-size: 0.9em; white-space: nowrap; }
.url { display: block; direction: ltr; text-align: left; font-family: 'JetBrains Mono', Menlo, monospace; font-size: 8.8pt; margin: 1pt 0; color: #4a2a7f; }
.ex { background: #f8f6fc; border-radius: 6px; padding: 2pt 8pt; margin: 3pt 0; }
.row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6pt; }
ul { margin: 2pt 0 0; padding-right: 15pt; }
li { margin: 1pt 0; }
.foot { margin-top: 7pt; text-align: center; font-size: 8.6pt; color: #6c6878; }
.foot b { color: #4a2a7f; }
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800'
         '&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">')

FOLDER = ('<svg width="15" height="12" viewBox="0 0 15 12"><path d="M1 2.2C1 1.5 1.5 1 2.2 1H5.6L7 2.6H12.8C13.5 2.6 14 3.1 14 3.8V9.8C14 10.5 13.5 11 12.8 11H2.2C1.5 11 1 10.5 1 9.8Z" '
          'fill="#b9a3e6" stroke="#4a2a7f" stroke-width="0.9"/></svg>')
FILE = ('<svg width="11" height="13" viewBox="0 0 11 13"><path d="M1 1.5C1 1.2 1.2 1 1.5 1H7L10 4V11.5C10 11.8 9.8 12 9.5 12H1.5C1.2 12 1 11.8 1 11.5Z" '
        'fill="#fff" stroke="#6c6878" stroke-width="0.9"/><path d="M7 1V4H10" fill="none" stroke="#6c6878" stroke-width="0.9"/></svg>')

BODY = f"""
<div class="top">
  <pre class="logo">{LOGO}</pre>
  <h1>Rosen Exam Builder</h1>
  <div class="tag">סקיל ל-Claude Code שבונה מבחנים בפיזיקה מהספר או מהחומר שלכם (ספרי עדי רוזן מוכרים מראש)</div>
</div>

<div class="card main">
  <h2>מה צריך לעשות? שלושה צעדים</h2>
  <div class="steps">
    <div>
      <div class="step"><span class="n">1</span><div><b class="h">מתקינים פעם אחת.</b> פותחים את Claude Code בתיקייה של הפרויקט שלכם, ומדביקים את הודעת ההתקנה שבתיבה למטה. ההתקנה גם יוצרת בפרויקט תיקייה בשם <b>ספרים</b>.</div></div>
      <div class="step"><span class="n">2</span><div><b class="h">שמים את הספר בתיקייה ספרים.</b> בשם הקובץ כותבים את המילה <b>פיזיקה</b>, למשל: <b style="white-space:nowrap">פיזיקה - אופטיקה</b><br>
        <span class="small">אפשר ספר של עדי רוזן, ספר אחר או חומר שלכם (סיכומים, דפי עבודה), כקובץ PDF, סריקות או צילומים.</span></div></div>
      <div class="step"><span class="n">3</span><div><b class="h">מבקשים מבחן.</b> כותבים למשל "תבנה לי מבחן באופטיקה לכיתה י׳", עונים על כמה שאלות קצרות, ומקבלים קובצי PDF מוכנים להדפסה.</div></div>
    </div>
    <div class="tree">
      <div class="cap">כך נראית תיקיית הפרויקט:</div>
      <div class="row">{FOLDER}<b>הפרויקט שלכם</b> <span class="mute">(כאן פותחים את Claude Code)</span></div>
      <div class="row in1">{FOLDER}<span class="hl">ספרים</span> <span class="pill">כאן שמים את הספר</span></div>
      <div class="row in2">{FILE}פיזיקה - אופטיקה</div>
      <div class="row in2">{FILE}פיזיקה - מכניקה כרך א</div>
      <div class="row in1">{FOLDER}<bdi dir="ltr" class="ltr">&lrm;.claude</bdi> <span class="mute">(הסקיל, נוצר בהתקנה)</span></div>
      <div class="row in1">{FOLDER}אופטיקה <span class="mute">(המבחנים נשמרים כאן)</span></div>
    </div>
  </div>
</div>

<div class="card">
  <h2>הודעת ההתקנה (צעד 1)</h2>
  <div class="prompt">התקן בפרויקט הזה את הסקיל rosen-exam-builder מהכתובת
  <span class="url">{REPO}</span>
  לתיקייה <span class="ltr">.claude/skills/rosen-exam-builder</span> של הפרויקט (לא בהתקנה גלובלית), צור בפרויקט תיקייה בשם ספרים,
  ובדוק ש-Python&nbsp;3.12+, Google&nbsp;Chrome ו-poppler מותקנים. אמור לי אם חסר משהו.</div>
  <span class="small">או מהטרמינל, מתוך תיקיית הפרויקט:</span>
  <div class="cmd">git clone {REPO}.git .claude/skills/rosen-exam-builder
mkdir ספרים</div>
</div>

<div class="row2">
  <div class="card">
    <h2>דוגמאות לבקשות (צעד 3)</h2>
    <div class="ex">תבנה לי מבחן באופטיקה לכיתה י׳ על פרקים א-ג, עם מבחן חזרה ודף תשובות</div>
    <div class="ex">בוחן של שעה במכניקה על קינמטיקה, שתי שאלות ברמת בגרות</div>
    <div class="ex">מבחן חוזר בחשמל משאלות 3, 8 ו-10 בפרק א</div>
    <span class="small">הסקיל ישאל: מקצוע, כיתה, משך, רמת קושי, מאיזה ספר, נושאים, כמה שאלות, מבחן חזרה ודף תשובות.</span>
  </div>
  <div class="card">
    <h2>מה מקבלים</h2>
    <ul>
      <li>מבחן A4 בעברית, כל שאלה בעמוד חדש</li>
      <li>דף תשובות מלא עם חישובים וסרטוטים</li>
      <li>מבחן חזרה עם הקשרים ומספרים אחרים</li>
      <li>כל תשובה נבדקה בקוד, בפתרון עיוור ובבדיקת דף התשובות</li>
    </ul>
    <span class="small">רוצים לשנות? כותבים במילים פשוטות, למשל "שאלה 2 קשה מדי", והסקיל בונה מחדש.</span>
  </div>
</div>

<div class="foot">אף ספר לא כלול בסקיל (זכויות יוצרים): כל מורה משתמש בעותק שלו, והסקיל מחפש רק בתיקיית הפרויקט.<br>
דרישות: Python 3.12+ · Google Chrome · poppler · חיבור לאינטרנט בזמן הבנייה<br>
<span class="ltr">{REPO}</span> &nbsp;·&nbsp; רישיון MIT &nbsp;·&nbsp; <b>RoeeAI</b></div>
"""


def main():
    html = HERE / "guide.html"
    html.write_text(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Rosen Exam Builder</title>'
                    f'{FONTS}<style>{CSS}</style></head><body>{BODY}</body></html>', encoding="utf-8")
    pdf = HERE / "rosen-exam-builder-guide.pdf"
    subprocess.run([find_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={pdf}", html.as_uri()], check=True, capture_output=True)
    print("wrote", pdf)


if __name__ == "__main__":
    main()
