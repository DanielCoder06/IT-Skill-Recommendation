from src.pipeline.load_jobs import load_jobs
from src.extractor.extractor_regex import extract_skills, save_job_skills
from src.extractor.extractor_gemini import extract_skills_with_gemini
from src.extractor.skill_merger import merge_skills, get_skill_sources


def run_pipeline():
    jobs = load_jobs()

    for job in jobs:
        title = job["title"]
        description = job["description"]

        # 1. Extract skills bằng Regex
        regex_skills = extract_skills(description)

        # 2. Extract skills bằng Gemini
        try:
            gemini_result = extract_skills_with_gemini(description)
            gemini_skills = set(gemini_result.skills)
        except Exception as error:
            print(f"Gemini error: {error}")
            gemini_skills = set()

        # 3. Merge hai kết quả
        final_skills = merge_skills(
            regex_skills,
            gemini_skills,
        )

        # 4. Xác định nguồn của từng skill
        skill_sources = get_skill_sources(
            regex_skills,
            gemini_skills,
        )

        # 5. Lưu skill và source vào database
        save_job_skills(
            job["id"],
            skill_sources,
        )

        # 6. Hiển thị kết quả
        print(f"\nJob: {title}")

        print("Regex:")
        for skill in sorted(regex_skills):
            print(f"- {skill}")

        print("Gemini:")
        for skill in sorted(gemini_skills):
            print(f"- {skill}")

        print("Final:")
        for skill in sorted(final_skills):
            print(f"- {skill}")


if __name__ == "__main__":
    run_pipeline()