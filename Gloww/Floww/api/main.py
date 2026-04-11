"""
api/main.py
───────────
FastAPI app — your control plane for Floww.

Endpoints:
  GET  /                     → health + stats summary
  GET  /jobs                 → list all jobs (filterable by status/platform)
  GET  /jobs/{id}            → single job detail
  GET  /jobs/{id}/resume     → get optimized resume text
  GET  /jobs/{id}/cover-letter → get cover letter text
  POST /discover             → trigger job discovery
  POST /pipeline             → run application pipeline
  POST /pipeline/{id}        → run pipeline for one specific job
  POST /reply/{id}           → generate recruiter reply for a job
  GET  /stats                → pipeline stats

Run with: uvicorn api.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlmodel import select, Session

from core.models import Job, Application, JobStatus, Platform
from core.database import engine, create_db_tables
from core.job_store import get_jobs_by_status, get_all_jobs, get_stats, update_job_status

app = FastAPI(
    title="Floww",
    description="Indira's automated job application system",
    version="1.0.0"
)

# Allow requests from any origin (useful when testing with a browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_tables()


# ─── Request models ───────────────────────────────────────────────────────────

class DiscoverRequest(BaseModel):
    platforms: list[str] = ["ycombinator", "wellfound", "linkedin"]
    roles: Optional[list[str]] = None
    location: str = "Hyderabad"


class PipelineRequest(BaseModel):
    job_ids: Optional[list[int]] = None
    dry_run: bool = False


class RecruiterReplyRequest(BaseModel):
    recruiter_name: str
    recruiter_company: str
    message_text: str
    platform: str = "linkedin"


class ManualJobRequest(BaseModel):
    """Add a job manually (paste JD from any platform)."""
    title: str
    company: str
    platform: str = "other"
    job_url: str
    description: str
    location: str = ""
    salary_range: str = ""


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    stats = get_stats()
    return {
        "service": "Floww — Job Application Automation",
        "status": "running",
        "pipeline": stats
    }


@app.get("/stats")
def pipeline_stats():
    return get_stats()


@app.get("/jobs")
def list_jobs(
    status: Optional[str] = None,
    platform: Optional[str] = None,
    min_relevance: float = 0.0
):
    """List jobs with optional filters."""
    with Session(engine) as session:
        query = select(Job)
        jobs = session.exec(query).all()

    # Apply filters
    if status:
        jobs = [j for j in jobs if j.status.value == status]
    if platform:
        jobs = [j for j in jobs if j.platform.value == platform]
    if min_relevance:
        jobs = [j for j in jobs if j.relevance_score >= min_relevance]

    # Sort by relevance descending
    jobs = sorted(jobs, key=lambda j: j.relevance_score, reverse=True)

    return [_job_summary(j) for j in jobs]


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    with Session(engine) as session:
        job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_detail(job)


@app.get("/jobs/{job_id}/resume")
def get_resume(job_id: int):
    """Get the optimized resume text for a job."""
    with Session(engine) as session:
        app = session.exec(
            select(Application).where(Application.job_id == job_id)
        ).first()
    if not app:
        raise HTTPException(status_code=404, detail="No application found for this job")
    return {
        "job_id": job_id,
        "resume_pdf_path": app.optimized_resume_path,
        "message": "Download the PDF from the path above"
    }


@app.get("/jobs/{job_id}/cover-letter")
def get_cover_letter(job_id: int):
    """Get the cover letter for a job."""
    with Session(engine) as session:
        application = session.exec(
            select(Application).where(Application.job_id == job_id)
        ).first()
    if not application or not application.cover_letter_text:
        raise HTTPException(status_code=404, detail="No cover letter found for this job")
    return {
        "job_id": job_id,
        "cover_letter": application.cover_letter_text,
        "word_count": len(application.cover_letter_text.split()),
        "pdf_path": application.cover_letter_path
    }


@app.post("/jobs/manual")
def add_manual_job(req: ManualJobRequest):
    """Add a job manually — paste JD from any platform."""
    from core.models import RoleType
    from core.job_store import save_job

    job = Job(
        title=req.title,
        company=req.company,
        platform=Platform(req.platform) if req.platform in [p.value for p in Platform] else Platform.OTHER,
        job_url=req.job_url,
        description=req.description,
        location=req.location,
        salary_range=req.salary_range,
        role_type=RoleType.OTHER,
        relevance_score=0.8,  # manually added = assumed relevant
        status=JobStatus.DISCOVERED
    )
    saved = save_job(job)
    return {"id": saved.id, "message": f"Job saved: {req.title} @ {req.company}"}


@app.post("/discover")
def trigger_discovery(req: DiscoverRequest, background_tasks: BackgroundTasks):
    """Trigger job discovery in the background."""
    background_tasks.add_task(_run_discovery, req.platforms, req.roles, req.location)
    return {
        "message": "Discovery started in background",
        "platforms": req.platforms,
        "roles": req.roles or "all target roles"
    }


@app.post("/pipeline")
def run_pipeline(req: PipelineRequest, background_tasks: BackgroundTasks):
    """Run the full application pipeline for pending jobs."""
    background_tasks.add_task(_run_pipeline, req.job_ids, req.dry_run)
    return {
        "message": "Pipeline started in background",
        "job_ids": req.job_ids or "all pending",
        "dry_run": req.dry_run
    }


@app.post("/pipeline/{job_id}")
def run_pipeline_for_job(job_id: int, dry_run: bool = False):
    """Run pipeline for a single specific job (synchronous — waits for result)."""
    from agents.orchestrator_agent import OrchestratorAgent
    agent = OrchestratorAgent()
    result = agent.run_pipeline(job_ids=[job_id], dry_run=dry_run)
    return {"job_id": job_id, "result": result}


@app.post("/reply/{job_id}")
def generate_recruiter_reply(job_id: int, req: RecruiterReplyRequest):
    """Generate a reply to a recruiter message for a specific job."""
    from agents.recruiter_reply_agent import RecruiterReplyAgent
    agent = RecruiterReplyAgent()
    result = agent.reply_to_recruiter(
        recruiter_name=req.recruiter_name,
        recruiter_company=req.recruiter_company,
        their_message=req.message_text,
        platform=req.platform,
        job_id=job_id
    )
    return {
        "job_id": job_id,
        "reply": result.our_reply,
        "recruiter": req.recruiter_name
    }


@app.patch("/jobs/{job_id}/status")
def update_status(job_id: int, status: str, notes: str = ""):
    """Manually update a job's status."""
    if status not in [s.value for s in JobStatus]:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    update_job_status(job_id, JobStatus(status), notes)
    return {"job_id": job_id, "new_status": status}


