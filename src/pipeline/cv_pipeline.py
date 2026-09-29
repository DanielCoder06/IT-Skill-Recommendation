from pathlib import Path

from src.extractor.document_extractor import extract_text_from_document
from src.extractor.extractor_regex import extract_skills


def extract_cv_skills(file_path: str | Path) -> set[str]:
    """
    Extract skills from a CV document.

    Current core pipeline:
        CV PDF/TXT
        -> Document Extraction
        -> Regex Skill Extraction

    Gemini-based extraction is currently disabled and kept
    as an experimental/future-work component.

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