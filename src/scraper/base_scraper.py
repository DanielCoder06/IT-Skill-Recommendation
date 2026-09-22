from abc import ABC, abstractmethod

from src.scraper.job_schema import JobRecord


class BaseScraper(ABC):

    @abstractmethod
    def scrape(self, url: str) -> list[JobRecord]:
        """Scrape jobs from a source URL."""
        raise NotImplementedError