"""
connectors/linkedin/connector.py
──────────────────────────────────
LinkedIn job search connector.

⚠️  Important notes about LinkedIn automation:
  - LinkedIn actively detects automation and will temporarily block accounts
  - We use realistic delays, proper user agents, and cookie persistence to minimize this
  - Never run this too aggressively — 50 jobs max per session, with delays
  - If you get a CAPTCHA or "unusual activity" block, wait 30 min before retrying

How LinkedIn job search works (the URL we use):
  https://www.linkedin.com/jobs/search/?keywords=Product+Manager
    &location=Hyderabad
    &f_E=3,4          ← experience level: 3=Associate, 4=Mid-Senior
    &f_TP=1,2,3,4     ← date posted: 1=24h, 2=week, 3=month
    &sortBy=DD        ← sort by date
"""

import asyncio
from urllib.parse import urlencode
from playwright.async_api import TimeoutError as PlaywrightTimeout
from connectors.base import BaseConnector, RawJob
from config.settings import settings
from rich.console import Console

console = Console()

# LinkedIn experience level filter codes
EXPERIENCE_LEVELS = {
    "internship": "1",
    "entry": "2",
    "associate": "3",
    "mid_senior": "4",
    "director": "5",
    "executive": "6"
}


class LinkedInConnector(BaseConnector):

    PLATFORM_NAME = "linkedin"

    async def _do_login(self, email: str, password: str) -> bool:
        try:
            await self._page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            await self._random_delay(1, 2)

            # Fill email
            await self._page.fill("#username", email)
            await self._random_delay(0.5, 1.2)

            # Fill password
            await self._page.fill("#password", password)
            await self._random_delay(0.5, 1.0)

            # Click sign in
            await self._page.click('[data-litms-control-urn="login-submit"]')
            await self._page.wait_for_load_state("networkidle", timeout=15000)

            return await self._verify_logged_in()

        except PlaywrightTimeout:
            console.print("[red]LinkedIn login timed out[/red]")
            return False
        except Exception as e:
            console.print(f"[red]LinkedIn login error: {e}[/red]")
            return False

    async def _verify_logged_in(self) -> bool:
        """Check if we're on a logged-in page."""
        try:
            await self._page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=10000)
            # If we're redirected to login, we're not logged in
            return "feed" in self._page.url or "mynetwork" in self._page.url
        except Exception:
            return False

    async def _do_search(self, role: str, location: str, max_results: int) -> list[RawJob]:
        """Search LinkedIn jobs and return raw job list."""
        jobs = []
        page_num = 0
        results_per_page = 25  # LinkedIn shows 25 per page

        while len(jobs) < max_results:
            url = self._build_search_url(role, location, offset=page_num * results_per_page)

            try:
                await self._page.goto(url, wait_until="domcontentloaded", timeout=15000)
                await self._random_delay(2, 4)

                # Scroll to load all cards on this page
                await self._scroll_to_bottom(steps=3)
                await self._random_delay(1, 2)

                # Extract job cards
                page_jobs = await self._extract_job_cards()

                if not page_jobs:
                    break  # no more results

                jobs.extend(page_jobs)
                console.print(f"  [dim]LinkedIn page {page_num + 1}: {len(page_jobs)} jobs[/dim]")

                page_num += 1
                await self._random_delay(2, 5)  # delay between pages

            except PlaywrightTimeout:
                console.print("[yellow]LinkedIn search page timed out — stopping[/yellow]")
                break

        return jobs[:max_results]

    def _build_search_url(self, role: str, location: str, offset: int = 0) -> str:
        """Build a LinkedIn job search URL with filters."""
        params = {
            "keywords": role,
            "location": location,
            "f_E": "3,4",      # Associate + Mid-Senior level
            "f_TP": "1,2,3",   # Posted in last month (1=24h, 2=week, 3=month)
            "sortBy": "DD",     # Sort by date (newest first)
            "start": offset,
        }
        return f"https://www.linkedin.com/jobs/search/?{urlencode(params)}"

    async def _extract_job_cards(self) -> list[RawJob]:
        """Extract job listings from the current search results page."""
        jobs = []

        # LinkedIn job cards are in a list — selector may change, so we try multiple
        card_selectors = [
            ".job-card-container",
            ".jobs-search-results__list-item",
            "[data-job-id]",
        ]

        cards = []
        for selector in card_selectors:
            cards = await self._page.query_selector_all(selector)
            if cards:
                break

        for card in cards:
            try:
                job = await self._parse_job_card(card)
                if job:
                    jobs.append(job)
            except Exception as e:
                console.print(f"  [dim]Skipping card: {e}[/dim]")
                continue

        return jobs

    async def _parse_job_card(self, card) -> RawJob | None:
        """Extract data from a single job card element."""
        # Title
        title_el = await card.query_selector(".job-card-list__title, .job-card-container__link")
        title = await title_el.inner_text() if title_el else ""
        title = title.strip()

        if not title:
            return None

        # Company
        company_el = await card.query_selector(".job-card-container__company-name, .artdeco-entity-lockup__subtitle")
        company = await company_el.inner_text() if company_el else ""
        company = company.strip()

        # Location
        location_el = await card.query_selector(".job-card-container__metadata-wrapper, .job-card-container__metadata-item")
        location = await location_el.inner_text() if location_el else ""
        location = location.strip()

        # Job URL
        link_el = await card.query_selector("a.job-card-list__title, a.job-card-container__link")
        job_url = ""
        if link_el:
            href = await link_el.get_attribute("href")
            if href:
                # Clean LinkedIn tracking params — keep just the job ID part
                base_url = href.split("?")[0]
                job_url = f"https://www.linkedin.com{base_url}" if base_url.startswith("/") else base_url

        if not job_url:
            return None

        # Job ID from data attribute
        job_id_attr = await card.get_attribute("data-job-id") or ""

        return RawJob(
            title=title,
            company=company,
            location=location,
            job_url=job_url,
            platform="linkedin",
            extra={"linkedin_job_id": job_id_attr}
        )

    async def _do_get_detail(self, job_url: str) -> str:
        """Fetch full job description from the job's detail page."""
        try:
            await self._page.goto(job_url, wait_until="domcontentloaded", timeout=12000)
            await self._random_delay(1.5, 3)

            # Try to click "See more" to expand the description
            see_more = await self._page.query_selector(
                ".jobs-description__footer-button, button[aria-label*='more']"
            )
            if see_more:
                await see_more.click()
                await self._random_delay(0.5, 1)

            # Extract description
            desc_selectors = [
                ".jobs-description-content__text",
                ".jobs-box__html-content",
                "#job-details",
                ".description__text"
            ]

            for selector in desc_selectors:
                desc_el = await self._page.query_selector(selector)
                if desc_el:
                    return (await desc_el.inner_text()).strip()

            # Fallback: get all text from the page body
            return await self._page.inner_text("body")

        except PlaywrightTimeout:
            return ""
        except Exception as e:
            console.print(f"[dim]Could not fetch detail for {job_url}: {e}[/dim]")
            return ""


# ─── Helper to run the connector from sync code ───────────────────────────────

async def search_linkedin_jobs(role: str, location: str = "Hyderabad", max_results: int = 30) -> list[RawJob]:
    """Standalone async function to search LinkedIn jobs."""
    async with LinkedInConnector() as connector:
        logged_in = await connector.login(
            email=settings.linkedin_email,
            password=settings.linkedin_password
        )
        if not logged_in:
            console.print("[red]LinkedIn login failed — check credentials in .env[/red]")
            return []

        return await connector.search_jobs(role, location, max_results)
