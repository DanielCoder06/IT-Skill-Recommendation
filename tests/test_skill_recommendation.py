from src.recommendation.skill_recommendation import recommend_skills


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