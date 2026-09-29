from src.evaluation.evaluation_cases import EVALUATION_CASES
from src.extractor.extractor_regex import extract_skills
from src.extractor.extractor_gemini import extract_skills_with_gemini
from src.extractor.skill_merger import merge_skills
from src.extractor.extractor_local_llm import extract_skills_with_local_llm


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

def evaluate_hybrid():
    results = []

    for case in EVALUATION_CASES:
        description = case["description"]
        expected = case["expected_skills"]

        regex_skills = extract_skills(description)

        try:
            gemini_result = extract_skills_with_gemini(description)
            gemini_skills = set(gemini_result.skills)
        except Exception as error:
            print("\n" + "=" * 60)
            print(f"CASE: {case['name']}")
            print("Gemini: FAILED")
            print(f"Reason: {error}")
            gemini_skills = set()

        hybrid_skills = merge_skills(
            regex_skills,
            gemini_skills,
        )

        metrics = calculate_metrics(
            hybrid_skills,
            expected,
        )

        results.append(metrics)

        print("\n" + "=" * 60)
        print(f"CASE: {case['name']}")

        print("\nExpected:")
        for skill in sorted(expected):
            print(f"- {skill}")

        print("\nRegex:")
        for skill in sorted(regex_skills):
            print(f"- {skill}")

        print("\nGemini:")
        for skill in sorted(gemini_skills):
            print(f"- {skill}")

        print("\nHybrid:")
        for skill in sorted(hybrid_skills):
            print(f"- {skill}")

        print("\nMetrics:")
        print(f"Precision: {metrics['precision']:.2f}")
        print(f"Recall:    {metrics['recall']:.2f}")
        print(f"F1:        {metrics['f1']:.2f}")

    return results

def evaluate_local_llm():
    results = []

    for case in EVALUATION_CASES:
        description = case["description"]
        expected = case["expected_skills"]

        try:
            local_llm_skills = extract_skills_with_local_llm(description)
        except Exception as error:
            print(f"Local LLM error: {error}")
            local_llm_skills = set()

        metrics = calculate_metrics(
            predicted=local_llm_skills,
            expected=expected,
        )

        results.append(metrics)

        print(f"\nCase: {case['name']}")
        print(f"Expected: {expected}")
        print(f"Local LLM: {local_llm_skills}")
        print(f"Metrics: {metrics}")

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
    hybrid_results = evaluate_hybrid()
    local_llm_results = evaluate_local_llm()

    regex_overall = calculate_overall_metrics(regex_results)
    gemini_overall = calculate_overall_metrics(gemini_results)
    hybrid_overall = calculate_overall_metrics(hybrid_results)
    local_llm_overall = calculate_overall_metrics(
        local_llm_results
    )

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
    
    print("\nHybrid:")
    print(f"Precision: {hybrid_overall['precision']:.2f}")
    print(f"Recall:    {hybrid_overall['recall']:.2f}")
    print(f"F1:        {hybrid_overall['f1']:.2f}")

    print("\n=== Local LLM Overall ===")
    print(local_llm_overall)