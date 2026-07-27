# BuildLog

BuildLog turns a real software-development iteration into an evidence-grounded LinkedIn post.

The project combines deterministic Python workflows with LLM reasoning:

```text
Development evidence
        ↓
Validation and preprocessing
        ↓
Story planning
        ↓
Draft generation
        ↓
Evaluation
        ↓
Revision
        ↓
Human review
        ↓
LinkedIn post
```

## Goal

BuildLog v0.1 has one job:

> Take one real development iteration and produce one clear, technically accurate, publishable LinkedIn draft.

The system does not invent projects, results, metrics, or business impact.

## Core principles

- Start from real work and real evidence.
- Use code for deterministic operations.
- Use LLMs only where judgment is required.
- Trace every important pipeline step.
- Evaluate high-agentic outputs.
- Keep the human in control.
- Prefer small working iterations over speculative complexity.

## Current scope

### Included

- Structured iteration input
- Input validation
- Story planning
- LinkedIn draft generation
- Draft evaluation
- One constrained revision
- Run, step, LLM-call, error, and artifact-lineage observability
- Replay metadata for input, code, prompts, model, and generation settings
- SQLite metadata and run relationships
- Markdown output

### Not included in v0.1

- Automatic LinkedIn publishing
- GitHub integration
- Web interface
- External database servers
- RAG
- Long-term memory
- Multi-platform content generation

## Example Outputs

The public architecture example is based on a real BuildLog development
iteration. Both posts were generated locally with the same Qwen3:8b model; the
prompt set changed from v1 to v2.

Follow the complete public path:

1. [Architecture iteration input](examples/buildlog_architecture_iteration.json)
2. [Generated LinkedIn post v1](examples/outputs/architecture/linkedin_v1.md)
3. [Generated LinkedIn post v2](examples/outputs/architecture/linkedin_v2.md)
4. [Output quality baseline](docs/output_quality_baseline.md)

The evaluation report compares automated scores with human editorial review.
It found that v2 improved the result but still required human review before
publishing. Complete raw traces remain local under `runs/` and are intentionally
not published.

## Planned stack

- Python
- Pydantic
- LiteLLM
- Ollama
- Qwen3
- JSON
- Markdown
- SQLite
- SQLAlchemy 2.0
- Pytest

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
cp .env.example .env
.venv/bin/python -m buildlog.main examples/local_agent_iteration.json
```

Use a model tag installed in Ollama. For example:

```bash
BUILDLOG_MODEL=ollama_chat/qwen3:8b \
  .venv/bin/python -m buildlog.main examples/local_agent_iteration.json
```

Set `BUILDLOG_PROMPT_VERSION=v2` to run the same pipeline with the versioned
v2 prompt set while preserving v1 for comparison.

Each execution writes readable artifacts under `runs/` and structured metadata
to `buildlog.db` by default. `BUILDLOG_DATABASE_URL` can point to another local
SQLite file.

Set `BUILDLOG_MODEL_DIGEST` to the immutable digest reported by the local model
runtime when it is available. A missing digest is recorded honestly and makes
the replay manifest partial; BuildLog never guesses one.

## Agent observability

Every run retains the existing content artifacts and adds three observation
views:

- `run_metadata.json` summarizes configuration, status, token availability,
  revision evidence, Git state, and replay requirements.
- `timeline.json` shows each fixed pipeline step, its status and duration, the
  slowest step, and the highest-token step when provider usage is available.
- `events.jsonl` preserves ordered run, step, LLM-call, artifact, revision, and
  error events for detailed audit.

The ten fixed steps are `validation`, `preprocessing`, `prompt_loading`,
`planner`, `writer`, `evaluator`, `revision_decision`, `reviser`,
`finalization`, and `persistence`. A step that does not run is recorded once as
`skipped`, including its reason.

BuildLog reports three independent outcomes:

- `pipeline_status`: whether content generation completed or failed.
- `observability_status`: whether telemetry capture is complete, partial, or
  failed.
- `reproducibility_status`: whether the saved evidence is sufficient to replay
  the same input, code, prompts, model, and configuration.

Replayability does not promise byte-identical model output at nonzero
temperature. Missing token usage remains `null` with an availability reason;
it is never estimated. Observability failures do not trigger another LLM call,
change the revision decision, or remove a successfully generated final draft.

## Persistence boundary

The filesystem is the inspectable source for generated JSON and Markdown.
SQLite indexes projects, iterations, runs, prompt versions, evaluations, and
artifact paths and hashes. It also provides query projections for run, step,
LLM-call, error, and direct artifact-dependency observations. SQLite does not
store full prompts, post bodies, or model responses and does not provide
authentication, an API, a UI, or publishing.

## Artifact layers

- [`runs/`](runs/) contains complete raw execution traces. These are internal
  evaluation source assets and remain ignored by Git.
- [`eval_corpus/`](eval_corpus/) is reserved for reviewed and sanitized
  evaluation records. No raw run is promoted automatically.
- [`examples/outputs/`](examples/outputs/) contains selected public examples
  that GitHub visitors can inspect without running BuildLog.
- [`docs/output_quality_baseline.md`](docs/output_quality_baseline.md) is the
  current scoring baseline for deciding whether a prompt, model, or evaluator
  change is an improvement.

## Documentation

Read [`PROJECT.md`](PROJECT.md) for the complete product definition, architecture, domain model, workflow, evaluation strategy, repository structure, and implementation instructions.

## Status

BuildLog v0.1 has a frozen local architecture, output-quality and
generalization baselines, a public example showcase, and explainable local run
observability. Generated posts still require human review before publishing.

```text
Real development evidence in.
Traceable, human-reviewed LinkedIn drafts out.
```
