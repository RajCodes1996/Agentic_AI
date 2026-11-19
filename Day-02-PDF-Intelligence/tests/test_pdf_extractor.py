
import pytest
import fitz

from src.ingestion.pdf_extractor import PDFExtractor


def create_sample_pdf(path):

    document = fitz.open()

    page1 = document.new_page()
    page1.insert_text(
        (72, 72),
        "Introduction to Artificial Intelligence"
    )

    page2 = document.new_page()
    page2.insert_text(
        (72, 72),
        "Machine Learning and Deep Learning"
    )

    document.save(path)
    document.close()


def test_pdf_text_extraction(tmp_path):

    pdf_path = tmp_path / "sample.pdf"

    create_sample_pdf(pdf_path)

    extractor = PDFExtractor()

    result = extractor.extract_text(str(pdf_path))

    assert len(result) == 2

    assert result[0]["page_number"] == 1

    assert "Artificial Intelligence" in result[0]["text"]

    assert result[1]["page_number"] == 2


def test_missing_pdf():

    extractor = PDFExtractor()

    with pytest.raises(FileNotFoundError):
        extractor.extract_text("missing.pdf")


def test_invalid_file_extension(tmp_path):

    file_path = tmp_path / "sample.txt"
    file_path.write_text("Not a PDF")

    extractor = PDFExtractor()

    with pytest.raises(ValueError):
        extractor.extract_text(str(file_path))


def test_empty_pdf(tmp_path):

    pdf_path = tmp_path / "empty.pdf"

    document = fitz.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    extractor = PDFExtractor()

    with pytest.raises(ValueError):
        extractor.extract_text(str(pdf_path))