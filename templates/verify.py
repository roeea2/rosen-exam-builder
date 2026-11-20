"""Recomputes every answer of {{TITLE}} and checks the values printed in the answer sheet.

Run it before every build. Add an assertion for every number that appears in the answer sheet, for every
"nice number" you designed the data around, and for every geometric fact a figure relies on (a point on a grid
node, a shadow inside the drawn floor, a ray that really hits the mirror).
"""
from data import *


def close(a, b, tol=0.051):
    assert abs(a - b) <= tol, (a, b)


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
print("all checks passed")
