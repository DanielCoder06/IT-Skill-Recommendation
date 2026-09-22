import json


def load_jobs():
    with open(
        "data/raw_jobs.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)