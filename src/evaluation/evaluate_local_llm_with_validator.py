from src.evaluation.evaluation_cases import EVALUATION_CASES
from src.evaluation.evaluate_extractors import (
    calculate_metrics,
    calculate_overall_metrics,
)
from src.extractor.extractor_local_llm import (
    extract_skills_with_local_llm,
    load_skill_dictionary,
)
from src.extractor.skill_evidence_validator import validate_skills


def evaluate_local_llm_with_validator():
    """
    Đánh giá Local LLM sau khi đi qua Evidence Validator.
    """
    skill_dictionary = load_skill_dictionary()

    results = []

    for case in EVALUATION_CASES:
        description = case["description"]
        expected = case["expected_skills"]

        try:
            candidate_skills = extract_skills_with_local_llm(
                description
            )

            validated_skills = validate_skills(
                text=description,
                candidate_skills=candidate_skills,
                skill_dictionary=skill_dictionary,
            )

        except Exception as error:
            print(f"Local LLM error: {error}")
            candidate_skills = set()
            validated_skills = set()

        metrics = calculate_metrics(
            predicted=validated_skills,
            expected=expected,
        )

        results.append(metrics)

        print(f"\nCase: {case['name']}")
        print(f"Expected:   {expected}")
        print(f"Candidate:  {candidate_skills}")
        print(f"Validated:  {validated_skills}")
        print(f"Metrics:    {metrics}")

    overall = calculate_overall_metrics(results)

    print("\n=== Local LLM + Evidence Validator Overall ===")
    print(f"Precision: {overall['precision']:.2f}")
    print(f"Recall:    {overall['recall']:.2f}")
    print(f"F1:        {overall['f1']:.2f}")

    return results


if __name__ == "__main__":
    evaluate_local_llm_with_validator()