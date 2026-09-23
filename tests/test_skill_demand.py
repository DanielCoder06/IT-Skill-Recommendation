from src.analytics.skill_demand import get_target_internship_jobs
from src.scraper.job_filter import is_it_job
from src.scraper.job_classifier import classify_job_level
from src.analytics.skill_demand import get_skill_demand
from src.analytics.skill_demand import get_skill_demand_percentage
from src.analytics.skill_demand import (
    get_analyzed_target_internship_jobs,
    get_skill_extraction_coverage,
)

def test_target_jobs_are_it_internships():
    jobs = get_target_internship_jobs()

    assert jobs

    for job in jobs:
        assert is_it_job(job)
        assert classify_job_level(job) == "internship"

def test_target_jobs_are_it_and_internship():
    jobs = get_target_internship_jobs()

    assert jobs

    for job in jobs:
        assert is_it_job(job)
        assert classify_job_level(job) == "internship"

def test_skill_demand_returns_sorted_results():
    demand = get_skill_demand()

    assert demand

    counts = [count for _, count in demand]

    assert counts == sorted(counts, reverse=True) 
    
def test_skill_demand_percentage():
    demand = get_skill_demand_percentage()

    assert demand

    for skill, percentage in demand:
        assert isinstance(skill, str)
        assert 0 < percentage <= 100
        
from src.analytics.skill_demand import (
    get_analyzed_target_internship_jobs,
    get_skill_extraction_coverage,
)

def test_analyzed_target_jobs_have_skills():
    jobs = get_analyzed_target_internship_jobs()

    assert jobs

    for job in jobs:
        assert job.url


def test_skill_extraction_coverage():
    total, analyzed, coverage = get_skill_extraction_coverage()

    assert total == 12
    assert analyzed == 10
    assert coverage == 83.3