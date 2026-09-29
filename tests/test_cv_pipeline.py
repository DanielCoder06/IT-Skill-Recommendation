from pathlib import Path

import pymupdf

from src.pipeline.cv_pipeline import extract_cv_skills


def create_test_pdf(file_path: Path, text: str) -> None:
    """Create a simple PDF containing the given text."""
    document = pymupdf.open()

    page = document.new_page()
    page.insert_text((72, 72), text)

    document.save(file_path)
    document.close()


def test_extract_cv_skills_from_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "resume.pdf"

    cv_text = """
    Data Analyst with experience in Python, SQL and Machine Learning.
    Used PostgreSQL, Git and GitHub.
    """

    create_test_pdf(pdf_path, cv_text)

    skills = extract_cv_skills(pdf_path)

    expected_skills = {
        "Python",
        "SQL",
        "Machine Learning",
        "PostgreSQL",
        "Git",
        "GitHub",
    }

    assert expected_skills.issubset(skills)


def test_extract_cv_skills_from_txt(tmp_path: Path) -> None:
    txt_path = tmp_path / "resume.txt"

    txt_path.write_text(
        """
        Python Developer with experience in SQL,
        Git and Machine Learning.
        """,
        encoding="utf-8",
    )

    skills = extract_cv_skills(txt_path)

    expected_skills = {
        "Python",
        "SQL",
        "Git",
        "Machine Learning",
    }

    assert expected_skills.issubset(skills)