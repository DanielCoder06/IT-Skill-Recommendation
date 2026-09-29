# -*- coding: utf-8 -*-

from pathlib import Path

import spacy

from experiments.ner.skill_matcher import SkillMatcher


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "experiments"
    / "ner"
    / "models"
    / "skill_ner_v1"
    / "model-best"
)

SKILL_DICTIONARY_PATH = (
    BASE_DIR
    / "config"
    / "skills_dictionary.json"
)


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [
    # --------------------------------------------------------
    # 1. Basic English
    # --------------------------------------------------------
    {
        "text": "I have experience with Python and SQL.",
        "expected": {"Python", "SQL"},
    },
    {
        "text": "Developed backend applications using Java and Spring Boot.",
        "expected": {"Java", "Spring Boot"},
    },

    # --------------------------------------------------------
    # 2. Alternative wording
    # --------------------------------------------------------
    {
        "text": "Built predictive models using machine learning techniques.",
        "expected": {"Machine Learning"},
    },
    {
        "text": "Worked on neural-network based applications.",
        "expected": {"Deep Learning"},
    },
    {
        "text": "Performed data manipulation with Pandas.",
        "expected": {"Pandas"},
    },
    {
        "text": "Created RESTful web services for internal applications.",
        "expected": {"REST API"},
    },

    # --------------------------------------------------------
    # 3. Vietnamese
    # --------------------------------------------------------
    {
        "text": "Có kinh nghiệm lập trình Python và làm việc với cơ sở dữ liệu SQL.",
        "expected": {"Python", "SQL"},
    },
    {
        "text": "Đã thực hiện các dự án học máy và phân tích dữ liệu.",
        "expected": {"Machine Learning", "Data Analysis"},
    },
    {
        "text": "Có kinh nghiệm xây dựng mô hình học sâu bằng PyTorch.",
        "expected": {"Deep Learning", "PyTorch"},
    },
    {
        "text": "Đã phát triển API REST cho hệ thống web.",
        "expected": {"REST API"},
    },

    # --------------------------------------------------------
    # 4. Abbreviation / short forms
    # --------------------------------------------------------
    {
        "text": "Worked on ML models for customer prediction.",
        "expected": {"Machine Learning"},
    },
    {
        "text": "Experience with DL architectures and PyTorch.",
        "expected": {"Deep Learning", "PyTorch"},
    },
    {
        "text": "Developed APIs following REST principles.",
        "expected": {"REST API"},
    },

    # --------------------------------------------------------
    # 5. Mixed Vietnamese + English
    # --------------------------------------------------------
    {
        "text": "Sử dụng Pandas để xử lý dữ liệu và xây dựng ML models.",
        "expected": {"Pandas", "Machine Learning"},
    },
    {
        "text": "Phát triển backend service bằng Python và FastAPI.",
        "expected": {"Python", "FastAPI"},
    },
    {
        "text": "Xây dựng hệ thống sử dụng Docker và Git.",
        "expected": {"Docker", "Git"},
    },

    # --------------------------------------------------------
    # 6. Multiple skills in one sentence
    # --------------------------------------------------------
    {
        "text": (
            "Developed machine learning applications using Python, "
            "Pandas, NumPy and Scikit-learn."
        ),
        "expected": {
            "Machine Learning",
            "Python",
            "Pandas",
            "NumPy",
            "Scikit-learn",
        },
    },
    {
        "text": (
            "Built backend services with Java, Spring Boot, "
            "Docker and PostgreSQL."
        ),
        "expected": {
            "Java",
            "Spring Boot",
            "Docker",
            "PostgreSQL",
        },
    },

    # --------------------------------------------------------
    # 7. No-skill sentences
    # --------------------------------------------------------
    {
        "text": (
            "I worked closely with the development team to "
            "complete several projects."
        ),
        "expected": set(),
    },
    {
        "text": (
            "I analyzed business requirements and prepared "
            "technical documents."
        ),
        "expected": set(),
    },
    {
        "text": (
            "Responsible for communicating with customers and "
            "coordinating project activities."
        ),
        "expected": set(),
    },
    {
        "text": (
            "Interested in learning new technologies and "
            "working in a collaborative environment."
        ),
        "expected": set(),
    },

    # --------------------------------------------------------
    # 8. Potentially ambiguous / semantic cases
    # --------------------------------------------------------
    {
        "text": "Worked with statistical analysis for business data.",
        "expected": {"Statistics"},
    },
    {
        "text": "Performed exploratory analysis on large datasets.",
        "expected": {"Data Analysis"},
    },
    {
        "text": "Designed object-oriented software components.",
        "expected": {"Object-Oriented Programming"},
    },
]


