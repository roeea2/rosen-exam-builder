"""SVG drawing kit for exam figures (optics rays, mirrors, shadows, grids, motion graphs, force arrows).

All functions return SVG fragments as strings; wrap the joined fragments with svg(w, h, body).
Screen coordinates: x to the right, y down. Angles passed as phi are in degrees, counter-clockwise, y up
(the usual math convention), so pt(cx, cy, r, 90) is straight above (cx, cy).

Compute every drawn point from the exam's data module, never by hand, so the figure, the question and the
answer sheet can not disagree.
"""
import math

INK = "#1c1b1f"
MUTED = "#6c6878"
GRID = "#e6e1ef"
ACCENT = "#4a2a7f"
RAY = "#e03131"
BLUE = "#1971c2"
GHOST = "#a5a1ad"
GREEN = "#2b8a3e"
PERSON = "#5f3dc4"
SHADOW = "#3b3943"
GLASS, GLASS_EDGE = "#e3f1fb", "#74b5e0"
WATER, WATER_EDGE = "#d4eafb", "#4d9fe0"
MIRROR, HATCH = "#9aa8bc", "#7b8698"
MATH = "'STIX Two Text', 'Times New Roman', serif"
FONT = "Heebo, Arial, sans-serif"


# ------------------------------------------------------------------ basics
def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'


def text(x, y, s, size=12, color=INK, anchor="middle", weight=400, family=MATH, italic=False):
    """Latin / math label (STIX). Use he() for Hebrew labels."""
    extra = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'dominant-baseline="central" font-weight="{weight}" font-family="{family}"{extra}>{s}</text>')


def he(x, y, s, size=11.5, color=INK, anchor="middle", weight=500):
    """Hebrew label (Heebo)."""
    return text(x, y, s, size, color, anchor, weight, FONT)


