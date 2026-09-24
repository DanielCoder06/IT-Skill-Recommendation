from dataclasses import dataclass
from src.recommendation.job_ranking import JobRankingResult, rank_jobs_for_cv
from src.recommendation.learning_roadmap import LearningStep, build_learning_roadmap
from src.recommendation.skill_recommendation import SkillRecommendation, recommend_skills

@dataclass
class JobRecommendationResult:
    job_id: int
    job_title: str
    match_rate: float
    matched_skills: set[str]
    missing_skills: set[str]
    extra_skills: set[str]
    recommendations: list[SkillRecommendation]
    learning_roadmap: list[LearningStep]

def recommend_for_job_result(
    job_result: JobRankingResult,
) -> JobRecommendationResult:
    """
    Hoàn thiện recommendation cho một job
    từ kết quả Job Ranking.
    """

    recommendations = recommend_skills(
        missing_skills=job_result.missing_skills,
    )

    learning_roadmap = build_learning_roadmap(
        target_skills=job_result.missing_skills,
    )

    return JobRecommendationResult(
        job_id=job_result.job_id,
        job_title=job_result.job_title,
        match_rate=job_result.match_rate,
        matched_skills=job_result.matched_skills,
        missing_skills=job_result.missing_skills,
        extra_skills=job_result.extra_skills,
        recommendations=recommendations,
        learning_roadmap=learning_roadmap,
    )

def recommend_for_cv(
    cv_id: int,
    top_n: int | None = None,
) -> list[JobRecommendationResult]:
    """
    Tạo recommendation end-to-end cho một CV.

    Flow:
        CV
        -> Job Ranking
        -> Skill Recommendation
        -> Learning Roadmap
    """

    rankings = rank_jobs_for_cv(
        cv_id=cv_id,
        top_n=top_n,
    )

    recommendations = []

    for job_result in rankings:
        recommendation = recommend_for_job_result(
            job_result=job_result,
        )

        recommendations.append(recommendation)

    return recommendations