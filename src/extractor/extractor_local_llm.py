import json
from pathlib import Path

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"

BASE_DIR = Path(__file__).resolve().parents[2]
SKILLS_DICTIONARY_PATH = BASE_DIR / "config" / "skills_dictionary.json"


def load_skill_dictionary() -> dict:
    """Đọc canonical skills và aliases từ skills_dictionary.json."""
    with open(SKILLS_DICTIONARY_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_skill_reference(skill_dictionary: dict) -> str:
    """Tạo danh sách canonical skill + aliases để đưa vào prompt."""
    lines = []

    for skill, data in skill_dictionary.items():
        aliases = data.get("aliases", [])

        alias_text = ", ".join(aliases)

        lines.append(
            f"- {skill}: {alias_text}"
        )

    return "\n".join(lines)


def build_prompt(text: str, skill_reference: str) -> str:
    """Tạo prompt yêu cầu Qwen trích xuất canonical skills."""
    return f"""
You are an IT skill extraction system.

Your task is to extract IT skills from the given text.

IMPORTANT RULES:

1. Extract only IT skills that have explicit textual evidence in the input text.

2. A skill may be extracted only if:
   - the canonical skill name appears explicitly, OR
   - a listed alias appears explicitly, OR
   - a clearly unambiguous synonym or abbreviation appears explicitly.

3. Do NOT infer skills from the general meaning of a sentence.

4. Do NOT infer a technology from a broad concept.

   Example:
   "modern web applications"
   -> empty

   Do NOT output:
   HTML
   CSS
   JavaScript
   React

5. Do NOT infer a skill from an activity or concept that is merely related to it.

   Example:
   "statistical analysis"
   -> empty

   Do NOT output:
   Statistics
   Data Visualization

6. Do NOT infer libraries or frameworks from a programming language.

   Example:
   "Python programming"
   -> Python

   Do NOT output:
   Pandas
   NumPy
   Scikit-learn

7. Do NOT infer skills from common soft-skill words unless they are
   explicitly required as a skill.

   Example:
   "Good communication skills and willingness to learn."
   -> empty

   Do NOT output:
   Communication

8. A skill must have direct evidence in the text.
   If you cannot point to the exact word or phrase supporting the skill,
   do not extract it.

9. Do not add skills because they are commonly used together.

10. Map explicit Vietnamese expressions, English expressions,
    abbreviations, and known synonyms to the canonical skill names.

11. Return only canonical skill names.

12. Return one skill per line.

13. Do not return explanations.

14. If there is no explicit skill evidence, return an empty response.

EXTRACTION EXAMPLES:

Text:
"Experience with Python and Pandas."

Output:
Python
Pandas


Text:
"Experience building RESTful services."

Output:
REST API


Text:
"Experience with Python programming."

Output:
Python

Do NOT output:
Pandas
NumPy
Scikit-learn


Text:
"Experience working with modern web applications."

Output:
(empty)

Do NOT output:
HTML
CSS
JavaScript
React


Text:
"Good communication skills and willingness to learn."

Output:
(empty)

Do NOT output:
Communication


Text:
"Experience analyzing structured datasets and performing
statistical analysis."

Output:
(empty)

Do NOT output:
Statistics
Data Visualization
NumPy


Text:
"Developed applications using Java, Spring Boot,
MySQL and Git."

Output:
Java
Spring Boot
MySQL
Git

CANONICAL SKILLS AND ALIASES:
{skill_reference}

TEXT:
{text}
""".strip()


def parse_skill_response(response_text: str, skill_dictionary: dict) -> set[str]:
    """Chuẩn hóa output của LLM thành tập canonical skills."""
    canonical_skills = skill_dictionary.keys()

    canonical_lookup = {
        skill.casefold(): skill
        for skill in canonical_skills
    }

    extracted_skills = set()

    for line in response_text.splitlines():
        skill = line.strip().lstrip("-").strip()

        normalized_skill = canonical_lookup.get(skill.casefold())

        if normalized_skill:
            extracted_skills.add(normalized_skill)

    return extracted_skills


def extract_skills_with_local_llm(text: str) -> set[str]:
    """
    Trích xuất kỹ năng từ text bằng Local LLM chạy qua Ollama.
    """
    if not isinstance(text, str):
        raise TypeError("text phải là string.")

    if not text.strip():
        return set()

    skill_dictionary = load_skill_dictionary()

    skill_reference = build_skill_reference(skill_dictionary)

    prompt = build_prompt(
        text=text,
        skill_reference=skill_reference,
    )

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    response_data = response.json()

    response_text = response_data.get("response", "")

    print("=== LOCAL LLM DEBUG ===")
    print(response_text)
    print("=======================")

    return parse_skill_response(
        response_text=response_text,
        skill_dictionary=skill_dictionary,
    )