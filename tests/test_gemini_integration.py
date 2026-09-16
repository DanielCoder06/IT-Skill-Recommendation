import pytest

from src.extractor.extractor_gemini import extract_skills_with_gemini


@pytest.mark.integration
def test_extract_skills_with_gemini():
    jd_text = """
    We are looking for a Python Intern.

    Requirements:
    - Basic knowledge of Python and SQL
    - Familiarity with Pandas and NumPy
    - Knowledge of Git and GitHub
    - Understanding of Machine Learning is a plus
    """

    result = extract_skills_with_gemini(jd_text)

    print("\nGemini skills:", result.skills)

    assert result.skills