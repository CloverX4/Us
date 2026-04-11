"""
core/profile.py
───────────────
Loads and provides Indira's profile to agents.

Every agent that generates text (resume, cover letter, recruiter reply)
gets the profile injected into its system prompt. This is what keeps
the "personal touch" intact even in automated output.

Usage:
    from core.profile import profile
    system_prompt = profile.build_system_prompt("cover_letter")
"""

import json
from pathlib import Path
from functools import lru_cache
from config.settings import settings


class UserProfile:
    def __init__(self, profile_data: dict):
        self.data = profile_data

    @property
    def name(self) -> str:
        return self.data["personal"]["name"]

    @property
    def email(self) -> str:
        return self.data["personal"]["email"]

    @property
    def target_roles(self) -> list[dict]:
        return self.data["target_roles"]

    @property
    def primary_role(self) -> str:
        return self.target_roles[0]["title"]

    @property
    def career_narrative(self) -> str:
        return self.data["career_narrative"]

    @property
    def key_achievements(self) -> list[dict]:
        return self.data["key_achievements"]

    @property
    def voice_guide(self) -> dict:
        return self.data["voice_guide"]

    @property
    def personality(self) -> dict:
        return self.data["personality"]

    def build_system_prompt(self, agent_type: str) -> str:
        """
        Builds a rich system prompt for a specific agent type.
        This is the main function agents call to get their instructions.

        agent_type options:
          - "resume_optimizer"
          - "cover_letter"
          - "recruiter_reply"
          - "job_discovery"
        """
        base = self._base_identity_block()

        if agent_type == "resume_optimizer":
            return base + self._resume_optimizer_instructions()
        elif agent_type == "cover_letter":
            return base + self._cover_letter_instructions()
        elif agent_type == "recruiter_reply":
            return base + self._recruiter_reply_instructions()
        elif agent_type == "job_discovery":
            return base + self._job_discovery_instructions()
        else:
            return base

    def _base_identity_block(self) -> str:
        """Core identity block injected into every agent prompt."""
        achievements = "\n".join([
            f"  - {a['title']}: {a['impact']}"
            for a in self.key_achievements
        ])
        traits = "\n".join([f"  - {t}" for t in self.personality["traits"]])
        values = "\n".join([f"  - {v}" for v in self.personality["values"]])

        return f"""You are working on behalf of {self.name}, a software engineer based in Hyderabad who is actively job searching.

## Their Career Story
{self.career_narrative}

## Key Achievements (use these for evidence)
{achievements}

## Who They Are (personality & working style)
{traits}

## What They Value in a Role
{values}

## Communication Style
Tone: {self.personality["tone"]}
They are a {self.personality["communication_style"]} — leads with context before conclusions, uses specific examples over generalities, and never sounds corporate or stiff.

"""

    def _resume_optimizer_instructions(self) -> str:
        return """## Your Task: Resume Optimization
You are optimizing Indira's resume for a specific job description.

Rules:
1. **ATS First**: Extract every keyword, skill, and phrase from the JD. Incorporate them naturally.
2. **Never fabricate**: Only use what's in her actual experience. Reframe, don't invent.
3. **Quantify everything**: If a bullet can have a number, add one. Numbers cut through noise.
4. **Action verbs**: Every bullet starts with a strong past-tense verb. No "responsible for".
5. **Mirror the JD language**: If they say "cross-functional collaboration", use that phrase.
6. **PM framing for PM roles**: For PM applications, frame engineering work in product terms:
   - "Contributed to AI reporting" → "Defined and shipped AI reporting features serving 24+ viz types"
   - Lead with user impact, not implementation detail
7. **Target ATS score ≥ 95**: Run your internal check after each section.

What NOT to change:
- Her core experiences and companies (those are facts)
- Her education (NIT Warangal — that's a strong signal, keep it prominent)
- Her recognitions (4x Change Agents is rare — keep all of them)
"""

    def _cover_letter_instructions(self) -> str:
        voice_rules = "\n".join([f"  - {r}" for r in self.voice_guide["language_rules"]])
        structure = "\n".join([f"  {i+1}. {s}" for i, s in enumerate(self.voice_guide["cover_letter_structure"])])
        differentiators = "\n".join([f"  - {d}" for d in self.voice_guide["what_makes_her_different"]])

        return f"""## Your Task: Cover Letter Writing
Write a cover letter that sounds like Indira — not like a template.

## Structure (follow this exactly)
{structure}

## Voice Rules
{voice_rules}

## What Makes Her Stand Out (weave these in naturally)
{differentiators}

## Hard Rules
- Max 350 words. Recruiters don't read beyond that.
- Never start with "I am writing to express my interest in..."
- Never end with "I look forward to hearing from you at your earliest convenience"
- Include at least one specific metric from her achievements
- For PM roles: explicitly address the career transition with confidence, not apology
"""

    def _recruiter_reply_instructions(self) -> str:
        structure = "\n".join([f"  {i+1}. {s}" for i, s in enumerate(self.voice_guide["recruiter_reply_structure"])])

        return f"""## Your Task: Recruiter Reply
Write a reply to a recruiter message on behalf of Indira.

## Structure
{structure}

## Rules
- Keep it under 150 words — recruiters are busy
- Be warm but confident, not eager or desperate
- Reference something specific about the role/company to show you actually read it
- If it's a PM role, briefly acknowledge the transition and frame it as a strength
- End with a specific ask (call, time to connect, next step) — not vague interest
"""

    def _job_discovery_instructions(self) -> str:
        roles = "\n".join([f"  - {r['title']} ({', '.join(r['seniority_levels'])})" for r in self.target_roles])

        return f"""## Your Task: Job Discovery
Find relevant job postings for Indira and assess their fit.

## Target Roles
{roles}

## Relevance Criteria (score 0-1)
High (0.8-1.0):
  - PM/APM roles at product-led companies (B2B SaaS, consumer, fintech, early-stage)
  - Senior SDE at companies where engineers influence product decisions
  - Roles with "data", "AI", "analytics" in scope — she has deep experience here
  - Companies that mention experimentation, user research, feedback loops

Medium (0.5-0.7):
  - SDE roles at large tech companies (still good, just not primary focus)
  - PM roles at large enterprises (more political, less ownership — flag this)

Low/Skip (< 0.5):
  - Pure maintenance/support roles
  - Roles requiring 5+ years PM experience (she's transitioning)
  - Roles at companies known for toxic culture or no work-life balance

## Location
  - Hyderabad preferred
  - Remote-friendly roles are also good
  - Not relocating internationally right now
"""


@lru_cache(maxsize=1)
def load_profile() -> UserProfile:
    """Load profile once and cache it. Call this everywhere."""
    profile_path = Path(settings.project_root) / settings.profile_path
    with open(profile_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return UserProfile(data)


# Convenience singleton — `from core.profile import profile`
profile = load_profile()
