import pytest

from src.recommendation.skill_gap import calculate_skill_gap


def test_skill_gap_normal_case():
    student_skills = {
        "Python",
        "SQL",
        "Git",
    }

    result = calculate_skill_gap(
        student_skills,
        8,
    )

    assert result.job_id == 8
    assert result.job_title == "Data Science Intern"

    assert result.matched_skills == {
        "Python",
        "SQL",
    }

    assert result.missing_skills == {
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Statistics",
        "Data Visualization",
        "Communication",
        "English",
    }

    assert result.extra_skills == {
        "Git",
    }

    assert result.match_rate == 22.22


def test_skill_gap_job_not_found():
    with pytest.raises(
        ValueError,
        match="Job không tồn tại: 999",
    ):
        calculate_skill_gap(
            {"Python", "SQL"},
            999,
        )


def test_skill_gap_student_has_no_skills():
    result = calculate_skill_gap(
        set(),
        8,
    )

    assert result.matched_skills == set()
    assert result.extra_skills == set()

    assert result.missing_skills == {
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "Machine Learning",
        "Statistics",
        "Data Visualization",
        "Communication",
        "English",
    }

    assert result.match_rate == 0.0


def test_skill_gap_student_has_all_job_skills():
    job_skills = {
        "Python",
        "Pandas",
        "NumPy",
        "SQL",
        "Machine Learning",
        "Statistics",
        "Data Visualization",
        "Communication",
        "English",
    }

    result = calculate_skill_gap(
        job_skills,
        8,
    )

    assert result.matched_skills == job_skills
    assert result.missing_skills == set()
    assert result.extra_skills == set()
    assert result.match_rate == 100.0