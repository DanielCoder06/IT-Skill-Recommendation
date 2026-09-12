import sqlite3


connection = sqlite3.connect("data/it_jobs.db")

cursor = connection.cursor()

cursor.execute("""
    SELECT
        jobs.title,
        skills.name,
        job_skills.source
    FROM job_skills
    JOIN jobs
        ON jobs.id = job_skills.job_id
    JOIN skills
        ON skills.id = job_skills.skill_id;
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()