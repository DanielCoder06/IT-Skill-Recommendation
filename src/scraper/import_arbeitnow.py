from src.pipeline.load_jobs_to_db import save_jobs_to_db
from src.scraper.arbeitnow_scraper import ArbeitnowScraper


def main() -> None:
    scraper = ArbeitnowScraper()

    jobs = scraper.scrape()

    print("Scraped jobs:", len(jobs))

    save_jobs_to_db(jobs)


if __name__ == "__main__":
    main()