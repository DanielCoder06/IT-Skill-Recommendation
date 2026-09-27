from pathlib import Path

import pymupdf
import pytest

from src.extractor.pdf_extractor import extract_text_from_pdf


def create_test_pdf(file_path: Path, text: str) -> None:
    """Create a simple PDF containing the given text."""
    document = pymupdf.open()

    page = document.new_page()
    page.insert_text((72, 72), text)

    document.save(file_path)
    document.close()


def test_extract_text_from_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "test_resume.pdf"
    expected_text = "Python Developer with experience in SQL and Git."

    create_test_pdf(pdf_path, expected_text)

    result = extract_text_from_pdf(pdf_path)

    assert expected_text in result


def test_extract_text_from_pdf_file_not_found(tmp_path: Path) -> None:
    pdf_path = tmp_path / "missing_resume.pdf"

    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(pdf_path)


def test_extract_text_from_pdf_rejects_non_pdf_file(tmp_path: Path) -> None:
    txt_path = tmp_path / "resume.txt"
    txt_path.write_text("This is not a PDF.", encoding="utf-8")

    with pytest.raises(ValueError):
        extract_text_from_pdf(txt_path)