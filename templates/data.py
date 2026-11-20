"""Single source of numbers for {{TITLE}}.

The questions, the figures and the answer sheet all read from this module, so they can never disagree.
Put every given value in a Q<n> dict and compute every answer below it (no hand-typed results).
"""
import math


def sind(a):
    return math.sin(math.radians(a))


def asind(s):
    return math.degrees(math.asin(s))


# >>> QUESTION
# ============================================================ question {{N}}
Q{{N}} = dict(d=6.0, v=1.5)                 # TODO: the given data of question {{N}}
q{{N}}_t = Q{{N}}["d"] / Q{{N}}["v"]        # TODO: every answer of question {{N}}, computed from the data

# <<< QUESTION
# >>> REVIEW
# ============================================================ review exam (same topics, different contexts and numbers)
# >>> RQUESTION
R{{N}} = dict(d=8.0, v=2.0)                 # TODO: the given data of review question {{N}}
r{{N}}_t = R{{N}}["d"] / R{{N}}["v"]        # TODO: every answer of review question {{N}}

# <<< RQUESTION
# <<< REVIEW
