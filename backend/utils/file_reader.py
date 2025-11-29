# backend/utils/file_reader.py
from backend.parser.pdf_extractor import extract_text_from_pdf
from backend.parser.docx_extractor import extract_text_from_docx
from backend.parser.clean_text import clean_text
import os

def read_file(path: str) -> str:
    path = path.strip()
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    ext = os.path.splitext(path)[1].lower()
    if ext in [".pdf"]:
        raw = extract_text_from_docx(path)
    elif ext in [".docx", ".doc"]:
        raw = extract_text_from_docx(path)
    else:
        # treat as text file
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    return clean_text(raw)