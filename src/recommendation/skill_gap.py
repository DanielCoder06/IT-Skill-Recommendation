import sqlite3
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"


@dataclass
class SkillGapResult:
    job_id: int
    job_title: str
    matched_skills: set[str]
    missing_skills: set[str]
    extra_skills: set[str]
    match_rate: float


def calculate_skill_gap(
    student_skills: set[str],
    job_id: int,
) -> SkillGapResult:

    connection = sqlite3.connect(DB_PATH)

    job_result = connection.execute(
        """
        SELECT title
        FROM jobs
        WHERE id = ?
        """,
        (job_id,),
    )

    job = job_result.fetchone()

    if job is None:
        connection.close()
        raise ValueError(f"Job không tồn tại: {job_id}")

    job_title = job[0]

    skill_result = connection.execute(
        """
        SELECT s.name
        FROM job_skills js
        JOIN skills s
            ON s.id = js.skill_id
        WHERE js.job_id = ?
        """,
        (job_id,),
    )

    job_skills = {
        row[0]
        for row in skill_result.fetchall()
    }

    connection.close()

    matched_skills = student_skills & job_skills
    missing_skills = job_skills - student_skills
    extra_skills = student_skills - job_skills

    if job_skills:
        match_rate = (
            len(matched_skills)
            / len(job_skills)
            * 100
        )
    else:
        match_rate = 0.0

    return SkillGapResult(
        job_id=job_id,
        job_title=job_title,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        extra_skills=extra_skills,
        match_rate=round(match_rate, 2),
    )