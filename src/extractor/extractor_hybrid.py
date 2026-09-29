# -*- coding: utf-8 -*-
"""
extractor_hybrid.py

Kết hợp Regex/SkillMatcher và NER trong quá trình phân tích CV.

Kiến trúc:
- Regex/SkillMatcher: nguồn skill đã xác nhận.
- NER: nguồn skill đề xuất.
- Normalizer: chuẩn hóa entity NER về canonical skill.
"""

from pathlib import Path

from src.extractor.extractor_ner import (
    extract_ner_entities,
    load_ner_model,
)
from src.extractor.extractor_regex import extract_skills
from src.extractor.skill_normalizer import (
    create_skill_matcher,
    normalize_ner_entities,
)


BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_MODEL_PATH = (
    BASE_DIR
    / "experiments"
    / "ner"
    / "models"
    / "skill_ner_v1"
    / "model-best"
)


def extract_hybrid_skills(
    text: str,
    model_path: str | Path = DEFAULT_MODEL_PATH,
) -> dict[str, set[str]]:
    """
    Trích xuất skill bằng Regex + NER.

    Returns:
        {
            "confirmed_skills": set(...),
            "suggested_skills": set(...),
        }

    confirmed_skills:
        Skill được Regex/SkillMatcher xác nhận.

    suggested_skills:
        Skill do NER nhận diện và chuẩn hóa được,
        nhưng chưa được xác nhận là skill chính thức.
    """
    if not isinstance(text, str):
        raise TypeError("text phải là string.")

    if not text.strip():
        return {
            "confirmed_skills": set(),
            "suggested_skills": set(),
        }

    # ---------------------------------------------------------
    # 1. Regex: nguồn skill đã xác nhận
    # ---------------------------------------------------------
    confirmed_skills = set(extract_skills(text))

    # ---------------------------------------------------------
    # 2. NER: nhận diện raw skill entities
    # ---------------------------------------------------------
    nlp = load_ner_model(model_path)

    ner_entities = extract_ner_entities(
        text=text,
        nlp=nlp,
    )

    # ---------------------------------------------------------
    # 3. Normalize NER entities → canonical skills
    # ---------------------------------------------------------
    matcher = create_skill_matcher()

    normalized_ner_skills = normalize_ner_entities(
        ner_entities=ner_entities,
        matcher=matcher,
    )

    # ---------------------------------------------------------
    # 4. Chỉ giữ NER skills chưa có trong Regex
    # ---------------------------------------------------------
    suggested_skills = normalized_ner_skills - confirmed_skills

    return {
        "confirmed_skills": confirmed_skills,
        "suggested_skills": suggested_skills,
    }