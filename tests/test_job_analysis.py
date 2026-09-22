from src.recommendation.job_analysis import (
    analyze_cv_for_job,
)


def test_analyze_cv_for_job():
    result = analyze_cv_for_job(
        cv_id=1,
        job_id=6,
    )

    assert result.job_id == 6
    assert result.job_title == "AI Engineer Intern"

    assert result.matched_skills == {
        "Python",
        "Machine Learning",
        "Deep Learning",
    }

    assert result.missing_skills == {
        "PyTorch",
        "Pandas",
        "Artificial Intelligence",
        "Git",
    }

    assert result.match_rate == 42.86

    assert result.recommendations

    recommended_skills = {
        recommendation.skill
        for recommendation in result.recommendations
    }

    assert recommended_skills.issubset(
        result.missing_skills
    )

    roadmap_skills = {
        step.skill
        for step in result.learning_roadmap
    }

    assert result.missing_skills.issubset(
        roadmap_skills
    )