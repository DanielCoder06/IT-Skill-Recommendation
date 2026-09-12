import json
import re
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DICTIONARY_PATH = BASE_DIR / "config" / "skills_dictionary.json"
DB_PATH = BASE_DIR / "data" / "it_jobs.db"


def load_skills_dictionary():
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_skills(jd_text: str) -> list[str]:
    skills_dictionary = load_skills_dictionary()

    found_skills = []

    for skill_name, skill_info in skills_dictionary.items():

        for alias in skill_info["aliases"]:

            pattern = rf"\b{re.escape(alias)}\b"

            if re.search(pattern, jd_text, re.IGNORECASE):
                found_skills.append(skill_name)
                break

    return found_skills


def save_job_skills(job_id: int, skill_names: list[str]):
    connection = sqlite3.connect(DB_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    for skill_name in skill_names:

        result = connection.execute(
            """
            SELECT id
            FROM skills
            WHERE name = ?
            """,
            (skill_name,)
        )

        skill = result.fetchone()

        if skill is None:
            continue

        skill_id = skill[0]

        connection.execute(
            """
            INSERT OR IGNORE INTO job_skills
            (job_id, skill_id, source)
            VALUES (?, ?, ?)
            """,
            (job_id, skill_id, "regex")
        )

    connection.commit()
    connection.close()


if __name__ == "__main__":

    jd = """
    Tuyển Intern Python Developer.

    Yêu cầu:
    - Biết Python và SQL
    - Sử dụng Git và GitHub
    - Có kiến thức Machine Learning
    - Có khả năng giao tiếp tiếng Anh
    - Làm việc nhóm tốt
    """

    skills = extract_skills(jd)

    print("Skills tìm được:")

    for skill in skills:
        print("-", skill)

    save_job_skills(1, skills)

    print("Đã lưu skills vào job_skills.")