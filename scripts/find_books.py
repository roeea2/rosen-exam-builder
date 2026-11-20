"""Find Adi Rosen textbook PDFs (and chapter scans) under one or more folders and report what each one is.

    python3 find_books.py [FOLDER ...]        (default: the current folder)

For every candidate PDF it prints the subject guess, the page count, and whether it has a text layer
(text layer: read it with pdftotext; scanned: render pages with render_pages.py and read the images).
Scans are sometimes upside down; look at one rendered page before reading a whole chapter.
"""
import re
import subprocess
import sys
from pathlib import Path

SUBJECTS = [
    ("optics", re.compile(r"אופטיקה|קרינה\s*וחומר|optic", re.I)),
    ("mechanics", re.compile(r"מכניקה|ניוטו?נית|קינמטיקה|mechanic", re.I)),
    ("electricity", re.compile(r"חשמל|אלקטרו|מגנטי|electric", re.I)),
]


def info(pdf):
    pages, text_chars = None, 0
    try:
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=30).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        pages = int(m.group(1)) if m else None
        txt = subprocess.run(["pdftotext", "-f", "5", "-l", "12", str(pdf), "-"], capture_output=True, text=True, timeout=60).stdout
        text_chars = len(re.sub(r"\s", "", txt))
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return pages, text_chars


def main(folders):
    found = 0
    for root in folders:
        for pdf in sorted(Path(root).rglob("*.pdf")):
            name = pdf.name
            subject = next((s for s, rx in SUBJECTS if rx.search(name)), None)
            scan = name.lower().startswith("scan")
            if not subject and not scan:
                continue
            pages, chars = info(pdf)
            if pages is not None and pages < 8 and not scan:
                continue                                   # small PDFs are exams and handouts, not books
            layer = "text layer" if chars > 400 else "scanned (no text layer)"
            print(f"{subject or 'unknown (scan)':12} | {pages or '?':>4} pages | {layer:24} | {pdf}")
            found += 1
    if not found:
        print("No textbook PDFs found. Ask the teacher where the book (or the chapter scans) is.")


if __name__ == "__main__":
    main(sys.argv[1:] or ["."])
