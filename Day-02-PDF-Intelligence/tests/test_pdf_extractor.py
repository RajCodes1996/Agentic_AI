import pytest
from src.ingestion.pdf_extractor import extract_pdf_text

def test_missing_pdf_raises_value_error():
    with pytest.raises(ValueError):
        extract_pdf_text("does-not-exist.pdf")
