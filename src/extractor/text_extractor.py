from pathlib import Path


def extract_text_from_file(file_path: str | Path) -> str:
    """
    Read text content from a UTF-8 text file.

    Args:
        file_path: Path to the text file.

    Returns:
        The content of the text file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the provided file is not a .txt file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Text file not found: {path}")

    if path.suffix.lower() != ".txt":
        raise ValueError(f"Expected a .txt file, got: {path.suffix}")

    return path.read_text(encoding="utf-8")