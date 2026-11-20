"""Figures for {{TITLE}}. Every drawn point is computed from data.py; answer=True adds the solution drawing.

Primitives: see svgkit.py (ray, arrow, arc, dim, mirror, lamp, eye, person, half_disk, Grid, Plot, he, theta...).
"""
from svgkit import *
import data as D


# >>> QUESTION
def q{{N}}(answer=False):
    """TODO: the figure of question {{N}} (this placeholder draws a length on a grid)."""
    g = Grid(10, 4)
    G = g.G
    o = [g.lines()]
    x0, y0 = G(1, 2)
    x1, y1 = G(1 + D.Q{{N}}["d"], 2)
    o.append(dot(x0, y0, INK, 3))
    o.append(dot(x1, y1, INK, 3))
    o.append(dim(x0, y0 + 16, x1, y1 + 16, f"{D.Q{{N}}['d']:g} m", (x0 + x1) / 2, y0 + 30))
    if answer:
        o.append(ray(x0, y0, x1, y1))
    return svg(g.w, g.h + 20, "".join(o))


# <<< QUESTION
# >>> REVIEW
# >>> RQUESTION
def r{{N}}(answer=False):
    """TODO: the figure of review question {{N}}."""
    g = Grid(10, 4)
    G = g.G
    o = [g.lines()]
    x0, y0 = G(1, 2)
    x1, y1 = G(1 + D.R{{N}}["d"], 2)
    o.append(dim(x0, y0 + 16, x1, y1 + 16, f"{D.R{{N}}['d']:g} m", (x0 + x1) / 2, y0 + 30))
    if answer:
        o.append(ray(x0, y0, x1, y1))
    return svg(g.w, g.h + 20, "".join(o))


# <<< RQUESTION
# <<< REVIEW
