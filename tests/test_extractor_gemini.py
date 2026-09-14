import pytest
from pydantic import ValidationError

from src.extractor.extractor_gemini import GeminiSkillOutput


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
        
def test_extra_field_is_rejected():
    with pytest.raises(ValidationError):
        GeminiSkillOutput(
            skills=["Python"],
            reason="Some explanation"
        )