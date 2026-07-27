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
- Run traces
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

## Persistence boundary

The filesystem is the inspectable source for generated JSON and Markdown.
SQLite indexes projects, iterations, runs, prompt versions, evaluations, and
artifact paths and hashes. It does not provide authentication, an API, a UI, or
publishing.

## Documentation

Read [`PROJECT.md`](PROJECT.md) for the complete product definition, architecture, domain model, workflow, evaluation strategy, repository structure, and implementation instructions.

## Status

BuildLog is currently in its first implementation iteration.

```text
One real iteration in.
One evidence-grounded LinkedIn post out.
```
