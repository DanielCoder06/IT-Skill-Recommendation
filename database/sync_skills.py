import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DICTIONARY_PATH = BASE_DIR / "config" / "skills_dictionary.json"
DB_PATH = BASE_DIR / "data" / "it_jobs.db"

def load_skills_dictionary():
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def sync_skills():
    skills_dictionary = load_skills_dictionary()
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    
    for skill_name, skill_info in skills_dictionary.items():
        
        category = skill_info["category"]
        aliases  = json.dumps(skill_info["aliases"], ensure_ascii=False)
        
        connection.execute(
            """INSERT OR IGNORE INTO skills
            (name, category, aliases)
            VALUES (?, ?, ?)""",
            (skill_name, category, aliases)
        )
        
    connection.commit()
    connection.close()
    
if __name__ == "__main__":
    sync_skills()
    print("Đã đồng bộ skill vào database.")