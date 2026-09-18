import sqlite3
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"

@dataclass
class SkillRecommendation:
    skill: str
    job_count: int
    job_percentage: float

def recommend_skills(missing_skills: set[str]) -> list[SkillRecommendation]:
    connection = sqlite3.connect(DB_PATH)

    placeholders = ", ".join("?" for _ in missing_skills)

    query = f"""
        SELECT
            s.name AS skill,
            COUNT(DISTINCT js.job_id) AS job_count
        FROM job_skills js
        JOIN skills s
            ON s.id = js.skill_id
        WHERE s.name IN ({placeholders})
        GROUP BY s.id, s.name
        ORDER BY job_count DESC, skill ASC
    """

    result = connection.execute(
        query,
        tuple(missing_skills),
    )

    rows = result.fetchall()
    total_jobs_result = connection.execute(
        """
        SELECT COUNT(*)
        FROM jobs
        """
    )

    total_jobs = total_jobs_result.fetchone()[0]

    connection.close()

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