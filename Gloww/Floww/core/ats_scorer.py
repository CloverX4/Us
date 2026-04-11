"""
core/ats_scorer.py
──────────────────
ATS (Applicant Tracking System) scorer.

What is ATS?
  Most companies use software to screen resumes before a human sees them.
  It scores your resume based on keyword match with the job description.
  A score below ~70 often means auto-rejection. We want 95+.

How this scorer works:
  1. Extract keywords from the JD (role-specific terms, skills, action phrases)
  2. Check how many appear in the resume
  3. Score by section (summary, experience, skills)
  4. Generate specific recommendations to close the gap

This is NOT the LLM — this is deterministic text analysis.
The LLM uses these recommendations to optimize the resume.
"""

import re
from collections import Counter
from core.models import ATSAnalysis


# ─── Keyword categories ───────────────────────────────────────────────────────

# Common filler words to ignore in keyword extraction
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "we", "our", "you", "your",
    "they", "their", "it", "its", "this", "that", "these", "those", "all",
    "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "than", "then", "too", "very", "just", "about", "above", "after",
    "before", "between", "during", "into", "through", "under", "while",
    "who", "which", "what", "when", "where", "how", "as", "if", "so",
    "not", "no", "nor", "yet", "also", "well", "can", "able", "need",
    "across", "within", "including", "ensure", "work", "team", "role",
    "position", "company", "opportunity", "candidate", "experience"
}

# High-value technical terms — these get extra weight in scoring
HIGH_VALUE_TERMS = {
    # PM terms
    "product manager", "product management", "product roadmap", "product strategy",
    "user research", "a/b testing", "experimentation", "go-to-market", "gtm",
    "okrs", "kpis", "metrics", "stakeholder", "agile", "scrum", "sprint",
    "user stories", "backlog", "prioritization", "customer discovery",
    # SDE terms
    "microservices", "api design", "system design", "distributed systems",
    "scalability", "performance", "data pipeline", "machine learning", "llm",
    "fastapi", "python", "sql", "azure", "databricks", "rag", "vector",
}


# ─── Extraction helpers ───────────────────────────────────────────────────────

def extract_keywords(text: str) -> set[str]:
    """
    Extract meaningful keywords from text.
    Returns lowercase set of single words and common 2-word phrases.
    """
    text_lower = text.lower()

    # Extract 2-word technical phrases first (e.g., "product manager", "a/b testing")
    bigrams = set()
    words = re.findall(r'\b[a-z][a-z0-9/+-]*\b', text_lower)
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if bigram in HIGH_VALUE_TERMS:
            bigrams.add(bigram)

    # Single keywords (filtered)
    single = {
        w for w in words
        if len(w) > 2 and w not in STOP_WORDS
    }

    return single | bigrams


def extract_jd_requirements(jd_text: str) -> dict[str, list[str]]:
    """
    Categorize JD keywords by type.
    Returns {"must_have": [...], "nice_to_have": [...], "skills": [...]}
    """
    must_signals = ["required", "must have", "you will", "you should", "minimum", "essential"]
    nice_signals = ["preferred", "nice to have", "bonus", "plus", "desirable"]

    lines = jd_text.lower().split("\n")
    must_have = []
    nice_to_have = []

    for line in lines:
        kws = extract_keywords(line)
        if any(sig in line for sig in must_signals):
            must_have.extend(kws)
        elif any(sig in line for sig in nice_signals):
            nice_to_have.extend(kws)

    return {
        "must_have": list(set(must_have)),
        "nice_to_have": list(set(nice_to_have)),
        "all": list(extract_keywords(jd_text))
    }


# ─── Main scorer ─────────────────────────────────────────────────────────────

def score_resume(resume_text: str, jd_text: str) -> ATSAnalysis:
    """
    Score a resume against a job description.

    Args:
        resume_text: Full text content of the resume
        jd_text: Full job description text

    Returns:
        ATSAnalysis with score, matched/missing keywords, and recommendations
    """
    resume_lower = resume_text.lower()

    # Extract keywords from JD
    jd_requirements = extract_jd_requirements(jd_text)
    jd_keywords = set(jd_requirements["all"])
    must_have = set(jd_requirements["must_have"])

    # Extract keywords from resume
    resume_keywords = extract_keywords(resume_text)

    # Keyword matching
    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    # Must-have keywords get extra penalty if missing
    missing_must_haves = must_have - resume_keywords

    # Score calculation
    # Base: keyword match ratio (60% of score)
    if len(jd_keywords) == 0:
        keyword_score = 50.0
    else:
        keyword_match_ratio = len(matched) / len(jd_keywords)
        keyword_score = keyword_match_ratio * 60

    # Must-have penalty (up to -20 if all missing)
    must_have_score = 20.0
    if len(must_have) > 0:
        must_have_coverage = 1 - (len(missing_must_haves) / len(must_have))
        must_have_score = must_have_coverage * 20

    # Section presence score (20 points)
    section_scores = _score_sections(resume_lower)
    section_total = sum(section_scores.values())

    # Total
    raw_score = keyword_score + must_have_score + section_total
    final_score = min(100.0, raw_score)  # cap at 100

    # Recommendations
    recommendations = _generate_recommendations(
        matched=matched,
        missing=missing,
        missing_must_haves=missing_must_haves,
        section_scores=section_scores,
        score=final_score
    )

    # Sort missing keywords by importance (high-value terms first)
    missing_sorted = sorted(
        list(missing),
        key=lambda k: (k in HIGH_VALUE_TERMS, len(k)),
        reverse=True
    )[:20]  # top 20 missing

    return ATSAnalysis(
        score=round(final_score, 1),
        matched_keywords=sorted(list(matched))[:30],  # top 30 matched
        missing_keywords=missing_sorted,
        section_scores=section_scores,
        recommendations=recommendations,
        breakdown=(
            f"Keyword match: {keyword_score:.1f}/60 | "
            f"Must-haves: {must_have_score:.1f}/20 | "
            f"Sections: {section_total:.1f}/20"
        )
    )


