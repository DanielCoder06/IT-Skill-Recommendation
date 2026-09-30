from abc import ABC, abstractmethod

from src.models.raw_job import RawJob


class BaseScraper(ABC):

    @abstractmethod
    def scrape(self, url: str) -> list[RawJob]:
        """Scrape raw jobs from a source."""
        raise NotImplementedError