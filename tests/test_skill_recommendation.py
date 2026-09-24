from src.recommendation.skill_recommendation import (
    get_analyzed_target_job_ids,
    recommend_skills,
)


def test_recommend_skills_normal_case():
    missing_skills = {
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Statistics",
        "Data Visualization",
        "Communication",
        "English",
    }

    results = recommend_skills(missing_skills)

    assert results

    for result in results:
        assert result.skill in missing_skills
        assert isinstance(result.job_count, int)
        assert result.job_count >= 0

        assert isinstance(result.job_percentage, float)
        assert 0 <= result.job_percentage <= 100


def test_recommend_skills_empty_input():
    results = recommend_skills(set())

    assert results == []


def test_recommend_skills_unknown_skill():
    results = recommend_skills({"PythonXYZ"})

    assert results == []


def test_recommend_skills_order():
    missing_skills = {
        "Statistics",
        "Python",
        "Pandas",
        "Communication",
    }

    results = recommend_skills(missing_skills)

    assert all(
        results[i].job_count >= results[i + 1].job_count
        for i in range(len(results) - 1)
    )

    assert all(
        results[i].skill <= results[i + 1].skill
        for i in range(len(results) - 1)
        if results[i].job_count == results[i + 1].job_count
    )
    
def test_get_analyzed_target_job_ids():
    job_ids = get_analyzed_target_job_ids()

    assert job_ids
    assert len(job_ids) == 10


def test_recommend_skills_uses_analyzed_target_jobs():
    recommendations = recommend_skills(
        missing_skills={
            "Python",
            "Git",
            "SQL",
        }
    )

    assert recommendations

    for recommendation in recommendations:
        assert recommendation.skill in {
            "Python",
            "Git",
            "SQL",
        }

        assert recommendation.job_count <= 10
        assert 0 <= recommendation.job_percentage <= 100


def test_recommend_skills_percentage_uses_ten_jobs():
    recommendations = recommend_skills(
        missing_skills={
            "Python",
        }
    )

    assert len(recommendations) == 1

    recommendation = recommendations[0]

    assert recommendation.skill == "Python"
    assert recommendation.job_count == 9
    assert recommendation.job_percentage == 90.0


def test_recommend_skills_empty_input():
    recommendations = recommend_skills(
        missing_skills=set(),
    )

    assert recommendations == []