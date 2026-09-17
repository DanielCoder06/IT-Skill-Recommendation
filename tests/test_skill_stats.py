from src.analytics.skill_stats import (
    get_skill_frequency,
    get_skill_percentage,
    get_skill_by_location,
    get_skill_count_per_job,
)


def test_get_skill_frequency():
    result = get_skill_frequency()

    assert isinstance(result, list)
    assert len(result) > 0

    # Python xuất hiện trong 9/10 job
    assert ("Python", 9) in result


def test_get_skill_percentage():
    result = get_skill_percentage()

    assert isinstance(result, list)
    assert len(result) > 0

    # Python xuất hiện trong 90% job
    assert ("Python", 9, 90.0) in result


def test_get_skill_by_location():
    result = get_skill_by_location()

    assert isinstance(result, list)
    assert len(result) > 0

    # Python xuất hiện trong 3 job ở Cần Thơ
    assert ("Cần Thơ", "Python", 3) in result


def test_get_skill_count_per_job():
    result = get_skill_count_per_job()

    assert isinstance(result, list)
    assert len(result) == 10

    assert result[0] == (
        1,
        "Python Intern",
        8,
    )

    assert result[-1] == (
        10,
        "Full Stack Developer Intern",
        14,
    )