def _score_sections(resume_lower: str) -> dict[str, float]:
    """Check presence and quality of key resume sections."""
    sections = {
        "contact_info": 0.0,
        "summary": 0.0,
        "experience": 0.0,
        "skills": 0.0,
        "education": 0.0,
    }

    # Contact info (2 points)
    if "@" in resume_lower and ("linkedin" in resume_lower or "github" in resume_lower):
        sections["contact_info"] = 2.0
    elif "@" in resume_lower:
        sections["contact_info"] = 1.0

    # Summary/objective (4 points) — critical for ATS context-setting
    if any(w in resume_lower for w in ["summary", "objective", "profile", "about"]):
        sections["summary"] = 4.0

    # Experience (8 points) — most important section
    exp_score = 0.0
    if "experience" in resume_lower or "work history" in resume_lower:
        exp_score += 3.0
    # Check for quantified bullets (numbers are ATS signals)
    numbers = re.findall(r'\b\d+[%+mx]?\b', resume_lower)
    if len(numbers) >= 5:
        exp_score += 3.0
    elif len(numbers) >= 2:
        exp_score += 1.5
    # Check for action verbs
    action_verbs = ["led", "built", "developed", "designed", "managed", "delivered",
                    "improved", "reduced", "increased", "launched", "automated",
                    "created", "implemented", "optimized", "drove"]
    verb_count = sum(1 for v in action_verbs if v in resume_lower)
    if verb_count >= 5:
        exp_score += 2.0
    elif verb_count >= 2:
        exp_score += 1.0
    sections["experience"] = min(8.0, exp_score)

    # Skills (4 points)
    if "skills" in resume_lower or "technologies" in resume_lower:
        sections["skills"] = 4.0

    # Education (2 points)
    if "education" in resume_lower or "bachelor" in resume_lower or "b.tech" in resume_lower:
        sections["education"] = 2.0

    return sections


def _generate_recommendations(
    matched: set,
    missing: set,
    missing_must_haves: set,
    section_scores: dict,
    score: float
) -> list[str]:
    """Generate specific, actionable recommendations."""
    recs = []

    # Critical missing must-haves
    if missing_must_haves:
        top_missing = list(missing_must_haves)[:5]
        recs.append(
            f"CRITICAL: Add these required keywords naturally: {', '.join(top_missing)}"
        )

    # No summary section
    if section_scores.get("summary", 0) == 0:
        recs.append(
            "Add a professional summary (3-4 lines) at the top — ATS systems weight this heavily"
        )

    # Low quantification
    if section_scores.get("experience", 0) < 5:
        recs.append(
            "Add more quantified impact: use numbers, percentages, and scale in experience bullets"
        )

    # Missing high-value technical terms
    missing_high_value = [k for k in missing if k in HIGH_VALUE_TERMS][:5]
    if missing_high_value:
        recs.append(
            f"Incorporate these high-value terms: {', '.join(missing_high_value)}"
        )

    # Score-specific guidance
    if score < 70:
        recs.append(
            "Score is below threshold — significant keyword gaps. Consider restructuring experience bullets to mirror JD language."
        )
    elif score < 85:
        recs.append(
            "Good foundation — focus on weaving in missing keywords and adding a summary section."
        )
    elif score >= 95:
        recs.append("ATS score target achieved. Resume is well-optimized for this role.")

    return recs


# ─── Quick test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from rich import print as rprint

    sample_jd = """
    We're looking for a Senior Product Manager to lead our analytics platform.
    You will define the product roadmap, work with engineering and design, and
    drive data-driven decisions. Must have: experience with SQL, data analytics,
    and agile methodologies. Nice to have: experience with AI/ML products,
    A/B testing, and enterprise B2B products. You should be comfortable with
    stakeholder management and cross-functional collaboration.
    """

    sample_resume = """
    Indira Nandepu - Software Engineer
    Led migration from DAX to SQL on Azure Databricks Delta Tables.
    Built AI-driven reporting with FastAPI, OpenAI, and ChromaDB.
    Reduced workflow clicks from 8 to 2. Delivered 24+ visualization types.
    Resolved 70+ incidents for enterprise clients. 4x Change Agent recognition.
    Skills: Python, SQL, FastAPI, Angular, Azure Databricks, ChromaDB, Elasticsearch.
    Education: B.Tech CSE, NIT Warangal.
    """

    result = score_resume(sample_resume, sample_jd)
    rprint(f"\n[bold]ATS Score:[/bold] {result.score}/100")
    rprint(f"[bold]Breakdown:[/bold] {result.breakdown}")
    rprint(f"[bold]Matched keywords:[/bold] {result.matched_keywords[:10]}")
    rprint(f"[bold]Missing keywords:[/bold] {result.missing_keywords[:10]}")
    rprint("\n[bold]Recommendations:[/bold]")
    for rec in result.recommendations:
        rprint(f"  • {rec}")
