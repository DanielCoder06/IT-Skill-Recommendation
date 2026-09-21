from src.recommendation.cv_profile_matching import (
    get_cv_profile,
    match_cv_profile_to_job,
)


def test_load_cv_profile():
    profile = get_cv_profile(1)

    assert profile["cv_id"] == 1
    assert isinstance(profile["skills"], list)


def test_match_real_cv_to_job():
    result = match_cv_profile_to_job(
        cv_id=1,
        job_id=8,
    )

    assert result.job_id == 8
    assert result.job_title == "Data Science Intern"
    assert isinstance(result.match_rate, float)