def theta(x, y, sub, color=ACCENT, anchor="middle", size=12.5):
    """θ with a Hebrew subscript, e.g. theta(x, y, "אוויר")."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}" dominant-baseline="central">'
            f'<tspan font-family="{MATH}" font-style="italic">θ</tspan>'
            f'<tspan font-family="{FONT}" font-size="{size * 0.68:.1f}" dy="4">{sub}</tspan></text>')


def pt(cx, cy, r, phi):
    """Point at distance r from (cx, cy) in direction phi (degrees, counter-clockwise, y up)."""
    return cx + r * math.cos(math.radians(phi)), cy - r * math.sin(math.radians(phi))


def line(x1, y1, x2, y2, color=INK, w=1.4, dash=None, opacity=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"{d}{o}/>'


def head(x, y, ang, size=9, color=RAY):
    """Arrow head at (x, y) pointing along ang (radians, screen coordinates)."""
    a1, a2 = ang + 2.7, ang - 2.7
    return (f'<path d="M{x:.1f},{y:.1f} L{x + size * math.cos(a1):.1f},{y + size * math.sin(a1):.1f} '
            f'L{x + size * math.cos(a2):.1f},{y + size * math.sin(a2):.1f} Z" fill="{color}"/>')


def ray(x1, y1, x2, y2, color=RAY, w=2, at=0.55, opacity=1):
    """Light ray with a direction arrow placed at fraction `at` of its length."""
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    g = f'<g opacity="{opacity}">' if opacity != 1 else "<g>"
    return g + line(x1, y1, x2, y2, color, w) + head(hx + 4.5 * math.cos(ang), hy + 4.5 * math.sin(ang), ang, 9, color) + "</g>"


def arrow(x1, y1, x2, y2, color=INK, w=1.8, size=9):
    """Vector arrow (force, velocity) with the head at the end."""
    ang = math.atan2(y2 - y1, x2 - x1)
    return line(x1, y1, x2 - 0.6 * size * math.cos(ang), y2 - 0.6 * size * math.sin(ang), color, w) + head(x2, y2, ang, size, color)


def normal(x1, y1, x2, y2):
    """Dashed normal line."""
    return line(x1, y1, x2, y2, MUTED, 1.1, "5 4")


def arc(cx, cy, r, phi1, phi2, label=None, color=ACCENT, lr=None, size=12):
    """Angle arc from phi1 to phi2 (counter-clockwise), label at the middle direction at radius lr."""
    x1, y1 = pt(cx, cy, r, phi1)
    x2, y2 = pt(cx, cy, r, phi2)
    large = 1 if phi2 - phi1 > 180 else 0
    out = f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" stroke-width="1.3"/>'
    if label:
        lx, ly = pt(cx, cy, lr or r + 14, (phi1 + phi2) / 2)
        out += text(lx, ly, label, size, color)
    return out


def dim(x1, y1, x2, y2, label="", lx=0, ly=0, anchor="middle", color=MUTED):
    """Dimension line with arrows at both ends; optional Latin label at (lx, ly). Use he() for a Hebrew label."""
    ang = math.atan2(y2 - y1, x2 - x1)
    out = line(x1, y1, x2, y2, color, 1) + head(x1, y1, ang + math.pi, 7, color) + head(x2, y2, ang, 7, color)
    return out + (text(lx, ly, label, 12.5, INK, anchor) if label else "")


def dot(x, y, color=GREEN, r=3.6, hollow=False):
    fill = "#fff" if hollow else color
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="1.6"/>'


# ------------------------------------------------------------------ optics props
def lamp(x, y, r=6):
    """Point light source: a small sun with short rays."""
    out = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 2.2:.1f}" fill="#ffd43b" opacity="0.28"/>']
    for k in range(8):
        a = k * math.pi / 4
        out.append(line(x + r * 1.25 * math.cos(a), y + r * 1.25 * math.sin(a),
                        x + r * 1.95 * math.cos(a), y + r * 1.95 * math.sin(a), "#f59f00", 1.4))
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#ffd43b" stroke="#f08c00" stroke-width="1.2"/>')
    return "".join(out)


def eye(x, y, phi, s=1.0):
    """An eye looking in direction phi (degrees, math convention) with its pupil exactly at (x, y)."""
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({-phi:.1f}) scale({s})">'
            f'<path d="M-17,0 Q-5,-10 7,0 Q-5,10 -17,0 Z" fill="#fff" stroke="{INK}" stroke-width="1.3"/>'
            f'<circle cx="-1" cy="0" r="4.2" fill="#3b5bdb"/><circle cx="0" cy="0" r="1.9" fill="{INK}"/></g>')


def person(x, yg, hp, color=PERSON, opacity=1):
    """Simple standing figure at x on the ground line yg; the top of the head is exactly hp above the ground."""
    r = hp * 0.105
    neck, hip = yg - hp + 2 * r, yg - hp * 0.47
    o = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<g{o}>'
            + line(x - hp * 0.035, hip, x - hp * 0.075, yg - 1.5, color, hp * 0.075)
            + line(x + hp * 0.035, hip, x + hp * 0.075, yg - 1.5, color, hp * 0.075)
            + line(x - hp * 0.13, neck + hp * 0.05, x - hp * 0.17, hip + hp * 0.02, color, hp * 0.055)
            + line(x + hp * 0.13, neck + hp * 0.05, x + hp * 0.17, hip + hp * 0.02, color, hp * 0.055)
            + f'<rect x="{x - hp * 0.12:.1f}" y="{neck:.1f}" width="{hp * 0.24:.1f}" height="{hip - neck + hp * 0.04:.1f}" rx="{hp * 0.07:.1f}" fill="{color}"/>'
            + f'<circle cx="{x:.1f}" cy="{yg - hp + r:.1f}" r="{r:.1f}" fill="{color}"/></g>')


def mirror(x1, y1, x2, y2, back):
    """Plane mirror from (x1, y1) to (x2, y2); hatching on the back side (back = direction in degrees, math convention)."""
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    bx, by = math.cos(math.radians(back)), -math.sin(math.radians(back))
    out = []
    n = max(1, int(L // 9))
    for k in range(n + 1):
        px, py = x1 + ux * k * L / n, y1 + uy * k * L / n
        out.append(line(px + bx * 2, py + by * 2, px + bx * 9 - ux * 6, py + by * 9 - uy * 6, HATCH, 1))
    out.append(line(x1, y1, x2, y2, MIRROR, 4.5))
    out.append(line(x1 - bx * 1.6, y1 - by * 1.6, x2 - bx * 1.6, y2 - by * 1.6, "#dfe5ee", 1.2))
    return "".join(out)


def ground(x1, x2, y):
    return f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="9" fill="#eee9e2"/>' + line(x1, y, x2, y, "#8d8478", 1.6)


def half_disk(cx, top, R, fill=GLASS, edge=GLASS_EDGE, ticks=True):
    """Semicircular block with the flat face on top (centre at (cx, top)), optional 10-degree ticks."""
    out = [f'<path d="M{cx - R},{top} A{R},{R} 0 0 0 {cx + R},{top} Z" fill="{fill}" stroke="{edge}" stroke-width="1.6"/>']
    if ticks:
        for k in range(1, 18):
            x1, y1 = pt(cx, top, R, -k * 10)
            x2, y2 = pt(cx, top, R - (7 if k % 3 == 0 else 4), -k * 10)
            out.append(line(x1, y1, x2, y2, edge, 1))
    return "".join(out)


def snell_out(theta_in, n_in, n_out):
    """Refraction angle in degrees, or None for total internal reflection."""
    s = n_in / n_out * math.sin(math.radians(theta_in))
    return None if abs(s) > 1 else math.degrees(math.asin(s))


# ------------------------------------------------------------------ grids and graphs
class Grid:
    """Square grid in grid units (y up). G(x, y) maps grid coordinates to SVG; x0, y0 are the lower-left grid values."""

    def __init__(self, nx, ny, x0=0, y0=0, s=26, pad=16):
        self.s, self.pad, self.nx, self.ny, self.x0, self.y0 = s, pad, nx, ny, x0, y0
        self.w, self.h = nx * s + 2 * pad, ny * s + 2 * pad

    def G(self, x, y):
        return self.pad + (x - self.x0) * self.s, self.pad + (self.ny - (y - self.y0)) * self.s

    def lines(self):
        out = []
        for i in range(self.nx + 1):
            x = self.pad + i * self.s
            out.append(line(x, self.pad, x, self.pad + self.ny * self.s, GRID, 0.9))
        for j in range(self.ny + 1):
            y = self.pad + j * self.s
            out.append(line(self.pad, y, self.pad + self.nx * self.s, y, GRID, 0.9))
        out.append(f'<rect x="{self.pad}" y="{self.pad}" width="{self.nx * self.s}" height="{self.ny * self.s}" fill="none" stroke="#cfc6de" stroke-width="1"/>')
        return "".join(out)


class Plot:
    """Axes for motion graphs (x-t, v-t, a-t, F-x...). P(x, y) maps data to SVG coordinates."""

    def __init__(self, xmin, xmax, ymin, ymax, w=420, h=260, left=48, right=24, top=18, bottom=40):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.w, self.h, self.l, self.r, self.t, self.b = w, h, left, right, top, bottom
        self.sx = (w - left - right) / (xmax - xmin)
        self.sy = (h - top - bottom) / (ymax - ymin)

    def P(self, x, y):
        return self.l + (x - self.xmin) * self.sx, self.h - self.b - (y - self.ymin) * self.sy

    def axes(self, xlabel, ylabel, xticks=(), yticks=(), gridlines=True):
        out = []
        for xv in xticks:
            px, _ = self.P(xv, 0)
            if gridlines:
                out.append(line(px, self.P(0, self.ymin)[1], px, self.P(0, self.ymax)[1], "#e3e7ee", 1))
            out.append(text(px, self.P(0, 0)[1] + 15, f"{xv:g}", 11, MUTED))
        for yv in yticks:
            _, py = self.P(0, yv)
            if gridlines:
                out.append(line(self.P(self.xmin, 0)[0], py, self.P(self.xmax, 0)[0], py, "#e3e7ee", 1))
            out.append(text(self.P(0, 0)[0] - 8, py, f"{yv:g}", 11, MUTED, "end"))
        x0, y0 = self.P(self.xmin, 0)
        x1, _ = self.P(self.xmax, 0)
        out.append(arrow(x0, y0, x1 + 10, y0, INK, 1.3, 8))
        ax, ay0 = self.P(0, self.ymin)
        _, ay1 = self.P(0, self.ymax)
        out.append(arrow(ax, ay0, ax, ay1 - 10, INK, 1.3, 8))
        out.append(text(x1 + 12, y0 + 16, xlabel, 12, INK, "end", italic=False))
        out.append(text(ax + 8, ay1 - 6, ylabel, 12, INK, "start"))
        return "".join(out)

    def curve(self, f, x_from, x_to, color=BLUE, w=2.2, n=200, dash=None):
        pts = " ".join(f"{self.P(x, f(x))[0]:.1f},{self.P(x, f(x))[1]:.1f}"
                       for x in (x_from + (x_to - x_from) * i / n for i in range(n + 1)))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{w}"{d}/>'

    def segments(self, points, color=BLUE, w=2.2):
        """Piecewise-linear graph through data points [(x, y), ...]."""
        pts = " ".join(f"{self.P(x, y)[0]:.1f},{self.P(x, y)[1]:.1f}" for x, y in points)
        return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"/>'
