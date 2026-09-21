import json
from pathlib import Path

from src.recommendation.cv_job_matching import match_cv_to_job


BASE_DIR = Path(__file__).resolve().parents[2]

PROFILE_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "resumes"
    / "resume_skill_profiles.json"
)


def load_cv_profiles() -> list[dict]:
    """
    Load toàn bộ CV skill profiles.
    """
    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_cv_profile(cv_id: int) -> dict:
    """
    Lấy skill profile của một CV theo cv_id.
    """
    profiles = load_cv_profiles()

    for profile in profiles:
        if profile["cv_id"] == cv_id:
            return profile

    raise ValueError(f"CV không tồn tại: {cv_id}")


def match_cv_profile_to_job(
    cv_id: int,
    job_id: int,
):
    """
    Lấy skill profile của CV rồi match với Job.
    """
    profile = get_cv_profile(cv_id)

    cv_skills = set(profile["skills"])

    return match_cv_to_job(
        cv_skills=cv_skills,
        job_id=job_id,
    )