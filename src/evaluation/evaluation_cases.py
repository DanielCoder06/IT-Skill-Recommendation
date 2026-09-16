EVALUATION_CASES = [
    {
        "name": "Exact skill names",
        "description": """
        Looking for an intern with Python, SQL and Git.
        """,
        "expected_skills": {
            "Python",
            "SQL",
            "Git",
        },
    },
    {
        "name": "RESTful synonym",
        "description": """
        Experience building RESTful services and web APIs.
        """,
        "expected_skills": {
            "REST API",
        },
    },
    {
        "name": "Vietnamese ML description",
        "description": """
        Có kiến thức cơ bản về học máy và mạng nơ-ron sâu.
        """,
        "expected_skills": {
            "Machine Learning",
            "Deep Learning",
        },
    },
    {
        "name": "Vietnamese and English",
        "description": """
        Có kinh nghiệm sử dụng Pandas để xử lý dữ liệu.
        Experience with NumPy is a plus.
        """,
        "expected_skills": {
            "Pandas",
            "NumPy",
        },
    },
    {
        "name": "Semantic data analysis description",
        "description": """
        Experience working with tabular data using Python
        data analysis libraries.
        """,
        "expected_skills": {
            "Python",
            "Pandas",
        },
    },
]