# ─── Background task runners ──────────────────────────────────────────────────

def _run_discovery(platforms: list[str], roles: list[str] | None, location: str):
    from agents.job_discovery_agent import JobDiscoveryAgent
    agent = JobDiscoveryAgent()
    agent.run_discovery(platforms=platforms, roles=roles, location=location)


def _run_pipeline(job_ids: list[int] | None, dry_run: bool):
    from agents.orchestrator_agent import OrchestratorAgent
    agent = OrchestratorAgent()
    agent.run_pipeline(job_ids=job_ids, dry_run=dry_run)


# ─── Response formatters ──────────────────────────────────────────────────────

def _job_summary(job: Job) -> dict:
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "platform": job.platform.value,
        "status": job.status.value,
        "relevance_score": job.relevance_score,
        "ats_before": job.ats_score_before,
        "ats_after": job.ats_score_after,
        "location": job.location,
        "discovered_at": job.discovered_at.isoformat() if job.discovered_at else None,
    }


def _job_detail(job: Job) -> dict:
    summary = _job_summary(job)
    summary.update({
        "job_url": job.job_url,
        "description": job.description[:500] + "..." if len(job.description) > 500 else job.description,
        "salary_range": job.salary_range,
        "notes": job.notes,
        "applied_at": job.applied_at.isoformat() if job.applied_at else None,
    })
    return summary
