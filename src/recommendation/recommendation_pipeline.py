from src.recommendation.job_ranking import JobRankingResult
from src.recommendation.skill_recommendation import recommend_skills


def recommend_for_job_result(
    job_result: JobRankingResult,
):
    return recommend_skills(
        missing_skills=job_result.missing_skills,
    )