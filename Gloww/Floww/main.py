"""
main.py
───────
Entry point for Floww.

Run modes:
  python main.py test-ats            → test the ATS scorer (no API key needed)
  python main.py test-resume         → test resume optimizer agent
  python main.py test-cover-letter   → test cover letter agent
  python main.py test-recruiter      → test recruiter reply agent
  python main.py test-discover-yc    → test job discovery on YC (no login needed)
  python main.py discover            → run full job discovery
  python main.py pipeline            → run application pipeline for all pending jobs
  python main.py pipeline --dry-run  → optimize + cover letters but don't apply
  python main.py api                 → start the FastAPI server (http://localhost:8000)
  python main.py setup               → first-time setup
"""

import sys
from rich.console import Console
from rich.panel import Panel

console = Console()


def print_banner():
    console.print(Panel.fit(
        "[bold cyan]Floww[/bold cyan] — Automated Job Application System\n"
        "[dim]Built for Indira Nandepu[/dim]",
        border_style="cyan"
    ))


def test_ats():
    """Quick test: score a resume against a sample JD."""
    from core.ats_scorer import score_resume

    jd = """
    Senior Product Manager — Data & Analytics
    Must have: SQL, product roadmap, stakeholder management, agile, data-driven decision making.
    Nice to have: AI/ML product experience, enterprise B2B, Python.
    You will: Define product strategy, work with engineers and designers, measure outcomes.
    """

    resume = """
    Indira Nandepu — Software Engineer
    Led migration from Power BI DAX to SQL on Azure Databricks Delta Tables. $2M+ cost savings.
    Built AI-driven RAG reporting system with FastAPI, OpenAI, ChromaDB. 24+ visualization types.
    Reduced consultant workflows from 8 clicks to 2. Resolved 70+ enterprise incidents in 3 months.
    4x Change Agent recognition. Led cross-functional delivery under tight deadlines.
    Skills: Python, SQL, FastAPI, Angular, Azure Databricks, ChromaDB, Qdrant, Elasticsearch.
    Education: B.Tech CSE, NIT Warangal.
    """

    result = score_resume(resume, jd)

    console.print(f"\n[bold]ATS Score:[/bold] {result.score}/100")
    console.print(f"[bold]Breakdown:[/bold] {result.breakdown}")
    console.print(f"\n[bold]Matched ({len(result.matched_keywords)}):[/bold] {', '.join(result.matched_keywords[:10])}")
    console.print(f"[bold]Missing ({len(result.missing_keywords)}):[/bold] {', '.join(result.missing_keywords[:10])}")
    console.print("\n[bold]Recommendations:[/bold]")
    for rec in result.recommendations:
        console.print(f"  • {rec}")


def test_resume_optimizer():
    """Test the full resume optimizer agent."""
    from agents.resume_optimizer_agent import ResumeOptimizerAgent

    agent = ResumeOptimizerAgent()
    result = agent.run_for_job(
        job_title="Product Manager",
        company="Razorpay",
        jd_text="""
        Product Manager — Payments Analytics
        We need a PM who can own the analytics and insights features of our payments platform.
        Must have: product thinking, SQL, stakeholder management, data-driven decisions.
        Nice to have: AI/ML products, enterprise B2B, fintech.
        You'll work with engineers, designers, and enterprise clients to ship features that matter.
        """
    )

    console.print(f"\n[bold green]ATS Score: {result.ats_score}/100[/bold green]")
    console.print(f"Sections optimized: {len(result.sections)}")
    console.print(f"\n[bold]Optimization Summary:[/bold]")
    console.print(result.optimization_summary[:800])


def test_cover_letter():
    """Test the cover letter agent."""
    from agents.cover_letter_agent import CoverLetterAgent

    agent = CoverLetterAgent()
    result = agent.write_for_job(
        job_title="Associate Product Manager",
        company="Groww",
        jd_text="""
        APM at Groww — Investment Products
        We're building the investment platform for India's next generation of investors.
        We need someone who thinks about the user first, can work with data,
        and isn't afraid to challenge assumptions. Engineering background a plus.
        """,
        company_context="Groww is India's largest retail investment platform. Strong product culture, data-driven decisions, user-first thinking."
    )

    console.print(f"\n[bold]Cover Letter ({result.word_count} words):[/bold]")
    console.print(f"{'─'*60}")
    console.print(result.text)
    console.print(f"\n[dim]Personalization: {result.personalization_notes}[/dim]")


