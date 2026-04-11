"""
connectors/ycombinator/connector.py
─────────────────────────────────────
YCombinator Work at a Startup connector.

workatastartup.com is the most scraper-friendly of all platforms:
  - No login required to browse
  - Clean HTML structure
  - Explicitly startup/product-focused roles
  - Good for finding APM and PM roles at early-stage companies

URL: https://www.workatastartup.com/jobs?role=product&remote=true&location=India
"""

import asyncio
from urllib.parse import urlencode
from playwright.async_api import TimeoutError as PlaywrightTimeout
from connectors.base import BaseConnector, RawJob
from rich.console import Console

console = Console()

# YC role filter values
YC_ROLE_MAP = {
    "Product Manager": "product",
    "APM": "product",
    "Senior Product Manager": "product",
    "Senior Software Engineer": "eng",
    "SDE": "eng",
    "Data Engineer": "data",
    "Designer": "design",
}


class YCombinatorConnector(BaseConnector):
    """
    Connector for YC's Work at a Startup board.
    No login needed — just scrape and go.
    """

    PLATFORM_NAME = "ycombinator"

    async def _do_login(self, email: str, password: str) -> bool:
        return True  # No login required

    async def _verify_logged_in(self) -> bool:
        return True  # Always "logged in"

    async def _do_search(self, role: str, location: str, max_results: int) -> list[RawJob]:
        """Search YC's job board."""
        jobs = []
        yc_role = YC_ROLE_MAP.get(role, "product")

        # Build search URL — YC allows remote + India filter
        params = {
            "role": yc_role,
            "remote": "true",  # most YC startups hire remotely from India
        }

        # Add India/location filter if available
        if "india" in location.lower() or "hyderabad" in location.lower():
            params["location"] = "India"

        search_url = f"https://www.workatastartup.com/jobs?{urlencode(params)}"

        try:
            await self._page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
            await self._random_delay(2, 3)

            # YC loads more on scroll
            last_count = 0
            for _ in range(5):  # max 5 scroll rounds
                await self._scroll_to_bottom(steps=4)
                await self._random_delay(1.5, 2.5)

                current_jobs = await self._extract_job_cards()
                if len(current_jobs) >= max_results or len(current_jobs) == last_count:
                    break
                last_count = len(current_jobs)

            jobs = await self._extract_job_cards()

        except PlaywrightTimeout:
            console.print("[yellow]YC search timed out[/yellow]")
        except Exception as e:
            console.print(f"[red]YC search error: {e}[/red]")

        return jobs[:max_results]

    async def _extract_job_cards(self) -> list[RawJob]:
        """Extract job cards from YC job board."""
        jobs = []

        # YC uses relatively stable class names
        cards = await self._page.query_selector_all(
            ".job-name, .jobs-list .job, [class*='JobCard'], a[href*='/jobs/']"
        )

        # Fallback: look for job listing containers
        if not cards:
            cards = await self._page.query_selector_all("div.border.rounded")

        for card in cards:
            try:
                job = await self._parse_yc_card(card)
                if job:
                    jobs.append(job)
            except Exception:
                continue

        return jobs

    async def _parse_yc_card(self, card) -> RawJob | None:
        """Parse a YC job card."""
        # Title
        title_el = await card.query_selector("h3, h2, .font-bold, [class*='title']")
        title = (await title_el.inner_text()).strip() if title_el else ""

        # Company name
        company_el = await card.query_selector(".company-name, [class*='company'], [class*='startup']")
        company = (await company_el.inner_text()).strip() if company_el else ""

        # Get URL
        href = await card.get_attribute("href")
        if not href:
            link = await card.query_selector("a")
            href = await link.get_attribute("href") if link else None

        if not href or not title:
            return None

        job_url = f"https://www.workatastartup.com{href}" if href.startswith("/") else href

        # Location / remote status
        location_el = await card.query_selector("[class*='location'], [class*='remote']")
        location = (await location_el.inner_text()).strip() if location_el else "Remote"

        # YC batch info (useful context — e.g. "W24" tells you how recent the company is)
        batch_el = await card.query_selector("[class*='batch'], [class*='Batch']")
        batch = (await batch_el.inner_text()).strip() if batch_el else ""

        return RawJob(
            title=title,
            company=company,
            location=location,
            job_url=job_url,
            platform="ycombinator",
            extra={"yc_batch": batch}
        )

    async def _do_get_detail(self, job_url: str) -> str:
        """Fetch JD from YC job detail page."""
        try:
            await self._page.goto(job_url, wait_until="domcontentloaded", timeout=12000)
            await self._random_delay(1, 2)

            # YC job pages have a clear description section
            desc_selectors = [
                ".prose",
                "[class*='description']",
                ".job-description",
                "article",
            ]

            for selector in desc_selectors:
                el = await self._page.query_selector(selector)
                if el:
                    return (await el.inner_text()).strip()

            # Fallback: page body minus nav
            return await self._page.inner_text("main") or ""

        except Exception as e:
            console.print(f"[dim]YC detail fetch failed: {e}[/dim]")
            return ""


async def search_yc_jobs(role: str, location: str = "India", max_results: int = 30) -> list[RawJob]:
    """Standalone async helper to search YC jobs — no login needed."""
    async with YCombinatorConnector() as connector:
        return await connector.search_jobs(role, location, max_results)
