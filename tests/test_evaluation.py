from src.recommendation.evaluation import (
    RecommendationEvaluation,
    evaluate_job_ranking,
)
from src.recommendation.job_ranking import JobRankingResult

def test_evaluate_job_ranking():
    rankings = [
        JobRankingResult(
            job_id=1,
            job_title="Python Intern",
            match_rate=50.0,
            matched_skills={"Python", "SQL"},
            missing_skills={"Git", "GitHub"},
            extra_skills={"Java"},
        )
    ]

    results = evaluate_job_ranking(rankings)

    assert len(results) == 1

    result = results[0]

    assert isinstance(result, RecommendationEvaluation)
    assert result.job_id == 1
    assert result.job_title == "Python Intern"
    assert result.match_rate == 50.0
    assert result.matched_skill_count == 2
    assert result.missing_skill_count == 2


def test_evaluate_empty_ranking():
    results = evaluate_job_ranking([])

    assert results == []


def test_evaluate_multiple_jobs():
    rankings = [
        JobRankingResult(
            job_id=1,
            job_title="Python Intern",
            match_rate=50.0,
            matched_skills={"Python", "SQL"},
            missing_skills={"Git", "GitHub"},
            extra_skills=set(),
        ),
        JobRankingResult(
            job_id=2,
            job_title="Machine Learning Intern",
            match_rate=75.0,
            matched_skills={
                "Python",
                "Machine Learning",
                "NumPy",
            },
            missing_skills={"PyTorch"},
            extra_skills={"Java"},
        ),
    ]

    results = evaluate_job_ranking(rankings)

    assert len(results) == 2

    assert results[0].job_id == 1
    assert results[0].matched_skill_count == 2
    assert results[0].missing_skill_count == 2

    assert results[1].job_id == 2
    assert results[1].matched_skill_count == 3
    assert results[1].missing_skill_count == 1