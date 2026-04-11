"""
agents/orchestrator_agent.py
──────────────────────────────
The Orchestrator Agent — the master pipeline.

This is the agent that runs the full flow end-to-end for each job:
  Discovered Job → Optimize Resume → Write Cover Letter → Generate PDFs → Apply

It coordinates the other agents (resume optimizer, cover letter) and
decides the order/priority of which jobs to process.

Think of this as the "project manager" of the whole system.
The other agents are specialists it delegates to.

Usage:
    agent = OrchestratorAgent()
    results = agent.run_pipeline(job_ids=[1, 2, 3])  # specific jobs
    results = agent.run_pipeline()                    # all pending jobs
"""

import json
import asyncio
from pathlib import Path
from core.models import Job, Application, JobStatus
from core.job_store import (
    get_jobs_by_status, update_job_status, update_job_scores,
    save_application, get_stats
)
from core.ats_scorer import score_resume
from core.resume_generator import generate_pdf, generate_cover_letter_pdf
from agents.base import BaseAgent, Tool
from agents.resume_optimizer_agent import ResumeOptimizerAgent, FULL_RESUME_TEXT
from agents.cover_letter_agent import CoverLetterAgent
from config.settings import settings
from rich.console import Console

console = Console()


class OrchestratorAgent(BaseAgent):
    """
    Master pipeline agent.

    Has tools to:
    - Get pending jobs from DB
    - Run resume optimizer for a job
    - Run cover letter agent for a job
    - Generate PDFs
    - Trigger application submission
    - Update job statuses
    """

    def __init__(self):
        super().__init__()
        self._resume_agent = ResumeOptimizerAgent()
        self._cover_agent = CoverLetterAgent()
        self._register_tools()

    @property
    def system_prompt(self) -> str:
        from core.profile import profile
        return profile.build_system_prompt("resume_optimizer") + """

## Your Role as Orchestrator
You coordinate Indira's entire application pipeline. For each job:
1. Check its current status
2. Optimize the resume (run resume optimizer tool)
3. Write a cover letter (run cover letter tool)
4. Generate PDFs
5. Attempt auto-apply if the job supports it
6. Update the job status

Be strategic: process high-relevance jobs first.
Flag jobs where something unusual comes up (asks for 10+ years, role has changed, etc).
"""

    def _register_tools(self):

        # ── Get jobs waiting to be processed ──────────────────────────────
        self.register_tool(Tool(
            name="get_pending_jobs",
            description=(
                "Get jobs from the database that haven't been processed yet. "
                "Returns jobs with DISCOVERED status, sorted by relevance score descending."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max number of jobs to return",
                        "default": 10
                    }
                },
                "required": []
            },
            function=self._tool_get_pending
        ))

        # ── Optimize resume for a job ──────────────────────────────────────
        self.register_tool(Tool(
            name="optimize_resume_for_job",
            description=(
                "Run the resume optimizer agent for a specific job. "
                "Tailors Indira's resume to the job description, targeting 95+ ATS score. "
                "Returns the ATS score achieved and path to optimized resume PDF."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "integer"},
                    "job_title": {"type": "string"},
                    "company": {"type": "string"},
                    "jd_text": {"type": "string", "description": "Full job description text"}
                },
                "required": ["job_id", "job_title", "company", "jd_text"]
            },
            function=self._tool_optimize_resume
        ))

        # ── Write cover letter for a job ───────────────────────────────────
        self.register_tool(Tool(
            name="write_cover_letter",
            description=(
                "Write a personalized cover letter for a specific job. "
                "Returns the cover letter text and path to PDF."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "integer"},
                    "job_title": {"type": "string"},
                    "company": {"type": "string"},
                    "jd_text": {"type": "string"},
                    "company_context": {
                        "type": "string",
                        "description": "Any extra context about the company",
                        "default": ""
                    }
                },
                "required": ["job_id", "job_title", "company", "jd_text"]
            },
            function=self._tool_write_cover_letter
        ))

        # ── Apply to a job ─────────────────────────────────────────────────
        self.register_tool(Tool(
            name="apply_to_job",
            description=(
                "Submit an application to a job. "
                "For LinkedIn jobs with Easy Apply: automates the form. "
                "For other platforms: returns the application URL for manual apply. "
                "Only call this after resume and cover letter are ready."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "integer"},
                    "job_url": {"type": "string"},
                    "platform": {"type": "string"},
                    "resume_pdf_path": {"type": "string"},
                    "cover_letter_text": {"type": "string"}
                },
                "required": ["job_id", "job_url", "platform", "resume_pdf_path", "cover_letter_text"]
            },
            function=self._tool_apply
        ))

        # ── Update job status ──────────────────────────────────────────────
        self.register_tool(Tool(
            name="update_job_status",
            description="Update the status of a job in the database.",
            input_schema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "integer"},
                    "status": {
                        "type": "string",
                        "enum": [s.value for s in JobStatus]
                    },
                    "notes": {"type": "string", "default": ""}
                },
                "required": ["job_id", "status"]
            },
            function=self._tool_update_status
        ))

        # ── Get pipeline stats ─────────────────────────────────────────────
        self.register_tool(Tool(
            name="get_pipeline_stats",
            description="Get current stats: how many jobs discovered, applied, in progress.",
            input_schema={"type": "object", "properties": {}, "required": []},
            function=lambda: json.dumps(get_stats(), indent=2)
        ))

    # ─── Tool implementations ─────────────────────────────────────────────

    def _tool_get_pending(self, limit: int = 10) -> str:
        jobs = get_jobs_by_status(JobStatus.DISCOVERED)
        # Sort by relevance score descending
        jobs.sort(key=lambda j: j.relevance_score, reverse=True)
        jobs = jobs[:limit]

        return json.dumps([{
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "platform": j.platform.value,
            "job_url": j.job_url,
            "relevance_score": j.relevance_score,
            "location": j.location,
            "has_description": bool(j.description)
        } for j in jobs], indent=2)

    def _tool_optimize_resume(
        self,
        job_id: int,
        job_title: str,
        company: str,
        jd_text: str
    ) -> str:
        # Score before
        before = score_resume(FULL_RESUME_TEXT, jd_text)

        # Run optimizer
        result = self._resume_agent.run_for_job(job_title, company, jd_text, job_id)

        # Generate PDF
        pdf_path = generate_pdf(result)

        # Save scores
        update_job_scores(job_id, ats_before=before.score, ats_after=result.ats_score)

        # Save application record
        app = Application(
            job_id=job_id,
            optimized_resume_path=str(pdf_path)
        )
        saved_app = save_application(app)

        update_job_status(job_id, JobStatus.RESUME_OPTIMIZED)

        return json.dumps({
            "ats_score_before": before.score,
            "ats_score_after": result.ats_score,
            "sections_optimized": len(result.sections),
            "resume_pdf": str(pdf_path),
            "application_id": saved_app.id,
            "summary": result.optimization_summary[:300]
        }, indent=2)

    def _tool_write_cover_letter(
        self,
        job_id: int,
        job_title: str,
        company: str,
        jd_text: str,
        company_context: str = ""
    ) -> str:
        result = self._cover_agent.write_for_job(
            job_title, company, jd_text, company_context, job_id
        )

        # Generate PDF
        pdf_path = generate_cover_letter_pdf(company, job_title, result.text)

        # Update application record with cover letter
        from core.job_store import get_application_for_job
        from sqlmodel import Session
        from core.database import engine

        with Session(engine) as session:
            app = get_application_for_job(job_id)
            if app:
                app = session.get(Application, app.id)
                if app:
                    app.cover_letter_text = result.text
                    app.cover_letter_path = str(pdf_path)
                    session.commit()

        return json.dumps({
            "word_count": result.word_count,
            "cover_letter_pdf": str(pdf_path),
            "personalization_notes": result.personalization_notes,
            "cover_letter_preview": result.text[:400]
        }, indent=2)

    def _tool_apply(
        self,
        job_id: int,
        job_url: str,
        platform: str,
        resume_pdf_path: str,
        cover_letter_text: str
    ) -> str:
        if platform == "linkedin":
            return asyncio.get_event_loop().run_until_complete(
                self._async_linkedin_apply(job_id, job_url, resume_pdf_path, cover_letter_text)
            )
        else:
            # For non-LinkedIn platforms, return the URL for manual apply
            update_job_status(job_id, JobStatus.APPLIED, notes=f"Manual apply needed: {job_url}")
            return json.dumps({
                "result": "manual_required",
                "message": f"Platform '{platform}' requires manual application. URL: {job_url}",
                "apply_url": job_url
            })

    async def _async_linkedin_apply(
        self,
        job_id: int,
        job_url: str,
        resume_pdf_path: str,
        cover_letter_text: str
    ) -> str:
        from connectors.linkedin.apply import LinkedInApplyConnector, ApplyResult

        async with LinkedInApplyConnector() as connector:
            logged_in = await connector.login(
                settings.linkedin_email,
                settings.linkedin_password
            )
            if not logged_in:
                return json.dumps({"result": "error", "message": "LinkedIn login failed"})

            outcome = await connector.apply_to_job(
                job_url=job_url,
                resume_pdf_path=resume_pdf_path,
                cover_letter_text=cover_letter_text
            )

        if outcome.result == ApplyResult.SUCCESS:
            update_job_status(job_id, JobStatus.APPLIED)
        elif outcome.result == ApplyResult.NEEDS_REVIEW:
            update_job_status(job_id, JobStatus.DISCOVERED, notes=f"Needs review: {outcome.message}")

        return json.dumps({
            "result": outcome.result.value,
            "message": outcome.message,
            "screenshot": outcome.screenshot_path
        })

    def _tool_update_status(self, job_id: int, status: str, notes: str = "") -> str:
        update_job_status(job_id, JobStatus(status), notes)
        return f"Updated job {job_id} to status '{status}'"

    # ─── Main entry point ─────────────────────────────────────────────────

    def run_pipeline(self, job_ids: list[int] | None = None, dry_run: bool = False) -> str:
        """
        Run the full application pipeline.

        Args:
            job_ids: Specific job IDs to process. If None, processes all pending.
            dry_run: If True, optimize and generate docs but don't submit applications.

        Returns:
            Summary of what was processed.
        """
        goal = f"""
Run the full application pipeline for Indira.

{"Processing specific job IDs: " + str(job_ids) if job_ids else "Process all pending (DISCOVERED) jobs."}
{"DRY RUN: Optimize resumes and write cover letters but DO NOT submit applications." if dry_run else ""}

For each job:
1. Get the job details (use get_pending_jobs to see what's available)
2. Optimize the resume for that specific JD (run optimize_resume_for_job)
3. Write a personalized cover letter (run write_cover_letter)
4. {"Log what would happen but skip actual submission" if dry_run else "Apply to the job (run apply_to_job)"}
5. Update status and move to next job

After processing all jobs, give a summary:
- How many jobs processed
- ATS scores achieved (before → after)
- Which applications were submitted vs need manual review
- Any issues encountered
- Top 2-3 jobs to prioritize manual follow-up on

Process in order of relevance score — highest first.
"""
        return self.run(goal)
