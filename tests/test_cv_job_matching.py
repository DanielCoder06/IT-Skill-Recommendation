from src.recommendation.cv_job_matching import match_cv_to_job


def test_cv_matches_data_science_job():
    cv_skills = {
        "Python",
        "SQL",
        "Pandas",
        "Git",
    }

    result = match_cv_to_job(
        cv_skills=cv_skills,
        job_id=8,
    )

    assert result.job_id == 8
    assert result.job_title == "Data Science Intern"

    assert result.matched_skills == {
        "Python",
        "SQL",
        "Pandas",
    }

    assert result.missing_skills == {
        "Machine Learning",
        "English",
        "Communication",
        "NumPy",
        "Statistics",
        "Data Visualization",
    }

    assert result.extra_skills == {
        "Git",
    }

    assert result.match_rate == 33.33