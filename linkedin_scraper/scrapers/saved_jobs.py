"""
Saved jobs scraper for LinkedIn.

Extracts saved job posting URLs from the user's Saved Jobs page.
"""

import logging
from typing import Optional

from playwright.async_api import Page

from ..callbacks import ProgressCallback, SilentCallback
from ..core.exceptions import ScrapingError
from .base import BaseScraper

logger = logging.getLogger(__name__)


class SavedJobsScraper(BaseScraper):
    """Scraper for LinkedIn Saved Jobs list."""

    def __init__(self, page: Page, callback: Optional[ProgressCallback] = None):
        """
        Initialize saved jobs scraper.

        Args:
            page: Playwright page object
            callback: Optional progress callback
        """
        super().__init__(page, callback or SilentCallback())

    async def scrape(
        self,
        limit: int = 50,
        max_scrolls: int = 5,
        pause_time: float = 1.0,
    ) -> list[str]:
        """
        Scrape saved job posting URLs.

        Args:
            limit: Maximum number of job URLs to return
            max_scrolls: Maximum scroll attempts to load more jobs
            pause_time: Pause between scrolls (seconds)

        Returns:
            List of saved job URLs

        Raises:
            AuthenticationError: If not logged in
            ScrapingError: If scraping fails
        """
        saved_jobs_url = "https://www.linkedin.com/my-items/saved-jobs/"
        logger.info("Starting saved jobs scraping")
        await self.callback.on_start("SavedJobs", saved_jobs_url)

        if limit <= 0:
            return []

        try:
            await self.navigate_and_wait(saved_jobs_url)
            await self.callback.on_progress("Navigated to saved jobs", 10)
            await self.ensure_logged_in()

            await self.page.wait_for_selector("main", timeout=10000)
            await self.wait_and_focus(1)

            await self.close_modals()
            await self.scroll_page_to_bottom(
                pause_time=pause_time, max_scrolls=max_scrolls
            )

            job_urls = await self._extract_job_urls(limit)
            await self.callback.on_progress(f"Found {len(job_urls)} saved jobs", 90)
            await self.callback.on_complete("SavedJobs", job_urls)

            logger.info("Saved jobs scraping complete: %s jobs", len(job_urls))
            return job_urls

        except Exception as e:
            await self.callback.on_error(e)
            raise ScrapingError(f"Failed to scrape saved jobs: {e}")

    async def _extract_job_urls(self, limit: int) -> list[str]:
        """
        Extract job URLs from the saved jobs page.

        Args:
            limit: Maximum number of URLs to extract

        Returns:
            List of job posting URLs
        """
        job_urls: list[str] = []
        seen_urls: set[str] = set()

        try:
            job_links = await self.page.locator('a[href*="/jobs/view/"]').all()

            for link in job_links:
                if len(job_urls) >= limit:
                    break

                try:
                    href = await link.get_attribute("href")
                    if not href or "/jobs/view/" not in href:
                        continue

                    clean_url = href.split("?")[0] if "?" in href else href
                    if not clean_url.startswith("http"):
                        clean_url = f"https://www.linkedin.com{clean_url}"

                    if clean_url not in seen_urls:
                        job_urls.append(clean_url)
                        seen_urls.add(clean_url)
                except Exception as e:
                    logger.debug("Error extracting saved job URL: %s", e)
                    continue

        except Exception as e:
            logger.warning("Error extracting saved job URLs: %s", e)

        return job_urls
