from unittest.mock import patch

from src.pipeline.job_pipeline import run_pipeline
from src.extractor.extractor_gemini import GeminiSkillOutput


def test_job_pipeline_merges_and_saves_skills():
    jobs = [
        {
            "id": 1,
            "title": "Python Intern",
            "description": """
            Looking for a Python intern with SQL and Pandas.
            """,
        }
    ]

    gemini_result = GeminiSkillOutput(
        skills=["Python", "Pandas"]
    )

    with patch(
        "src.pipeline.job_pipeline.load_jobs",
        return_value=jobs,
    ), patch(
        "src.pipeline.job_pipeline.extract_skills_with_gemini",
        return_value=gemini_result,
    ), patch(
        "src.pipeline.job_pipeline.save_job_skills"
    ) as mock_save:

        run_pipeline()

    mock_save.assert_called_once_with(
        1,
        {
            "Python": "both",
            "Pandas": "both",
            "SQL": "regex",
        },
    )