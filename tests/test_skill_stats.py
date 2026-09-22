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

    for skill, job_count in result:
        assert isinstance(skill, str)
        assert isinstance(job_count, int)
        assert job_count > 0


def test_get_skill_percentage():
    result = get_skill_percentage()

    assert isinstance(result, list)
    assert len(result) > 0

    for skill, job_count, percentage in result:
        assert isinstance(skill, str)
        assert isinstance(job_count, int)
        assert job_count > 0

        assert isinstance(percentage, float)
        assert 0 <= percentage <= 100


def test_get_skill_by_location():
    result = get_skill_by_location()

    assert isinstance(result, list)
    assert len(result) > 0

    for location, skill, job_count in result:
        assert isinstance(location, str)
        assert isinstance(skill, str)
        assert isinstance(job_count, int)
        assert job_count > 0


def test_get_skill_count_per_job():
    result = get_skill_count_per_job()

    assert isinstance(result, list)
    assert len(result) > 0

    for job_id, title, skill_count in result:
        assert isinstance(job_id, int)
        assert isinstance(title, str)
        assert isinstance(skill_count, int)
        assert skill_count >= 0