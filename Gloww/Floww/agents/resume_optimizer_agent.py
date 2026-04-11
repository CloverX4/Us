"""
agents/resume_optimizer_agent.py
─────────────────────────────────
The Resume Optimizer Agent.

Given a job description, it:
  1. Runs ATS analysis on the current resume
  2. Identifies keyword gaps and framing opportunities
  3. Rewrites each section to hit 95%+ ATS score
  4. Returns the optimized resume with change summary

This agent has 4 tools:
  - score_resume_ats     → runs our ATS scorer
  - get_resume_sections  → fetches current resume content
  - optimize_section     → rewrites one section with LLM
  - finalize_resume      → assembles final output

How the agent USES these tools:
  The LLM gets the JD, reads the tool descriptions, and decides:
  "I should first score the current resume, then look at the gaps,
   then optimize section by section, then finalize."
  We don't hardcode this order — the LLM figures it out.
"""

import json
from pathlib import Path
from core.models import OptimizedResume, ResumeSection, ATSAnalysis
from core.ats_scorer import score_resume
from core.profile import profile
from agents.base import BaseAgent, Tool
from config.settings import settings


# ─── Raw resume content ───────────────────────────────────────────────────────
# This is the base resume text. In Phase 3, we'll parse from PDF dynamically.
# For now, structured as sections so the agent can work section-by-section.

BASE_RESUME_SECTIONS = {
    "summary": "",  # Currently no summary — the agent will add one!

    "experience_gep_full": """Software Engineer | GEP Worldwide | June 2023 – Present | Hyderabad, Telangana
• Redesigned query formation logic from Power BI's DAX to SQL on Delta Tables, contributing to a potential $2M+ annual cost reduction from BI annual subscription.
• Automated end-to-end migration and verification via Postman & Python scripts for 180+ UAT domains within 3 months, driving rapid rollout of the new SQL-based reporting stack and reducing onboarding effort for developers and teams.
• Contributed significantly to AI-driven reporting using RAG with FastAPI, OpenAI, and VectorDB, supporting 24+ visualization types and 20+ data transformation operations for enhanced Excel/CSV data analysis for consultants, improving workflows like report search, generation, and email trigger clicks from 8+ to 2 per operation. Delivered multiple prototypes under tight deadlines for ad-hoc client demos.
• Led Frontend v1 to v2 migration within a strict 2-week deadline due to platform upgrades.
• Delivered multiple feature enhancements in the BI Insights module, including access control on shared reports, user persona-based UI, and data access restrictions via feature flagging, improving privacy & customization.
• Resolved 70+ incident issues for 20+ enterprise clients in 3 months and fixed 20+ UI bugs from UX team reviews, expanding expertise in product architecture and Angular plugin development.""",

    "experience_gep_intern": """Software Engineer Intern | GEP Worldwide | May 2022 – August 2022 | Mumbai, Maharashtra
• Developed and scheduled ADB Notebook jobs for automated data quality report generation using PyDeequ with PySpark in Azure Databricks, ensuring regular integrity and consistency checks on selected Delta Tables.""",

    "skills": """Languages: C#, Python, SQL, C++, TypeScript, Java
Developer Tools: GitHub, Jira, New Relic, Postman, Visual Studio, PyCharm, Swagger, SonarCloud, Fiddler
Technologies & Frameworks: .NET, FastAPI, Angular, Cypress, Elasticsearch, ChromaDB, Qdrant
Databases & Cloud: Azure Databricks, MongoDB, Oracle SQL Developer""",

    "projects": """Blockchain based KYC in Banking and Finance | Hyperledger Fabric, Go, IPFS, ReactJs, NodeJs
• Developed an early prototype for immutable KYC using blockchain and distributed file storage.

Graphical Password Authenticator | ReactJS, NodeJS, Firebase
• Secured 2nd place in an internal Techathon by building a React-based graphical password authenticator as an NPM package.""",

    "recognitions": """GEP Kudos — Employee Recognitions:
• Change Agents (Q1&Q2 2025): Recognized for key ongoing contributions to the DBSQL solution implementation and client onboarding, supporting a high-impact reporting transformation under tight deadlines.
• Catalyst (Q3 2024): Recognized for owning AI-related deliverables for urgent demos and successfully delivering UI upgrades under tight deadlines, by stepping beyond individual responsibilities to drive high-impact results.
• SPOT Recognition (October 2024): Awarded for ensuring smooth sync-ups and successfully completing UI version upgrades on schedule.
• Change Agents (Q2 2024): Recognized for adapting AI scopes within the Analytics module, driving project improvements, SLA compliance, and client impact through cross-team collaboration.""",

    "education": """National Institute of Technology, Warangal | Sep 2019 – May 2023
Bachelor of Technology in Computer Science & Engineering""",

    "certifications": """Blockchain Specialization — University at Buffalo and The State University of New York (Coursera, Jan 2023)"""
}

