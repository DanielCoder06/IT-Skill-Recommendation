from src.recommendation.learning_roadmap import (
    get_prerequisites,
    build_learning_roadmap,
)


def test_get_pytorch_prerequisites():
    prerequisites = get_prerequisites("PyTorch")

    assert prerequisites == {
        "Deep Learning",
    }


def test_build_pytorch_learning_roadmap():
    roadmap = build_learning_roadmap(
        {"PyTorch"}
    )

    skills = [
        step.skill
        for step in roadmap
    ]

    assert set(skills) == {
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "Machine Learning",
        "Deep Learning",
        "PyTorch",
    }

    assert skills.index("Python") < skills.index("Machine Learning")
    assert skills.index("NumPy") < skills.index("Machine Learning")
    assert skills.index("Pandas") < skills.index("Machine Learning")
    assert skills.index("Statistics") < skills.index("Machine Learning")
    assert skills.index("Machine Learning") < skills.index("Deep Learning")
    assert skills.index("Deep Learning") < skills.index("PyTorch")