# -*- coding: utf-8 -*-
"""
skill_normalizer.py

Chuẩn hóa skill được NER nhận diện thành canonical skill
dựa trên SkillMatcher hiện có.

Vai trò:
- Nhận raw entity từ NER.
- Tìm canonical skill tương ứng trong skill dictionary.
- Trả về None nếu không chuẩn hóa được.
"""

from pathlib import Path

from src.extractor.skill_matcher import SkillMatcher

BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_DICTIONARY_PATH = (
    BASE_DIR / "config" / "skills_dictionary.json"
)


def normalize_ner_skill(
    ner_text: str,
    matcher: SkillMatcher,
) -> str | None:
    """
    Chuẩn hóa một raw NER entity thành canonical skill.

    Ví dụ:
        "Python" -> "Python"
        "python3" -> "Python"
        "machine learning" -> "Machine Learning"

    Nếu entity không khớp dictionary thì trả về None.
    """
    if not isinstance(ner_text, str):
        raise TypeError("ner_text phải là string.")

    ner_text = ner_text.strip()

    if not ner_text:
        return None

    matched_skills = matcher.extract(ner_text)

    if not matched_skills:
        return None

    return matched_skills[0]["skill"]


def normalize_ner_entities(
    ner_entities: list[str],
    matcher: SkillMatcher,
) -> set[str]:
    """
    Chuẩn hóa danh sách raw NER entities thành tập canonical skills.

    Các entity không chuẩn hóa được sẽ bị bỏ qua.
    """
    normalized_skills: set[str] = set()

    for entity in ner_entities:
        skill = normalize_ner_skill(
            ner_text=entity,
            matcher=matcher,
        )

        if skill is not None:
            normalized_skills.add(skill)

    return normalized_skills


def create_skill_matcher(
    dictionary_path: str | Path = DEFAULT_DICTIONARY_PATH,
) -> SkillMatcher:
    """
    Tạo SkillMatcher từ skills_dictionary.json.
    """
    dictionary_path = Path(dictionary_path)

    if not dictionary_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy skill dictionary:\n{dictionary_path}"
        )

    return SkillMatcher(dictionary_path)