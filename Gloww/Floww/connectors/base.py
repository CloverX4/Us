"""
connectors/base.py
──────────────────
BaseConnector — abstract class all platform connectors inherit from.

Every connector does the same three things:
  1. login()       → authenticate, save cookies so we don't re-login next time
  2. search_jobs() → return a list of raw job dicts
  3. get_job_detail() → fetch full JD for a specific job URL

The BaseConnector handles:
  - Playwright browser setup (one shared browser instance)
  - Cookie persistence (saves to data/sessions/<platform>.json)
  - Rate limiting helpers (random delays, so we don't get banned)
  - Common error handling

Each platform subclass only needs to implement:
  - _do_login()
  - _do_search()
  - _do_get_detail()
"""

import json
import random
import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass, field
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from rich.console import Console
from config.settings import settings

console = Console()


@dataclass
class RawJob:
    """
    Raw job data as scraped from a platform.
    Gets converted to a core.models.Job after deduplication + scoring.
    """
    title: str
    company: str
    job_url: str
    platform: str
    location: str = ""
    description: str = ""
    salary_range: str = ""
    posted_date: str = ""
    extra: dict = field(default_factory=dict)  # platform-specific extras


class BaseConnector(ABC):
    """
    Base class for all job platform connectors.

    Usage (in subclass):
        connector = LinkedInConnector()
        async with connector:
            jobs = await connector.search_jobs("Product Manager", "Hyderabad")
    """

    PLATFORM_NAME: str = "base"  # override in subclass

    def __init__(self):
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None
        self._sessions_dir = Path(settings.project_root) / "data" / "sessions"
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        self._cookies_file = self._sessions_dir / f"{self.PLATFORM_NAME}.json"

    # ─── Context manager — use `async with connector:` ────────────────────

    async def __aenter__(self):
        await self._start_browser()
        return self

    async def __aexit__(self, *args):
        await self._close_browser()

    # ─── Public interface ─────────────────────────────────────────────────

    async def login(self, email: str, password: str) -> bool:
        """
        Log in to the platform. Saves cookies so we don't re-login next run.
        Returns True if login succeeded.
        """
        # Try loading saved cookies first
        if await self._load_cookies():
            console.print(f"[dim]{self.PLATFORM_NAME}: using saved session[/dim]")
            if await self._verify_logged_in():
                return True
            console.print(f"[dim]{self.PLATFORM_NAME}: session expired, re-logging in[/dim]")

        # Fresh login
        console.print(f"[cyan]{self.PLATFORM_NAME}:[/cyan] logging in as {email}...")
        success = await self._do_login(email, password)

        if success:
            await self._save_cookies()
            console.print(f"[green]{self.PLATFORM_NAME}: logged in ✓[/green]")

        return success

    async def search_jobs(self, role: str, location: str = "Hyderabad", max_results: int = 50) -> list[RawJob]:
        """
        Search for jobs on this platform.

        Args:
            role: Job title to search for (e.g. "Product Manager")
            location: Location filter
            max_results: Max jobs to return

        Returns:
            List of RawJob objects
        """
        console.print(f"[cyan]{self.PLATFORM_NAME}:[/cyan] searching '{role}' in {location}...")
        jobs = await self._do_search(role, location, max_results)
        console.print(f"[green]{self.PLATFORM_NAME}:[/green] found {len(jobs)} jobs")
        return jobs

    async def get_job_detail(self, job_url: str) -> str:
        """Fetch the full job description from a job's detail page."""
        await self._random_delay(1.5, 3.0)  # be polite
        return await self._do_get_detail(job_url)

    # ─── Abstract methods — implement in each platform subclass ──────────

    @abstractmethod
    async def _do_login(self, email: str, password: str) -> bool:
        """Platform-specific login logic."""
        pass

    @abstractmethod
    async def _do_search(self, role: str, location: str, max_results: int) -> list[RawJob]:
        """Platform-specific job search logic."""
        pass

    @abstractmethod
    async def _do_get_detail(self, job_url: str) -> str:
        """Platform-specific detail page scraping."""
        pass

    @abstractmethod
    async def _verify_logged_in(self) -> bool:
        """Check if the saved session is still valid."""
        pass

    # ─── Shared helpers ───────────────────────────────────────────────────

    async def _start_browser(self):
        """Launch a headless Chromium browser."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=True,  # set False to watch it work (good for debugging)
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        self._context = await self._browser.new_context(
            # Pretend to be a real Chrome browser
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        # Block images and fonts — speeds up scraping significantly
        await self._context.route(
            "**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf}",
            lambda route: route.abort()
        )
        self._page = await self._context.new_page()

    async def _close_browser(self):
        if self._browser:
            await self._browser.close()
        if hasattr(self, "_playwright"):
            await self._playwright.stop()

    async def _save_cookies(self):
        """Save current browser cookies to file for next session."""
        cookies = await self._context.cookies()
        with open(self._cookies_file, "w") as f:
            json.dump(cookies, f)

    async def _load_cookies(self) -> bool:
        """Load saved cookies into the browser context. Returns True if file exists."""
        if not self._cookies_file.exists():
            return False
        with open(self._cookies_file) as f:
            cookies = json.load(f)
        await self._context.add_cookies(cookies)
        return True

    async def _random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Wait a random amount between actions — mimics human behavior."""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)

    async def _scroll_to_bottom(self, page: Page | None = None, steps: int = 5):
        """Scroll down a page incrementally to trigger lazy loading."""
        p = page or self._page
        for _ in range(steps):
            await p.evaluate("window.scrollBy(0, window.innerHeight * 0.8)")
            await self._random_delay(0.5, 1.2)
