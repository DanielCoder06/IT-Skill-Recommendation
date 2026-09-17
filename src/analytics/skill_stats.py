import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"


def get_skill_frequency() -> list[tuple[str, int]]:
    connection = sqlite3.connect(DB_PATH)

    result = connection.execute("""
        SELECT
            s.name AS skill,
            COUNT(DISTINCT js.job_id) AS job_count
        FROM job_skills js
        JOIN skills s
            ON s.id = js.skill_id
        GROUP BY s.id, s.name
        ORDER BY job_count DESC, skill ASC
    """)

    rows = result.fetchall()

    connection.close()

    return rows

def get_skill_percentage() -> list[tuple[str, int, float]]:
    connection = sqlite3.connect(DB_PATH)

    result = connection.execute("""
        SELECT
            s.name AS skill,
            COUNT(DISTINCT js.job_id) AS job_count,
            ROUND(
                100.0 * COUNT(DISTINCT js.job_id)
                / (SELECT COUNT(*) FROM jobs),
                2
            ) AS job_percentage
        FROM job_skills js
        JOIN skills s
            ON s.id = js.skill_id
        GROUP BY s.id, s.name
        ORDER BY job_count DESC, skill ASC
    """)

    rows = result.fetchall()

    connection.close()

    return rows

def get_skill_by_location() -> list[tuple[str, str, int]]:
    connection = sqlite3.connect(DB_PATH)

    result = connection.execute("""
        SELECT
            l.city AS location,
            s.name AS skill,
            COUNT(DISTINCT js.job_id) AS job_count
        FROM job_skills js
        JOIN skills s
            ON s.id = js.skill_id
        JOIN jobs j
            ON j.id = js.job_id
        JOIN locations l
            ON l.id = j.location_id
        GROUP BY l.city, s.id, s.name
        ORDER BY l.city, job_count DESC, skill ASC
    """)

    rows = result.fetchall()

    connection.close()

    return rows

def get_skill_count_per_job() -> list[tuple[int, str, int]]:
    connection = sqlite3.connect(DB_PATH)

    result = connection.execute("""
        SELECT
            j.id,
            j.title,
            COUNT(DISTINCT js.skill_id) AS skill_count
        FROM jobs j
        LEFT JOIN job_skills js
            ON j.id = js.job_id
        GROUP BY j.id, j.title
        ORDER BY j.id
    """)

    rows = result.fetchall()

    connection.close()

    return rows