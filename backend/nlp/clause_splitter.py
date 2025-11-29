# backend/nlp/clause_splitter.py
import re
from typing import List

HEADING_RE = re.compile(
    r'(?:(?:^|\n)\s*(?:section|article)\s+\w+[:\.\s-]*)'  # section / article headings
    r'|(?:(?:^|\n)\s*\d+(?:\.\d+)*\s*[A-Z]?\s*[\-\.\)]?\s+)',  # 1. 1.1 2) etc.
    flags=re.IGNORECASE
)

SPLIT_SENT_RE = re.compile(r'(?<=[\.\?\!])\s+')

def split_into_clauses(text: str) -> List[str]:
    """Improved clause splitter that preserves headings with their bodies."""
    if not text:
        return []

    # Normalize whitespace but keep newlines for heading detection
    text = re.sub(r'\r\n?', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text).strip()

    # Protect common abbreviations that contain periods so we don't split them (simple approach)
    protected = {
        "pvt. ltd.": "pvt__ltd__",
        "e.g.": "eg__",
        "i.e.": "ie__",
        "etc.": "etc__",
        "Mr.": "Mr__",
        "Mrs.": "Mrs__",
        "Dr.": "Dr__",
    }
    lower_text = text.lower()
    for k, v in protected.items():
        lower_text = lower_text.replace(k, v)

    # Split into sections by detecting headings (keep delimiters)
    parts = []
    last_index = 0
    for m in HEADING_RE.finditer(lower_text):
        start = m.start()
        if start > last_index:
            parts.append(text[last_index:start].strip())
        # include heading text from original (preserve case)
        parts.append(text[start:m.end()].strip())
        last_index = m.end()
    # remaining tail
    if last_index < len(text):
        parts.append(text[last_index:].strip())

    # Now merge headings that are isolated (e.g., "1. SCOPE OF WORK") with the next part
    merged = []
    i = 0
    while i < len(parts):
        p = parts[i].strip()
        # if part looks like a short heading (few words and ends without long body), merge with next
        if i + 1 < len(parts):
            # heuristic: heading lines are short (<=8 words) and next part is longer
            if len(p.split()) <= 8 and len(parts[i+1].split()) > 2:
                merged.append((p + " " + parts[i+1]).strip())
                i += 2
                continue
        merged.append(p)
        i += 1

    # Finally split merged sections into smaller clauses by sentence punctuation,
    # but only if the section is long.
    clauses = []
    for sec in merged:
        sec_clean = sec.strip()
        if not sec_clean:
            continue
        if len(sec_clean) < 200:
            clauses.append(sec_clean)
        else:
            # split into sentence-like pieces and keep each
            for s in SPLIT_SENT_RE.split(sec_clean):
                s = s.strip()
                if s:
                    clauses.append(s)

    # restore protected tokens back
    def restore(s):
        return s.replace("pvt__ltd__", "Pvt. Ltd.") \
                .replace("eg__", "e.g.") \
                .replace("ie__", "i.e.") \
                .replace("etc__", "etc.") \
                .replace("Mr__", "Mr.") \
                .replace("Mrs__", "Mrs.") \
                .replace("Dr__", "Dr.")

    out = []
    seen = set()
    for c in clauses:
        r = restore(c)
        if r not in seen:
            out.append(r)
            seen.add(r)
    return out
