"""
core/resume_generator.py
─────────────────────────
Generates ATS-friendly PDF and DOCX resumes from optimized content.

ATS-friendly means:
  - Single column layout (no tables for structure, no text boxes)
  - Standard fonts: Calibri, Arial, Times New Roman
  - No images, no fancy headers
  - Clean section names: Summary, Experience, Skills, Education
  - Readable by both machines AND humans

We generate DOCX (via python-docx) and PDF (via reportlab).
DOCX is easier to edit; PDF is what most platforms want to upload.
"""

from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from core.models import OptimizedResume
from agents.resume_optimizer_agent import BASE_RESUME_SECTIONS
from config.settings import settings


# ─── Output paths ─────────────────────────────────────────────────────────────

def _resume_output_dir() -> Path:
    out = Path(settings.project_root) / "data" / "resumes"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _filename(company: str, role: str, ext: str) -> str:
    safe = lambda s: s.replace(" ", "_").replace("/", "-")[:30]
    ts = datetime.now().strftime("%m%d")
    return f"Indira_Nandepu_{safe(role)}_{safe(company)}_{ts}.{ext}"


# ─── PDF Generator ────────────────────────────────────────────────────────────

def generate_pdf(optimized: OptimizedResume) -> Path:
    """
    Generate an ATS-optimized PDF resume.

    Returns path to the generated PDF.
    """
    out_dir = _resume_output_dir()
    filename = _filename(optimized.company, optimized.job_title, "pdf")
    out_path = out_dir / filename

    # Merge optimized sections with originals
    sections = _merge_sections(optimized)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = _build_styles()
    story = []

    # ── Header ──────────────────────────────────────────────────────────
    story.append(Paragraph("Indira Nandepu", styles["name"]))
    story.append(Paragraph(
        "inandepu@gmail.com  |  linkedin.com/in/indira-nandepu  |  Hyderabad, Telangana",
        styles["contact"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#2C3E50")))
    story.append(Spacer(1, 0.3 * cm))

    # ── Summary (if present) ─────────────────────────────────────────────
    if sections.get("summary"):
        story.append(Paragraph("SUMMARY", styles["section_header"]))
        story.append(Paragraph(sections["summary"], styles["body"]))
        story.append(Spacer(1, 0.3 * cm))

    # ── Experience ───────────────────────────────────────────────────────
    story.append(Paragraph("EXPERIENCE", styles["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BDC3C7")))
    story.append(Spacer(1, 0.15 * cm))

    for key in ["experience_gep_full", "experience_gep_intern"]:
        if sections.get(key):
            _add_experience_block(story, sections[key], styles)
            story.append(Spacer(1, 0.2 * cm))

    # ── Skills ───────────────────────────────────────────────────────────
    if sections.get("skills"):
        story.append(Paragraph("TECHNICAL SKILLS", styles["section_header"]))
        story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BDC3C7")))
        story.append(Spacer(1, 0.15 * cm))
        for line in sections["skills"].split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["body"]))
        story.append(Spacer(1, 0.3 * cm))

    # ── Projects ─────────────────────────────────────────────────────────
    if sections.get("projects"):
        story.append(Paragraph("PROJECTS", styles["section_header"]))
        story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BDC3C7")))
        story.append(Spacer(1, 0.15 * cm))
        for line in sections["projects"].split("\n"):
            if line.strip():
                prefix = "• " if line.strip().startswith("•") else ""
                text = line.strip().lstrip("•").strip()
                style = styles["bullet"] if prefix else styles["job_title"]
                story.append(Paragraph(f"{prefix}{text}", style))
        story.append(Spacer(1, 0.3 * cm))

    # ── Recognitions ─────────────────────────────────────────────────────
    if sections.get("recognitions"):
        story.append(Paragraph("RECOGNITIONS", styles["section_header"]))
        story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BDC3C7")))
        story.append(Spacer(1, 0.15 * cm))
        for line in sections["recognitions"].split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["body"]))
        story.append(Spacer(1, 0.3 * cm))

    # ── Education ────────────────────────────────────────────────────────
    if sections.get("education"):
        story.append(Paragraph("EDUCATION", styles["section_header"]))
        story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor("#BDC3C7")))
        story.append(Spacer(1, 0.15 * cm))
        for line in sections["education"].split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["body"]))

    doc.build(story)
    return out_path


