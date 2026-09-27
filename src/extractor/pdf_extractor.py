from pathlib import Path

import pymupdf


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text from all pages.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the provided file is not a PDF file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path.suffix}")

    with pymupdf.open(path) as document:
        pages = [page.get_text() for page in document]

    return "\n".join(pages)