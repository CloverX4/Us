"""
agents/recruiter_reply_agent.py
────────────────────────────────
Handles all recruiter communications:
  1. Inbound messages (LinkedIn InMail, Naukri messages, Instahyre)
  2. Proactive outreach to recruiters at target companies

This agent is lean — it doesn't need many tools.
The main work is writing in Indira's voice, briefly and memorably.

Why this matters:
  Most people either ignore recruiter messages or send back walls of text.
  A sharp, specific, 3-sentence reply that shows you actually read the JD
  cuts through noise better than any resume optimization.
"""

from core.models import RecruiterMessage
from core.profile import profile
from agents.base import BaseAgent, Tool
from datetime import datetime


class RecruiterReplyAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self._register_tools()

    @property
    def system_prompt(self) -> str:
        return profile.build_system_prompt("recruiter_reply")

    def _register_tools(self):

        self.register_tool(Tool(
            name="get_relevant_hook",
            description=(
                "Get a relevant hook/talking point for a specific role or company type. "
                "Use this to make the reply feel specific, not templated."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "role_type": {
                        "type": "string",
                        "enum": ["product_manager", "senior_sde", "apm", "data_engineer", "general"],
                        "description": "Role type to get a hook for"
                    },
                    "company_stage": {
                        "type": "string",
                        "enum": ["startup", "series_a_b", "late_stage", "enterprise", "unknown"],
                        "description": "Stage of the company"
                    }
                },
                "required": ["role_type"]
            },
            function=self._tool_get_hook
        ))

    def _tool_get_hook(self, role_type: str, company_stage: str = "unknown") -> str:
        hooks = {
            "product_manager": (
                "I've been the engineer in the room asking 'but why is this the right feature?' "
                "for 2 years — that's actually what drew me to PM. At GEP I've owned AI feature delivery, "
                "pushed back on scoped requirements, and shipped things that reduced user workflows from 8 "
                "clicks to 2. I want the title that matches the work."
            ),
            "senior_sde": (
                "I've shipped full-stack AI systems in production — RAG pipelines, FastAPI backends, "
                "Angular frontends — and I've seen what happens when engineering doesn't talk to product. "
                "I'm the kind of engineer who asks 'what does success look like for the user?' before "
                "writing a single line."
            ),
            "apm": (
                "APM roles are where I want to be — I have the technical depth to earn credibility with "
                "engineering teams and the product instincts I've been sharpening in practice. "
                "I've been doing the PM work; now I want to do it with the right title."
            ),
            "data_engineer": (
                "Data engineering is where I've done some of my most impactful work — from migrating "
                "Power BI's DAX queries to SQL on Azure Databricks (potential $2M+ cost reduction) to "
                "building RAG-based AI pipelines that cut analyst workflows by 75%."
            ),
            "general": (
                "I'm a software engineer at GEP Worldwide with a track record of shipping things that "
                "actually move metrics — $2M+ cost reduction, AI features reducing workflows from 8 clicks "
                "to 2, 4x Change Agent recognition. I'm actively looking for my next challenge."
            )
        }

        startup_note = ""
        if company_stage == "startup":
            startup_note = " Early-stage especially interests me — I want to own product decisions, not just implement them."
        elif company_stage == "series_a_b":
            startup_note = " Series A/B is a sweet spot for me — enough traction to have real users, enough greenfield to actually shape the product."

        return hooks.get(role_type, hooks["general"]) + startup_note

    def reply_to_recruiter(
        self,
        recruiter_name: str,
        recruiter_company: str,
        their_message: str,
        platform: str = "linkedin",
        job_id: int | None = None
    ) -> RecruiterMessage:
        """
        Generate a reply to an inbound recruiter message.

        Args:
            recruiter_name: Their name
            recruiter_company: Company they're recruiting for
            their_message: The message they sent
            platform: Where the message came from
            job_id: Linked job ID if we have one

        Returns:
            RecruiterMessage with our generated reply
        """
        goal = f"""
A recruiter has messaged Indira on {platform}. Write her reply.

Recruiter: {recruiter_name} from {recruiter_company}
Their message:
---
{their_message}
---

Process:
1. Assess what role/type they're recruiting for
2. Get a relevant hook for that role type
3. Write a reply that:
   - Opens by acknowledging something specific from their message (not "Thank you for reaching out")
   - Positions Indira in 1-2 sentences using the hook
   - Expresses genuine interest if the role is relevant
   - Asks for a specific next step (call? send JD? connect?)
   - Is under 120 words total

If the role doesn't seem like a fit (e.g., 10+ years required, unrelated domain),
write a polite decline that leaves the door open.

Output the reply text directly.
"""

        reply_text = self.run(goal)

        from core.models import Platform
        platform_enum = Platform(platform) if platform in [p.value for p in Platform] else Platform.OTHER

        return RecruiterMessage(
            job_id=job_id,
            platform=platform_enum,
            recruiter_name=recruiter_name,
            recruiter_company=recruiter_company,
            message_text=their_message,
            our_reply=reply_text,
            replied_at=datetime.utcnow()
        )

    def write_proactive_outreach(
        self,
        target_name: str,
        target_company: str,
        target_role: str,
        reason_for_interest: str
    ) -> str:
        """
        Write a proactive message to send to a recruiter or hiring manager.
        Use this for cold outreach on LinkedIn.
        """
        goal = f"""
Write a proactive LinkedIn connection message from Indira to a recruiter/hiring manager.

Target: {target_name} at {target_company}
Role they're hiring for (if known): {target_role}
Why Indira is interested: {reason_for_interest}

Rules:
- LinkedIn connection messages max 300 characters (the short note field)
- For InMail, max 200 words
- Must feel human and specific, not copy-paste
- Reference something real about their company or role
- End with a soft ask (would love to connect / happy to share more)

Write both versions:
CONNECTION_NOTE (under 300 chars):
[text]

INMAIL (under 200 words):
[text]
"""
        return self.run(goal)


# ─── Quick test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agent = RecruiterReplyAgent()

    result = agent.reply_to_recruiter(
        recruiter_name="Priya Sharma",
        recruiter_company="Razorpay",
        their_message="""
        Hi Indira, I came across your profile and was impressed by your experience
        in AI-driven analytics at GEP. We have an open Product Manager role on our
        analytics platform team. The role involves owning the product roadmap for
        our reporting and insights features. Would you be open to a quick call to
        discuss? Let me know a good time.
        """,
        platform="linkedin"
    )

    print(f"\n{'='*60}")
    print(f"Reply to {result.recruiter_name} @ {result.recruiter_company}")
    print(f"{'='*60}\n")
    print(result.our_reply)
