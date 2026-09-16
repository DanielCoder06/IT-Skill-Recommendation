def merge_skills(
    regex_skills: set[str],
    gemini_skills: set[str],
) -> set[str]:
    return regex_skills | gemini_skills


def get_skill_sources(
    regex_skills: set[str],
    gemini_skills: set[str],
) -> dict[str, str]:
    final_skills = merge_skills(regex_skills, gemini_skills)

    sources = {}

    for skill in final_skills:
        if skill in regex_skills and skill in gemini_skills:
            sources[skill] = "both"
        elif skill in regex_skills:
            sources[skill] = "regex"
        elif skill in gemini_skills:
            sources[skill] = "gemini"

    return sources