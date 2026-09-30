from src.pipeline.load_jobs_to_db import save_jobs_to_db
from src.scraper.arbeitnow_scraper import ArbeitnowScraper
from src.scraper.job_adapter import raw_jobs_to_job_records


def main() -> None:
    scraper = ArbeitnowScraper()

    raw_jobs = scraper.scrape()

    print("Scraped raw jobs:", len(raw_jobs))

    jobs = raw_jobs_to_job_records(raw_jobs)

    print("Converted jobs:", len(jobs))

    save_jobs_to_db(jobs)


if __name__ == "__main__":
    main()