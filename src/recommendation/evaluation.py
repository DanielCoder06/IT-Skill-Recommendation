from dataclasses import dataclass
from src.recommendation.job_ranking import JobRankingResult

@dataclass
class RecommendationEvaluation:
    job_id: int
    job_title: str
    match_rate: float
    matched_skill_count: int
    missing_skill_count: int

def evaluate_job_ranking(
    rankings: list[JobRankingResult],
) -> list[RecommendationEvaluation]:
    """
    Đánh giá kết quả Job Ranking dựa trên các thông tin
    đã có trong JobRankingResult.
    """
    evaluations = []

    for ranking in rankings:
        evaluation = RecommendationEvaluation(
            job_id=ranking.job_id,
            job_title=ranking.job_title,
            match_rate=ranking.match_rate,
            matched_skill_count=len(ranking.matched_skills),
            missing_skill_count=len(ranking.missing_skills),
        )

        evaluations.append(evaluation)

    return evaluations