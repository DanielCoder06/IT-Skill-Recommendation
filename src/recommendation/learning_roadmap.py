import sqlite3
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "it_jobs.db"


@dataclass
class LearningStep:
    skill: str
    level: int


def get_prerequisites(skill_name: str) -> set[str]:
    """
    Lấy trực tiếp các prerequisite của một skill.
    """
    connection = sqlite3.connect(DB_PATH)

    result = connection.execute(
        """
        SELECT prerequisite.name
        FROM skill_prerequisites sp
        JOIN skills skill
            ON skill.id = sp.skill_id
        JOIN skills prerequisite
            ON prerequisite.id = sp.prerequisite_skill_id
        WHERE skill.name = ?
        """,
        (skill_name,),
    )

    prerequisites = {
        row[0]
        for row in result.fetchall()
    }

    connection.close()

    return prerequisites


def build_learning_roadmap(
    target_skills: set[str],
) -> list[LearningStep]:
    """
    Xây dựng learning roadmap từ target skills
    dựa trên quan hệ prerequisite.
    """
    visited = set()
    ordered_skills = []

    def visit(skill: str, level: int) -> None:
        if skill in visited:
            return

        prerequisites = get_prerequisites(skill)

        for prerequisite in prerequisites:
            visit(prerequisite, level + 1)

        visited.add(skill)
        ordered_skills.append(
            LearningStep(
                skill=skill,
                level=level,
            )
        )

    for skill in target_skills:
        visit(skill, 0)

    return ordered_skills