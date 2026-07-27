"""Orchestrate the BuildLog v0.1 pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from buildlog.config import Settings
from buildlog.evaluator import evaluate_draft, passes_thresholds
from buildlog.exceptions import PersistenceError
from buildlog.input_loader import load_iteration
from buildlog.llm_client import LLMClient
from buildlog.planner import create_plan
from buildlog.preprocessor import normalize_iteration
from buildlog.prompt_loader import inspect_prompt_files
from buildlog.repository import RunRepository
from buildlog.reviser import revise_draft
from buildlog.run_persistence import (
    create_run_record,
    persist_artifact,
    persist_evaluation,
    persist_run_inputs,
)
from buildlog.trace import create_run_trace
from buildlog.writer import write_draft

LOGGER = logging.getLogger(__name__)
HUMAN_REVIEW_WARNING = (
    "\n\n---\n\n"
    "Human review required before publishing: check for secrets, API keys, "
    "employer-confidential information, customer data, private repository details, "
    "and unpublished business information.\n"
)


@dataclass(frozen=True)
class PipelineResult:
    """Summary of a completed BuildLog run."""

    run_dir: Path
    final_path: Path
    evaluation_scores: dict[str, int]
    revision_performed: bool


def run_pipeline(
    input_path: Path,
    settings: Settings,
    repository: RunRepository,
) -> PipelineResult:
    """Run the complete BuildLog pipeline for one iteration file."""
    LOGGER.info("pipeline start")
    iteration = load_iteration(input_path)
    LOGGER.info("validation success")
    normalized = normalize_iteration(iteration)
    prompts = inspect_prompt_files(settings.prompts_dir)
    persist_run_inputs(repository, iteration, normalized, prompts)

    trace = create_run_trace(settings.runs_dir, iteration.id)
    run_id = trace.run_dir.name
    repository.save_run(create_run_record(run_id, normalized, settings, prompts))

    try:
        input_artifact = trace.write_json("00_input.json", iteration)
        persist_artifact(repository, run_id, "input", input_artifact)

        normalized_artifact = trace.write_json("01_normalized_input.json", normalized)
        persist_artifact(repository, run_id, "normalized_input", normalized_artifact)

        client = LLMClient(settings)

        LOGGER.info("planner start")
        plan = create_plan(normalized, client, settings)
        plan_artifact = trace.write_json("02_plan.json", plan)
        persist_artifact(repository, run_id, "plan", plan_artifact)
        LOGGER.info("planner complete")

        LOGGER.info("writer start")
        draft = write_draft(normalized, plan, client, settings)
        draft_artifact = trace.write_text("03_draft.md", draft)
        persist_artifact(repository, run_id, "draft", draft_artifact)
        LOGGER.info("writer complete")

        LOGGER.info("evaluator start")
        evaluation = evaluate_draft(normalized, draft, client, settings)
        evaluation_artifact = trace.write_json("04_evaluation.json", evaluation)
        persist_artifact(repository, run_id, "evaluation", evaluation_artifact)
        persist_evaluation(repository, run_id, evaluation)
        LOGGER.info("evaluator complete")

        revision_performed = False
        final_draft = draft
        if not passes_thresholds(evaluation, settings):
            LOGGER.info("revision required")
            revision_performed = True
            final_draft = revise_draft(normalized, draft, evaluation, client, settings)
            revised_artifact = trace.write_text("05_revised_draft.md", final_draft)
            persist_artifact(repository, run_id, "revised_draft", revised_artifact)
        else:
            LOGGER.info("revision not required")

        final_path = trace.write_text("06_final.md", final_draft + HUMAN_REVIEW_WARNING)
        persist_artifact(repository, run_id, "final", final_path)
        metadata_path = trace.write_json(
            "run_metadata.json",
            {
                "run_id": run_id,
                "iteration_id": normalized.id,
                "model": settings.model,
                "prompt_versions": {
                    name: prompt.version for name, prompt in prompts.items()
                },
                "revision_performed": revision_performed,
                "status": "completed",
            },
        )
        persist_artifact(repository, run_id, "run_metadata", metadata_path)
        repository.complete_run(run_id, revision_performed, datetime.now(UTC))
    except Exception as exc:
        _mark_run_failed(repository, run_id, exc)
        raise

    LOGGER.info("pipeline complete")
    return PipelineResult(
        run_dir=trace.run_dir,
        final_path=final_path,
        evaluation_scores={
            "technical_accuracy": evaluation.technical_accuracy,
            "specificity": evaluation.specificity,
            "readability": evaluation.readability,
            "reader_value": evaluation.reader_value,
            "evidence_coverage": evaluation.evidence_coverage,
        },
        revision_performed=revision_performed,
    )


def _mark_run_failed(repository: RunRepository, run_id: str, error: Exception) -> None:
    try:
        repository.fail_run(run_id, str(error), datetime.now(UTC))
    except PersistenceError:
        LOGGER.exception("could not mark failed run %s", run_id)
