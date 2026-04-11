"""
core/job_store.py
─────────────────
All database operations for jobs and applications.
This keeps DB logic out of agents and connectors — they just call these functions.

Why a separate store module?
  Agents shouldn't know about sessions, commits, or SQL.
  They call `job_store.save_job(job)` and it just works.
"""

from datetime import datetime
from sqlmodel import Session, select
from core.models import Job, Application, JobStatus, Platform
from core.database import engine
from rich.console import Console

console = Console()


# ─── Job operations ───────────────────────────────────────────────────────────

def save_job(job: Job) -> Job:
    """
    Save a job, skipping if the URL already exists (deduplication).
    Returns the saved job (existing or new).
    """
    with Session(engine) as session:
        existing = session.exec(
            select(Job).where(Job.job_url == job.job_url)
        ).first()

        if existing:
            return existing  # already have this one

        session.add(job)
        session.commit()
        session.refresh(job)
        return job


def get_job_by_url(url: str) -> Job | None:
    with Session(engine) as session:
        return session.exec(select(Job).where(Job.job_url == url)).first()


def get_jobs_by_status(status: JobStatus) -> list[Job]:
    with Session(engine) as session:
        return list(session.exec(select(Job).where(Job.status == status)).all())


def get_all_jobs() -> list[Job]:
    with Session(engine) as session:
        return list(session.exec(select(Job)).all())


def update_job_status(job_id: int, status: JobStatus, notes: str = "") -> None:
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if job:
            job.status = status
            if notes:
                job.notes = notes
            if status == JobStatus.APPLIED:
                job.applied_at = datetime.utcnow()
            session.commit()


def update_job_scores(job_id: int, ats_before: float = 0, ats_after: float = 0) -> None:
    with Session(engine) as session:
        job = session.get(Job, job_id)
        if job:
            if ats_before:
                job.ats_score_before = ats_before
            if ats_after:
                job.ats_score_after = ats_after
            session.commit()


def get_stats() -> dict:
    """Summary stats for the dashboard."""
    jobs = get_all_jobs()
    return {
        "total_discovered": len(jobs),
        "applied": len([j for j in jobs if j.status == JobStatus.APPLIED]),
        "pending_application": len([j for j in jobs if j.status == JobStatus.RESUME_OPTIMIZED]),
        "recruiter_replies": len([j for j in jobs if j.status == JobStatus.RECRUITER_REPLIED]),
        "interviews": len([j for j in jobs if j.status == JobStatus.INTERVIEW_SCHEDULED]),
        "by_platform": {
            p.value: len([j for j in jobs if j.platform == p])
            for p in Platform
        }
    }


# ─── Application operations ──────────────────────────────────────────────────

def save_application(application: Application) -> Application:
    with Session(engine) as session:
        session.add(application)
        session.commit()
        session.refresh(application)
        return application


def get_application_for_job(job_id: int) -> Application | None:
    with Session(engine) as session:
        return session.exec(
            select(Application).where(Application.job_id == job_id)
        ).first()
