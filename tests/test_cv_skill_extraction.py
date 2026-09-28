from src.extractor.extractor_regex import extract_skills


def test_extract_skills_from_cv_text():
    cv_text = """
    Languages: Python, SQL, Java, C++.

    Tools: Apache Airflow, Apache Spark, Pandas, NumPy,
    Matplotlib, MySQL, PostgreSQL, Tableau, PowerBI.

    Project Management: AGILE, SCRUM, JIRA, GitHub,
    GitLab, Confluence.

    Developed a personalized product recommendation system
    using Python and machine learning libraries such as
    Scikit-learn.

    Problem-solving and analytical thinking.
    """

    skills = extract_skills(cv_text)

    expected_skills = {
        "Python",
        "SQL",
        "Java",
        "Pandas",
        "NumPy",
        "MySQL",
        "PostgreSQL",
        "GitHub",
        "Machine Learning",
        "Scikit-learn",
        "Problem Solving",
    }

    assert expected_skills.issubset(skills)