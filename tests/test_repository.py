"""Tests for SQLAlchemy metadata persistence."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import inspect

from buildlog.domain import (
    ArtifactRecord,
    EvaluationRecord,
    IterationRecord,
    ProjectRecord,
    PromptVersionRecord,
    RunRecord,
)
from buildlog.sqlalchemy_repository import SQLAlchemyRunRepository

EXPECTED_TABLES = {
    "artifact_dependencies",
    "artifacts",
    "error_observations",
    "evaluations",
    "iterations",
    "llm_call_observations",
    "projects",
    "prompt_versions",
    "run_observations",
    "runs",
    "step_observations",
}


def test_database_creation(tmp_path: Path) -> None:
    repository = _repository(tmp_path)

    assert set(inspect(repository.engine).get_table_names()) == EXPECTED_TABLES


def test_run_persistence(tmp_path: Path) -> None:
    repository = _repository_with_run(tmp_path)

    repository.complete_run("run-001", True, datetime.now(UTC))
    stored = repository.get_run("run-001")

    assert stored is not None
    assert stored.iteration_id == "iteration-001"
    assert stored.status == "completed"
    assert stored.revision_performed
    assert stored.planner_prompt_version_id == "planner-v1-hash"


def test_evaluation_persistence(tmp_path: Path) -> None:
    repository = _repository_with_run(tmp_path)
    repository.save_evaluation(
        EvaluationRecord(
            id="evaluation-001",
            run_id="run-001",
            technical_accuracy=8,
            specificity=7,
            readability=9,
            reader_value=8,
            evidence_coverage=7,
            feedback={
                "unsupported_claims": [],
                "revision_instructions": ["Tighten the ending."],
            },
        )
    )

    stored = repository.get_evaluation("run-001")

    assert stored is not None
    assert stored.technical_accuracy == 8
    assert stored.feedback["revision_instructions"] == ["Tighten the ending."]


def test_artifact_relationships(tmp_path: Path) -> None:
    repository = _repository_with_run(tmp_path)
    repository.save_artifact(
        ArtifactRecord(
            id="artifact-001",
            run_id="run-001",
            artifact_type="final",
            file_path="/tmp/run-001/06_final.md",
            content_hash="a" * 64,
        )
    )

    artifacts = repository.list_artifacts("run-001")

    assert len(artifacts) == 1
    assert artifacts[0].run_id == "run-001"
    assert artifacts[0].artifact_type == "final"
    assert artifacts[0].content_hash == "a" * 64


def _repository(tmp_path: Path) -> SQLAlchemyRunRepository:
    repository = SQLAlchemyRunRepository(f"sqlite:///{tmp_path / 'buildlog.db'}")
    repository.initialize()
    return repository


def _repository_with_run(tmp_path: Path) -> SQLAlchemyRunRepository:
    repository = _repository(tmp_path)
    repository.save_project(ProjectRecord(id="project-001", name="Project"))
    repository.save_iteration(
        IterationRecord(
            id="iteration-001",
            project_id="project-001",
            title="Iteration",
            goal="Ship a small pipeline.",
            context="Local development.",
            problem="Metadata was file-only.",
            audience="Engineers",
            raw_input={"id": "iteration-001"},
        )
    )
    prompt_ids: dict[str, str] = {}
    for name in ("planner", "writer", "evaluator", "reviser"):
        prompt_id = f"{name}-v1-hash"
        prompt_ids[name] = prompt_id
        repository.save_prompt_version(
            PromptVersionRecord(
                id=prompt_id,
                prompt_name=name,
                version="v1",
                file_path=f"/tmp/{name}_v1.md",
                content_hash=name.ljust(64, "0"),
            )
        )
    repository.save_run(
        RunRecord(
            id="run-001",
            iteration_id="iteration-001",
            model="ollama_chat/qwen3:8b",
            planner_prompt_version_id=prompt_ids["planner"],
            writer_prompt_version_id=prompt_ids["writer"],
            evaluator_prompt_version_id=prompt_ids["evaluator"],
            reviser_prompt_version_id=prompt_ids["reviser"],
        )
    )
    return repository