FULL_RESUME_TEXT = "\n\n".join(BASE_RESUME_SECTIONS.values())


# ─── Agent class ──────────────────────────────────────────────────────────────

class ResumeOptimizerAgent(BaseAgent):
    """
    Optimizes Indira's resume for a specific job description.

    Usage:
        agent = ResumeOptimizerAgent()
        result = agent.run_for_job(
            job_title="Product Manager",
            company="Groww",
            jd_text="We're looking for a PM to..."
        )
        print(result.ats_score)  # should be 95+
    """

    def __init__(self):
        super().__init__()
        self._register_tools()
        self._current_jd: str = ""
        self._current_job_title: str = ""
        self._current_company: str = ""
        self._optimized_sections: list[ResumeSection] = []

    @property
    def system_prompt(self) -> str:
        return profile.build_system_prompt("resume_optimizer")

    def _register_tools(self):
        """Register all tools this agent can use."""

        # ── Tool 1: Score current resume against JD ───────────────────────
        self.register_tool(Tool(
            name="score_resume_ats",
            description=(
                "Score the current resume against a job description using ATS analysis. "
                "Returns score (0-100), matched keywords, missing keywords, and specific recommendations. "
                "Always call this first before optimizing, and again after to verify improvement."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "jd_text": {
                        "type": "string",
                        "description": "The full job description text to score against"
                    },
                    "resume_text": {
                        "type": "string",
                        "description": "The resume text to score. Leave empty to use the current base resume."
                    }
                },
                "required": ["jd_text"]
            },
            function=self._tool_score_ats
        ))

        # ── Tool 2: Get a resume section ──────────────────────────────────
        self.register_tool(Tool(
            name="get_resume_section",
            description=(
                "Get the current content of a specific resume section. "
                "Available sections: summary, experience_gep_full, experience_gep_intern, "
                "skills, projects, recognitions, education, certifications"
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "section_name": {
                        "type": "string",
                        "enum": list(BASE_RESUME_SECTIONS.keys()),
                        "description": "Which section to retrieve"
                    }
                },
                "required": ["section_name"]
            },
            function=self._tool_get_section
        ))

        # ── Tool 3: Save an optimized section ────────────────────────────
        self.register_tool(Tool(
            name="save_optimized_section",
            description=(
                "Save an optimized version of a resume section. "
                "Call this after you've written the improved version of a section. "
                "The optimized text will be assembled into the final resume."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "section_name": {
                        "type": "string",
                        "description": "Name of the section being saved"
                    },
                    "optimized_text": {
                        "type": "string",
                        "description": "The improved text for this section"
                    },
                    "optimization_notes": {
                        "type": "string",
                        "description": "Brief explanation of what was changed and why"
                    }
                },
                "required": ["section_name", "optimized_text", "optimization_notes"]
            },
            function=self._tool_save_section
        ))

        # ── Tool 4: Get full resume text ──────────────────────────────────
        self.register_tool(Tool(
            name="get_full_resume_text",
            description="Get the complete current resume as a single text block.",
            input_schema={
                "type": "object",
                "properties": {},
                "required": []
            },
            function=self._tool_get_full_resume
        ))

    # ─── Tool implementations ─────────────────────────────────────────────

    def _tool_score_ats(self, jd_text: str, resume_text: str = "") -> str:
        text = resume_text if resume_text else FULL_RESUME_TEXT
        analysis = score_resume(text, jd_text)
        return json.dumps({
            "score": analysis.score,
            "matched_keywords": analysis.matched_keywords[:20],
            "missing_keywords": analysis.missing_keywords[:20],
            "section_scores": analysis.section_scores,
            "recommendations": analysis.recommendations,
            "breakdown": analysis.breakdown
        }, indent=2)

    def _tool_get_section(self, section_name: str) -> str:
        return BASE_RESUME_SECTIONS.get(section_name, f"Section '{section_name}' not found")

    def _tool_save_section(
        self,
        section_name: str,
        optimized_text: str,
        optimization_notes: str
    ) -> str:
        original = BASE_RESUME_SECTIONS.get(section_name, "")
        self._optimized_sections.append(ResumeSection(
            section_name=section_name,
            original_text=original,
            optimized_text=optimized_text,
            optimization_notes=optimization_notes
        ))
        return f"Saved optimized '{section_name}' section ({len(optimized_text)} chars)"

    def _tool_get_full_resume(self) -> str:
        return FULL_RESUME_TEXT

    # ─── Main entry point ─────────────────────────────────────────────────

    def run_for_job(
        self,
        job_title: str,
        company: str,
        jd_text: str,
        job_id: int = 0
    ) -> OptimizedResume:
        """
        Optimize the resume for a specific job. This is what you call externally.

        Args:
            job_title: e.g. "Product Manager"
            company: e.g. "Groww"
            jd_text: Full job description text
            job_id: DB ID of the job (for linking)

        Returns:
            OptimizedResume with all optimized sections and final ATS score
        """
        self._current_jd = jd_text
        self._current_job_title = job_title
        self._current_company = company
        self._optimized_sections = []

        goal = f"""
Optimize Indira's resume for this position:
  Role: {job_title} at {company}

Job Description:
{jd_text}

Steps to follow:
1. First, score the current resume against the JD to see where we stand
2. Read the full resume to understand all sections
3. Identify the top missing keywords and framing gaps
4. For each section that needs work (especially summary and main experience):
   a. Get the current section text
   b. Rewrite it with: better keyword density, stronger action verbs, JD-aligned framing
   c. Save the optimized version with notes on what changed
5. Re-score the optimized resume to verify it hits 95+
6. Give a final summary of: ATS score achieved, key changes made, and any keywords you couldn't naturally fit

Important: For a PM role, frame engineering work in product outcomes.
For an SDE role, highlight technical depth and scale.
"""

        final_response = self.run(goal)

        # Build the final score from optimized sections
        optimized_text = self._build_optimized_resume_text()
        final_analysis_json = json.loads(
            self._tool_score_ats(jd_text, optimized_text)
        )

        return OptimizedResume(
            job_id=job_id,
            job_title=job_title,
            company=company,
            ats_score=final_analysis_json["score"],
            sections=self._optimized_sections,
            keywords_added=[s.optimization_notes for s in self._optimized_sections],
            keywords_missing=final_analysis_json["missing_keywords"][:10],
            optimization_summary=final_response
        )

    def _build_optimized_resume_text(self) -> str:
        """Merge optimized sections with original sections."""
        optimized_map = {s.section_name: s.optimized_text for s in self._optimized_sections}
        sections = {}
        for name, original in BASE_RESUME_SECTIONS.items():
            sections[name] = optimized_map.get(name, original)
        return "\n\n".join(sections.values())


# ─── Quick test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_jd = """
    Senior Product Manager — Analytics Platform
    Company: Fintech Startup, Hyderabad

    We're building the future of financial analytics. We need a PM who can:
    - Own the product roadmap for our analytics and reporting features
    - Work closely with data engineers and frontend teams
    - Define success metrics and run A/B tests
    - Translate user research into actionable product requirements
    - Communicate with enterprise clients and gather feedback

    Must have:
    - 2+ years of product management experience OR strong engineering background with product exposure
    - Experience with data products, analytics, or reporting tools
    - SQL proficiency and comfort with data
    - Agile/Scrum experience
    - Strong communication and stakeholder management

    Nice to have:
    - Experience with AI/ML products
    - B2B enterprise product experience
    """

    agent = ResumeOptimizerAgent()
    result = agent.run_for_job(
        job_title="Senior Product Manager",
        company="Fintech Startup",
        jd_text=sample_jd
    )

    print(f"\n✅ ATS Score: {result.ats_score}/100")
    print(f"📝 Sections optimized: {len(result.sections)}")
    print(f"\n--- Optimization Summary ---")
    print(result.optimization_summary[:500])
