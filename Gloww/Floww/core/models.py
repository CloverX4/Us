"""
core/models.py
──────────────
All data models for Floww. These are the "nouns" of our system.

We use SQLModel — it's SQLAlchemy + Pydantic in one class.
  - `table=True`  → stored in the database
  - `table=False` (default) → pure Pydantic validation model (for API I/O, agent responses)

Every time an agent does something, it produces or updates one of these.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field
import json


# ─── Enums ────────────────────────────────────────────────────────────────────

class JobStatus(str, Enum):
    DISCOVERED = "discovered"       # Found by job discovery agent
    FILTERED_OUT = "filtered_out"   # Didn't pass relevance filter
    RESUME_OPTIMIZED = "resume_optimized"  # Resume tailored for this job
    APPLIED = "applied"             # Application submitted
    RECRUITER_REPLIED = "recruiter_replied"  # They replied
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTED = "rejected"
    OFFER = "offer"


class Platform(str, Enum):
    LINKEDIN = "linkedin"
    NAUKRI = "naukri"
    WELLFOUND = "wellfound"
    YCOMBINATOR = "ycombinator"
    INSTAHYRE = "instahyre"
    OTHER = "other"


class RoleType(str, Enum):
    PM = "product_manager"
    SDE = "senior_sde"
    APM = "apm"
    OTHER = "other"


# ─── Database Models (table=True) ─────────────────────────────────────────────

class Job(SQLModel, table=True):
    """
    A job posting discovered from any platform.
    This is the central entity — everything else references a Job.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    # Identity
    title: str
    company: str
    platform: Platform
    job_url: str = Field(unique=True)  # prevents duplicates across runs

    # Content
    description: str = ""           # full JD text
    location: str = ""
    salary_range: str = ""
    role_type: RoleType = RoleType.OTHER

    # Scoring
    relevance_score: float = 0.0    # 0-1, how relevant to target roles
    ats_score_before: float = 0.0   # ATS score before optimization
    ats_score_after: float = 0.0    # ATS score after optimization

    # Tracking
    status: JobStatus = JobStatus.DISCOVERED
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    applied_at: Optional[datetime] = None
    notes: str = ""                 # agent notes, recruiter messages, etc.


class Application(SQLModel, table=True):
    """
    Tracks one application attempt for a specific job.
    One Job can have one Application (we don't double-apply).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="job.id")

    # Generated documents
    optimized_resume_path: str = ""   # path to the tailored resume PDF
    cover_letter_text: str = ""       # full cover letter content
    cover_letter_path: str = ""       # path to PDF if generated

    # Application metadata
    submitted_at: Optional[datetime] = None
    platform_application_id: str = ""  # ID from the platform if available

    # Recruiter communication
    recruiter_name: str = ""
    recruiter_message: str = ""       # their message to us
    our_reply: str = ""               # what we replied


class RecruiterMessage(SQLModel, table=True):
    """
    Inbound recruiter messages (LinkedIn InMail, Naukri messages, etc.)
    The recruiter reply agent processes these.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    platform: Platform
    recruiter_name: str = ""
    recruiter_company: str = ""
    message_text: str
    our_reply: str = ""
    replied_at: Optional[datetime] = None
    received_at: datetime = Field(default_factory=datetime.utcnow)


# ─── Non-DB Models (pure Pydantic, for agent I/O) ─────────────────────────────

class ResumeSection(SQLModel):
    """A single section of a resume (summary, experience bullet, etc.)"""
    section_name: str       # e.g. "summary", "experience_gep", "skills"
    original_text: str
    optimized_text: str = ""
    optimization_notes: str = ""  # why the agent changed what it changed


class OptimizedResume(SQLModel):
    """
    The output of the resume optimizer agent for a specific job.
    Contains the full tailored resume content + ATS score.
    """
    job_id: int
    job_title: str
    company: str
    ats_score: float
    sections: list[ResumeSection]
    keywords_added: list[str] = []       # keywords from JD that were added
    keywords_missing: list[str] = []     # keywords we couldn't naturally add
    optimization_summary: str = ""       # agent's explanation of changes


class CoverLetter(SQLModel):
    """Output of the cover letter agent."""
    job_id: int
    job_title: str
    company: str
    text: str                   # full cover letter text
    word_count: int = 0
    personalization_notes: str = ""  # what specific elements were personalized


class ATSAnalysis(SQLModel):
    """
    Output of the ATS scorer utility.
    Tells us how well the current resume matches a JD.
    """
    score: float                        # 0-100
    matched_keywords: list[str]
    missing_keywords: list[str]
    section_scores: dict[str, float]    # score per section
    recommendations: list[str]         # specific things to fix
    breakdown: str                      # human-readable explanation


class JobSearchQuery(SQLModel):
    """Input to the job discovery agent."""
    role: str
    location: str = "Hyderabad"
    remote_ok: bool = True
    experience_years_min: int = 2
    experience_years_max: int = 6
    platforms: list[Platform] = [Platform.LINKEDIN, Platform.WELLFOUND]
