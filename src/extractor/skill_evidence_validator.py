import re


def _contains_phrase(
    text: str,
    phrase: str,
    case_sensitive: bool = False,
) -> bool:
    if not phrase:
        return False

    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = rf"\b{re.escape(phrase)}\b"

    return re.search(pattern, text, flags=flags) is not None


def _find_phrase_positions(
    text: str,
    phrase: str,
    case_sensitive: bool = False,
) -> list[tuple[int, int]]:
    if not phrase:
        return []

    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = rf"\b{re.escape(phrase)}\b"

    return [
        match.span()
        for match in re.finditer(pattern, text, flags=flags)
    ]


def _has_negative_evidence(
    text: str,
    skill_data: dict,
) -> bool:
    for pattern in skill_data.get("negative_patterns", []):
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


def _has_context_near_position(
    text: str,
    start: int,
    end: int,
    context_terms: list[str],
    window: int = 100,
) -> bool:
    left = max(0, start - window)
    right = min(len(text), end + window)

    context_text = text[left:right]

    return any(
        _contains_phrase(context_text, term)
        for term in context_terms
    )


def _has_ambiguous_evidence(
    text: str,
    ambiguous_alias: str,
    context_terms: list[str],
) -> bool:
    positions = _find_phrase_positions(
        text=text,
        phrase=ambiguous_alias,
    )

    for start, end in positions:
        if _has_context_near_position(
            text=text,
            start=start,
            end=end,
            context_terms=context_terms,
        ):
            return True

    return False


def has_skill_evidence(
    text: str,
    skill: str,
    skill_dictionary: dict,
) -> bool:
    if not isinstance(text, str):
        raise TypeError("text phải là string.")

    skill_data = skill_dictionary.get(skill)

    if skill_data is None:
        return False

    # 1. Negative evidence luôn được ưu tiên.
    if _has_negative_evidence(
        text=text,
        skill_data=skill_data,
    ):
        return False

    # 2. Alias mơ hồ phải có context.
    ambiguous_aliases = skill_data.get(
        "ambiguous_aliases",
        {},
    )

    for ambiguous_alias, context_terms in ambiguous_aliases.items():
        if _has_ambiguous_evidence(
            text=text,
            ambiguous_alias=ambiguous_alias,
            context_terms=context_terms,
        ):
            return True

    # 3. Case-sensitive aliases.
    for alias in skill_data.get(
        "case_sensitive_aliases",
        [],
    ):
        if _contains_phrase(
            text=text,
            phrase=alias,
            case_sensitive=True,
        ):
            return True

    # 4. Canonical name + aliases an toàn.
    safe_candidates = [skill]
    safe_candidates.extend(
        skill_data.get("aliases", [])
    )

    for candidate in safe_candidates:
        # Nếu candidate cũng là ambiguous alias,
        # không chấp nhận bằng kiểm tra thông thường.
        if candidate.casefold() in {
            alias.casefold()
            for alias in ambiguous_aliases
        }:
            continue

        if _contains_phrase(
            text=text,
            phrase=candidate,
        ):
            return True

    return False


def validate_skills(
    text: str,
    candidate_skills: set[str],
    skill_dictionary: dict,
) -> set[str]:
    if not isinstance(text, str):
        raise TypeError("text phải là string.")

    if not isinstance(candidate_skills, set):
        raise TypeError("candidate_skills phải là set.")

    validated_skills = set()

    for skill in candidate_skills:
        if has_skill_evidence(
            text=text,
            skill=skill,
            skill_dictionary=skill_dictionary,
        ):
            validated_skills.add(skill)

    return validated_skills