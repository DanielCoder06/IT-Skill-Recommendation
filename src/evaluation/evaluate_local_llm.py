from src.evaluation.evaluation_cases import EVALUATION_CASES
from src.evaluation.evaluate_extractors import (
    calculate_metrics,
    calculate_overall_metrics,
)
from src.extractor.extractor_local_llm import extract_skills_with_local_llm


def evaluate_local_llm():
    """Đánh giá Local LLM trên toàn bộ evaluation cases."""
    results = []

    for case in EVALUATION_CASES:
        description = case["description"]
        expected = case["expected_skills"]

        try:
            predicted = extract_skills_with_local_llm(description)
        except Exception as error:
            print(f"Local LLM error: {error}")
            predicted = set()

        metrics = calculate_metrics(
            predicted=predicted,
            expected=expected,
        )

        results.append(metrics)

        print(f"\nCase: {case['name']}")
        print(f"Expected: {expected}")
        print(f"Local LLM: {predicted}")
        print(f"Metrics: {metrics}")

    overall = calculate_overall_metrics(results)

    print("\n=== Local LLM Overall ===")
    print(f"Precision: {overall['precision']:.2f}")
    print(f"Recall:    {overall['recall']:.2f}")
    print(f"F1:        {overall['f1']:.2f}")

    return results


if __name__ == "__main__":
    evaluate_local_llm()