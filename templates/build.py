"""Builds {{TITLE}} as A4 PDFs (exam{{DOCS}}).

    python3 build.py                  # runs every check in verify.py first and stops if one fails
    python3 rtl_scan.py *.html        # right-to-left typesetting traps and leftover TODO placeholders
"""
from pathlib import Path

import verify  # noqa: F401  (recomputes and checks every answer; an AssertionError here means: fix data.py first)
import examkit as K
from examkit import m, frac, part, sub, eq, res, fig, side_by_side, keep, th, IMP, NBSP
import figs as F
import data as D

HERE = Path(__file__).resolve().parent
OUT = HERE.parent                      # the PDFs go next to this source folder
SUBJECT = "{{SUBJECT}}"                # optics | mechanics | electricity (picks the formula box)
DURATION = "{{DURATION}}"
N_Q = {{NQ}}
SUBTITLE = K.subtitle("{{TOPICS}}", "{{GRADE}}")
TITLE = "{{TITLE}}"
FILE = "{{FILE}}"


def close_exam(body):
    """Put "בהצלחה!" at the end of the last question."""
    i = body.rfind("</section>")
    return body[:i] + K.END + body[i:]


# ================================================================== the exam
exam = K.header(TITLE, SUBTITLE) + K.notes(DURATION, N_Q, SUBJECT)
# >>> QUESTION
exam += K.section({{N}}, "TODO: נושא השאלה", f"""
  <p>TODO (the stem; every number comes from data.py) הגוף עובר {m(f"{D.Q{{N}}['d']:g} m")} במהירות קבועה של {m(f"{D.Q{{N}}['v']:g} m/s")} (ראו איור).</p>
  {fig(F.q{{N}}(), 9)}
  {part("א", "TODO: כמה זמן נמשכת התנועה?")}
  {part("ב", sub(1, "TODO") + sub(2, "TODO"))}
""", first={{N}} == 1)
# <<< QUESTION
exam = close_exam(exam)

# >>> ANSWERS
# ================================================================== the answer sheet
answers = K.header("תשובות: " + TITLE, SUBTITLE, grade_box=False) + K.teacher_note(
    "כל המספרים חושבו ונבדקו בקוד, מאותם נתונים שמהם סורטטו האיורים. TODO: on which book chapters and exercises each question is based.")
# >>> QUESTION
answers += K.section({{N}}, "TODO: נושא השאלה", f"""
  {part("א", "TODO: the reasoning in full sentences, then the calculation:"
        + eq(f"<i>t</i> = {frac('<i>d</i>', '<i>v</i>')} = {frac(f'{D.Q{{N}}['d']:g}', f'{D.Q{{N}}['v']:g}')} = {D.q{{N}}_t:g} s")
        + res(m(f"{D.q{{N}}_t:g} s")))}
  {fig(F.q{{N}}(answer=True), 8.6)}
  {part("ב", sub(1, "TODO") + sub(2, "TODO"))}
""", first={{N}} == 1)
# <<< QUESTION
# <<< ANSWERS

# >>> REVIEW
# ================================================================== the review exam
REVIEW_TITLE = "{{REVIEW_TITLE}}"
REVIEW_FILE = "{{REVIEW_FILE}}"
review = K.header(REVIEW_TITLE, SUBTITLE) + K.notes(DURATION, N_Q, SUBJECT)
# >>> RQUESTION
review += K.section({{N}}, "TODO: נושא השאלה", f"""
  <p>TODO (same topic and skills as the exam question, a different context and different numbers) הגוף עובר {m(f"{D.R{{N}}['d']:g} m")} במהירות של {m(f"{D.R{{N}}['v']:g} m/s")} בקירוב.</p>
  {fig(F.r{{N}}(), 9)}
  {part("א", "TODO")}
""", first={{N}} == 1)
# <<< RQUESTION
review = close_exam(review)
# >>> ANSWERS
review_answers = K.header("תשובות: " + REVIEW_TITLE, SUBTITLE, grade_box=False) + K.teacher_note("TODO")
# >>> RQUESTION
review_answers += K.section({{N}}, "TODO: נושא השאלה", f"""
  {part("א", "TODO" + eq(f"<i>t</i> = {D.r{{N}}_t:g} s") + res(m(f"{D.r{{N}}_t:g} s")))}
  {fig(F.r{{N}}(answer=True), 8.6)}
""", first={{N}} == 1)
# <<< RQUESTION
# <<< ANSWERS
# <<< REVIEW

if __name__ == "__main__":
    K.build_pdf(exam, FILE, OUT, HERE, "exam")
    # >>> ANSWERS
    K.build_pdf(answers, FILE + " - תשובות", OUT, HERE, "answers", cls="ans")
    # <<< ANSWERS
    # >>> REVIEW
    K.build_pdf(review, REVIEW_FILE, OUT, HERE, "review")
    # >>> ANSWERS
    K.build_pdf(review_answers, REVIEW_FILE + " - תשובות", OUT, HERE, "review_answers", cls="ans")
    # <<< ANSWERS
    # <<< REVIEW
