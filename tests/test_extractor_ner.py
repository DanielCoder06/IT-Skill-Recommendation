from pathlib import Path

import pytest

from src.extractor.extractor_ner import (
    extract_ner_entities,
    extract_ner_entities_detailed,
    load_ner_model,
)


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "ner"
    / "models"
    / "skill_ner_v1"
    / "model-best"
)


@pytest.fixture(scope="module")
def nlp():
    return load_ner_model(MODEL_PATH)


def test_load_ner_model(nlp):
    assert nlp is not None


def test_extract_python_and_sql(nlp):
    text = "I have experience with Python and SQL."

    skills = set(
        extract_ner_entities(
            text,
            nlp,
        )
    )

    assert "Python" in skills
    assert "SQL" in skills


def test_extract_multiple_skills(nlp):
    text = (
        "Developed machine learning applications "
        "using Python, Pandas and NumPy."
    )

    skills = set(
        extract_ner_entities(
            text,
            nlp,
        )
    )

    assert "Python" in skills


def test_no_skill_sentence(nlp):
    text = (
        "I worked closely with the development team "
        "to complete several projects."
    )

    skills = extract_ner_entities(
        text,
        nlp,
    )

    assert skills == []


def test_empty_text(nlp):
    assert extract_ner_entities("", nlp) == []


def test_detailed_entities(nlp):
    text = "I have experience with Python."

    entities = extract_ner_entities_detailed(
        text,
        nlp,
    )

    assert isinstance(entities, list)

    for entity in entities:
        assert entity["label"] == "SKILL"
        assert entity["start"] < entity["end"]
        assert entity["text"]