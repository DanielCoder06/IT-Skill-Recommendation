from src.extractor.extractor_regex import extract_skills


def test_basic_skills():
    text = "We need Python, SQL and Git."
    skills = extract_skills(text)

    assert "Python" in skills
    assert "SQL" in skills
    assert "Git" in skills


def test_python_programming():
    text = "Experience with Python programming."
    skills = extract_skills(text)

    assert "Python" in skills


def test_react_js():
    text = "Experience with React.js."
    skills = extract_skills(text)

    assert "React" in skills


def test_node_js():
    text = "Experience with Node.js."
    skills = extract_skills(text)

    assert "Node.js" in skills


def test_ci_cd():
    text = "Knowledge of CI/CD is required."
    skills = extract_skills(text)

    assert "CI/CD" in skills


def test_mysql():
    text = "Experience with MySQL."
    skills = extract_skills(text)

    assert "MySQL" in skills


def test_postgresql():
    text = "Experience with PostgreSQL."
    skills = extract_skills(text)

    assert "PostgreSQL" in skills


def test_no_false_positive():
    text = "The candidate has experience with Python."
    skills = extract_skills(text)

    assert "Java" not in skills
    assert "React" not in skills
    assert "Docker" not in skills
    
def test_mysql_overlap():
    text = "Experience with MySQL."
    skills = extract_skills(text)

    print("\nMySQL test:", skills)

    assert "MySQL" in skills
    assert "SQL" not in skills


def test_postgresql_overlap():
    text = "Experience with PostgreSQL."
    skills = extract_skills(text)

    print("\nPostgreSQL test:", skills)

    assert "PostgreSQL" in skills
    assert "SQL" not in skills
    
def test_javascript_not_java():
    text = "Experience with JavaScript."
    skills = extract_skills(text)

    print("\nJavaScript test:", skills)

    assert "JavaScript" in skills
    assert "Java" not in skills


def test_github_not_git():
    text = "Experience with GitHub."
    skills = extract_skills(text)

    print("\nGitHub test:", skills)

    assert "GitHub" in skills
    assert "Git" not in skills


def test_case_insensitive():
    text = "Experience with PYTHON, javascript and GITHUB."
    skills = extract_skills(text)

    print("\nCase insensitive test:", skills)

    assert "Python" in skills
    assert "JavaScript" in skills
    assert "GitHub" in skills

def test_common_aliases():
    text = """
    We are looking for candidates with ML and DL experience.
    Knowledge of Postgres, React.js and NumPy is a plus.
    """

    skills = extract_skills(text)

    print("\nAlias test:", skills)

    assert "Machine Learning" in skills
    assert "Deep Learning" in skills
    assert "PostgreSQL" in skills
    assert "React" in skills
    assert "NumPy" in skills
    
def test_vietnamese_skills():
    text = """
    Ứng viên có kiến thức về lập trình Python.
    Có kinh nghiệm học máy và học sâu.
    Biết sử dụng Git và GitHub.
    Có khả năng giao tiếp tiếng Anh và làm việc nhóm.
    """

    skills = extract_skills(text)

    print("\nVietnamese test:", skills)

    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "Deep Learning" in skills
    assert "Git" in skills
    assert "GitHub" in skills
    assert "English" in skills
    assert "Communication" in skills
    assert "Teamwork" in skills