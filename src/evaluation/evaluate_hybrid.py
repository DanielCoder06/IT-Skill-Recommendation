from src.evaluation.evaluation_cases import EVALUATION_CASES
from src.evaluation.evaluate_extractors import (
    calculate_metrics,
    calculate_overall_metrics,
)
from src.extractor.extractor_local_llm import extract_skills_with_local_llm
from src.extractor.extractor_regex import extract_skills


def evaluate_hybrid():
    """Đánh giá Hybrid Regex + Local LLM."""

    results = []

    for case in EVALUATION_CASES:
        description = case["description"]
        expected = case["expected_skills"]

        try:
            regex_skills = extract_skills(description)
        except Exception as error:
            print(f"Regex error: {error}")
            regex_skills = set()

        try:
            local_llm_skills = extract_skills_with_local_llm(description)
        except Exception as error:
            print(f"Local LLM error: {error}")
            local_llm_skills = set()

        hybrid_skills = regex_skills | local_llm_skills

        metrics = calculate_metrics(
            predicted=hybrid_skills,
            expected=expected,
        )

        results.append(metrics)

        print(f"\nCase: {case['name']}")
        print(f"Expected:    {expected}")
        print(f"Regex:       {regex_skills}")
        print(f"Local LLM:   {local_llm_skills}")
        print(f"Hybrid:      {hybrid_skills}")
        print(f"Metrics:     {metrics}")

    overall = calculate_overall_metrics(results)

    print("\n=== Hybrid Overall ===")
    print(f"Precision: {overall['precision']:.2f}")
    print(f"Recall:    {overall['recall']:.2f}")
    print(f"F1:        {overall['f1']:.2f}")

    return results


if __name__ == "__main__":
    evaluate_hybrid()