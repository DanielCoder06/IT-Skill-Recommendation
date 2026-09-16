from src.evaluation.evaluation_cases import EVALUATION_CASES


def test_evaluation_cases_are_valid():
    assert EVALUATION_CASES

    for case in EVALUATION_CASES:
        assert case["name"]
        assert case["description"]
        assert case["expected_skills"]

        assert isinstance(case["expected_skills"], set)