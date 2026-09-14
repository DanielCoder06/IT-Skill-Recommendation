from src.pipeline.load_jobs import load_jobs
from src.extractor.extractor_regex import extract_skills, save_job_skills
def run_pipeline():
    jobs = load_jobs()
    
    for job in jobs:
        title = job["title"]
        description = job["description"]
        
        skills = extract_skills(description)
        save_job_skills(job["id"], skills)
        
        print(f"\nJob: {title}")
        print("Skills found:")
        
        for skill in skills:
            print(f"- {skill}")

if __name__ == "__main__":
    run_pipeline()