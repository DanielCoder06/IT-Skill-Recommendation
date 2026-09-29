from pathlib import Path

from src.extractor.document_extractor import extract_text_from_document
from src.extractor.extractor_hybrid import extract_hybrid_skills
from src.extractor.extractor_regex import extract_skills


def extract_cv_skills(file_path: str | Path) -> set[str]:
    """
    Extract confirmed skills from a CV document.

    Current core pipeline:
        CV PDF/TXT
        -> Document Extraction
        -> Regex Skill Extraction

    This function is intentionally kept unchanged for
    backward compatibility with the recommendation system.

    Args:
        file_path: Path to the CV document.

    Returns:
        A set of canonical skill names detected in the CV.

    Raises:
        FileNotFoundError: If the CV file does not exist.
        ValueError: If the document format is unsupported.
    """
    cv_text = extract_text_from_document(file_path)

    return extract_skills(cv_text)


def extract_cv_skills_hybrid(
    file_path: str | Path,
) -> dict[str, set[str]]:
    """
    Extract CV skills using the hybrid Regex + NER pipeline.

    Pipeline:
        CV PDF/TXT
        -> Document Extraction
        -> Regex + NER
        -> Normalize NER entities

    Returns:
        {
            "confirmed_skills": set(...),
            "suggested_skills": set(...),
        }

    confirmed_skills:
        Skills detected and confirmed by the existing
        Regex/SkillMatcher pipeline.

    suggested_skills:
        Skills detected by NER and normalized successfully,
        but not already confirmed by Regex.

    Args:
        file_path: Path to the CV document.

    Returns:
        A dictionary containing confirmed and suggested skills.

    Raises:
        FileNotFoundError: If the CV file does not exist.
        ValueError: If the document format is unsupported.
    """
    cv_text = extract_text_from_document(file_path)

    return extract_hybrid_skills(cv_text)