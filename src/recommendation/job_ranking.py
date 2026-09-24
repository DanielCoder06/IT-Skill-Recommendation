import sqlite3
from dataclasses import dataclass
from pathlib import Path

from src.recommendation.cv_job_matching import match_cv_to_job
from src.recommendation.cv_profile_matching import get_cv_profile
from src.scraper.job_classifier import classify_job_level
from src.scraper.job_filter import is_it_job
from src.scraper.job_schema import JobRecord


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


def get_target_job_ids() -> list[int]:
    """
    Lấy ID của các job vừa là IT job vừa là internship.
    """
    connection = sqlite3.connect(DB_PATH)

    rows = connection.execute(
        """
        SELECT
            jobs.id,
            jobs.title,
            companies.name,
            jobs.jd_raw,
            locations.city,
            jobs.job_url,
            jobs.experience
        FROM jobs
        JOIN companies
            ON jobs.company_id = companies.id
        LEFT JOIN locations
            ON jobs.location_id = locations.id
        """
    ).fetchall()

    connection.close()

    job_ids = []

    for row in rows:
        job = JobRecord(
            title=row[1],
            company=row[2],
            description=row[3] or "",
            location=row[4] or "",
            url=row[5],
            experience=row[6] or "",
        )

        if (
            is_it_job(job)
            and classify_job_level(job) == "internship"
        ):
            job_ids.append(row[0])

    return job_ids


def rank_jobs_for_cv(
    cv_id: int,
    top_n: int | None = None,
) -> list[JobRankingResult]:
    """
    Xếp hạng các IT internship dựa trên mức độ phù hợp với một CV.
    """

    profile = get_cv_profile(cv_id)
    cv_skills = set(profile["skills"])

    job_ids = get_target_job_ids()

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