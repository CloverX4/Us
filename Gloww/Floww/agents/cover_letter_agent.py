"""
agents/cover_letter_agent.py
─────────────────────────────
The Cover Letter Agent.

Writes personalized cover letters in Indira's voice.
NOT generic. NOT templated. Each one references something specific about
the company/role and connects it to a real story from her experience.

This agent is simpler than the resume optimizer — it uses fewer tools
because cover letters are more generative than analytical.
"""

from core.models import CoverLetter
from core.profile import profile
from agents.base import BaseAgent, Tool


class CoverLetterAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self._register_tools()

    @property
    def system_prompt(self) -> str:
        return profile.build_system_prompt("cover_letter")

    def _register_tools(self):

        # ── Tool 1: Get relevant achievement for this role type ───────────
        self.register_tool(Tool(
            name="get_relevant_achievements",
            description=(
                "Get Indira's most relevant achievements for a specific role type. "
                "Use this to pick the right story/example to feature in the cover letter."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "role_type": {
                        "type": "string",
                        "enum": ["product_manager", "senior_sde", "apm", "data_engineer"],
                        "description": "The type of role to get relevant achievements for"
                    }
                },
                "required": ["role_type"]
            },
            function=self._tool_get_achievements
        ))

        # ── Tool 2: Get her career transition narrative (for PM roles) ────
        self.register_tool(Tool(
            name="get_pm_transition_narrative",
            description=(
                "Get Indira's prepared narrative for why she's transitioning to PM. "
                "Use this for PM/APM applications to frame the transition confidently."
            ),
            input_schema={
                "type": "object",
                "properties": {},
                "required": []
            },
            function=self._tool_get_pm_narrative
        ))

    def _tool_get_achievements(self, role_type: str) -> str:
        achievements = {
            "product_manager": """
Most relevant achievements for PM roles:

1. AI Reporting System (strongest PM story):
   "I defined and shipped an AI-driven reporting system (RAG + FastAPI + OpenAI) that reduced
   consultant workflows from 8+ clicks to 2. Supporting 24+ visualization types. I built this under
   tight deadlines for client demos — owning scope, prioritization, and delivery."
   → Shows: product thinking, user impact measurement, delivery under pressure

2. DAX → SQL Migration ($2M impact):
   "Led a migration project that contributed to $2M+ annual cost reduction. Built a centralized
   onboarding repo (50+ scripts) that became the base for all production onboarding — I initiated
   this infrastructure without being asked because I saw the team needed it."
   → Shows: initiative, systems thinking, measurable business impact

3. Feature enhancements in BI Insights:
   "Delivered access control, user persona-based UI, and feature flagging — I pushed for the
   persona-based approach because I was thinking about who our different users actually were."
   → Shows: user-centric thinking, proactive product ownership

4. Recognition pattern (4x Change Agent):
   "Consistently recognized for stepping outside individual responsibilities to drive team outcomes.
   This is who I am as a collaborator — I don't wait to be told."
   → Shows: cross-functional leadership, initiative
""",
            "senior_sde": """
Most relevant achievements for Senior SDE roles:

1. RAG + FastAPI AI System:
   "Built production AI reporting pipeline: RAG with FastAPI, OpenAI, ChromaDB/Qdrant.
   24+ viz types, 20+ data transformations. Reduced 8+ click workflows to 2."
   → Shows: full-stack AI development, system design, delivery

2. DAX → SQL on Azure Databricks:
   "Complex CTE development, running sums, cumulative aggregations on Delta Tables.
   Automated migration + verification for 180+ domains. Built 50+ reusable scripts."
   → Shows: data engineering depth, automation mindset, scale

3. Frontend v1 → v2 migration (2-week deadline):
   "Led complete frontend migration under strict timeline — Angular plugin development."
   → Shows: full-stack capability, deadline delivery

4. 70+ incidents resolved in 3 months:
   "Rapid incident resolution for 20+ enterprise clients — debugging across multiple systems."
   → Shows: production engineering experience, enterprise scale
""",
            "apm": """
Same as product_manager but emphasize the learning mindset and "first PM role" framing:
  "I have PM instincts built from 2 years of engineering practice — now I want the title
   and the seat at the table that comes with it."
""",
            "data_engineer": """
Most relevant:
1. DAX → SQL migration (Delta Tables, complex CTEs, Azure Databricks)
2. PyDeequ data quality automation (intern project)
3. AI pipeline with vector databases (ChromaDB, Qdrant)
"""
        }
        return achievements.get(role_type, achievements["product_manager"])

    def _tool_get_pm_narrative(self) -> str:
        return """
PM Transition Narrative (use this for PM applications):

"I've been doing product thinking as an engineer — asking 'why are we building this?',
pushing back on requirements that served one client instead of the platform, and initiating
tooling that the whole team would benefit from (like the migration repo that's now 50+ scripts
used in production onboarding).

What changed isn't my skills — it's my clarity. I want to be in the room where the roadmap is
decided. I want to be accountable to the user, not just the ticket. My technical background
means I can have real conversations with engineering, challenge estimates meaningfully, and spot
when a technical decision is actually a product decision in disguise.

This isn't a pivot away from tech — it's a step toward using what I know in its highest form."

Tone note: Say this with confidence, not apology.
Don't frame it as "I know I don't have PM experience, but..."
Frame it as "I've been doing this work — here's the evidence."
"""

    def write_for_job(
        self,
        job_title: str,
        company: str,
        jd_text: str,
        company_context: str = "",
        job_id: int = 0
    ) -> CoverLetter:
        """
        Write a personalized cover letter for a specific job.

        Args:
            job_title: Role title
            company: Company name
            jd_text: Full job description
            company_context: Optional — anything known about the company culture, product, etc.
            job_id: DB ID for linking

        Returns:
            CoverLetter with the text + personalization notes
        """
        goal = f"""
Write a cover letter for Indira applying to:
  Role: {job_title} at {company}

Job Description:
{jd_text}

{f"Company Context: {company_context}" if company_context else ""}

Process:
1. Identify the role type (PM, SDE, APM) so you get the right achievements
2. Get the relevant achievements for this role type
3. If it's a PM or APM role, get the PM transition narrative
4. Write the cover letter following the structure:
   - Hook: something specific about the company or the problem they're solving
   - Bridge: connect their challenge to something you've genuinely experienced
   - Evidence: one concrete story with numbers
   - Why them, why now: specific to this company, not generic
   - Close: genuine curiosity, specific ask

Length: 300-350 words maximum.
Voice: Conversational, confident, specific. Not corporate.

Output the final cover letter text directly, then on a new line write:
PERSONALIZATION_NOTES: [what specific elements you personalized and why]
"""

        result_text = self.run(goal)

        # Split cover letter from notes
        cover_text = result_text
        personalization_notes = ""

        if "PERSONALIZATION_NOTES:" in result_text:
            parts = result_text.split("PERSONALIZATION_NOTES:")
            cover_text = parts[0].strip()
            personalization_notes = parts[1].strip() if len(parts) > 1 else ""

        word_count = len(cover_text.split())

        return CoverLetter(
            job_id=job_id,
            job_title=job_title,
            company=company,
            text=cover_text,
            word_count=word_count,
            personalization_notes=personalization_notes
        )


# ─── Quick test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agent = CoverLetterAgent()

    result = agent.write_for_job(
        job_title="Product Manager - Analytics",
        company="Razorpay",
        jd_text="""
        We're looking for a Product Manager to own our analytics and reporting suite.
        You'll work with data engineers, design, and enterprise clients to define what
        gets built and why. We care about impact over process. You should be comfortable
        with data, have strong product instincts, and be able to communicate clearly
        to both technical and non-technical audiences.
        """,
        company_context="Razorpay is India's leading payments infrastructure company. Known for strong engineering culture and product ownership."
    )

    print(f"\n{'='*60}")
    print(f"Cover Letter — {result.job_title} @ {result.company}")
    print(f"Word count: {result.word_count}")
    print(f"{'='*60}\n")
    print(result.text)
    print(f"\n--- Personalization Notes ---")
    print(result.personalization_notes)
