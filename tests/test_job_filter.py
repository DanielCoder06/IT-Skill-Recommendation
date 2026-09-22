from src.scraper.job_filter import (
    calculate_it_score,
    is_it_job,
)
from src.scraper.job_schema import JobRecord


def make_job(
    title: str,
    description: str = "",
) -> JobRecord:
    return JobRecord(
        title=title,
        company="Test Company",
        description=description,
        location="Remote",
        url="https://example.com/test",
        experience="",
    )


def test_software_engineer_is_it():
    job = make_job(
        "Senior Software Engineer",
        "Develop backend services using Python.",
    )

    assert is_it_job(job)


def test_data_engineer_is_it():
    job = make_job(
        "Data Engineer",
        "Build data pipelines using Python and SQL.",
    )

    assert is_it_job(job)


def test_fullstack_developer_is_it():
    job = make_job(
        "Fullstack Developer",
        "Develop web applications using React and Node.js.",
    )

    assert is_it_job(job)


def test_sales_manager_with_ai_is_not_it():
    job = make_job(
        "Sales Manager - AI",
        "Sell AI solutions to enterprise customers.",
    )

    assert not is_it_job(job)


def test_talent_acquisition_with_ai_is_not_it():
    job = make_job(
        "Talent Acquisition Specialist - AI",
        "Recruit employees for an AI company.",
    )

    assert not is_it_job(job)


def test_bauleiter_is_not_it():
    job = make_job(
        "Bauleiter",
        "Construction project management.",
    )

    assert not is_it_job(job)


def test_sales_engineer_ai_is_not_it():
    job = make_job(
        "Senior Sales Engineer - AI Agents",
        "Sell AI agent solutions to customers.",
    )

    assert not is_it_job(job)


def test_ai_data_team_lead_is_not_necessarily_it():
    job = make_job(
        "Team Lead Weiterbildungen AI & Data Science",
        "Manage training programs and educational activities.",
    )

    assert not is_it_job(job)


def test_it_score_is_higher_for_software_engineer():
    job = make_job(
        "Software Engineer",
        "Python, Docker, Kubernetes.",
    )

    assert calculate_it_score(job) >= 3