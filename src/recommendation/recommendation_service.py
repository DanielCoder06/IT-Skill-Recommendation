from dataclasses import dataclass

from src.recommendation.evaluation import (
    RecommendationEvaluation,
    evaluate_job_ranking,
)
from src.recommendation.job_ranking import (
    JobRankingResult,
    rank_jobs_for_cv,
)
from src.recommendation.learning_roadmap import (
    LearningStep,
    build_learning_roadmap,
)
from src.recommendation.skill_recommendation import (
    SkillRecommendation,
    recommend_skills,
)


@dataclass
class RecommendationServiceResult:
    job_id: int
    job_title: str
    match_rate: float
    matched_skills: set[str]
    missing_skills: set[str]
    extra_skills: set[str]
    recommendations: list[SkillRecommendation]
    learning_roadmap: list[LearningStep]
    evaluation: RecommendationEvaluation


class RecommendationService:
    """
    Service điều phối toàn bộ quá trình recommendation
    cho một CV.
    """

    def rank_jobs(
        self,
        cv_id: int,
        top_n: int | None = None,
    ) -> list[JobRankingResult]:
        """
        Xếp hạng các IT internship phù hợp với CV.
        """
        return rank_jobs_for_cv(
            cv_id=cv_id,
            top_n=top_n,
        )

    def build_recommendation(
        self,
        job_result: JobRankingResult,
    ) -> RecommendationServiceResult:
        """
        Hoàn thiện recommendation cho một job đã được ranking.
        """
        recommendations = recommend_skills(
            missing_skills=job_result.missing_skills,
        )

        learning_roadmap = build_learning_roadmap(
            target_skills=job_result.missing_skills,
        )

        evaluation = evaluate_job_ranking(
            [job_result]
        )[0]

        return RecommendationServiceResult(
            job_id=job_result.job_id,
            job_title=job_result.job_title,
            match_rate=job_result.match_rate,
            matched_skills=job_result.matched_skills,
            missing_skills=job_result.missing_skills,
            extra_skills=job_result.extra_skills,
            recommendations=recommendations,
            learning_roadmap=learning_roadmap,
            evaluation=evaluation,
        )

    def recommend(
        self,
        cv_id: int,
        top_n: int | None = None,
    ) -> list[RecommendationServiceResult]:
        """
        Chạy toàn bộ recommendation pipeline cho một CV.

        Flow:
            CV
            -> Job Ranking
            -> Skill Recommendation
            -> Learning Roadmap
            -> Evaluation
        """
        rankings = self.rank_jobs(
            cv_id=cv_id,
            top_n=top_n,
        )

        return [
            self.build_recommendation(job_result)
            for job_result in rankings
        ]