from src.recommendation.recommendation_pipeline import (
    JobRecommendationResult,
    recommend_for_cv,
    recommend_for_job_result,
)
from src.recommendation.job_ranking import (
    JobRankingResult, rank_jobs_for_cv,
)


def test_recommend_missing_skills_for_ranked_job():
    rankings = rank_jobs_for_cv(
        cv_id=1,
        top_n=1,
    )

    job_result = rankings[0]

    result = recommend_for_job_result(
        job_result
    )

    assert result

    recommended_names = {
        recommendation.skill
        for recommendation in result.recommendations
    }

    missing_skills = job_result.missing_skills

    assert recommended_names.issubset(
        missing_skills
    )

def test_recommend_for_job_result():
    job_result = JobRankingResult(
        job_id=1,
        job_title="Python Intern",
        match_rate=25.0,
        matched_skills={
            "Python",
            "Machine Learning",
        },
        missing_skills={
            "Git",
            "SQL",
        },
        extra_skills={
            "Java",
        },
    )

    result = recommend_for_job_result(
        job_result=job_result,
    )

    assert isinstance(
        result,
        JobRecommendationResult,
    )

    assert result.job_id == 1
    assert result.job_title == "Python Intern"
    assert result.match_rate == 25.0

    assert result.matched_skills == {
        "Python",
        "Machine Learning",
    }

    assert result.missing_skills == {
        "Git",
        "SQL",
    }

    assert result.extra_skills == {
        "Java",
    }

    assert isinstance(
        result.recommendations,
        list,
    )

    assert isinstance(
        result.learning_roadmap,
        list,
    )


def test_recommend_for_cv():
    results = recommend_for_cv(
        cv_id=1,
        top_n=3,
    )

    assert len(results) == 3

    assert all(
        isinstance(
            result,
            JobRecommendationResult,
        )
        for result in results
    )

    assert all(
        isinstance(result.match_rate, float)
        for result in results
    )

    assert all(
        isinstance(result.matched_skills, set)
        for result in results
    )

    assert all(
        isinstance(result.missing_skills, set)
        for result in results
    )

    assert all(
        isinstance(result.recommendations, list)
        for result in results
    )

    assert all(
        isinstance(result.learning_roadmap, list)
        for result in results
    )


def test_recommend_for_cv_respects_ranking_order():
    results = recommend_for_cv(
        cv_id=1,
        top_n=3,
    )

    assert all(
        results[i].match_rate >= results[i + 1].match_rate
        for i in range(len(results) - 1)
    )