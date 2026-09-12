import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "data" / "it_jobs.db"
DICTIONARY_PATH = BASE_DIR / "config" / "skills_dictionary.json"


def load_skills():
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def insert_skills():
    skills = load_skills()

    connection = sqlite3.connect(DB_PATH)

    for skill_name, skill_info in skills.items():
        connection.execute(
            """
            INSERT OR IGNORE INTO skills (name, category, aliases)
            VALUES (?, ?, ?)
            """,
            (
                skill_name,
                skill_info["category"],
                json.dumps(skill_info["aliases"], ensure_ascii=False)
            )
        )

    connection.commit()
    connection.close()

    print(f"Đã load {len(skills)} skills vào database.")


if __name__ == "__main__":
    insert_skills()