from pathlib import Path
import sys
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from src.scraper.itviec_scraper import ITviecScraper


BASE_DIR = Path(__file__).resolve().parents[1]

HTML_PATH = (
    BASE_DIR
    / "data"
    / "external"
    / "itviec"
    / "Việc làm AI, Data.html"
)


def main() -> None:
    scraper = ITviecScraper()

    jobs = scraper.scrape(
        str(HTML_PATH)
    )

    urls = [
        job.job_url
        for job in jobs
    ]

    duplicate_urls = [
        url
        for url, count in Counter(urls).items()
        if count > 1
    ]

    empty_titles = [
        job
        for job in jobs
        if not job.title
    ]

    empty_companies = [
        job
        for job in jobs
        if not job.company
    ]

    empty_locations = [
        job
        for job in jobs
        if not job.location
    ]

    print("=== ITVIEC DATA QUALITY ===")
    print("TOTAL:", len(jobs))
    print("UNIQUE URL:", len(set(urls)))
    print("DUPLICATE URL:", len(duplicate_urls))
    print("EMPTY TITLE:", len(empty_titles))
    print("EMPTY COMPANY:", len(empty_companies))
    print("EMPTY LOCATION:", len(empty_locations))
    print("WITH TAGS:", sum(1 for job in jobs if job.tags))

    if duplicate_urls:
        print("\n=== DUPLICATE URLS ===")
        for url in duplicate_urls:
            print(url)


if __name__ == "__main__":
    main()