"""
connectors/linkedin/apply.py
──────────────────────────────
LinkedIn Easy Apply automation.

Easy Apply is LinkedIn's one-click apply flow — no external redirect.
The form has variable fields (name, phone, resume upload, cover letter, screening questions).
This handles the common cases and gracefully skips complex forms.

Flow:
  1. Go to job URL
  2. Click "Easy Apply" button
  3. Handle each form step (may be multiple pages):
     - Contact info (usually pre-filled)
     - Resume upload (upload our optimized PDF)
     - Cover letter (paste our generated text)
     - Screening questions (answer common ones, flag unknown ones)
  4. Submit or return NEEDS_REVIEW if there are questions we can't answer

⚠️  LinkedIn Easy Apply forms vary wildly by company. Some are 1 step, some are 5+.
    We handle the common patterns and flag anything unusual for manual review.
"""

import asyncio
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout
from connectors.base import BaseConnector
from rich.console import Console

console = Console()


class ApplyResult(str, Enum):
    SUCCESS = "success"
    NEEDS_REVIEW = "needs_review"      # Complex form — needs human to finish
    NOT_EASY_APPLY = "not_easy_apply"  # External application link
    ALREADY_APPLIED = "already_applied"
    ERROR = "error"


@dataclass
class ApplicationOutcome:
    result: ApplyResult
    message: str = ""
    screenshot_path: str = ""  # screenshot of final state for review