def test_recruiter_reply():
    """Test the recruiter reply agent."""
    from agents.recruiter_reply_agent import RecruiterReplyAgent

    agent = RecruiterReplyAgent()
    result = agent.reply_to_recruiter(
        recruiter_name="Ankit Mehta",
        recruiter_company="PhonePe",
        their_message="""
        Hi Indira! I noticed your background in AI and data engineering at GEP.
        We have a Product Manager opening on our analytics team at PhonePe.
        It's a high-ownership role — you'd be defining the roadmap for our
        merchant insights product. Would you be open to a 20-min call this week?
        """,
        platform="linkedin"
    )

    console.print(f"\n[bold]Reply to {result.recruiter_name} @ {result.recruiter_company}:[/bold]")
    console.print(f"{'─'*60}")
    console.print(result.our_reply)


def run_discovery():
    """Run job discovery across all configured platforms."""
    from agents.job_discovery_agent import JobDiscoveryAgent
    from core.database import create_db_tables
    create_db_tables()

    agent = JobDiscoveryAgent()

    # Parse optional args: python main.py discover --platforms yc wellfound --role "Product Manager"
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--platforms", nargs="+", default=["ycombinator", "wellfound", "linkedin"])
    parser.add_argument("--roles", nargs="+", default=None)
    parser.add_argument("--location", default="Hyderabad")
    args, _ = parser.parse_known_args()

    summary = agent.run_discovery(
        platforms=args.platforms,
        roles=args.roles,
        location=args.location
    )

    console.print(f"\n[bold]Discovery Summary:[/bold]")
    console.print(summary)


def test_discovery_yc():
    """Quick test: run discovery on YC only (no login needed)."""
    from agents.job_discovery_agent import JobDiscoveryAgent
    from core.database import create_db_tables
    create_db_tables()

    agent = JobDiscoveryAgent()
    summary = agent.run_discovery(
        platforms=["ycombinator"],
        roles=["Product Manager"],
        location="India"
    )
    console.print(f"\n[bold]YC Discovery Result:[/bold]\n{summary}")


def start_api():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


def setup():
    """First-time setup: install playwright browsers, create DB tables."""
    import subprocess
    from core.database import create_db_tables

    console.print("[bold]Running first-time setup...[/bold]")
    console.print("1. Creating database tables...")
    create_db_tables()
    console.print("[green]✓ Database ready[/green]")

    console.print("2. Installing Playwright browsers...")
    subprocess.run(["playwright", "install", "chromium"], check=True)
    console.print("[green]✓ Playwright ready[/green]")

    console.print("\n[bold green]Setup complete! Copy .env.example to .env and add your credentials.[/bold green]")


def run_pipeline_cmd():
    """Run the full application pipeline."""
    from agents.orchestrator_agent import OrchestratorAgent
    from core.database import create_db_tables
    create_db_tables()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Optimize but don't submit")
    parser.add_argument("--job-ids", nargs="+", type=int, help="Specific job IDs to process")
    args, _ = parser.parse_known_args()

    agent = OrchestratorAgent()
    result = agent.run_pipeline(job_ids=args.job_ids, dry_run=args.dry_run)
    console.print(f"\n[bold]Pipeline Result:[/bold]\n{result}")


COMMANDS = {
    "test-ats": test_ats,
    "test-resume": test_resume_optimizer,
    "test-cover-letter": test_cover_letter,
    "test-recruiter": test_recruiter_reply,
    "test-discover-yc": test_discovery_yc,
    "discover": run_discovery,
    "pipeline": run_pipeline_cmd,
    "api": start_api,
    "setup": setup,
}


if __name__ == "__main__":
    print_banner()

    if len(sys.argv) < 2:
        console.print("\nUsage: python main.py <command>")
        console.print("\nCommands:")
        for cmd in COMMANDS:
            console.print(f"  {cmd}")
        sys.exit(0)

    command = sys.argv[1]
    if command not in COMMANDS:
        console.print(f"[red]Unknown command: {command}[/red]")
        sys.exit(1)

    COMMANDS[command]()
