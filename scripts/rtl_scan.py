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


def scan(path):
    s = open(path, encoding="utf-8").read()
    body = s[s.find("<body"):] if "<body" in s else s
    hits = [f"placeholder left in the document: ...{body[max(0, mm.start() - 20): mm.end() + 30]}..."
            for mm in re.finditer(r"TODO", body)]
    body = re.sub(r"<svg.*?</svg>", "", body, flags=re.S)
    body = re.sub(r'<div class="eq".*?</div></div>', "", body, flags=re.S)
    for mm in re.finditer(r'<span class="m" dir="ltr">((?:(?!</span>).)*?)</span>(?:</span>)?\s?([.,:;?])', body, flags=re.S):
        txt = html.unescape(re.sub(r"<[^>]+>", "", mm.group(1))).strip()
        if re.match(r"[\d(≈−+-]", txt):
            hits.append(f"math followed by '{mm.group(2)}': {txt}")
    plain = html.unescape(re.sub(r"<[^>]+>", "", body))
    for mm in re.finditer(r"(?<![\w.])\d[\d.,]*\s*[.,:;?](?=\s|$)", plain):
        hits.append("number followed by punctuation: ..." + plain[max(0, mm.start() - 25): mm.end() + 3].replace("\n", " "))
    no_math = re.sub(r'<span class="m" dir="ltr">.*?</span>', "", body, flags=re.S)
    no_math = html.unescape(re.sub(r"<[^>]+>", "", no_math))
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
