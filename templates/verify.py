"""Recomputes every answer of {{TITLE}} and checks the values printed in the answer sheet.

build.py imports this module first, so a failed check stops the build and no PDF is written with a wrong answer.
Add an assertion for every number that appears in the answer sheet, for every "nice number" you designed the data
around, and for every geometric fact a figure relies on (a point on a grid node, a shadow inside the drawn floor,
a ray that really hits the mirror).
"""
from data import *

N_CHECKS = 0


def close(a, b, tol=0.051):
    """A computed value equals the value printed in the answer sheet (to the printed precision)."""
    global N_CHECKS
    N_CHECKS += 1
    assert abs(a - b) <= tol, (a, b)


def check(cond, what):
    """A fact a question or a figure relies on, e.g. check(0 <= x <= 12, "the shadow ends on the drawn floor")."""
    global N_CHECKS
    N_CHECKS += 1
    assert cond, what


# >>> QUESTION
# ---------------------------------------------------------------- question {{N}}
close(q{{N}}_t, 4.0)                        # TODO: the value printed in the answer sheet

# <<< QUESTION
# >>> REVIEW
# >>> RQUESTION
# ---------------------------------------------------------------- review question {{N}}
close(r{{N}}_t, 4.0)                        # TODO

# <<< RQUESTION
# <<< REVIEW
print(f"verify: all {N_CHECKS} checks passed")
