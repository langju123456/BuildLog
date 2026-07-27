"""Tests for pipeline orchestration."""

from __future__ import annotations

import json
from pathlib import Path

from buildlog.config import load_settings
from buildlog.pipeline import run_pipeline
from buildlog.sqlalchemy_repository import SQLAlchemyRunRepository


class FakeClient:
    """Deterministic client used in place of LLM calls."""

    def complete_json(self, prompt: str, schema: type):
        name = schema.__name__
        if name == "StoryPlan":
            return schema.model_validate(
                {
                    "central_idea": "Adapter boundaries made the local agent easier to reason about.",
                    "hook": "I ran into a compatibility issue while moving an agent tutorial local.",
                    "technical_points": ["LiteLLM", "Ollama", "Qwen3"],
                    "decision_story": "I kept the tutorial structure and changed only the model adapter.",
                    "reader_value": "Small adapter boundaries make debugging clearer.",
                    "ending": "The useful lesson was the boundary, not the tool list.",
                }
            )
        return schema.model_validate(
            {
                "technical_accuracy": 6,
                "specificity": 8,
                "readability": 8,
                "reader_value": 8,
                "evidence_coverage": 8,
                "unsupported_claims": ["unsupported duration"],
                "vague_sections": [],
                "revision_instructions": ["Remove the unsupported duration."],
                "hard_failure": False,
            }
        )

    def complete_text(self, prompt: str) -> str:
        if "constrained reviser" in prompt:
            return "Revised draft using only supported evidence."
        return "First draft with one weak claim."


def test_one_revision_limit(tmp_path: Path, monkeypatch) -> None:
    input_path = tmp_path / "iteration.json"
    fixture = Path(__file__).parent / "fixtures" / "valid_iteration.json"
    input_path.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    settings = load_settings(Path.cwd())
    settings = settings.__class__(
        **{
            **settings.__dict__,
            "runs_dir": tmp_path / "runs",
            "database_url": f"sqlite:///{tmp_path / 'buildlog.db'}",
        }
    )
    repository = SQLAlchemyRunRepository(settings.database_url)
    repository.initialize()

    import buildlog.pipeline as pipeline

    monkeypatch.setattr(pipeline, "LLMClient", lambda settings: FakeClient())

    result = run_pipeline(input_path, settings, repository)

    revised_files = list(result.run_dir.glob("05_revised_draft.md"))
    stored_run = repository.get_run(result.run_dir.name)
    artifact_types = {
        artifact.artifact_type for artifact in repository.list_artifacts(result.run_dir.name)
    }
    stored_evaluation = repository.get_evaluation(result.run_dir.name)

    assert result.revision_performed
    assert len(revised_files) == 1
    assert result.final_path.read_text(encoding="utf-8").startswith("Revised draft")
    assert stored_run is not None
    assert stored_run.status == "completed"
    assert stored_run.revision_performed
    assert "revised_draft" in artifact_types
    assert "final" in artifact_types
    assert stored_evaluation is not None
    assert stored_evaluation.technical_accuracy == 6
