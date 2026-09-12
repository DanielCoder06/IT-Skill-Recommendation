from src.extractor.extractor_regex import extract_skills

job_text = """
We are looking for a Python Intern.
Knowledge of SQL and Git is required.
Experience with Machine Learning is a plus.
"""

skills = extract_skills(job_text)

print("Skills found:")
for skill in skills:
    print("-", skill)
    
