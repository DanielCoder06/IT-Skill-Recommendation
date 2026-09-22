from src.recommendation.job_ranking import rank_jobs_for_cv
from src.recommendation.recommendation_pipeline import (
    recommend_for_job_result,
)


def test_recommend_missing_skills_for_ranked_job():
    rankings = rank_jobs_for_cv(
        cv_id=1,
        top_n=1,
    )

    job_result = rankings[0]

    recommendations = recommend_for_job_result(
        job_result
    )

    assert recommendations

    recommended_names = {
        recommendation.skill
        for recommendation in recommendations
    }

    assert recommended_names.issubset(
        job_result.missing_skills
    )