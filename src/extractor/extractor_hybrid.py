# -*- coding: utf-8 -*-
"""
extractor_hybrid.py

Kết hợp Regex/SkillMatcher, NER và Local LLM
trong quá trình phân tích CV.

Vai trò:
- Regex/SkillMatcher: nguồn skill đã xác nhận.
- NER: nguồn skill bổ sung.
- Local LLM: nguồn skill bổ sung.
- Regex vẫn là baseline chính.
"""

from pathlib import Path

from src.extractor.extractor_ner import (
    extract_ner_entities,
    load_ner_model,
)
from src.extractor.extractor_regex import extract_skills
from src.extractor.extractor_local_llm import (
    extract_skills_with_local_llm,
)
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
    Trích xuất skill bằng Regex + NER + Local LLM.

    Regex:
        nguồn xác nhận chính.

    NER + Local LLM:
        nguồn skill bổ sung.

    Returns:
        {
            "confirmed_skills": set[str],
            "suggested_skills": set[str],
        }
    """

    if not isinstance(text, str):
        raise TypeError("text phải là string.")

    if not text.strip():
        return {
            "confirmed_skills": set(),
            "suggested_skills": set(),
        }

    # ---------------------------------------------------------
    # 1. Regex / SkillMatcher
    # ---------------------------------------------------------
    confirmed_skills = set(extract_skills(text))

    # ---------------------------------------------------------
    # 2. NER
    # ---------------------------------------------------------
    nlp = load_ner_model(model_path)

    ner_entities = extract_ner_entities(
        text=text,
        nlp=nlp,
    )

    matcher = create_skill_matcher()

    normalized_ner_skills = normalize_ner_entities(
        ner_entities=ner_entities,
        matcher=matcher,
    )

    # ---------------------------------------------------------
    # 3. Local LLM
    # ---------------------------------------------------------
    local_llm_skills = extract_skills_with_local_llm(text)

    # ---------------------------------------------------------
    # 4. Hợp nhất candidate skills
    # ---------------------------------------------------------
    candidate_skills = (
        normalized_ner_skills
        | local_llm_skills
    )

    # ---------------------------------------------------------
    # 5. Không lặp lại skill đã được Regex xác nhận
    # ---------------------------------------------------------
    suggested_skills = (
        candidate_skills - confirmed_skills
    )

    return {
        "confirmed_skills": confirmed_skills,
        "suggested_skills": suggested_skills,
    }