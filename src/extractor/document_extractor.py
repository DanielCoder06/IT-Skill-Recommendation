from pathlib import Path

from src.extractor.pdf_extractor import extract_text_from_pdf
from src.extractor.text_extractor import extract_text_from_file


def extract_text_from_document(file_path: str | Path) -> str:
    """
    Extract text from a supported document.

    Supported formats:
        - PDF
        - TXT

    Args:
        file_path: Path to the document.

    Returns:
        Extracted text as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is unsupported.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(path)

    if extension == ".txt":
        return extract_text_from_file(path)

    raise ValueError(
        f"Unsupported document format: {extension}"
    )