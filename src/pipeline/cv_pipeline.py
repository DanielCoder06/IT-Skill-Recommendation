from pathlib import Path

from src.extractor.document_extractor import extract_text_from_document
from src.extractor.extractor_regex import extract_skills
from src.extractor.extractor_gemini import extract_skills_with_gemini
from src.extractor.skill_merger import merge_skills

def extract_cv_skills(file_path: str | Path) -> set[str]:
    """
    Extract skills from a CV document.

    The document can be a PDF or TXT file.

    Args:
        file_path: Path to the CV document.

    Returns:
        A set of canonical skill names detected in the CV.

    Raises:
        FileNotFoundError: If the CV file does not exist.
        ValueError: If the document format is unsupported.
    """
    cv_text = extract_text_from_document(file_path)

    regex_skills = extract_skills(cv_text)

    try:
        gemini_result = extract_skills_with_gemini(cv_text)
        gemini_skills = set(gemini_result.skills)
    except Exception as error:
        print(f"Gemini error: {error}")
        gemini_skills = set()

    return merge_skills(
        regex_skills,
        gemini_skills,
    )