"""Scan built exam HTML files for right-to-left typesetting traps.

    python3 rtl_scan.py exam.html answers.html ...

In a Hebrew (RTL) paragraph a punctuation mark that follows a left-to-right run is drawn on the run's left side,
which is where its FIRST character is. When the run starts with a digit, "של 30°." is shown as ".30°" and reads
like a decimal number. The scan flags:
  1. inline math (class="m") that starts with a digit, a sign or ≈ and is followed directly by . , : ; ?
  2. plain-text numbers followed by punctuation (e.g. a calculation typed without m(), or "עמ' 39;")
  3. plain-text calculations such as "2 · 4 = 8" outside m(), which the bidi algorithm can reverse
  4. a TODO placeholder left from the scaffold anywhere in the document (text or figures)
Fix by rewording so the sentence ends with a Hebrew word ("ביחס לאנך", "בקירוב"), or by wrapping the
calculation in m() with no punctuation after it.
"""
import html
import re
import sys


MATH_OPEN = re.compile(r'<span class="m" dir="ltr">')
SPAN_TAG = re.compile(r"<span\b|</span>")


def math_spans(body):
    """Yield (start, inner_start, end) for every inline-math span; nested spans (fractions) stay inside it."""
    pos = 0
    while (mm := MATH_OPEN.search(body, pos)):
        depth, i = 1, mm.end()
        while depth:
            tag = SPAN_TAG.search(body, i)
            if not tag:
                i = len(body)
                break
            depth += 1 if tag.group() == "<span" else -1
            i = tag.end()
        yield mm.start(), mm.end(), i
        pos = i


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def scan(path):
    s = open(path, encoding="utf-8").read()
    body = s[s.find("<body"):] if "<body" in s else s
    hits = [f"placeholder left in the document: ...{body[max(0, mm.start() - 20): mm.end() + 30]}..."
            for mm in re.finditer(r"TODO", body)]
    body = re.sub(r"<svg.*?</svg>", "", body, flags=re.S)
    body = re.sub(r'<div class="eq".*?</div></div>', "", body, flags=re.S)
    pieces, last = [], 0
    for start, inner, end in math_spans(body):
        txt = text(body[inner:end]).strip()
        after = re.match(r"(?:</span>)?\s?([.,:;?])", body[end:])
        if after and re.match(r"[\d(≈−+-]", txt):
            hits.append(f"math followed by '{after.group(1)}': {txt}")
        pieces.append(body[last:start])
        last = end
    # the text without formulas; a marker keeps the words on both sides of a formula apart
    no_math = text("".join(p + " ◊ " for p in pieces) + body[last:])
    for mm in re.finditer(r"(?<![\w.])\d[\d.,]*\s*[.,:;?](?=\s|$)", no_math):
        hits.append("number followed by punctuation: ..." + no_math[max(0, mm.start() - 25): mm.end() + 3].replace("\n", " "))
    for mm in re.finditer(r"\d+(?:\.\d+)?\s*[·×+−=]\s*\d", no_math):
        hits.append("calculation outside m(): ..." + no_math[max(0, mm.start() - 15): mm.end() + 10].replace("\n", " "))
    return hits


if __name__ == "__main__":
    total = 0
    for p in sys.argv[1:]:
        for h in scan(p):
            print(f"{p}: {h}")
            total += 1
    print(f"rtl scan: {total} issue(s)")
    sys.exit(1 if total else 0)
