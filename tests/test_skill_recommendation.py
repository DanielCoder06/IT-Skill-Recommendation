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

    assert results[0].skill == "Communication"
    assert results[0].job_count == 4
    assert results[0].job_percentage == 40.0

    assert results[1].skill == "Machine Learning"
    assert results[1].job_count == 4
    assert results[1].job_percentage == 40.0

    assert results[2].skill == "Pandas"
    assert results[2].job_count == 4
    assert results[2].job_percentage == 40.0
    
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

    assert [result.skill for result in results] == [
        "Python",
        "Communication",
        "Pandas",
        "Statistics",
    ]