from fastapi import FastAPI, HTTPException, Query

from src.recommendation.recommendation_service import (
    RecommendationService,
)


app = FastAPI(
    title="IT Skill Recommendation API",
    description="API for IT internship recommendation based on CV skills.",
    version="1.0.0",
)


recommendation_service = RecommendationService()


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Kiểm tra API có đang hoạt động hay không.
    """
    return {
        "message": "IT Skill Recommendation API is running."
    }


@app.get("/recommendations/{cv_id}")
def get_recommendations(
    cv_id: int,
    top_n: int | None = Query(
        default=5,
        ge=1,
        le=20,
    ),
):
    """
    Trả về danh sách job recommendation cho một CV.
    """
    try:
        results = recommendation_service.recommend(
            cv_id=cv_id,
            top_n=top_n,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return {
        "cv_id": cv_id,
        "count": len(results),
        "recommendations": [
            {
                "job_id": result.job_id,
                "job_title": result.job_title,
                "match_rate": result.match_rate,
                "matched_skills": sorted(
                    result.matched_skills
                ),
                "missing_skills": sorted(
                    result.missing_skills
                ),
                "extra_skills": sorted(
                    result.extra_skills
                ),
                "skill_recommendations": [
                    {
                        "skill": recommendation.skill,
                        "job_count": recommendation.job_count,
                        "job_percentage": (
                            recommendation.job_percentage
                        ),
                    }
                    for recommendation in result.recommendations
                ],
                "learning_roadmap": [
                    {
                        "skill": step.skill,
                        "level": step.level,
                    }
                    for step in result.learning_roadmap
                ],
                "evaluation": {
                    "match_rate": result.evaluation.match_rate,
                    "matched_skill_count": (
                        result.evaluation.matched_skill_count
                    ),
                    "missing_skill_count": (
                        result.evaluation.missing_skill_count
                    ),
                },
            }
            for result in results
        ],
    }