# -*- coding: utf-8 -*-
"""
extractor_ner.py

NER-based skill extraction.

Vai trò:
- Load pretrained NER model.
- Nhận diện các entity có label = SKILL.
- Trả về raw skill entities.
- Không tự động thay đổi confirmed skills từ Regex/SkillMatcher.
"""

from pathlib import Path

import spacy
from spacy.language import Language


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_MODEL_PATH = (
    BASE_DIR
    / "experiments"
    / "ner"
    / "models"
    / "skill_ner_v1"
    / "model-best"
)


# ============================================================
# MODEL LOADING
# ============================================================

def load_ner_model(
    model_path: str | Path = DEFAULT_MODEL_PATH,
) -> Language:
    """
    Load pretrained NER model.

    Parameters
    ----------
    model_path:
        Đường dẫn tới spaCy NER model.

    Returns
    -------
    Language
        spaCy NLP pipeline.
    """

    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy NER model:\n{model_path}"
        )

    return spacy.load(model_path)


# ============================================================
# NER EXTRACTION
# ============================================================

def extract_ner_entities(
    text: str,
    nlp: Language,
) -> list[str]:
    """
    Trích xuất raw SKILL entities từ văn bản.

    Chỉ lấy entity có label = SKILL.

    Ví dụ:
        "I use Python and FastAPI."

    Có thể trả về:
        ["Python", "FastAPI"]
    """

    if not isinstance(text, str):
        raise TypeError(
            "text phải là string."
        )

    if not text.strip():
        return []

    doc = nlp(text)

    return [
        entity.text.strip()
        for entity in doc.ents
        if entity.label_ == "SKILL"
        and entity.text.strip()
    ]


# ============================================================
# DETAILED EXTRACTION
# ============================================================

def extract_ner_entities_detailed(
    text: str,
    nlp: Language,
) -> list[dict]:
    """
    Trích xuất SKILL entities kèm vị trí trong văn bản.

    Output:
        [
            {
                "text": "Python",
                "start": 10,
                "end": 16,
                "label": "SKILL",
            }
        ]
    """

    if not isinstance(text, str):
        raise TypeError(
            "text phải là string."
        )

    if not text.strip():
        return []

    doc = nlp(text)

    return [
        {
            "text": entity.text.strip(),
            "start": entity.start_char,
            "end": entity.end_char,
            "label": entity.label_,
        }
        for entity in doc.ents
        if entity.label_ == "SKILL"
        and entity.text.strip()
    ]


# ============================================================
# CONVENIENCE FUNCTION
# ============================================================

def extract_ner_skills(
    text: str,
    model_path: str | Path = DEFAULT_MODEL_PATH,
) -> set[str]:
    """
    Load model và trả về tập skill do NER nhận diện.

    Đây là hàm tiện ích cho các module phía trên.
    """

    nlp = load_ner_model(model_path)

    return set(
        extract_ner_entities(
            text=text,
            nlp=nlp,
        )
    )