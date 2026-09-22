from src.recommendation.job_ranking import rank_jobs_for_cv


def test_rank_jobs_for_cv():
    rankings = rank_jobs_for_cv(
        cv_id=1,
    )

    assert len(rankings) > 0

    assert all(
        isinstance(result.match_rate, float)
        for result in rankings
    )

    assert all(
        rankings[i].match_rate >= rankings[i + 1].match_rate
        for i in range(len(rankings) - 1)
    )


def test_top_n_job_ranking():
    rankings = rank_jobs_for_cv(
        cv_id=1,
        top_n=3,
    )

    assert len(rankings) == 3

    assert all(
        isinstance(result.job_id, int)
        for result in rankings
    )


def test_job_ranking_contains_skill_gap():
    rankings = rank_jobs_for_cv(
        cv_id=1,
        top_n=1,
    )

    result = rankings[0]

    assert isinstance(result.matched_skills, set)
    assert isinstance(result.missing_skills, set)
    assert isinstance(result.extra_skills, set)

    assert result.matched_skills