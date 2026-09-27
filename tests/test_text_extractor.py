from pathlib import Path

import pytest

from src.extractor.text_extractor import extract_text_from_file


def test_extract_text_from_txt(tmp_path: Path) -> None:
    file_path = tmp_path / "resume.txt"
    file_path.write_text(
        "Python Developer\nPython\nSQL\nGit",
        encoding="utf-8",
    )

    result = extract_text_from_file(file_path)

    assert result == "Python Developer\nPython\nSQL\nGit"


def test_extract_text_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        extract_text_from_file("missing_resume.txt")


def test_extract_text_rejects_non_txt_file(tmp_path: Path) -> None:
    file_path = tmp_path / "resume.pdf"
    file_path.write_text("fake pdf", encoding="utf-8")

    with pytest.raises(ValueError):
        extract_text_from_file(file_path)