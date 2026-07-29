"""Environment-backed configuration for BuildLog."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the BuildLog pipeline."""

    model: str
    model_digest: str | None
    api_base: str | None
    temperature: float
    max_tokens: int
    threshold_accuracy: int
    threshold_specificity: int
    threshold_readability: int
    threshold_value: int
    threshold_evidence: int
    prompt_version: str
    prompts_dir: Path
    runs_dir: Path
    database_url: str


def load_settings(project_root: Path | None = None) -> Settings:
    """Load settings from environment variables and defaults."""
    import os

    root = project_root or Path.cwd()
    load_dotenv(root / ".env")
    return Settings(
        model=os.getenv("BUILDLOG_MODEL", "ollama_chat/qwen3"),
        model_digest=os.getenv("BUILDLOG_MODEL_DIGEST") or None,
        api_base=os.getenv("BUILDLOG_API_BASE", "http://127.0.0.1:11434"),
        temperature=float(os.getenv("BUILDLOG_TEMPERATURE", "0.4")),
        max_tokens=int(os.getenv("BUILDLOG_MAX_TOKENS", "2200")),
        threshold_accuracy=int(os.getenv("BUILDLOG_EVAL_THRESHOLD_ACCURACY", "8")),
        threshold_specificity=int(os.getenv("BUILDLOG_EVAL_THRESHOLD_SPECIFICITY", "7")),
        threshold_readability=int(os.getenv("BUILDLOG_EVAL_THRESHOLD_READABILITY", "7")),
        threshold_value=int(os.getenv("BUILDLOG_EVAL_THRESHOLD_VALUE", "7")),
        threshold_evidence=int(os.getenv("BUILDLOG_EVAL_THRESHOLD_EVIDENCE", "7")),
        prompt_version=os.getenv("BUILDLOG_PROMPT_VERSION", "v1"),
        prompts_dir=root / "prompts",
        runs_dir=root / "runs",
        database_url=os.getenv("BUILDLOG_DATABASE_URL", f"sqlite:///{root / 'buildlog.db'}"),
    )
