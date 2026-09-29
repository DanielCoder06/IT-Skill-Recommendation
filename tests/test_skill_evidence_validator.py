from src.extractor.skill_evidence_validator import (
    has_skill_evidence,
    validate_skills,
)


def test_validate_explicit_canonical_skill():
    skill_dictionary = {
        "Python": {
            "aliases": ["python"],
        }
    }

    text = "Experience with Python."

    assert has_skill_evidence(
        text=text,
        skill="Python",
        skill_dictionary=skill_dictionary,
    )


def test_validate_skill_from_alias():
    skill_dictionary = {
        "REST API": {
            "aliases": [
                "RESTful services",
            ],
        }
    }

    text = "Experience building RESTful services."

    assert has_skill_evidence(
        text=text,
        skill="REST API",
        skill_dictionary=skill_dictionary,
    )


def test_reject_skill_without_evidence():
    skill_dictionary = {
        "NumPy": {
            "aliases": [
                "numpy",
                "np",
            ],
        }
    }

    text = (
        "Experience analyzing structured datasets "
        "and performing statistical analysis."
    )

    assert not has_skill_evidence(
        text=text,
        skill="NumPy",
        skill_dictionary=skill_dictionary,
    )


def test_validate_filters_false_positive():
    skill_dictionary = {
        "Python": {
            "aliases": ["python"],
        },
        "Pandas": {
            "aliases": ["pandas"],
        },
        "NumPy": {
            "aliases": ["numpy", "np"],
        },
    }

    text = "Experience with Python and Pandas."

    candidate_skills = {
        "Python",
        "Pandas",
        "NumPy",
    }

    result = validate_skills(
        text=text,
        candidate_skills=candidate_skills,
        skill_dictionary=skill_dictionary,
    )

    assert result == {
        "Python",
        "Pandas",
    }


def test_validator_does_not_add_new_skills():
    skill_dictionary = {
        "Python": {
            "aliases": ["python"],
        },
        "Pandas": {
            "aliases": ["pandas"],
        },
    }

    text = "Experience with Python."

    candidate_skills = {
        "Python",
    }

    result = validate_skills(
        text=text,
        candidate_skills=candidate_skills,
        skill_dictionary=skill_dictionary,
    )

    assert result == {
        "Python",
    }
    
def test_case_sensitive_alias_is_valid():
    skill_dictionary = {
        "C": {
            "aliases": [],
            "case_sensitive_aliases": ["C"],
            "ambiguous_aliases": {},
        }
    }

    text = "Experience with C programming."

    assert has_skill_evidence(
        text=text,
        skill="C",
        skill_dictionary=skill_dictionary,
    )


def test_ambiguous_alias_without_context_is_rejected():
    skill_dictionary = {
        "React": {
            "aliases": [],
            "case_sensitive_aliases": [],
            "ambiguous_aliases": {
                "react": ["JavaScript", "frontend", "library"]
            },
        }
    }

    text = "The system can react quickly."

    assert not has_skill_evidence(
        text=text,
        skill="React",
        skill_dictionary=skill_dictionary,
    )


def test_ambiguous_alias_with_context_is_valid():
    skill_dictionary = {
        "React": {
            "aliases": [],
            "case_sensitive_aliases": [],
            "ambiguous_aliases": {
                "react": ["JavaScript", "frontend", "library"]
            },
        }
    }

    text = "Experience with React and JavaScript frontend development."

    assert has_skill_evidence(
        text=text,
        skill="React",
        skill_dictionary=skill_dictionary,
    )


def test_negative_pattern_rejects_skill():
    skill_dictionary = {
        "C": {
            "aliases": [],
            "case_sensitive_aliases": ["C"],
            "ambiguous_aliases": {},
            "negative_patterns": [
                r"\bC\+\+"
            ],
        }
    }

    text = "Experience with C++."

    assert not has_skill_evidence(
        text=text,
        skill="C",
        skill_dictionary=skill_dictionary,
    )