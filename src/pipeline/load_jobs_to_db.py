import sqlite3

from src.pipeline.load_jobs import load_jobs


DB_PATH = "data/it_jobs.db"


def get_or_create_company(
    connection: sqlite3.Connection,
    company_name: str,
) -> int:
    result = connection.execute(
        """
        SELECT id
        FROM companies
        WHERE name = ?
        """,
        (company_name,),
    )

    company = result.fetchone()

    if company is not None:
        return company[0]

    cursor = connection.execute(
        """
        INSERT INTO companies (name)
        VALUES (?)
        """,
        (company_name,),
    )

    return cursor.lastrowid


def get_or_create_location(
    connection: sqlite3.Connection,
    city: str,
) -> int:
    result = connection.execute(
        """
        SELECT id
        FROM locations
        WHERE city = ?
        """,
        (city,),
    )

    location = result.fetchone()

    if location is not None:
        return location[0]

    cursor = connection.execute(
        """
        INSERT INTO locations (city)
        VALUES (?)
        """,
        (city,),
    )

    return cursor.lastrowid


def load_jobs_to_db() -> None:
    connection = sqlite3.connect(DB_PATH)

    jobs = load_jobs()

    print("Số lượng jobs:", len(jobs))

    for job in jobs:
        company_id = get_or_create_company(
            connection,
            job["company"],
        )

        location_id = get_or_create_location(
            connection,
            job["location"],
        )

        existing_job = connection.execute(
            """
            SELECT id
            FROM jobs
            WHERE job_url = ?
            """,
            (job["url"],),
        ).fetchone()

        if existing_job is None:
            connection.execute(
                """
                INSERT INTO jobs (
                    title,
                    company_id,
                    location_id,
                    jd_raw,
                    job_url,
                    experience
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    job["title"],
                    company_id,
                    location_id,
                    job["description"],
                    job["url"],
                    job["experience"],
                ),
            )

            print("INSERT:", job["title"])

        else:
            connection.execute(
                """
                UPDATE jobs
                SET
                    title = ?,
                    company_id = ?,
                    location_id = ?,
                    jd_raw = ?,
                    experience = ?
                WHERE job_url = ?
                """,
                (
                    job["title"],
                    company_id,
                    location_id,
                    job["description"],
                    job["experience"],
                    job["url"],
                ),
            )

            print("UPDATE:", job["title"])

    connection.commit()
    connection.close()


if __name__ == "__main__":
    load_jobs_to_db()