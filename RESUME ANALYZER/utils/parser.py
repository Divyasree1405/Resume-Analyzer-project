# utils/parser.py
from PyPDF2 import PdfReader
import docx2txt
import os

def extract_text_from_file(path: str) -> str:
    path_lower = path.lower()

    if path_lower.endswith(".pdf"):
        text_chunks = []
        with open(path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
        return "\n".join(text_chunks)

    elif path_lower.endswith(".docx"):
        # docx2txt needs a file path
        return docx2txt.process(path) or ""

    elif path_lower.endswith(".txt"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        # Fallback: try reading as text
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")
