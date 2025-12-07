import re

def clean_text(raw: str) -> str:
    if not raw:
        return ""
    # Normalize whitespace
    text = re.sub(r"\s+", " ", raw)
    # Remove weird ASCII sequence
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = text.strip()
    return text

print(clean_text(" is used to normalize whitespace in a string by replacing all newline characters with spaces and then collapsing all sequences of whitespace (spaces, tabs, multiple newlines) into a single space between words. "))