"""
agents/job_discovery_agent.py
──────────────────────────────
The Job Discovery Agent.

This is the "eyes" of the system — it finds the jobs.

What it does in one run:
  1. Gets target roles from profile (PM + Senior SDE)
  2. Calls each connector to fetch raw job listings
  3. Fetches the full JD for each promising-looking job
  4. Scores each job for relevance (0-1) based on Indira's profile
  5. Saves qualifying jobs to the database (skipping duplicates)
  6. Returns a summary: how many found, top picks, anything notable

Why an agent for this instead of just calling connectors directly?
  The LLM decides WHICH jobs to fetch JDs for (not all — some are clearly off)
  and scores relevance with nuance a keyword filter can't do.
  e.g. "VP of Product at a 3-person startup" — technically PM but not right.
"""

import asyncio
import json
from core.models import Job, Platform, RoleType, JobStatus
from core.job_store import save_job, get_job_by_url, get_stats
from core.ats_scorer import score_resume
from core.profile import profile
from agents.base import BaseAgent, Tool
from agents.resume_optimizer_agent import FULL_RESUME_TEXT
from config.settings import settings
from rich.console import Console

console = Console()


class JobDiscoveryAgent(BaseAgent):
    """
    Discovers and scores jobs across platforms.

    Usage:
        agent = JobDiscoveryAgent()
        summary = await agent.run_discovery()
    """

    def __init__(self):
        super().__init__()
        self._register_tools()
        self._discovered_jobs: list[Job] = []

    @property
    def system_prompt(self) -> str:
        return profile.build_system_prompt("job_discovery")

    def _register_tools(self):

        # ── Tool 1: Search a platform ──────────────────────────────────────
        self.register_tool(Tool(
            name="search_platform",
            description=(
                "Search a specific job platform for a role. "
                "Returns a list of jobs with title, company, URL, and location. "
                "Note: descriptions are empty at this stage — use fetch_job_description for those."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["linkedin", "wellfound", "ycombinator"],
                        "description": "Which platform to search"
                    },
                    "role": {
                        "type": "string",
                        "description": "Job title to search for (e.g. 'Product Manager', 'Senior Software Engineer')"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter",
                        "default": "Hyderabad"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Max number of jobs to fetch",
                        "default": 30
                    }
                },
                "required": ["platform", "role"]
            },
            function=self._tool_search_platform
        ))

        # ── Tool 2: Fetch full job description ─────────────────────────────
        self.register_tool(Tool(
            name="fetch_job_description",
            description=(
                "Fetch the full job description for a specific job URL. "
                "Only call this for jobs that look potentially relevant — "
                "it loads a new page for each call so use it selectively."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "platform": {
                        "type": "string",
                        "enum": ["linkedin", "wellfound", "ycombinator"]
                    },
                    "job_url": {
                        "type": "string",
                        "description": "The URL of the job to fetch details for"
                    }
                },
                "required": ["platform", "job_url"]
            },
            function=self._tool_fetch_description
        ))

        # ── Tool 3: Score job relevance ────────────────────────────────────
        self.register_tool(Tool(
            name="score_job_relevance",
            description=(
                "Score how relevant a job is for Indira (0.0 to 1.0). "
                "Takes job title, company description, and JD text. "
                "Returns score + reasoning. Jobs scoring < 0.5 will be skipped."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "job_title": {"type": "string"},
                    "company": {"type": "string"},
                    "description": {"type": "string", "description": "Job description text"},
                    "platform": {"type": "string"}
                },
                "required": ["job_title", "company", "description"]
            },
            function=self._tool_score_relevance
        ))

        # ── Tool 4: Save a job to database ─────────────────────────────────
        self.register_tool(Tool(
            name="save_job",
            description=(
                "Save a relevant job to the database. "
                "Only call this for jobs with relevance_score >= 0.6. "
                "Automatically deduplicates — safe to call for already-saved jobs."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "platform": {
                        "type": "string",
                        "enum": ["linkedin", "wellfound", "ycombinator", "naukri", "instahyre", "other"]
                    },
                    "job_url": {"type": "string"},
                    "description": {"type": "string"},
                    "location": {"type": "string", "default": ""},
                    "salary_range": {"type": "string", "default": ""},
                    "relevance_score": {"type": "number", "description": "0.0 to 1.0"},
                    "role_type": {
                        "type": "string",
                        "enum": ["product_manager", "senior_sde", "apm", "other"],
                        "default": "other"
                    }
                },
                "required": ["title", "company", "platform", "job_url", "description", "relevance_score"]
            },
            function=self._tool_save_job
        ))

        # ── Tool 5: Get current stats ──────────────────────────────────────
        self.register_tool(Tool(
            name="get_pipeline_stats",
            description="Get stats about jobs discovered and applications in progress.",
            input_schema={"type": "object", "properties": {}, "required": []},
            function=self._tool_get_stats
        ))

    # ─── Tool implementations ─────────────────────────────────────────────

    def _tool_search_platform(
        self,
        platform: str,
        role: str,
        location: str = "Hyderabad",
        max_results: int = 30
    ) -> str:
        """Sync wrapper that runs async connector search."""
        return asyncio.get_event_loop().run_until_complete(
            self._async_search_platform(platform, role, location, max_results)
        )

    async def _async_search_platform(self, platform: str, role: str, location: str, max_results: int) -> str:
        """Actual async search logic."""
        from connectors.linkedin.connector import LinkedInConnector
        from connectors.wellfound.connector import WellfoundConnector
        from connectors.ycombinator.connector import YCombinatorConnector

        connector_map = {
            "linkedin": LinkedInConnector,
            "wellfound": WellfoundConnector,
            "ycombinator": YCombinatorConnector,
        }

        ConnectorClass = connector_map.get(platform)
        if not ConnectorClass:
            return f"Unknown platform: {platform}"

        async with ConnectorClass() as connector:
            # Login for platforms that need it
            if platform == "linkedin" and settings.linkedin_email:
                await connector.login(settings.linkedin_email, settings.linkedin_password)
            elif platform == "wellfound" and settings.wellfound_email:
                await connector.login(settings.wellfound_email, settings.wellfound_password)
            # YC doesn't need login

            jobs = await connector.search_jobs(role, location, max_results)

        # Return as JSON so the LLM can read it
        return json.dumps([{
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "url": j.job_url,
            "platform": j.platform,
            "salary_range": j.salary_range
        } for j in jobs], indent=2)

    def _tool_fetch_description(self, platform: str, job_url: str) -> str:
        """Fetch full JD for a job URL."""
        return asyncio.get_event_loop().run_until_complete(
            self._async_fetch_description(platform, job_url)
        )

    async def _async_fetch_description(self, platform: str, job_url: str) -> str:
        from connectors.linkedin.connector import LinkedInConnector
        from connectors.wellfound.connector import WellfoundConnector
        from connectors.ycombinator.connector import YCombinatorConnector

        connector_map = {
            "linkedin": LinkedInConnector,
            "wellfound": WellfoundConnector,
            "ycombinator": YCombinatorConnector,
        }

        ConnectorClass = connector_map.get(platform)
        if not ConnectorClass:
            return ""

        async with ConnectorClass() as connector:
            if platform == "linkedin" and settings.linkedin_email:
                await connector.login(settings.linkedin_email, settings.linkedin_password)
            return await connector.get_job_detail(job_url)

    def _tool_score_relevance(
        self,
        job_title: str,
        company: str,
        description: str,
        platform: str = ""
    ) -> str:
        """
        Scores job relevance. This uses our ATS scorer as a signal,
        but the LLM calling this tool makes the final judgment.
        """
        if not description:
            return json.dumps({"score": 0.3, "reason": "No description available to evaluate"})

        # Use ATS scorer as a quantitative signal
        ats = score_resume(FULL_RESUME_TEXT, description)

        # Also check for PM-specific signals
        description_lower = description.lower()
        pm_signals = ["product manager", "product roadmap", "user research", "product strategy", "a/b test"]
        sde_signals = ["senior engineer", "senior developer", "sde", "backend", "full stack", "data engineer"]

        pm_score = sum(1 for s in pm_signals if s in description_lower) / len(pm_signals)
        sde_score = sum(1 for s in sde_signals if s in description_lower) / len(sde_signals)

        # Experience mismatch check — flag 10+ year requirements
        requires_too_much = any(
            phrase in description_lower
            for phrase in ["10+ years", "10 years", "15 years", "15+ years", "vp of product", "head of product"]
        )

        data = {
            "ats_keyword_match": ats.score,
            "pm_signal": round(pm_score, 2),
            "sde_signal": round(sde_score, 2),
            "experience_mismatch": requires_too_much,
            "missing_keywords": ats.missing_keywords[:8],
            "matched_keywords": ats.matched_keywords[:8],
            "note": "Use these signals + your judgment to set the final relevance score (0.0-1.0)"
        }
        return json.dumps(data, indent=2)

    def _tool_save_job(
        self,
        title: str,
        company: str,
        platform: str,
        job_url: str,
        description: str,
        relevance_score: float,
        location: str = "",
        salary_range: str = "",
        role_type: str = "other"
    ) -> str:
        """Save a job to the database."""
        platform_map = {
            "linkedin": Platform.LINKEDIN,
            "wellfound": Platform.WELLFOUND,
            "ycombinator": Platform.YCOMBINATOR,
            "naukri": Platform.NAUKRI,
            "instahyre": Platform.INSTAHYRE,
            "other": Platform.OTHER,
        }
        role_type_map = {
            "product_manager": RoleType.PM,
            "senior_sde": RoleType.SDE,
            "apm": RoleType.APM,
            "other": RoleType.OTHER,
        }

        job = Job(
            title=title,
            company=company,
            platform=platform_map.get(platform, Platform.OTHER),
            job_url=job_url,
            description=description,
            location=location,
            salary_range=salary_range,
            role_type=role_type_map.get(role_type, RoleType.OTHER),
            relevance_score=relevance_score,
            status=JobStatus.DISCOVERED
        )

        saved = save_job(job)
        return f"Saved job ID={saved.id}: {title} @ {company} (relevance={relevance_score})"

    def _tool_get_stats(self) -> str:
        return json.dumps(get_stats(), indent=2)

    # ─── Main entry point ─────────────────────────────────────────────────

    def run_discovery(
        self,
        platforms: list[str] | None = None,
        roles: list[str] | None = None,
        location: str = "Hyderabad"
    ) -> str:
        """
        Run a full job discovery cycle.

        Args:
            platforms: Which platforms to search. Defaults to all configured ones.
            roles: Which roles to search for. Defaults to profile target roles.
            location: Location filter.

        Returns:
            Summary string from the agent.
        """
        _platforms = platforms or ["linkedin", "wellfound", "ycombinator"]
        _roles = roles or settings.target_roles_list

        goal = f"""
Run a job discovery cycle for Indira.

Platforms to search: {_platforms}
Roles to search for: {_roles}
Location: {location} (also include remote-friendly roles)

Process:
1. Check current pipeline stats first
2. For each platform × role combination, search for jobs
3. For each job returned, quickly assess if it's worth fetching the full JD:
   - Skip if title obviously doesn't match (e.g. "Sales Manager", "10+ years required")
   - Fetch JD for anything that looks potentially relevant
4. Score each fetched job for relevance
5. Save jobs with relevance score >= 0.6 to the database
6. After saving, give a summary:
   - How many jobs found per platform
   - How many saved (passed relevance filter)
   - Top 3-5 most promising jobs (title, company, why they stand out)
   - Any patterns noticed (e.g. "PM roles mostly require 5+ years, but 3 companies have APM openings")

Be selective but not too strict — Indira is actively looking and would rather
review a few extra jobs than miss a good one.
"""
        return self.run(goal)


# ─── Quick test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from core.database import create_db_tables
    create_db_tables()

    agent = JobDiscoveryAgent()
    # Test with just YC (no login needed) to verify the pipeline works
    summary = agent.run_discovery(
        platforms=["ycombinator"],
        roles=["Product Manager"],
        location="India"
    )
    print("\n" + "="*60)
    print("Discovery Summary")
    print("="*60)
    print(summary)
