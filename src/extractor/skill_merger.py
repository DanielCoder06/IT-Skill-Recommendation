def merge_skills(
    confirmed_skills: set[str],
    suggested_skills: set[str],
) -> set[str]:
    return confirmed_skills | suggested_skills


def get_skill_sources(
    confirmed_skills: set[str],
    suggested_skills: set[str],
) -> dict[str, str]:
    final_skills = merge_skills(
        confirmed_skills,
        suggested_skills,
    )

    sources = {}

    for skill in final_skills:
        if skill in confirmed_skills:
            sources[skill] = "regex"
        elif skill in suggested_skills:
            sources[skill] = "supplementary"

    return sources