def _add_experience_block(story, text: str, styles: dict):
    """Parse and render one experience block with proper formatting."""
    lines = text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "|" in line and any(year in line for year in ["2022", "2023", "2024", "2025", "Present"]):
            # This is the role/company/date header line
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                story.append(Paragraph(f"<b>{parts[0]}</b>  |  {parts[1]}", styles["job_title"]))
                if len(parts) >= 4:
                    story.append(Paragraph(f"{parts[2]}  |  {parts[3]}", styles["job_meta"]))
        elif line.startswith("•"):
            story.append(Paragraph(line, styles["bullet"]))
        else:
            story.append(Paragraph(line, styles["body"]))


def _build_styles() -> dict:
    """Build all paragraph styles for the PDF."""
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle("name", fontSize=18, fontName="Helvetica-Bold",
                               alignment=TA_CENTER, spaceAfter=2, textColor=colors.HexColor("#1A252F")),
        "contact": ParagraphStyle("contact", fontSize=9, fontName="Helvetica",
                                  alignment=TA_CENTER, textColor=colors.HexColor("#5D6D7E")),
        "section_header": ParagraphStyle("section_header", fontSize=10, fontName="Helvetica-Bold",
                                          spaceBefore=6, spaceAfter=2,
                                          textColor=colors.HexColor("#2C3E50"),
                                          letterSpacing=1),
        "job_title": ParagraphStyle("job_title", fontSize=10, fontName="Helvetica-Bold",
                                     spaceBefore=4, textColor=colors.HexColor("#1A252F")),
        "job_meta": ParagraphStyle("job_meta", fontSize=9, fontName="Helvetica-Oblique",
                                    textColor=colors.HexColor("#7F8C8D")),
        "bullet": ParagraphStyle("bullet", fontSize=9.5, fontName="Helvetica",
                                  leftIndent=12, spaceAfter=2, leading=13,
                                  textColor=colors.HexColor("#2C3E50")),
        "body": ParagraphStyle("body", fontSize=9.5, fontName="Helvetica",
                                spaceAfter=2, leading=13, textColor=colors.HexColor("#2C3E50")),
    }


def _merge_sections(optimized: OptimizedResume) -> dict[str, str]:
    """Merge optimized sections with base resume sections."""
    optimized_map = {s.section_name: s.optimized_text for s in optimized.sections}
    result = {}
    for name, original in BASE_RESUME_SECTIONS.items():
        result[name] = optimized_map.get(name, original)
    return result


# ─── Cover letter PDF ─────────────────────────────────────────────────────────

def generate_cover_letter_pdf(company: str, job_title: str, text: str) -> Path:
    """Generate a simple, clean cover letter PDF."""
    out_dir = _resume_output_dir()
    filename = _filename(company, f"CL_{job_title}", "pdf")
    out_path = out_dir / filename

    styles = _build_styles()
    doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                             rightMargin=3*cm, leftMargin=3*cm,
                             topMargin=3*cm, bottomMargin=3*cm)
    story = []

    # Date
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), styles["body"]))
    story.append(Spacer(1, 0.5*cm))

    # Body paragraphs
    for para in text.split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para, styles["body"]))
            story.append(Spacer(1, 0.35*cm))

    # Signature
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Sincerely,", styles["body"]))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph("<b>Indira Nandepu</b>", styles["body"]))
    story.append(Paragraph("inandepu@gmail.com  |  linkedin.com/in/indira-nandepu", styles["body"]))

    doc.build(story)
    return out_path
