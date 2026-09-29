# -*- coding: utf-8 -*-

from pathlib import Path

import spacy

from skill_matcher import SkillMatcher


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


TEST_CASES = [
    "I have experience with Python and SQL.",

    "Developed REST APIs using Python and FastAPI.",

    "Worked on machine learning models using Pandas and Scikit-learn.",

    "Built deep learning models with PyTorch.",

    "I worked closely with the development team to complete projects.",

    "I analyzed business requirements and prepared technical documents.",

    "Responsible for designing backend services, testing APIs, and maintaining Git repositories.",

    "Có kinh nghiệm lập trình Python và làm việc với cơ sở dữ liệu SQL.",

    "Đã thực hiện các dự án học máy và xử lý dữ liệu bằng Pandas.",

    "Interested in data analysis and artificial intelligence.",
]


def load_components():
    print("=" * 60)
    print("LOAD HYBRID COMPONENTS")
    print("=" * 60)

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy NER model: {MODEL_PATH}"
        )

    if not SKILL_DICTIONARY_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy skill dictionary: "
            f"{SKILL_DICTIONARY_PATH}"
        )

    nlp = spacy.load(MODEL_PATH)

    matcher = SkillMatcher(
        SKILL_DICTIONARY_PATH
    )

    print("NER model: loaded")
    print("SkillMatcher: loaded")
    print()

    return nlp, matcher


def extract_ner_skills(
    text: str,
    nlp,
) -> list[str]:
    """
    Lấy các entity SKILL do NER phát hiện.
    """

    doc = nlp(text)

    return [
        entity.text
        for entity in doc.ents
        if entity.label_ == "SKILL"
    ]


def extract_dictionary_skills(
    text: str,
    matcher: SkillMatcher,
) -> list[str]:
    """
    Lấy skill canonical từ SkillMatcher.
    """

    return sorted(
        matcher.skills(text)
    )


def run_hybrid(
    text: str,
    nlp,
    matcher: SkillMatcher,
) -> dict:
    """
    Hybrid v1:

        SkillMatcher
            -> confirmed

        NER
            -> suggested

    NER không tự động thay đổi confirmed skills.
    """

    confirmed = extract_dictionary_skills(
        text,
        matcher,
    )

    ner_skills = extract_ner_skills(
        text,
        nlp,
    )

    return {
        "confirmed": confirmed,
        "ner_suggestions": ner_skills,
    }


def print_result(
    index: int,
    text: str,
    result: dict,
):
    print("=" * 60)
    print(f"TEST CASE {index}")
    print("=" * 60)

    print(f"Text:")
    print(text)
    print()

    print(
        "Confirmed by SkillMatcher:"
    )

    if result["confirmed"]:
        for skill in result["confirmed"]:
            print(f"  ✓ {skill}")
    else:
        print("  []")

    print()

    print(
        "Suggested by NER:"
    )

    if result["ner_suggestions"]:
        for skill in result["ner_suggestions"]:
            print(f"  ? {skill}")
    else:
        print("  []")

    print()


def main():
    nlp, matcher = load_components()

    print("=" * 60)
    print("HYBRID NER V1")
    print("=" * 60)
    print()

    for index, text in enumerate(
        TEST_CASES,
        start=1,
    ):
        result = run_hybrid(
            text=text,
            nlp=nlp,
            matcher=matcher,
        )

        print_result(
            index=index,
            text=text,
            result=result,
        )


if __name__ == "__main__":
    main()