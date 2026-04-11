"""
config/settings.py
──────────────────
Central settings. Now supports multiple LLM providers via LiteLLM.

To switch providers, just change LLM_PROVIDER + LLM_MODEL in your .env.
Everything else in the codebase stays the same.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"          # don't error on unknown .env keys
    )

    # ── LLM Provider (pick one, set the matching API key below) ───────────
    # Options:
    #   "anthropic"  → needs ANTHROPIC_API_KEY
    #   "gemini"     → needs GEMINI_API_KEY       (free at aistudio.google.com)
    #   "groq"       → needs GROQ_API_KEY         (free at console.groq.com)
    #   "openai"     → needs OPENAI_API_KEY
    #   "ollama"     → no key needed, runs locally (needs ollama installed)
    llm_provider: str = "gemini"

    # ── Model name per provider ────────────────────────────────────────────
    # Anthropic:  claude-sonnet-4-6 | claude-haiku-4-5-20251001
    # Gemini:     gemini/gemini-1.5-flash | gemini/gemini-1.5-pro
    # Groq:       groq/llama-3.1-70b-versatile | groq/mixtral-8x7b-32768
    # OpenAI:     gpt-4o-mini | gpt-4o
    # Ollama:     ollama/llama3.2 | ollama/mistral
    llm_model: str = "gemini/gemini-1.5-flash"

    # ── API Keys (only the one matching your provider is required) ─────────
    anthropic_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""
    openai_api_key: str = ""
    # Ollama needs no key — it runs on localhost:11434

    # ── Platform credentials ───────────────────────────────────────────────
    linkedin_email: str = ""
    linkedin_password: str = ""
    naukri_email: str = ""
    naukri_password: str = ""
    wellfound_email: str = ""
    wellfound_password: str = ""

    # ── App config ─────────────────────────────────────────────────────────
    database_url: str = "sqlite:///./floww.db"
    profile_path: str = "data/profile/indira_profile.json"
    log_level: str = "INFO"

    # ── Job search preferences ─────────────────────────────────────────────
    target_roles: str = "Product Manager,Senior Software Engineer,APM,SDE II"
    max_jobs_per_platform: int = 50
    ats_score_threshold: int = 85

    @property
    def target_roles_list(self) -> list[str]:
        return [r.strip() for r in self.target_roles.split(",")]

    @property
    def project_root(self) -> Path:
        return Path(__file__).parent.parent

    @property
    def active_api_key(self) -> str:
        """Return whichever API key matches the current provider."""
        return {
            "anthropic": self.anthropic_api_key,
            "gemini": self.gemini_api_key,
            "groq": self.groq_api_key,
            "openai": self.openai_api_key,
            "ollama": "",
        }.get(self.llm_provider, "")


settings = Settings()
