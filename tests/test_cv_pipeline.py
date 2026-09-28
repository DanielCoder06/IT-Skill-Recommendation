from pathlib import Path

import pymupdf

from src.extractor.extractor_gemini import GeminiSkillOutput
from src.pipeline.cv_pipeline import extract_cv_skills


def create_test_pdf(file_path: Path, text: str) -> None:
    """Create a simple PDF containing the given text."""
    document = pymupdf.open()

    page = document.new_page()
    page.insert_text((72, 72), text)

    document.save(file_path)
    document.close()


def mock_gemini_skills(text: str) -> GeminiSkillOutput:
    """
    Mock Gemini skill extraction for unit tests.
    """
    return GeminiSkillOutput(
        skills=[
            "Python",
            "SQL",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "PostgreSQL",
            "Git",
            "GitHub",
        ]
    )


def test_extract_cv_skills_from_pdf(
    tmp_path: Path,
    monkeypatch,
) -> None:
    pdf_path = tmp_path / "resume.pdf"

    cv_text = """
    Data Analyst with experience in Python, SQL and Machine Learning.
    Used Pandas, NumPy, PostgreSQL, Git and GitHub.
    """

    create_test_pdf(pdf_path, cv_text)

    monkeypatch.setattr(
        "src.pipeline.cv_pipeline.extract_skills_with_gemini",
        mock_gemini_skills,
    )

    skills = extract_cv_skills(pdf_path)

    expected_skills = {
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "PostgreSQL",
        "Git",
        "GitHub",
    }

    assert expected_skills.issubset(skills)


def test_extract_cv_skills_from_txt(
    tmp_path: Path,
    monkeypatch,
) -> None:
    txt_path = tmp_path / "resume.txt"

    txt_path.write_text(
        """
        Python Developer with experience in SQL,
        Git and Machine Learning.
        """,
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "src.pipeline.cv_pipeline.extract_skills_with_gemini",
        mock_gemini_skills,
    )

    skills = extract_cv_skills(txt_path)

    expected_skills = {
        "Python",
        "SQL",
        "Git",
        "Machine Learning",
    }

    assert expected_skills.issubset(skills)