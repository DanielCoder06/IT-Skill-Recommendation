from dataclasses import dataclass

from src.recommendation.cv_profile_matching import (
    get_cv_profile,
)
from src.recommendation.cv_job_matching import (
    match_cv_to_job,
)

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"


@dataclass
class JobRankingResult:
    job_id: int
    job_title: str
    match_rate: float
    matched_skills: set[str]
    missing_skills: set[str]
    extra_skills: set[str]

def rank_jobs_for_cv(
    cv_id: int,
    top_n: int | None = None,
) -> list[JobRankingResult]:
    """
    Xếp hạng các Job dựa trên mức độ phù hợp với một CV.
    """

    profile = get_cv_profile(cv_id)
    cv_skills = set(profile["skills"])

    connection = sqlite3.connect(DB_PATH)

    job_result = connection.execute(
        """
        SELECT id
        FROM jobs
        ORDER BY id
        """
    )

    job_ids = [row[0] for row in job_result.fetchall()]

    connection.close()

    rankings = []

    for job_id in job_ids:
        result = match_cv_to_job(
            cv_skills=cv_skills,
            job_id=job_id,
        )
        rankings.append(
            JobRankingResult(
                job_id=result.job_id,
                job_title=result.job_title,
                match_rate=result.match_rate,
                matched_skills=result.matched_skills,
                missing_skills=result.missing_skills,
                extra_skills=result.extra_skills,
            )
        )

    rankings.sort(
        key=lambda result: result.match_rate,
        reverse=True,
    )

    if top_n is not None:
        rankings = rankings[:top_n]

    return rankings