class LinkedInApplyConnector(BaseConnector):
    """Handles LinkedIn Easy Apply form submission."""

    PLATFORM_NAME = "linkedin"

    async def _do_login(self, email: str, password: str) -> bool:
        # Reuse same login logic as search connector
        from connectors.linkedin.connector import LinkedInConnector
        # Login by navigating — cookies will be shared via the same session dir
        try:
            await self._page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            await self._random_delay(1, 2)
            await self._page.fill("#username", email)
            await self._page.fill("#password", password)
            await self._page.click('[data-litms-control-urn="login-submit"]')
            await self._page.wait_for_load_state("networkidle", timeout=15000)
            return await self._verify_logged_in()
        except Exception:
            return False

    async def _verify_logged_in(self) -> bool:
        try:
            await self._page.goto("https://www.linkedin.com/feed/", timeout=8000)
            return "feed" in self._page.url
        except Exception:
            return False

    async def _do_search(self, *args, **kwargs):
        pass  # not used in apply connector

    async def _do_get_detail(self, *args, **kwargs):
        return ""

    async def apply_to_job(
        self,
        job_url: str,
        resume_pdf_path: str,
        cover_letter_text: str,
        phone_number: str = ""
    ) -> ApplicationOutcome:
        """
        Attempt to apply to a job via LinkedIn Easy Apply.

        Args:
            job_url: LinkedIn job URL
            resume_pdf_path: Path to the optimized resume PDF
            cover_letter_text: Cover letter text to paste
            phone_number: Phone number for contact form

        Returns:
            ApplicationOutcome indicating success/failure/needs-review
        """
        try:
            await self._page.goto(job_url, wait_until="domcontentloaded", timeout=15000)
            await self._random_delay(2, 3)

            # Check if already applied
            if await self._page.query_selector(".artdeco-inline-feedback--success"):
                return ApplicationOutcome(
                    result=ApplyResult.ALREADY_APPLIED,
                    message="Already applied to this job"
                )

            # Find Easy Apply button
            easy_apply_btn = await self._find_easy_apply_button()
            if not easy_apply_btn:
                return ApplicationOutcome(
                    result=ApplyResult.NOT_EASY_APPLY,
                    message="No Easy Apply button found — this job uses an external application"
                )

            await easy_apply_btn.click()
            await self._random_delay(1.5, 2.5)

            # Handle the multi-step form
            return await self._handle_application_form(resume_pdf_path, cover_letter_text, phone_number)

        except PlaywrightTimeout:
            return ApplicationOutcome(result=ApplyResult.ERROR, message="Page timed out")
        except Exception as e:
            return ApplicationOutcome(result=ApplyResult.ERROR, message=str(e))

    async def _find_easy_apply_button(self):
        """Find the Easy Apply button on a job page."""
        selectors = [
            ".jobs-apply-button--top-card",
            "button.jobs-apply-button",
            "button[aria-label*='Easy Apply']",
            ".jobs-s-apply button",
        ]
        for selector in selectors:
            btn = await self._page.query_selector(selector)
            if btn:
                text = (await btn.inner_text()).lower()
                if "easy apply" in text:
                    return btn
        return None

    async def _handle_application_form(
        self,
        resume_pdf_path: str,
        cover_letter_text: str,
        phone_number: str
    ) -> ApplicationOutcome:
        """
        Walk through the Easy Apply form steps.

        LinkedIn forms can have 1-5+ steps. Each step has a "Next" or "Submit" button.
        We try to fill what we know and flag what we don't.
        """
        max_steps = 8
        for step in range(max_steps):
            await self._random_delay(1, 2)

            # Check what's on this step
            step_content = await self._page.content()

            # ── Fill phone if asked ──────────────────────────────────────
            phone_field = await self._page.query_selector(
                'input[id*="phone"], input[name*="phone"], input[aria-label*="Phone"]'
            )
            if phone_field and phone_number:
                current = await phone_field.input_value()
                if not current:
                    await phone_field.fill(phone_number)

            # ── Upload resume ────────────────────────────────────────────
            resume_upload = await self._page.query_selector(
                'input[type="file"][accept*="pdf"], input[type="file"][name*="resume"]'
            )
            if resume_upload and Path(resume_pdf_path).exists():
                await resume_upload.set_input_files(resume_pdf_path)
                await self._random_delay(1, 2)
                console.print(f"  [green]Resume uploaded[/green]")

            # ── Fill cover letter ────────────────────────────────────────
            cover_letter_field = await self._page.query_selector(
                'textarea[id*="cover"], textarea[aria-label*="cover"], textarea[placeholder*="cover"]'
            )
            if cover_letter_field and cover_letter_text:
                await cover_letter_field.fill(cover_letter_text)

            # ── Handle Yes/No screening questions (common ones) ──────────
            await self._answer_common_questions()

            # ── Check for unhandled required fields ──────────────────────
            unfilled = await self._find_unfilled_required_fields()
            if unfilled:
                screenshot_path = await self._take_screenshot(f"step_{step}_needs_review")
                return ApplicationOutcome(
                    result=ApplyResult.NEEDS_REVIEW,
                    message=f"Step {step + 1} has fields we can't auto-fill: {unfilled}. Screenshot saved.",
                    screenshot_path=screenshot_path
                )

            # ── Check for Submit button (final step) ─────────────────────
            submit_btn = await self._page.query_selector(
                "button[aria-label='Submit application'], button:has-text('Submit application')"
            )
            if submit_btn:
                await submit_btn.click()
                await self._random_delay(2, 3)
                return ApplicationOutcome(
                    result=ApplyResult.SUCCESS,
                    message="Application submitted successfully"
                )

            # ── Click Next to go to next step ────────────────────────────
            next_btn = await self._page.query_selector(
                "button[aria-label='Continue to next step'], button:has-text('Next')"
            )
            if next_btn:
                await next_btn.click()
            else:
                # No next, no submit — something unexpected
                screenshot_path = await self._take_screenshot(f"step_{step}_stuck")
                return ApplicationOutcome(
                    result=ApplyResult.NEEDS_REVIEW,
                    message=f"Stuck at step {step + 1} — no Next or Submit button found",
                    screenshot_path=screenshot_path
                )

        return ApplicationOutcome(
            result=ApplyResult.NEEDS_REVIEW,
            message="Exceeded max form steps — manual review needed"
        )

    async def _answer_common_questions(self):
        """Answer common Yes/No and radio screening questions."""
        # Common Yes/No questions we can confidently answer
        yes_patterns = [
            "authorized to work",
            "legally authorized",
            "eligible to work",
            "currently located",
            "agree to",
        ]
        no_patterns = [
            "require sponsorship",
            "visa sponsorship",
            "require work authorization",
        ]

        # Handle radio buttons
        radios = await self._page.query_selector_all('fieldset input[type="radio"]')
        for radio in radios:
            label = await radio.get_attribute("aria-label") or ""
            label_lower = label.lower()

            parent = await radio.query_selector("xpath=ancestor::fieldset[1]")
            question_text = ""
            if parent:
                question_text = (await parent.inner_text()).lower()

            if any(p in question_text for p in yes_patterns):
                if "yes" in label_lower:
                    await radio.click()
            elif any(p in question_text for p in no_patterns):
                if "no" in label_lower:
                    await radio.click()

        # Handle dropdowns with Yes/No options
        selects = await self._page.query_selector_all("select")
        for select in selects:
            options = await select.query_selector_all("option")
            option_texts = [await o.inner_text() for o in options]
            if "Yes" in option_texts and "No" in option_texts:
                # Get parent question text
                parent_text = ""
                try:
                    container = await select.query_selector("xpath=ancestor::div[3]")
                    if container:
                        parent_text = (await container.inner_text()).lower()
                except Exception:
                    pass

                if any(p in parent_text for p in yes_patterns):
                    await select.select_option("Yes")
                elif any(p in parent_text for p in no_patterns):
                    await select.select_option("No")

    async def _find_unfilled_required_fields(self) -> list[str]:
        """Return labels of required fields that are still empty."""
        unfilled = []
        required_fields = await self._page.query_selector_all(
            'input[required]:not([type="file"]):not([type="hidden"]), '
            'textarea[required], select[required]'
        )
        for field in required_fields:
            value = await field.input_value() if hasattr(field, "input_value") else ""
            if not value:
                label = await field.get_attribute("aria-label") or await field.get_attribute("placeholder") or "unknown"
                unfilled.append(label)
        return unfilled

    async def _take_screenshot(self, name: str) -> str:
        """Save a screenshot for manual review."""
        screenshots_dir = Path("data") / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        path = screenshots_dir / f"{name}.png"
        await self._page.screenshot(path=str(path))
        return str(path)
