import html
import re


def clean_job_description(text: str) -> str:
    """
    Convert encoded HTML job description into clean plain text.
    """
    text = html.unescape(text)

    # Replace common block-level HTML tags with line breaks
    text = re.sub(
        r"<(br|p|div|li|h[1-6]|tr|hr)[^>]*>",
        "\n",
        text,
        flags=re.IGNORECASE,
    )

    # Remove remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()