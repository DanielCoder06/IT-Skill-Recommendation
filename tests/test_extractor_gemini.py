import pytest
from pydantic import ValidationError

from src.extractor.extractor_gemini import GeminiSkillOutput, build_gemini_prompt


def test_valid_output():
    result = GeminiSkillOutput(
        skills=["Python", "SQL", "Machine Learning"]
    )

    assert result.skills == [
        "Python",
        "SQL",
        "Machine Learning"
    ]


def test_skills_must_be_list():
    with pytest.raises(ValidationError):
        GeminiSkillOutput(
            skills="Python"
        )


def test_empty_skills_not_allowed():
    with pytest.raises(ValidationError):
        GeminiSkillOutput(
            skills=[]
        )


def test_skills_must_be_strings():
    with pytest.raises(ValidationError):
        GeminiSkillOutput(
            skills=[1, 2, 3]
        )
        
def test_unknown_skill_is_rejected():
    with pytest.raises(ValidationError):
        GeminiSkillOutput(
            skills=["Python", "SQL", "Quantum Computing"]
        )

def test_build_gemini_prompt():
    jd_text = """
    We are looking for a Python intern with knowledge of SQL and Pandas.
    """

    prompt = build_gemini_prompt(jd_text)

    assert "JOB DESCRIPTION:" in prompt
    assert jd_text in prompt

    assert "Python" in prompt
    assert "SQL" in prompt
    assert "Pandas" in prompt

    assert "Only select skills from the allowed skill list." in prompt