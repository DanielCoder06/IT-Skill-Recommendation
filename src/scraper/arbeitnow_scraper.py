import requests

from src.scraper.base_scraper import BaseScraper
from src.scraper.job_schema import JobRecord
from src.scraper.text_cleaner import clean_job_description


ARBEITNOW_API_URL = "https://www.arbeitnow.com/api/job-board-api"


class ArbeitnowScraper(BaseScraper):

    def scrape(self, url: str = ARBEITNOW_API_URL) -> list[JobRecord]:
        response = requests.get(
            url,
            timeout=20,
        )
        response.raise_for_status()

        data = response.json()

        jobs = []

        for job in data["data"]:
            job_record = JobRecord(
                title=job["title"],
                company=job["company_name"],
                description=clean_job_description(job["description"]),
                location=job["location"],
                url=job["url"],
                experience="",
            )

            jobs.append(job_record)

        return jobs