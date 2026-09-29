from unittest.mock import Mock, patch

from src.extractor.extractor_local_llm import (
    build_prompt,
    build_skill_reference,
    load_skill_dictionary,
    parse_skill_response,
)


def test_load_skill_dictionary():
    skill_dictionary = load_skill_dictionary()

    assert isinstance(skill_dictionary, dict)
    assert "Python" in skill_dictionary
    assert "Pandas" in skill_dictionary
    assert "NumPy" in skill_dictionary
    assert "Machine Learning" in skill_dictionary
    assert "Deep Learning" in skill_dictionary
    assert "REST API" in skill_dictionary


def test_build_skill_reference():
    skill_dictionary = {
        "Python": {
            "aliases": ["python", "python programming"],
        },
        "Pandas": {
            "aliases": ["pandas", "python pandas"],
        },
    }

    reference = build_skill_reference(skill_dictionary)

    assert "Python:" in reference
    assert "python" in reference
    assert "Pandas:" in reference
    assert "python pandas" in reference


def test_build_prompt_contains_text_and_rules():
    prompt = build_prompt(
        text="Experience with Python and Pandas.",
        skill_reference="Python: python\nPandas: pandas",
    )

    assert "Experience with Python and Pandas." in prompt
    assert "Python: python" in prompt
    assert "Pandas: pandas" in prompt
    assert "Do NOT infer skills from the general meaning of a sentence." in prompt    
    assert "Return only canonical skill names." in prompt


def test_parse_skill_response_accepts_canonical_skills():
    skill_dictionary = {
        "Python": {"aliases": ["python"]},
        "Pandas": {"aliases": ["pandas"]},
    }

    response = """
    - Python
    - Pandas
    """

    result = parse_skill_response(
        response_text=response,
        skill_dictionary=skill_dictionary,
    )

    assert result == {"Python", "Pandas"}


def test_parse_skill_response_ignores_unknown_skills():
    skill_dictionary = {
        "Python": {"aliases": ["python"]},
        "Pandas": {"aliases": ["pandas"]},
    }

    response = """
    - Python
    - NumPy
    - Something Random
    """

    result = parse_skill_response(
        response_text=response,
        skill_dictionary=skill_dictionary,
    )

    assert result == {"Python"}


@patch("src.extractor.extractor_local_llm.requests.post")
def test_extract_skills_with_local_llm(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "response": """
        - Python
        - Pandas
        """
    }

    mock_post.return_value = mock_response

    from src.extractor.extractor_local_llm import (
        extract_skills_with_local_llm,
    )

    result = extract_skills_with_local_llm(
        "Experience with Python and Pandas."
    )

    assert result == {"Python", "Pandas"}

    mock_post.assert_called_once()