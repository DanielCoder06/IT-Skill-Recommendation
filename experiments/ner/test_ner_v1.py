# -*- coding: utf-8 -*-

from pathlib import Path

import spacy


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "experiments"
    / "ner"
    / "models"
    / "skill_ner_v1"
    / "model-best"
)


TEST_CASES = [
    # --------------------------------------------------------
    # 1. Skill rõ ràng
    # --------------------------------------------------------
    "I have experience with Python and SQL.",

    # --------------------------------------------------------
    # 2. Skill trong ngữ cảnh công việc
    # --------------------------------------------------------
    "Developed REST APIs using Python and FastAPI.",

    # --------------------------------------------------------
    # 3. ML / Data
    # --------------------------------------------------------
    "Worked on machine learning models using Pandas and Scikit-learn.",

    # --------------------------------------------------------
    # 4. Deep Learning
    # --------------------------------------------------------
    "Built deep learning models with PyTorch.",

    # --------------------------------------------------------
    # 5. Không có skill
    # --------------------------------------------------------
    "I worked closely with the development team to complete projects.",

    # --------------------------------------------------------
    # 6. Dễ gây false positive
    # --------------------------------------------------------
    "I analyzed business requirements and prepared technical documents.",

    # --------------------------------------------------------
    # 7. Skill được viết trong câu dài
    # --------------------------------------------------------
    "Responsible for designing backend services, testing APIs, and maintaining Git repositories.",

    # --------------------------------------------------------
    # 8. Vietnamese
    # --------------------------------------------------------
    "Có kinh nghiệm lập trình Python và làm việc với cơ sở dữ liệu SQL.",

    # --------------------------------------------------------
    # 9. Vietnamese ML
    # --------------------------------------------------------
    "Đã thực hiện các dự án học máy và xử lý dữ liệu bằng Pandas.",

    # --------------------------------------------------------
    # 10. Không nên suy diễn
    # --------------------------------------------------------
    "Interested in data analysis and artificial intelligence.",
]


def load_model():
    print("=" * 60)
    print("LOAD NER MODEL")
    print("=" * 60)
    print(f"Model: {MODEL_PATH}")
    print()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy model: {MODEL_PATH}"
        )

    nlp = spacy.load(MODEL_PATH)

    print("Model loaded successfully.")
    print()

    return nlp


def test_model(nlp):
    print("=" * 60)
    print("NER V1 TEST")
    print("=" * 60)

    for index, text in enumerate(
        TEST_CASES,
        start=1,
    ):
        doc = nlp(text)

        skills = [
            entity.text
            for entity in doc.ents
            if entity.label_ == "SKILL"
        ]

        print()
        print(f"[{index}]")
        print(f"Text: {text}")

        if skills:
            print(f"SKILL: {skills}")
        else:
            print("SKILL: []")


def main():
    nlp = load_model()
    test_model(nlp)


if __name__ == "__main__":
    main()