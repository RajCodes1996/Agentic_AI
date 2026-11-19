"""Safe PDF text extraction with useful error messages."""
from pathlib import Path
from typing import BinaryIO

def extract_pdf_text(file: str | Path | BinaryIO) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Install pypdf to process PDF files.") from exc
    try:
        reader = PdfReader(file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception as exc:
        raise ValueError(f"Unable to read PDF: {exc}") from exc
    if not text:
        raise ValueError("No extractable text was found. This may be a scanned PDF.")
    return text
