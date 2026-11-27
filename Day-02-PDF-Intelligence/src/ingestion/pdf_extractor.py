
from pathlib import Path
import re
import pymupdf


class PDFExtractor:

    def _clean_text(self, text: str) -> str:
        """
        Normalize extracted PDF text without removing meaningful words.
        """
        # Normalize Unicode line separators and paragraph separators.
        text = text.replace("\u2028", "\n")
        text = text.replace("\u2029", "\n")

        # Normalize Windows and old-style line endings.
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove trailing spaces from each line.
        lines = [line.strip() for line in text.split("\n")]

        # Keep paragraph boundaries, but remove excessive blank lines.
        text = "\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def extract_text(self, pdf_path: str | Path) -> list[dict[str, int | str]]:
        """
        Extract text from a PDF while preserving 1-based page numbers.
        """
        if pdf_path is None:
            raise ValueError("PDF path cannot be None.")

        pdf_file = Path(pdf_path)

        if not pdf_file.exists() or not pdf_file.is_file():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")

        extracted_pages: list[dict[str, int | str]] = []

        try:
            with pymupdf.open(pdf_file) as document:
                for page_index, page in enumerate(document):
                    raw_text = page.get_text("text")
                    text = self._clean_text(raw_text)

                    if not text:
                        continue

                    extracted_pages.append({
                        "page_number": page_index + 1,
                        "text": text,
                    })

        except pymupdf.FileDataError as exc:
            raise ValueError(
                f"Invalid or corrupted PDF file: {pdf_path}"
            ) from exc

        if not extracted_pages:
            raise ValueError("No extractable text found in the PDF.")

        return extracted_pages
