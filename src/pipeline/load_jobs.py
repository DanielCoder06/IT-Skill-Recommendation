import json

def load_jobs():
    with open("data/raw_jobs.json", "r", encoding="utf-8") as file:
        jobs = json.load(file)
    return jobs

jobs = load_jobs()

print(jobs)