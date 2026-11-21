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
@page { size: A4; margin: 11mm 13mm 10mm 13mm; }
* { box-sizing: border-box; }
html, body { margin: 0; background: #fff; }
body { font-family: Heebo, Arial, sans-serif; font-size: 10.3pt; line-height: 1.45; color: #1c1b1f; }
.top { background: linear-gradient(135deg, #2a1650, #4a2a7f 60%, #6a3fb0); color: #fff; border-radius: 12px; padding: 8pt 14pt 9pt; text-align: center; }
.logo { font-family: 'JetBrains Mono', Menlo, Consolas, monospace; font-size: 7.4pt; line-height: 1.12; margin: 0 auto 4pt; display: inline-block; text-align: left; direction: ltr; color: #e9dcff; }
h1 { margin: 0; font-size: 19pt; letter-spacing: 0.4pt; direction: ltr; }
.tag { font-size: 10.5pt; color: #e9dcff; margin-top: 1pt; }
h2 { font-size: 11.6pt; color: #4a2a7f; margin: 0 0 3pt; display: flex; align-items: center; gap: 6pt; }
h2 .n { background: #4a2a7f; color: #fff; border-radius: 50%; width: 17pt; height: 17pt; display: inline-flex; align-items: center; justify-content: center; font-size: 9.5pt; flex: none; }
.card { border: 1px solid #ddd3ee; border-radius: 10px; padding: 6pt 11pt 7pt; margin-top: 7pt; }
.prompt { background: #f3eefb; border-right: 4px solid #4a2a7f; border-radius: 6px; padding: 5pt 9pt; margin: 4pt 0; font-weight: 500; }
.cmd { font-family: 'JetBrains Mono', Menlo, Consolas, monospace; font-size: 8.8pt; direction: ltr; text-align: left; background: #1f1b2e; color: #e9e3ff; border-radius: 6px; padding: 4pt 8pt; margin: 3pt 0; white-space: pre; }
.ltr { direction: ltr; unicode-bidi: isolate; font-family: 'JetBrains Mono', Menlo, monospace; font-size: 0.92em; white-space: nowrap; }
.url { display: block; direction: ltr; text-align: left; font-family: 'JetBrains Mono', Menlo, monospace; font-size: 9pt; margin: 2pt 0; color: #4a2a7f; }
.ex { background: #f8f6fc; border-radius: 6px; padding: 3pt 9pt; margin: 3pt 0; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14pt; }
ul, ol { margin: 2pt 0 0; padding-right: 15pt; }
li { margin: 1pt 0; }
.row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 7pt; }
.row2 .card { margin-top: 7pt; }
.note { font-size: 9.2pt; color: #555; }
.foot { margin-top: 8pt; text-align: center; font-size: 8.8pt; color: #6c6878; }
.foot b { color: #4a2a7f; }
"""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800'
         '&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">')

BODY = f"""
<div class="top">
  <pre class="logo">{LOGO}</pre>
  <h1>Rosen Exam Builder</h1>
  <div class="tag">סקיל ל-Claude Code שבונה מבחנים בפיזיקה מספרי עדי רוזן: מבחן, דף תשובות ומבחן חזרה, מוכנים להדפסה</div>
</div>

<div class="card">
  <h2><span class="n">1</span>התקנה בתוך הפרויקט (לא גלובלית)</h2>
  פותחים את Claude Code בתיקיית הפרויקט שלכם, ומדביקים:
  <div class="prompt">התקן בפרויקט הזה את הסקיל rosen-exam-builder מהכתובת
  <span class="url">{REPO}</span>
  שכפל אותו לתיקייה <span class="ltr">.claude/skills/rosen-exam-builder</span> של הפרויקט (לא בהתקנה גלובלית),
  בדוק ש-Python&nbsp;3.12+, Google&nbsp;Chrome ו-poppler מותקנים, ואמור לי אם חסר משהו.</div>
  או מהטרמינל, מתוך תיקיית הפרויקט:
  <div class="cmd">git clone {REPO}.git .claude/skills/rosen-exam-builder</div>
  <span class="note">אחרי ההתקנה פותחים מחדש את Claude Code באותה תיקייה. הספרים מוגנים בזכויות יוצרים ואינם חלק מהסקיל: בפעם הראשונה הסקיל יבקש את העותק שלכם (PDF או סריקה של הפרקים).</span>
</div>

<div class="card">
  <h2><span class="n">2</span>מבקשים מבחן</h2>
  <div class="ex">תבנה לי מבחן באופטיקה לכיתה י׳ על פרקים א-ג, עם מבחן חזרה ודף תשובות</div>
  <div class="ex">בוחן של שעה במכניקה על קינמטיקה, שתי שאלות ברמת בגרות</div>
  <div class="ex">מבחן חוזר בחשמל משאלות 3, 8 ו-10 בפרק א (הנוסח המקורי נשמר)</div>
  <span class="note">אפשר גם להקליד</span> <span class="ltr">/rosen-exam-builder</span>
</div>

<div class="row2">
  <div class="card">
    <h2><span class="n">3</span>הסקיל ישאל</h2>
    <ol>
      <li>מקצוע: אופטיקה, מכניקה או חשמל</li>
      <li>כיתה ורמה: י׳, יא׳ או יב׳ (5 יח״ל)</li>
      <li>משך: שעה, שעה וחצי או שעתיים</li>
      <li>רמת קושי: קל, בינוני או בגרות</li>
      <li><b>הספר שלכם:</b> גוררים את ה-PDF לחלון</li>
      <li>נושאים, לפי פרקי הספר</li>
      <li>כמות שאלות, מבחן חזרה ודף תשובות</li>
    </ol>
  </div>
  <div class="card">
    <h2><span class="n">4</span>מה מקבלים</h2>
    <ul>
      <li>מבחן A4 בעברית, כל שאלה בעמוד חדש</li>
      <li>דף תשובות מלא עם חישובים וסרטוטים</li>
      <li>מבחן חזרה עם הקשרים ומספרים אחרים</li>
      <li>תיקיית מקור לשינויים ובנייה מחדש</li>
      <li>כל תשובה נבדקה בקוד ובפתרון עיוור</li>
    </ul>
  </div>
</div>

<div class="card">
  <h2><span class="n">5</span>שינויים</h2>
  אומרים במילים פשוטות מה לשנות, למשל: "שאלה 2 קשה מדי", "תחליף את ההקשר של שאלה 1", "המבחן צריך להיות שעה וחצי".
  הסקיל מעדכן את הנתונים, בודק שוב את כל התשובות ובונה מחדש את קובצי ה-PDF.
</div>

<div class="foot">דרישות: Python 3.12+ · Google Chrome · poppler · חיבור לאינטרנט בזמן הבנייה<br>
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
