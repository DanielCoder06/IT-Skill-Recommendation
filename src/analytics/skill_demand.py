import sqlite3
from pathlib import Path

from src.scraper.job_schema import JobRecord
from src.scraper.job_filter import is_it_job
from src.scraper.job_classifier import classify_job_level


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"


def load_jobs_from_db() -> list[JobRecord]:
    connection = sqlite3.connect(DB_PATH)

    rows = connection.execute(
        """
        SELECT
            title,
            companies.name,
            jd_raw,
            locations.city,
            job_url,
            experience
        FROM jobs
        JOIN companies
            ON jobs.company_id = companies.id
        LEFT JOIN locations
            ON jobs.location_id = locations.id
        """
    ).fetchall()

    connection.close()

    return [
        JobRecord(
            title=row[0],
            company=row[1],
            description=row[2] or "",
            location=row[3] or "",
            url=row[4],
            experience=row[5] or "",
        )
        for row in rows
    ]


def get_target_internship_jobs() -> list[JobRecord]:
    jobs = load_jobs_from_db()

    return [
        job
        for job in jobs
        if is_it_job(job)
        and classify_job_level(job) == "internship"
    ]


def get_skill_demand() -> list[tuple[str, int]]:
    target_jobs = get_analyzed_target_internship_jobs()

    connection = sqlite3.connect(DB_PATH)

    placeholders = ",".join("?" for _ in target_jobs)

    if not target_jobs:
        connection.close()
        return []

    job_urls = [job.url for job in target_jobs]

    rows = connection.execute(
        f"""
        SELECT
            skills.name,
            COUNT(DISTINCT job_skills.job_id) AS job_count
        FROM job_skills
        JOIN skills
            ON job_skills.skill_id = skills.id
        JOIN jobs
            ON job_skills.job_id = jobs.id
        WHERE jobs.job_url IN ({placeholders})
        GROUP BY skills.id
        ORDER BY job_count DESC, skills.name ASC
        """,
        job_urls,
    ).fetchall()

    connection.close()

    return [(row[0], row[1]) for row in rows]


def get_skill_demand_percentage() -> list[tuple[str, float]]:
    analyzed_jobs = get_analyzed_target_internship_jobs()

    if not analyzed_jobs:
        return []

    demand = get_skill_demand()

    total_jobs = len(analyzed_jobs)

    return [
        (skill, round(count / total_jobs * 100, 1))
        for skill, count in demand
    ]

def get_analyzed_target_internship_jobs() -> list[JobRecord]:
    target_jobs = get_target_internship_jobs()

    if not target_jobs:
        return []

    connection = sqlite3.connect(DB_PATH)

    job_urls = [job.url for job in target_jobs]
    placeholders = ",".join("?" for _ in job_urls)

    rows = connection.execute(
        f"""
        SELECT DISTINCT jobs.job_url
        FROM jobs
        JOIN job_skills
            ON jobs.id = job_skills.job_id
        WHERE jobs.job_url IN ({placeholders})
        """,
        job_urls,
    ).fetchall()

    connection.close()

    analyzed_urls = {row[0] for row in rows}

    return [
        job
        for job in target_jobs
        if job.url in analyzed_urls
    ]
    
def get_skill_extraction_coverage() -> tuple[int, int, float]:
    target_jobs = get_target_internship_jobs()
    analyzed_jobs = get_analyzed_target_internship_jobs()

    total = len(target_jobs)
    analyzed = len(analyzed_jobs)

    if total == 0:
        return 0, 0, 0.0

    percentage = round(analyzed / total * 100, 1)

    return total, analyzed, percentage