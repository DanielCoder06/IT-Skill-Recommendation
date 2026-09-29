from pathlib import Path

import pytest

from src.extractor.extractor_hybrid import extract_hybrid_skills


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "ner"
    / "models"
    / "skill_ner_v1"
    / "model-best"
)


def test_hybrid_returns_expected_structure():
    text = "I have experience with Python and SQL."

    result = extract_hybrid_skills(
        text,
        MODEL_PATH,
    )

    assert "confirmed_skills" in result
    assert "suggested_skills" in result

    assert isinstance(result["confirmed_skills"], set)
    assert isinstance(result["suggested_skills"], set)


def test_regex_skills_are_confirmed():
    text = "I have experience with Python and SQL."

    result = extract_hybrid_skills(
        text,
        MODEL_PATH,
    )

    assert "Python" in result["confirmed_skills"]
    assert "SQL" in result["confirmed_skills"]


def test_ner_does_not_duplicate_confirmed_skills():
    text = "I have experience with Python and SQL."

    result = extract_hybrid_skills(
        text,
        MODEL_PATH,
    )

    assert not (
        result["confirmed_skills"]
        & result["suggested_skills"]
    )


def test_empty_text():
    result = extract_hybrid_skills(
        "",
        MODEL_PATH,
    )

    assert result == {
        "confirmed_skills": set(),
        "suggested_skills": set(),
    }


def test_no_skill_sentence():
    text = (
        "I worked closely with the development team "
        "to complete several projects."
    )

    result = extract_hybrid_skills(
        text,
        MODEL_PATH,
    )

    assert result["confirmed_skills"] == set()
    assert result["suggested_skills"] == set()