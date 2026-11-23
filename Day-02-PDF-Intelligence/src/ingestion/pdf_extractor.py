from pathlib import Path
import pymupdf


class PDFExtractor:

    def extract_text(self, pdf_path: str | Path) -> list[dict[str, int | str]]:
        """
        Extract text from a PDF while preserving 1-based page numbers.
        """
        if pdf_path is None:
            raise ValueError("PDF path cannot be None.")

        pdf_file = Path(pdf_path)

        # Validate file existence and ensure it is a regular file
        if not pdf_file.exists() or not pdf_file.is_file():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        # Validate file extension
        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        extracted_pages: list[dict[str, int | str]] = []

        try:
            with pymupdf.open(pdf_file) as document:
                for page_index, page in enumerate(document):
                    text = page.get_text("text").strip()

                    # Ignore empty pages
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
            raise ValueError(
                "No extractable text found in the PDF."
            )

        return extracted_pages