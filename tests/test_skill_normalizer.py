from pathlib import Path

import pytest

from src.extractor.skill_normalizer import (
    create_skill_matcher,
    normalize_ner_entities,
    normalize_ner_skill,
)


DICTIONARY_PATH = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "skills_dictionary.json"
)


@pytest.fixture(scope="module")
def matcher():
    return create_skill_matcher(DICTIONARY_PATH)


def test_normalize_python(matcher):
    result = normalize_ner_skill("Python", matcher)

    assert result == "Python"


def test_normalize_python_alias(matcher):
    result = normalize_ner_skill("python3", matcher)

    assert result == "Python"


def test_normalize_sql(matcher):
    result = normalize_ner_skill("SQL", matcher)

    assert result == "SQL"


def test_unknown_skill_returns_none(matcher):
    result = normalize_ner_skill(
        "SomeUnknownSkill",
        matcher,
    )

    assert result is None


def test_empty_entity_returns_none(matcher):
    assert normalize_ner_skill("", matcher) is None
    assert normalize_ner_skill("   ", matcher) is None


def test_normalize_multiple_entities(matcher):
    entities = [
        "Python",
        "python3",
        "SQL",
    ]

    result = normalize_ner_entities(
        entities,
        matcher,
    )

    assert result == {
        "Python",
        "SQL",
    }