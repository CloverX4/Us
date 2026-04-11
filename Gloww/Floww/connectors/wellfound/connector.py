"""
connectors/wellfound/connector.py
──────────────────────────────────
Wellfound (formerly AngelList Talent) job search connector.

Wellfound is more scraper-friendly than LinkedIn.
URL pattern: https://wellfound.com/jobs?role=product-manager&location=india

Note: Wellfound's job listings are mostly startup roles — exactly the kind
Indira wants (ownership, experimentation culture, early-stage product work).
"""

import asyncio
from urllib.parse import urlencode, quote
from playwright.async_api import TimeoutError as PlaywrightTimeout
from connectors.base import BaseConnector, RawJob
from config.settings import settings
from rich.console import Console

console = Console()

# Wellfound role slugs — their URL uses these exact strings
ROLE_SLUGS = {
    "Product Manager": "product-manager",
    "APM": "product-manager",
    "Senior Product Manager": "product-manager",
    "Senior Software Engineer": "software-engineer",
    "SDE": "software-engineer",
    "Backend Engineer": "backend-engineer",
    "Full Stack Engineer": "full-stack-engineer",
    "Data Engineer": "data-engineer",
}


class WellfoundConnector(BaseConnector):

    PLATFORM_NAME = "wellfound"

    async def _do_login(self, email: str, password: str) -> bool:
        try:
            await self._page.goto("https://wellfound.com/login", wait_until="domcontentloaded")
            await self._random_delay(1, 2)

            # Click "Continue with email" if present
            email_btn = await self._page.query_selector('[data-test="EmailLoginButton"]')
            if email_btn:
                await email_btn.click()
                await self._random_delay(0.5, 1)

            await self._page.fill('[name="email"], input[type="email"]', email)
            await self._random_delay(0.5, 1)
            await self._page.fill('[name="password"], input[type="password"]', password)
            await self._random_delay(0.5, 1)
            await self._page.press('input[type="password"]', "Enter")
            await self._page.wait_for_load_state("networkidle", timeout=12000)

            return await self._verify_logged_in()

        except Exception as e:
            console.print(f"[red]Wellfound login error: {e}[/red]")
            return False

    async def _verify_logged_in(self) -> bool:
        try:
            await self._page.goto("https://wellfound.com/jobs", wait_until="domcontentloaded", timeout=8000)
            # If we see the job listings, we're in
            return "login" not in self._page.url
        except Exception:
            return False

    async def _do_search(self, role: str, location: str, max_results: int) -> list[RawJob]:
        """Search Wellfound for jobs."""
        jobs = []
        role_slug = ROLE_SLUGS.get(role, role.lower().replace(" ", "-"))

        # Wellfound location values
        location_param = "india" if "hyderabad" in location.lower() or "india" in location.lower() else location.lower()

        params = {
            "role": role_slug,
            "location": location_param,
        }
        search_url = f"https://wellfound.com/jobs?{urlencode(params)}"

        try:
            await self._page.goto(search_url, wait_until="domcontentloaded", timeout=15000)
            await self._random_delay(2, 3)

            # Scroll to load more jobs (Wellfound lazy-loads)
            loaded = 0
            while loaded < max_results:
                await self._scroll_to_bottom(steps=4)
                await self._random_delay(1.5, 2.5)

                page_jobs = await self._extract_job_cards()
                if len(page_jobs) <= loaded:
                    break  # no new jobs loaded
                loaded = len(page_jobs)

                # Click "Load more" button if present
                load_more = await self._page.query_selector('[data-test="LoadMore"], button:has-text("Load more")')
                if load_more:
                    await load_more.click()
                    await self._random_delay(2, 3)
                else:
                    break

            jobs = await self._extract_job_cards()

        except PlaywrightTimeout:
            console.print("[yellow]Wellfound search timed out[/yellow]")

        return jobs[:max_results]

    async def _extract_job_cards(self) -> list[RawJob]:
        """Extract all job cards from the current Wellfound page."""
        jobs = []

        # Wellfound job card selectors (these can change — check if broken)
        cards = await self._page.query_selector_all(
            '[data-test="JobListing"], .styles_component__Ey28k, [class*="JobListing"]'
        )

        # Fallback: try anchor tags that look like job links
        if not cards:
            cards = await self._page.query_selector_all('a[href*="/jobs/"]')

        for card in cards:
            try:
                job = await self._parse_wellfound_card(card)
                if job:
                    jobs.append(job)
            except Exception:
                continue

        return jobs

    async def _parse_wellfound_card(self, card) -> RawJob | None:
        """Parse a single Wellfound job card."""
        # Job title
        title_el = await card.query_selector(
            '[data-test="JobTitle"], h2, h3, [class*="title"], [class*="Title"]'
        )
        title = (await title_el.inner_text()).strip() if title_el else ""

        # Company
        company_el = await card.query_selector(
            '[data-test="StartupName"], [class*="company"], [class*="Company"], [class*="startup"]'
        )
        company = (await company_el.inner_text()).strip() if company_el else ""

        # Location
        location_el = await card.query_selector('[data-test="JobLocation"], [class*="location"]')
        location = (await location_el.inner_text()).strip() if location_el else ""

        # URL
        href = await card.get_attribute("href")
        if not href:
            link_el = await card.query_selector("a")
            href = await link_el.get_attribute("href") if link_el else None

        if not href or not title:
            return None

        job_url = f"https://wellfound.com{href}" if href.startswith("/") else href

        # Compensation (Wellfound often shows this in listings)
        comp_el = await card.query_selector('[data-test="JobCompensation"], [class*="compensation"]')
        salary = (await comp_el.inner_text()).strip() if comp_el else ""

        return RawJob(
            title=title,
            company=company,
            location=location,
            job_url=job_url,
            platform="wellfound",
            salary_range=salary
        )

    async def _do_get_detail(self, job_url: str) -> str:
        """Fetch full JD from Wellfound job detail page."""
        try:
            await self._page.goto(job_url, wait_until="domcontentloaded", timeout=12000)
            await self._random_delay(1, 2)

            desc_selectors = [
                '[data-test="JobDescription"]',
                '[class*="JobDescription"]',
                '[class*="description"]',
                "section.prose",
            ]

            for selector in desc_selectors:
                el = await self._page.query_selector(selector)
                if el:
                    return (await el.inner_text()).strip()

            return ""

        except Exception as e:
            console.print(f"[dim]Wellfound detail fetch failed: {e}[/dim]")
            return ""


async def search_wellfound_jobs(role: str, location: str = "India", max_results: int = 30) -> list[RawJob]:
    """Standalone async helper to search Wellfound."""
    async with WellfoundConnector() as connector:
        if settings.wellfound_email and settings.wellfound_password:
            await connector.login(settings.wellfound_email, settings.wellfound_password)
        return await connector.search_jobs(role, location, max_results)
