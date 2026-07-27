"""Prompt loading helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from buildlog.hashing import sha256_file

PROMPT_FILES = {
    "planner": ("v1", "planner_v1.md"),
    "writer": ("v1", "writer_v1.md"),
    "evaluator": ("v1", "evaluator_v1.md"),
    "reviser": ("v1", "reviser_v1.md"),
}


@dataclass(frozen=True)
class PromptFile:
    """Versioned prompt file metadata."""

    name: str
    version: str
    path: Path
    content_hash: str


def load_prompt(prompts_dir: Path, filename: str) -> str:
    """Load a prompt file from the configured prompt directory."""
    return (prompts_dir / filename).read_text(encoding="utf-8")


def inspect_prompt_files(prompts_dir: Path) -> dict[str, PromptFile]:
    """Return version and content metadata for all v0.1 prompts."""
    prompts: dict[str, PromptFile] = {}
    for name, (version, filename) in PROMPT_FILES.items():
        path = (prompts_dir / filename).resolve()
        prompts[name] = PromptFile(
            name=name,
            version=version,
            path=path,
            content_hash=sha256_file(path),
        )
    return prompts
