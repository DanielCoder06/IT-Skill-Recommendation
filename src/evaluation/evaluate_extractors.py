from src.evaluation.evaluation_cases import EVALUATION_CASES
from src.extractor.extractor_regex import extract_skills
from src.extractor.extractor_gemini import extract_skills_with_gemini


def calculate_metrics(
    predicted: set[str],
    expected: set[str],
) -> dict[str, float]:

    true_positive = len(predicted & expected)
    false_positive = len(predicted - expected)
    false_negative = len(expected - predicted)

    if true_positive + false_positive == 0:
        precision = 0.0
    else:
        precision = true_positive / (true_positive + false_positive)

    if true_positive + false_negative == 0:
        recall = 0.0
    else:
        recall = true_positive / (true_positive + false_negative)

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def evaluate_regex():
    results = []

    for case in EVALUATION_CASES:
        predicted = extract_skills(case["description"])
        expected = case["expected_skills"]

        metrics = calculate_metrics(predicted, expected)

        results.append(metrics)

        print("\n" + "=" * 60)
        print(f"CASE: {case['name']}")

        print("\nExpected:")
        for skill in sorted(expected):
            print(f"- {skill}")

        print("\nRegex:")
        for skill in sorted(predicted):
            print(f"- {skill}")

        print("\nMetrics:")
        print(f"Precision: {metrics['precision']:.2f}")
        print(f"Recall:    {metrics['recall']:.2f}")
        print(f"F1:        {metrics['f1']:.2f}")

    return results


def evaluate_gemini():
    results = []

    for case in EVALUATION_CASES:
        description = case["description"]
        expected = case["expected_skills"]

        try:
            result = extract_skills_with_gemini(description)
        except Exception as error:
            print("\n" + "=" * 60)
            print(f"CASE: {case['name']}")
            print("Gemini: SKIPPED")
            print(f"Reason: {error}")
            continue

        predicted = set(result.skills)
        metrics = calculate_metrics(predicted, expected)

        results.append(metrics)

        print("\n" + "=" * 60)
        print(f"CASE: {case['name']}")

        print("\nExpected:")
        for skill in sorted(expected):
            print(f"- {skill}")

        print("\nGemini:")
        for skill in sorted(predicted):
            print(f"- {skill}")

        print("\nMetrics:")
        print(f"Precision: {metrics['precision']:.2f}")
        print(f"Recall:    {metrics['recall']:.2f}")
        print(f"F1:        {metrics['f1']:.2f}")

    return results


def calculate_overall_metrics(
    results: list[dict[str, float]],
) -> dict[str, float]:

    if not results:
        return {
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
        }

    return {
        "precision": sum(
            result["precision"] for result in results
        ) / len(results),

        "recall": sum(
            result["recall"] for result in results
        ) / len(results),

        "f1": sum(
            result["f1"] for result in results
        ) / len(results),
    }


if __name__ == "__main__":
    regex_results = evaluate_regex()
    gemini_results = evaluate_gemini()

    regex_overall = calculate_overall_metrics(regex_results)
    gemini_overall = calculate_overall_metrics(gemini_results)

    print("\n" + "=" * 60)
    print("OVERALL RESULTS")

    print("\nRegex:")
    print(f"Precision: {regex_overall['precision']:.2f}")
    print(f"Recall:    {regex_overall['recall']:.2f}")
    print(f"F1:        {regex_overall['f1']:.2f}")

    print("\nGemini:")
    print(f"Precision: {gemini_overall['precision']:.2f}")
    print(f"Recall:    {gemini_overall['recall']:.2f}")
    print(f"F1:        {gemini_overall['f1']:.2f}")