import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
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
            raise ValueError(
                f"Skill không tồn tại trong dictionary: {unknown_skills}"
            )

        return skills

def create_gemini_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY chưa được cấu hình")

    return genai.Client(api_key=api_key)

def build_gemini_prompt(jd_text: str) -> str:
    skills_dictionary = load_skills_dictionary()
    
    allowed_skills = "\n".join(skills_dictionary.keys())
    
    prompt = f"""
    You are an IT job skill extraction system.

    Extract the technical and professional skills from the job description.

    IMPORTANT RULES:
    - Only select skills from the allowed skill list.
    - Do not create new skills.
    - Return canonical skill names exactly as they appear in the allowed skill list.
    - Do not return explanations.

    ALLOWED SKILLS:
    {allowed_skills}

    JOB DESCRIPTION:
    {jd_text}
    """

    return prompt

def extract_skills_with_gemini(jd_text: str) -> GeminiSkillOutput:
    client = create_gemini_client()
    prompt = build_gemini_prompt(jd_text)
    interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": GeminiSkillOutput.model_json_schema(),
        },
    )

    return GeminiSkillOutput.model_validate_json(
        interaction.output_text
    )