"""Find Adi Rosen textbook PDFs, or check the file a teacher gave, and report what each one is.

    python3 find_books.py <workspace> [--subject optics|mechanics|electricity]   list candidate books in a folder
    python3 find_books.py "<the teacher's file or folder>" --all                check what the teacher gave

For each PDF it prints the subject guess (from the file name), the page count, and whether it has a text layer
(text layer: read it with pdftotext; scanned: render pages with render_pages.py and read the images).
A normal folder search lists PDFs whose names look like physics books and skips PDFs under 8 pages (exams and
handouts), except inside a ספרים folder, where everything is the teacher's material and is always listed.
--all lists every PDF whatever its name or size, and counts page images (scans or photos): use it on a path the
teacher gave.
A file given directly is always reported.
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
    ("physics", re.compile(r"פיזיקה|פיסיקה|physic", re.I)),      # a general book: a candidate for every subject
]
IMAGES = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".tif", ".tiff"}
MIN_BOOK_PAGES = 8
BOOKS_DIR = "ספרים"                                            # where the skill asks teachers to put their material


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
    ap.add_argument("--subject", choices=["optics", "mechanics", "electricity"], help="list only books of this subject")
    ap.add_argument("--all", action="store_true", help="every PDF whatever its name or size, plus page images")
    a = ap.parse_args()
    found = 0
    for path in map(Path, a.paths):
        if path.is_file():                                   # a file the teacher gave: always report it
            report(path, subject_of(path.name), *info(path))
            found += 1
            continue
        if not path.is_dir():
            print(f"not found: {path}")
            continue
        for pdf in sorted(path.rglob("*.pdf")):
            subject = subject_of(pdf.name)
            if not (a.all or BOOKS_DIR in pdf.parts):          # everything in ספרים/ is the teacher's material
                if not subject and not pdf.name.lower().startswith("scan"):
                    continue
                if a.subject and subject not in (a.subject, None, "physics"):
                    continue
            pages, chars = info(pdf)
            if not (a.all or BOOKS_DIR in pdf.parts) and pages is not None and pages < MIN_BOOK_PAGES:
                continue                                     # exams and handouts, not books
            report(pdf, subject, pages, chars)
            found += 1
        folders = {}
        for img in path.rglob("*"):
            if img.suffix.lower() in IMAGES and (a.all or BOOKS_DIR in img.parts):
                folders.setdefault(img.parent, []).append(img)
        for folder, imgs in sorted(folders.items()):
            print(f"{'images':11} | {len(imgs):>4} files | scans or photos of pages | {folder}")
            found += 1
    if not found:
        print("Nothing found. Ask the teacher where their book or material is, or to put it in <workspace>/ספרים"
              " (SKILL.md section 2).")


if __name__ == "__main__":
    main()
