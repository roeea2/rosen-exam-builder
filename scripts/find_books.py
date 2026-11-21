"""Find Adi Rosen textbook PDFs, or check the file a teacher gave, and report what each one is.

    python3 find_books.py <workspace> [--subject optics|mechanics|electricity]   list candidates in a folder
    python3 find_books.py "<the teacher's file>.pdf"                            check one file

For each PDF it prints the subject guess (from the file name), the page count, and whether it has a text layer
(text layer: read it with pdftotext; scanned: render pages with render_pages.py and read the images).
Folder search skips PDFs under 8 pages (exams and handouts); a file given directly is always reported.
Scans are sometimes upside down; look at one rendered page before reading a whole chapter.
The result is only a list of candidates: always ask the teacher which copy to use (SKILL.md section 2).
"""
import argparse
import re
import subprocess
from pathlib import Path

SUBJECTS = [
    ("optics", re.compile(r"אופטיקה|קרינה\s*וחומר|optic", re.I)),
    ("mechanics", re.compile(r"מכניקה|ניוטו?נית|קינמטיקה|mechanic", re.I)),
    ("electricity", re.compile(r"חשמל|אלקטרו|מגנטי|electric", re.I)),
]
MIN_BOOK_PAGES = 8


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


def subject_of(name):
    return next((s for s, rx in SUBJECTS if rx.search(name)), None)


def report(pdf, subject, pages, chars):
    layer = "text layer" if chars > 400 else "scanned (no text layer)"
    print(f"{subject or 'unknown':11} | {pages or '?':>4} pages | {layer:24} | {pdf}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=["."], help="folders to search, or PDF files to check")
    ap.add_argument("--subject", choices=[s for s, _ in SUBJECTS], help="list only books of this subject")
    a = ap.parse_args()
    found = 0
    for path in map(Path, a.paths):
        if path.is_file():                                   # a file the teacher gave: always report it
            report(path, subject_of(path.name), *info(path))
            found += 1
            continue
        for pdf in sorted(path.rglob("*.pdf")):
            subject = subject_of(pdf.name)
            if not subject and not pdf.name.lower().startswith("scan"):
                continue
            if a.subject and subject not in (a.subject, None):
                continue
            pages, chars = info(pdf)
            if pages is not None and pages < MIN_BOOK_PAGES:
                continue                                     # exams and handouts, not books
            report(pdf, subject, pages, chars)
            found += 1
    if not found:
        print("No textbook PDF found. Ask the teacher for their copy: drag the PDF (or chapter scans) into the chat,"
              " or give its full path.")


if __name__ == "__main__":
    main()
