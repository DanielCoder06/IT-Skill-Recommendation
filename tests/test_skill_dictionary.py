from src.extractor.skill_matcher import SkillMatcher


def create_matcher():
    return SkillMatcher("config/skills_dictionary.json")


# ============================================================
# A. Alias hợp lệ
# ============================================================

def test_python_alias():
    matcher = create_matcher()

    skills = matcher.skills("Ứng viên có kinh nghiệm Python3.")

    assert "Python" in skills


def test_postgresql_alias():
    matcher = create_matcher()

    skills = matcher.skills("Experience with Postgres database.")

    assert "PostgreSQL" in skills


def test_reactjs_alias():
    matcher = create_matcher()

    skills = matcher.skills("Frontend developer using ReactJS.")

    assert "React" in skills


def test_sklearn_alias():
    matcher = create_matcher()

    skills = matcher.skills("Experience with sklearn.")

    assert "Scikit-learn" in skills


def test_node_js_alias():
    matcher = create_matcher()

    skills = matcher.skills("Backend development with Node JS.")

    assert "Node.js" in skills


# ============================================================
# B. Case-insensitive
# ============================================================

def test_case_insensitive():
    matcher = create_matcher()

    skills = matcher.skills(
        "PYTHON JAVASCRIPT POSTGRESQL GITHUB"
    )

    assert "Python" in skills
    assert "JavaScript" in skills
    assert "PostgreSQL" in skills
    assert "GitHub" in skills


# ============================================================
# C. Tiếng Việt
# ============================================================

def test_vietnamese_aliases():
    matcher = create_matcher()

    skills = matcher.skills(
        "Có kiến thức lập trình Python, học máy, "
        "trí tuệ nhân tạo và làm việc nhóm."
    )

    assert "Python" in skills
    assert "Machine Learning" in skills
    assert "Artificial Intelligence" in skills
    assert "Teamwork" in skills


# ============================================================
# D. Kiểm tra false positive
# ============================================================

def test_graphql_api_is_not_rest_api():
    matcher = create_matcher()

    skills = matcher.skills(
        "Develop APIs using GraphQL."
    )

    assert "REST API" not in skills


def test_generic_container_is_not_docker():
    matcher = create_matcher()

    skills = matcher.skills(
        "Experience with container technology."
    )

    assert "Docker" not in skills


def test_generic_version_control_is_not_git():
    matcher = create_matcher()

    skills = matcher.skills(
        "Experience with version control systems."
    )

    assert "Git" not in skills