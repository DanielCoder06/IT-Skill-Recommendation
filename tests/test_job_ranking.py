import sqlite3

from src.recommendation.job_ranking import (
    DB_PATH,
    get_target_job_ids,
    rank_jobs_for_cv,
)
from src.scraper.job_classifier import classify_job_level
from src.scraper.job_filter import is_it_job
from src.scraper.job_schema import JobRecord


def test_rank_jobs_for_cv():
    rankings = rank_jobs_for_cv(
        cv_id=1,
    )

    assert len(rankings) > 0

    assert all(
        isinstance(result.match_rate, float)
        for result in rankings
    )

    assert all(
        rankings[i].match_rate >= rankings[i + 1].match_rate
        for i in range(len(rankings) - 1)
    )


def test_top_n_job_ranking():
    rankings = rank_jobs_for_cv(
        cv_id=1,
        top_n=3,
    )

    assert len(rankings) == 3

    assert all(
        isinstance(result.job_id, int)
        for result in rankings
    )


def test_job_ranking_contains_skill_gap():
    rankings = rank_jobs_for_cv(
        cv_id=1,
        top_n=1,
    )

    result = rankings[0]

    assert isinstance(result.matched_skills, set)
    assert isinstance(result.missing_skills, set)
    assert isinstance(result.extra_skills, set)

    assert result.matched_skills


def test_target_job_ids_are_it_internships():
    job_ids = get_target_job_ids()

    assert job_ids

    connection = sqlite3.connect(DB_PATH)

    rows = connection.execute(
        """
        SELECT
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
        WHERE jobs.id IN ({})
        """.format(
            ",".join("?" for _ in job_ids)
        ),
        job_ids,
    ).fetchall()

    connection.close()

    assert len(rows) == len(job_ids)

    for row in rows:
        job = JobRecord(
            title=row[0],
            company=row[1],
            description=row[2] or "",
            location=row[3] or "",
            url=row[4],
            experience=row[5] or "",
        )

        assert is_it_job(job)
        assert classify_job_level(job) == "internship"