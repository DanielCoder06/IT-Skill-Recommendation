from unittest.mock import patch

from src.pipeline.job_pipeline import run_pipeline


def test_job_pipeline_merges_and_saves_skills():
    jobs = [
        {
            "id": 1,
            "title": "Python Intern",
            "company_name": "ABC",
            "description": """
            Looking for a Python intern with SQL and Pandas.
            """,
            "location": "Can Tho",
            "url": "https://example.com/python-intern",
            "experience": "Intern",
            "skills": [],
        }
    ]

    hybrid_result = {
        "confirmed_skills": {
            "Python",
            "SQL",
        },
        "suggested_skills": {
            "Pandas",
        },
    }

    with patch(
        "src.pipeline.job_pipeline.load_jobs",
        return_value=jobs,
    ), patch(
        "src.pipeline.job_pipeline.save_jobs_to_db",
        return_value={
            "https://example.com/python-intern": 1,
        },
    ), patch(
        "src.pipeline.job_pipeline.extract_hybrid_skills",
        return_value=hybrid_result,
    ), patch(
        "src.pipeline.job_pipeline.save_job_skills",
    ) as mock_save:

        run_pipeline()

    mock_save.assert_called_once_with(
        1,
        {
            "Python": "regex",
            "SQL": "regex",
            "Pandas": "supplementary",
        },
    )