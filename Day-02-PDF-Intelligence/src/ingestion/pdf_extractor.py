
from pathlib import Path
import fitz


class PDFExtractor:

    def extract_text(self, pdf_path: str) -> list[dict]:

        """
        Extract text from a PDF while preserving page numbers.
        """

        pdf_file = Path(pdf_path)

        # Validate file existence
        if not pdf_file.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        # Validate file extension
        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        extracted_pages = []

        # Open PDF document
        with fitz.open(pdf_file) as document:

            # Process every page
            for page_index, page in enumerate(document):

                # Extract text
                text = page.get_text("text").strip()

                # Ignore empty pages
                if not text:
                    continue

                # Store page information
                extracted_pages.append({
                    "page_number": page_index + 1,
                    "text": text
                })

        if not extracted_pages:
            raise ValueError(
                "No extractable text found in the PDF."
            )

        return extracted_pages