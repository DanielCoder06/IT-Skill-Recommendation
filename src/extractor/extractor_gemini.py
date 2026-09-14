import json
from pathlib import Path

from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parents[2]
DICTIONARY_PATH = BASE_DIR / "config" / "skills_dictionary.json"

def load_skills_dictionary() -> dict:
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

class GeminiSkillOutput(BaseModel):
    skills: list[str]
    
    @field_validator("skills")
    @classmethod
    def validate_skills(cls, skills: list[str]) -> list[str]:
        if not skills:
            raise ValueError("skills không được rỗng")  
        
        skills_dictionary = load_skills_dictionary()
        
        unknown_skills = [
            skill 
            for skill in skills
            if skill not in skills_dictionary
        ]
        
        if unknown_skills:
            raise ValueError(f"Skill không tồn tại trong dictionary: {unknown_skills}")
        
        return skills
    