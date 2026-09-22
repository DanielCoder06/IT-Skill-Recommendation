from dataclasses import dataclass

from src.recommendation.cv_profile_matching import (
    match_cv_profile_to_job,
)
from src.recommendation.skill_recommendation import (
    SkillRecommendation,
    recommend_skills,
)
from src.recommendation.learning_roadmap import (
    LearningStep,
    build_learning_roadmap,
)


@dataclass
class JobAnalysisResult:
    job_id: int
    job_title: str

    matched_skills: set[str]
    missing_skills: set[str]
    extra_skills: set[str]

    match_rate: float

    recommendations: list[SkillRecommendation]
    learning_roadmap: list[LearningStep]


def analyze_cv_for_job(
    cv_id: int,
    job_id: int,
) -> JobAnalysisResult:
    skill_gap = match_cv_profile_to_job(
        cv_id=cv_id,
        job_id=job_id,
    )

    recommendations = recommend_skills(
        missing_skills=skill_gap.missing_skills,
    )

    roadmap = build_learning_roadmap(
        target_skills=skill_gap.missing_skills,
    )

    return JobAnalysisResult(
        job_id=skill_gap.job_id,
        job_title=skill_gap.job_title,
        matched_skills=skill_gap.matched_skills,
        missing_skills=skill_gap.missing_skills,
        extra_skills=skill_gap.extra_skills,
        match_rate=skill_gap.match_rate,
        recommendations=recommendations,
        learning_roadmap=roadmap,
    )