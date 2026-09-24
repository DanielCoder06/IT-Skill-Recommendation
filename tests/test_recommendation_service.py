from src.recommendation.evaluation import RecommendationEvaluation
from src.recommendation.job_ranking import JobRankingResult
from src.recommendation.learning_roadmap import LearningStep
from src.recommendation.recommendation_service import (
    RecommendationService,
    RecommendationServiceResult,
)
from src.recommendation.skill_recommendation import SkillRecommendation


def test_build_recommendation():
    service = RecommendationService()

    job_result = JobRankingResult(
        job_id=1,
        job_title="Python Intern",
        match_rate=50.0,
        matched_skills={"Python", "SQL"},
        missing_skills={"Git", "GitHub"},
        extra_skills={"Java"},
    )

    result = service.build_recommendation(job_result)

    assert isinstance(result, RecommendationServiceResult)

    assert result.job_id == 1
    assert result.job_title == "Python Intern"
    assert result.match_rate == 50.0

    assert result.matched_skills == {"Python", "SQL"}
    assert result.missing_skills == {"Git", "GitHub"}
    assert result.extra_skills == {"Java"}

    assert isinstance(result.recommendations, list)
    assert all(
        isinstance(item, SkillRecommendation)
        for item in result.recommendations
    )

    assert isinstance(result.learning_roadmap, list)
    assert all(
        isinstance(item, LearningStep)
        for item in result.learning_roadmap
    )

    assert isinstance(
        result.evaluation,
        RecommendationEvaluation,
    )

    assert result.evaluation.job_id == 1
    assert result.evaluation.match_rate == 50.0
    assert result.evaluation.matched_skill_count == 2
    assert result.evaluation.missing_skill_count == 2


def test_rank_jobs():
    service = RecommendationService()

    results = service.rank_jobs(
        cv_id=1,
        top_n=3,
    )

    assert len(results) == 3

    assert all(
        isinstance(result, JobRankingResult)
        for result in results
    )

    assert all(
        results[index].match_rate
        >= results[index + 1].match_rate
        for index in range(len(results) - 1)
    )


def test_recommend():
    service = RecommendationService()

    results = service.recommend(
        cv_id=1,
        top_n=3,
    )

    assert len(results) == 3

    assert all(
        isinstance(result, RecommendationServiceResult)
        for result in results
    )

    for result in results:
        assert isinstance(result.job_id, int)
        assert isinstance(result.job_title, str)
        assert isinstance(result.match_rate, float)

        assert isinstance(result.matched_skills, set)
        assert isinstance(result.missing_skills, set)
        assert isinstance(result.extra_skills, set)

        assert isinstance(result.recommendations, list)
        assert isinstance(result.learning_roadmap, list)
        assert isinstance(
            result.evaluation,
            RecommendationEvaluation,
        )


def test_recommend_respects_ranking_order():
    service = RecommendationService()

    results = service.recommend(
        cv_id=1,
        top_n=5,
    )

    assert all(
        results[index].match_rate
        >= results[index + 1].match_rate
        for index in range(len(results) - 1)
    )


def test_recommend_empty_result_for_invalid_top_n():
    service = RecommendationService()

    results = service.recommend(
        cv_id=1,
        top_n=0,
    )

    assert results == []