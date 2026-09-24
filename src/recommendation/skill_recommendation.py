import sqlite3
from dataclasses import dataclass
from pathlib import Path

from src.scraper.job_classifier import classify_job_level
from src.scraper.job_filter import is_it_job
from src.scraper.job_schema import JobRecord    

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"

@dataclass
class SkillRecommendation:
    skill: str
    job_count: int
    job_percentage: float
    
def get_analyzed_target_job_ids() -> list[int]:
    """
    Lấy ID của các job vừa là IT internship
    vừa đã được phân tích skill.
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

    analyzed_rows = connection.execute(
        """
        SELECT DISTINCT job_id
        FROM job_skills
        """
    ).fetchall()

    connection.close()

    analyzed_job_ids = {
        row[0]
        for row in analyzed_rows
    }

    target_job_ids = []

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
            row[0] in analyzed_job_ids
            and is_it_job(job)
            and classify_job_level(job) == "internship"
        ):
            target_job_ids.append(row[0])

    return target_job_ids


def recommend_skills(
    missing_skills: set[str],
) -> list[SkillRecommendation]:
    """
    Recommend missing skills based on their demand
    across analyzed target IT internships.
    """
    if not missing_skills:
        return []

    target_job_ids = get_analyzed_target_job_ids()

    if not target_job_ids:
        return []

    connection = sqlite3.connect(DB_PATH)

    skill_placeholders = ", ".join(
        "?" for _ in missing_skills
    )

    job_placeholders = ", ".join(
        "?" for _ in target_job_ids
    )

    query = f"""
        SELECT
            s.name AS skill,
            COUNT(DISTINCT js.job_id) AS job_count
        FROM job_skills js
        JOIN skills s
            ON s.id = js.skill_id
        WHERE s.name IN ({skill_placeholders})
          AND js.job_id IN ({job_placeholders})
        GROUP BY s.id, s.name
        ORDER BY job_count DESC, skill ASC
    """

    parameters = (
        tuple(missing_skills)
        + tuple(target_job_ids)
    )

    result = connection.execute(
        query,
        parameters,
    )

    rows = result.fetchall()

    connection.close()

    total_jobs = len(target_job_ids)

    recommendations = []

    for skill, job_count in rows:
        job_percentage = (
            job_count / total_jobs * 100
        )

        recommendation = SkillRecommendation(
            skill=skill,
            job_count=job_count,
            job_percentage=round(job_percentage, 2),
        )

        recommendations.append(recommendation)

    return recommendations

def recommend_missing_skills_for_job(
    missing_skills: set[str],
) -> list[SkillRecommendation]:
    """
    Recommend missing skills based on their demand
    across analyzed target IT internships.
    """
    return recommend_skills(
        missing_skills=missing_skills,
    )