from src.extractor.skill_merger import merge_skills, get_skill_sources


def test_merge_skills():
    regex_skills = {"Python", "SQL", "Git"}
    gemini_skills = {"Python", "SQL", "Pandas"}

    result = merge_skills(regex_skills, gemini_skills)

    assert result == {"Python", "SQL", "Git", "Pandas"}


def test_merge_identical_skills():
    regex_skills = {"Python", "SQL"}
    gemini_skills = {"Python", "SQL"}

    result = merge_skills(regex_skills, gemini_skills)

    assert result == {"Python", "SQL"}


def test_merge_with_empty_regex():
    regex_skills = set()
    gemini_skills = {"Python", "SQL"}

    result = merge_skills(regex_skills, gemini_skills)

    assert result == {"Python", "SQL"}


def test_merge_with_empty_gemini():
    regex_skills = {"Python", "SQL"}
    gemini_skills = set()

    result = merge_skills(regex_skills, gemini_skills)

    assert result == {"Python", "SQL"}


def test_merge_both_empty():
    regex_skills = set()
    gemini_skills = set()

    result = merge_skills(regex_skills, gemini_skills)

    assert result == set()
    
def test_get_skill_sources():
    regex_skills = {"Python", "SQL", "Git"}
    gemini_skills = {"Python", "SQL", "Pandas"}

    result = get_skill_sources(
        regex_skills,
        gemini_skills,
    )

    assert result == {
        "Python": "both",
        "SQL": "both",
        "Git": "regex",
        "Pandas": "gemini",
    }


def test_get_skill_sources_with_empty_gemini():
    regex_skills = {"Python", "SQL"}

    result = get_skill_sources(
        regex_skills,
        set(),
    )

    assert result == {
        "Python": "regex",
        "SQL": "regex",
    }


def test_get_skill_sources_with_empty_regex():
    gemini_skills = {"Python", "SQL"}

    result = get_skill_sources(
        set(),
        gemini_skills,
    )

    assert result == {
        "Python": "gemini",
        "SQL": "gemini",
    }