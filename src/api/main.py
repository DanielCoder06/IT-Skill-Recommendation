from pathlib import Path
import tempfile

from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from src.extractor.document_extractor import extract_text_from_document
from src.pipeline.cv_pipeline import extract_cv_skills
from src.recommendation.recommendation_service import (
    RecommendationService,
)


app = FastAPI(
    title="IT Skill Recommendation API",
    description="API for IT internship recommendation based on CV skills.",
    version="1.0.0",
)


recommendation_service = RecommendationService()

ALLOWED_EXTENSIONS = {".pdf", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def serialize_recommendation(result) -> dict:
    """
    Chuyển RecommendationServiceResult
    thành dictionary để trả về JSON.
    """
    return {
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
    Trả về danh sách job recommendation cho một CV
    đã tồn tại trong database.
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
            serialize_recommendation(result)
            for result in results
        ],
    }


@app.post("/recommendations/upload")
async def upload_cv_and_recommend(
    file: UploadFile = File(...),
    top_n: int | None = Query(
        default=5,
        ge=1,
        le=20,
    ),
):
    """
    Upload CV PDF/TXT và trả về job recommendations.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Tên file không hợp lệ.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Định dạng CV không được hỗ trợ. "
                "Chỉ chấp nhận PDF hoặc TXT."
            ),
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="File CV rỗng.",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File CV vượt quá giới hạn 10 MB.",
        )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temporary_file:
            temporary_file.write(file_content)
            temporary_path = Path(temporary_file.name)

        # Kiểm tra document có thể được đọc hay không.
        extract_text_from_document(temporary_path)

        # CV -> Skills
        cv_skills = extract_cv_skills(
            temporary_path
        )

        # Skills -> Recommendation
        results = recommendation_service.recommend_from_skills(
            cv_skills=cv_skills,
            top_n=top_n,
        )

        return {
            "filename": file.filename,
            "cv_skills": sorted(cv_skills),
            "cv_skill_count": len(cv_skills),
            "count": len(results),
            "recommendations": [
                serialize_recommendation(result)
                for result in results
            ],
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể phân tích CV: {error}",
        ) from error

    finally:
        if temporary_path is not None:
            temporary_path.unlink(
                missing_ok=True
            )