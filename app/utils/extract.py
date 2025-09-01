from typing import Tuple
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text_parts = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text("text"))
    return "\n".join(text_parts).strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    f = BytesIO(file_bytes)
    doc = Document(f)
    paras = [p.text for p in doc.paragraphs]
    return "\n".join(paras).strip()


def guess_and_extract(filename: str, data: bytes) -> Tuple[str, str]:
    name = filename.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(data)
    elif name.endswith(".docx"):
        return extract_text_from_docx(data)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX allowed.")