# ============================================================
# HELPERS
# ============================================================

def normalize_ner_skill(
    ner_text: str,
    matcher: SkillMatcher,
) -> str | None:
    """
    Cố gắng map text mà NER nhận diện về canonical skill.

    Quan trọng:
    - Không tự tạo skill mới.
    - Chỉ nhận nếu SkillMatcher có thể map được span đó.
    - Nếu không map được thì giữ lại dưới dạng raw NER ở output.
    """

    matched = matcher.extract(ner_text)

    if not matched:
        return None

    return matched[0]["skill"]


def get_ner_skills(
    nlp,
    text: str,
    matcher: SkillMatcher,
) -> tuple[list[str], set[str]]:
    """
    Trả về:
        raw_entities
        normalized_skills
    """

    doc = nlp(text)

    raw_entities = []
    normalized_skills = set()

    for ent in doc.ents:
        if ent.label_ != "SKILL":
            continue

        raw_text = ent.text.strip()

        if not raw_text:
            continue

        raw_entities.append(raw_text)

        normalized = normalize_ner_skill(
            raw_text,
            matcher,
        )

        if normalized:
            normalized_skills.add(normalized)

    return raw_entities, normalized_skills


def calculate_metrics(
    expected: set[str],
    predicted: set[str],
) -> tuple[int, int, int]:
    """
    Tính TP / FP / FN.
    """

    true_positive = len(expected & predicted)
    false_positive = len(predicted - expected)
    false_negative = len(expected - predicted)

    return true_positive, false_positive, false_negative


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():
    print("=" * 70)
    print("NER SUPPLEMENT EVALUATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy NER model:\n{MODEL_PATH}"
        )

    # --------------------------------------------------------
    # Load NER
    # --------------------------------------------------------

    print("\nLoading NER model...")

    nlp = spacy.load(MODEL_PATH)

    print(f"Model: {MODEL_PATH}")

    # --------------------------------------------------------
    # Load SkillMatcher
    # --------------------------------------------------------

    print("\nLoading SkillMatcher...")

    matcher = SkillMatcher(SKILL_DICTIONARY_PATH)

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    matcher_tp = 0
    matcher_fp = 0
    matcher_fn = 0

    ner_tp = 0
    ner_fp = 0
    ner_fn = 0

    new_ner_total = 0
    new_ner_correct = 0
    new_ner_false_positive = 0

    # --------------------------------------------------------
    # Run test cases
    # --------------------------------------------------------

    for index, case in enumerate(TEST_CASES, start=1):

        text = case["text"]
        expected = set(case["expected"])

        matcher_skills = matcher.skills(text)

        raw_ner, ner_skills = get_ner_skills(
            nlp,
            text,
            matcher,
        )

        # ----------------------------------------------------
        # Metrics for SkillMatcher
        # ----------------------------------------------------

        tp, fp, fn = calculate_metrics(
            expected,
            matcher_skills,
        )

        matcher_tp += tp
        matcher_fp += fp
        matcher_fn += fn

        # ----------------------------------------------------
        # Metrics for NER
        # ----------------------------------------------------

        tp, fp, fn = calculate_metrics(
            expected,
            ner_skills,
        )

        ner_tp += tp
        ner_fp += fp
        ner_fn += fn

        # ----------------------------------------------------
        # New skills from NER
        # ----------------------------------------------------

        new_ner = ner_skills - matcher_skills

        new_ner_correct_set = new_ner & expected
        new_ner_fp_set = new_ner - expected

        new_ner_total += len(new_ner)
        new_ner_correct += len(new_ner_correct_set)
        new_ner_false_positive += len(new_ner_fp_set)

        # ----------------------------------------------------
        # Output
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print(f"CASE {index}")
        print("-" * 70)

        print(f"Text:")
        print(text)

        print(f"\nExpected:")
        print(
            sorted(expected)
            if expected
            else "[]"
        )

        print(f"\nSkillMatcher:")
        print(
            sorted(matcher_skills)
            if matcher_skills
            else "[]"
        )

        print(f"\nNER raw:")
        print(
            raw_ner
            if raw_ner
            else "[]"
        )

        print(f"\nNER normalized:")
        print(
            sorted(ner_skills)
            if ner_skills
            else "[]"
        )

        print(f"\nNew skills from NER:")
        print(
            sorted(new_ner)
            if new_ner
            else "[]"
        )

        if new_ner_correct_set:
            print(
                f"New correct skills: "
                f"{sorted(new_ner_correct_set)}"
            )

        if new_ner_fp_set:
            print(
                f"New false positives: "
                f"{sorted(new_ner_fp_set)}"
            )

    # ========================================================
    # FINAL METRICS
    # ========================================================

    def metric_values(tp, fp, fn):
        precision = (
            tp / (tp + fp)
            if tp + fp > 0
            else 0.0
        )

        recall = (
            tp / (tp + fn)
            if tp + fn > 0
            else 0.0
        )

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0
            else 0.0
        )

        return precision, recall, f1

    matcher_precision, matcher_recall, matcher_f1 = metric_values(
        matcher_tp,
        matcher_fp,
        matcher_fn,
    )

    ner_precision, ner_recall, ner_f1 = metric_values(
        ner_tp,
        ner_fp,
        ner_fn,
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n\n")
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    print("\nSkillMatcher")
    print(f"  TP:        {matcher_tp}")
    print(f"  FP:        {matcher_fp}")
    print(f"  FN:        {matcher_fn}")
    print(f"  Precision: {matcher_precision:.2%}")
    print(f"  Recall:    {matcher_recall:.2%}")
    print(f"  F1:        {matcher_f1:.2%}")

    print("\nNER")
    print(f"  TP:        {ner_tp}")
    print(f"  FP:        {ner_fp}")
    print(f"  FN:        {ner_fn}")
    print(f"  Precision: {ner_precision:.2%}")
    print(f"  Recall:    {ner_recall:.2%}")
    print(f"  F1:        {ner_f1:.2%}")

    print("\nNER Supplement")
    print(f"  New NER skills:          {new_ner_total}")
    print(f"  New correct skills:      {new_ner_correct}")
    print(f"  New false positives:     {new_ner_false_positive}")

    if new_ner_total > 0:
        supplement_precision = (
            new_ner_correct / new_ner_total
        )
    else:
        supplement_precision = 0.0

    print(
        f"  Supplement precision:    "
        f"{supplement_precision:.2%}"
    )

    print("\n" + "=" * 70)

    if new_ner_correct > 0 and new_ner_false_positive == 0:
        print(
            "RESULT: NER có dấu hiệu bổ sung skill mới "
            "mà không tạo false positive trong test này."
        )
    elif new_ner_correct > 0:
        print(
            "RESULT: NER có bổ sung skill mới nhưng "
            "cần kiểm soát false positive."
        )
    else:
        print(
            "RESULT: Chưa chứng minh được NER bổ sung "
            "skill mới so với SkillMatcher."
        )

    print("=" * 70)


if __name__ == "__main__":
    main()