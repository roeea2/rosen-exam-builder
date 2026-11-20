"""Render PDF pages to PNG, optionally as side-by-side contact sheets (right-to-left, like a Hebrew book spread).

    python3 render_pages.py BOOK.pdf --pages 38-43 --dpi 75 --out /tmp/book --sheet 3
    python3 render_pages.py exam.pdf --dpi 80 --out /tmp/check --sheet 2

Use it for two jobs:
  * reading scanned textbook pages (no text layer): 3 pages per sheet at 75 dpi is readable and cheap;
  * checking a built exam: every page, 2 per sheet at 80 dpi.
Needs pdftoppm (poppler). Contact sheets need Pillow; without it the single pages are kept.
"""
import argparse
import subprocess
import sys
from pathlib import Path


def render(pdf, first, last, dpi, out, prefix="p"):
    out.mkdir(parents=True, exist_ok=True)
    args = ["pdftoppm", "-r", str(dpi), "-png"]
    if first:
        args += ["-f", str(first)]
    if last:
        args += ["-l", str(last)]
    subprocess.run(args + [str(pdf), str(out / prefix)], check=True)
    return sorted(out.glob(f"{prefix}-*.png"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))


def sheets(pngs, per, out, name):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed: kept single pages only", file=sys.stderr)
        return pngs
    made = []
    for i in range(0, len(pngs), per):
        group = [Image.open(p) for p in pngs[i:i + per]]
        w, h = max(g.width for g in group), max(g.height for g in group)
        sheet = Image.new("RGB", (w * per, h), "white")
        for k, g in enumerate(group):              # first page on the right, like an open Hebrew book
            sheet.paste(g, ((per - 1 - k) * w, 0))
        path = out / f"{name}-{i // per + 1}.png"
        sheet.save(path)
        made.append(path)
    return made


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="e.g. 38-43 (PDF page numbers)")
    ap.add_argument("--dpi", type=int, default=75)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sheet", type=int, default=0, help="pages per contact sheet (0 = single pages only)")
    a = ap.parse_args()
    first = last = None
    if a.pages:
        first, _, last = a.pages.partition("-")
        first, last = int(first), int(last or first)
    out = Path(a.out)
    pngs = render(a.pdf, first, last, a.dpi, out)
    result = sheets(pngs, a.sheet, out, "sheet") if a.sheet > 1 else pngs
    for p in result:
        print(p)
