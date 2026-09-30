from dataclasses import replace
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

from src.models.raw_job import RawJob
from src.scraper.base_scraper import BaseScraper

class ITviecScraper(BaseScraper):
    def scrape(
        self,
        url: str,
    ) -> list[RawJob]:
        html = self._load_html(url)

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        unique_jobs: dict[str, RawJob] = {}

        for title_element in soup.select(
            "h3.job-title"
        ):
            job_link = title_element.find("a")

            if job_link is None:
                continue

            title = job_link.get_text(
                " ",
                strip=True,
            )

            job_url = self._clean_url(
                job_link.get("href", "")
            )

            if not job_url:
                continue

            # Bỏ job trùng URL
            if job_url in unique_jobs:
                continue

            card = title_element.find_parent(
                "div",
                class_="ipx-4",
            )

            if card is None:
                continue

            location_element = card.select_one(
                "p.text-dark-grey.small-text.text-start"
            )

            company_element = card.select_one(
                "div.d-flex.align-items-center."
                "justify-content-between "
                "a.text-rich-grey.text-clamp-2"
            )

            tag_elements = card.select(
                "a[data-responsive-tag-list-target='tag']"
            )

            location = (
                location_element.get_text(
                    " ",
                    strip=True,
                )
                if location_element
                else None
            )

            company = (
                company_element.get_text(
                    " ",
                    strip=True,
                )
                if company_element
                else None
            )

            tags = [
                tag.get_text(
                    " ",
                    strip=True,
                )
                for tag in tag_elements
            ]

            raw_job = RawJob(
                source="itviec",
                external_id=self._extract_external_id(
                    job_url
                ),
                title=title,
                company=company,
                location=location,
                description="",
                job_url=job_url,
                tags=tags,
                remote=None,
                raw_data={
                    "tags": tags,
                },
            )

            unique_jobs[job_url] = raw_job

        return list(unique_jobs.values())

    @staticmethod
    def _fetch_detail_html(url: str) -> str:
        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

        return response.text

    @staticmethod
    def _extract_detail_description(
        html: str,
    ) -> str:
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        sections = []

        for heading_text in [
            "Mô tả công việc",
            "Yêu cầu công việc",
        ]:
            heading = soup.find(
                "h2",
                string=lambda text: (
                    text
                    and text.strip()
                    == heading_text
                ),
            )

            if heading is None:
                continue

            parent = heading.parent

            text = parent.get_text(
                "\n",
                strip=True,
            )

            if text:
                sections.append(text)

        return "\n\n".join(sections)

    @classmethod
    def enrich_job_detail(
        cls,
        job: RawJob,
    ) -> RawJob:
        html = cls._fetch_detail_html(
            job.job_url
        )

        description = cls._extract_detail_description(
            html
        )

        return replace(
            job,
            description=description,
        )

    @staticmethod
    def _load_html(path: str) -> str:
        return Path(path).read_text(
            encoding="utf-8",
            errors="ignore",
        )

    @staticmethod
    def _clean_url(url: str) -> str:
        parts = urlsplit(url)

        return urlunsplit(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                "",
                "",
            )
        )

    @staticmethod
    def _extract_external_id(
        url: str,
    ) -> str | None:
        if not url:
            return None

        slug = url.rstrip("/").split("/")[-1]

        if "-" not in slug:
            return slug

        return slug.rsplit("-", 1)[-1]
