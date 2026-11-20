"""Scaffold a new exam folder that builds out of the box (with TODO placeholders to replace).

    python3 new_exam.py "<exam folder>" --subject optics --questions 3 --duration "שעתיים" \
        --title "מבחן בפיזיקה - אופטיקה גאומטרית" --file "מבחן באופטיקה - כיתה י" \
        --topics "פרקים א-ג: אור וראייה, החזרת אור, שבירת אור" --grade "כיתה י׳" \
        --answers --review --review-title "מבחן חזרה - אופטיקה גאומטרית" --review-file "מבחן חזרה באופטיקה - כיתה י"

Creates <exam folder>/מקור/ with data.py, verify.py, figs.py, build.py and copies of examkit.py, svgkit.py and
rtl_scan.py, so the folder keeps building even without the skill. The PDFs are written to <exam folder>/.
"""
import argparse
import re
import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"
KITS = ["examkit.py", "svgkit.py", "rtl_scan.py"]


def blocks(text, tag, keep, repeat=None):
    """Handle '# >>> TAG' ... '# <<< TAG' blocks: drop them, keep them, or repeat them with {{N}} = 1..repeat."""
    pat = re.compile(rf"^([ \t]*)# >>> {tag}\n(.*?)^[ \t]*# <<< {tag}\n", re.S | re.M)

    def sub(mm):
        body = mm.group(2)
        if not keep:
            return ""
        if repeat:
            return "".join(body.replace("{{N}}", str(n)) for n in range(1, repeat + 1))
        return body
    return pat.sub(sub, text)


def render(name, a):
    t = (TEMPLATES / name).read_text(encoding="utf-8")
    t = blocks(t, "RQUESTION", a.review, a.questions)
    t = blocks(t, "QUESTION", True, a.questions)
    t = blocks(t, "ANSWERS", a.answers)
    t = blocks(t, "REVIEW", a.review)
    docs = (", answer sheet" if a.answers else "") + (", review exam" if a.review else "") + \
           (", review answer sheet" if a.review and a.answers else "")
    tokens = {"TITLE": a.title, "FILE": a.file, "SUBJECT": a.subject, "DURATION": a.duration, "NQ": str(a.questions),
              "TOPICS": a.topics, "GRADE": a.grade, "REVIEW_TITLE": a.review_title or "מבחן חזרה - " + a.title,
              "REVIEW_FILE": a.review_file or "מבחן חזרה - " + a.file, "DOCS": docs}
    for k, v in tokens.items():
        t = t.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", t)
    assert not left, f"unreplaced tokens in {name}: {left}"
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--subject", choices=["optics", "mechanics", "electricity"], required=True)
    ap.add_argument("--questions", type=int, default=3)
    ap.add_argument("--duration", default="שעתיים")
    ap.add_argument("--title", required=True, help="title printed in the exam header")
    ap.add_argument("--file", required=True, help="PDF file name (without .pdf)")
    ap.add_argument("--topics", required=True)
    ap.add_argument("--grade", required=True, help='e.g. "כיתה י׳" or "כיתה יב׳ · 5 יח״ל"')
    ap.add_argument("--answers", action="store_true")
    ap.add_argument("--review", action="store_true")
    ap.add_argument("--review-title")
    ap.add_argument("--review-file")
    ap.add_argument("--src-name", default="מקור")
    ap.add_argument("--force", action="store_true", help="overwrite existing source files")
    a = ap.parse_args()

    src = Path(a.folder) / a.src_name
    src.mkdir(parents=True, exist_ok=True)
    for name in ["data.py", "verify.py", "figs.py", "build.py"]:
        dest = src / name
        if dest.exists() and not a.force:
            raise SystemExit(f"{dest} exists; use --force to overwrite")
        dest.write_text(render(name, a), encoding="utf-8")
    for kit in KITS:
        shutil.copy2(SKILL / "scripts" / kit, src / kit)
    print(f"scaffolded {src}")
    print("next: edit data.py, verify.py, figs.py, build.py; then run  python3 verify.py && python3 build.py")


if __name__ == "__main__":
    main()
