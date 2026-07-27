# BuildLog — Project Specification

> This file is the primary product and engineering context for humans and coding agents working on BuildLog.

---

## 1. Project identity

**Name:** BuildLog

**Current version:** v0.1

**Project type:** AI-assisted developer tool

**Primary output:** LinkedIn post draft

**Primary user:** A developer who wants to convert real development work into accurate, reusable technical content

---

## 2. Vision

BuildLog is an AI-assisted workspace for preserving and reusing the value created during software development.

Software development produces more than code. It produces:

- problem understanding
- debugging knowledge
- architecture decisions
- trade-off analysis
- failed attempts
- implementation lessons
- reusable technical insight

Most of this disappears after the code works.

Git records what changed, but it rarely preserves why the change mattered, what alternatives were considered, what failed, or what the developer learned.

BuildLog captures one real development iteration and transforms it into structured, evidence-grounded technical content.

The long-term goal is not content generation for its own sake.

The long-term goal is to preserve, organize, evaluate, and reuse the value created through real engineering work.

---

## 3. Problem statement

Developers regularly solve meaningful problems but struggle to communicate that work.

Common outcomes include:

- GitHub repositories with little explanation
- generic LinkedIn posts
- outdated portfolios
- weak resume bullets
- forgotten technical decisions
- repeated debugging work
- undocumented lessons
- content that exaggerates what was actually built

Existing content-generation tools often begin with a writing request and ask the model to create a compelling story.

This creates several risks:

- hallucinated results
- exaggerated business impact
- unsupported technical claims
- generic writing
- loss of the developer's real reasoning
- unstable output quality

BuildLog begins with structured development evidence rather than a blank prompt.

---

## 4. Product goal

### v0.1 goal

BuildLog v0.1 must:

> Transform one real software-development iteration into one technically accurate, specific, readable, and useful LinkedIn post draft.

### Input

One structured development iteration.

### Output

One Markdown file containing a LinkedIn post draft.

### Success condition

A user can provide evidence from a real development iteration, run the pipeline, inspect every major intermediate artifact, and receive a final draft that requires only human review or light editing.

---

## 5. Non-goals for v0.1

The following are explicitly outside the current implementation scope:

- automatic LinkedIn authentication
- automatic LinkedIn publishing
- scraping LinkedIn
- GitHub API integration
- automatic Git-diff collection
- screenshot understanding
- web browsing
- vector databases
- RAG
- persistent user memory
- external database servers
- database-backed authentication
- database migrations beyond table creation on startup
- multi-user accounts
- web application
- mobile application
- analytics dashboard
- autonomous multi-agent organization
- unbounded self-revision
- resume generation
- portfolio generation
- article generation
- content scheduling

These may be considered later, but they must not block v0.1.

---

## 6. Product philosophy

### 6.1 Start from a real need

The project must begin with real user work, not with a technology looking for a use case.

The sequence is:

```text
Real need
    ↓
Observed friction
    ↓
Defined problem
    ↓
Evidence
    ↓
Decision
    ↓
Implementation
    ↓
Validation
    ↓
Iteration
```

Technology is a mechanism, not the objective.

### 6.2 Iteration is the unit of work

BuildLog is organized around an `Iteration`.

An iteration can represent:

- a debugging session
- a feature implementation
- an architecture decision
- a failed experiment
- a compatibility fix
- a deployment improvement
- a workflow redesign
- a product experiment
- a lesson from actual use

An iteration does not need to be a major milestone.

It only needs to contain meaningful evidence of problem-solving.

### 6.3 Deterministic work belongs in code

Never use an LLM for operations that can be implemented reliably with normal code.

Examples:

- loading files
- checking file existence
- validating fields
- parsing JSON
- sorting timestamps
- creating directories
- generating run IDs
- enforcing revision limits
- applying numeric thresholds
- writing Markdown files

### 6.4 LLMs are used for judgment

Use an LLM only when the task requires interpretation, selection, synthesis, or language generation.

Examples:

- selecting the strongest story
- identifying the most useful technical insight
- explaining why a decision mattered
- describing trade-offs
- adapting detail for the target audience
- evaluating clarity and specificity
- revising weak writing

### 6.5 High-agentic steps require evaluation

The more freedom a model has, the more inspection and evaluation the system must provide.

Every major LLM output must be:

- stored
- inspectable
- associated with a prompt version
- evaluated where appropriate
- reproducible as far as practical

### 6.6 Human approval is mandatory

The system generates a draft.

It does not decide whether the post is true, safe to publish, confidential, or representative of the user.

The human remains responsible for final approval.

---

## 7. Domain model

The primary domain object is `Iteration`.

### 7.1 Iteration

```text
Iteration
├── id
├── title
├── goal
├── context
├── problem
├── actions
├── decisions
├── trade_offs
├── result
├── lessons
├── evidence
├── audience
├── created_at
└── metadata
```

### 7.2 Field definitions

#### `id`

Unique identifier for the iteration.

#### `title`

Short human-readable name.

#### `goal`

What the developer was trying to achieve.

#### `context`

Relevant background needed to understand the work.

#### `problem`

The concrete friction, failure, limitation, or uncertainty addressed.

#### `actions`

Steps actually taken.

#### `decisions`

Important choices made during the iteration.

Each decision should contain:

```text
decision
reason
alternatives_considered
```

#### `trade_offs`

Costs, limitations, or compromises associated with a decision.

#### `result`

What happened after the implementation.

The result must not contain unsupported metrics.

#### `lessons`

Reusable knowledge derived from the work.

#### `evidence`

Facts supporting the final narrative.

Examples:

- terminal output
- test result
- observed behavior
- code change
- error message
- working pipeline
- benchmark result
- screenshot reference
- commit reference

#### `audience`

The intended readers.

Example:

```text
AI engineers, software engineers, and technical recruiters
```

#### `metadata`

Optional structured context such as:

- project name
- repository
- branch
- tools used
- model used
- operating system
- tags

---

## 8. Example input schema

```json
{
  "id": "local-agent-001",
  "title": "Running my first local AI agent",
  "goal": "Run the Hugging Face Agents Course example locally with Ollama and Qwen3.",
  "context": "The original example used a hosted model, while the goal was to understand and run the full pipeline locally.",
  "problem": "The model backend and installed Gradio version were incompatible with the original tutorial defaults.",
  "actions": [
    "Replaced the hosted model wrapper with LiteLLMModel.",
    "Connected LiteLLMModel to the local Ollama endpoint.",
    "Used Qwen3 as the local model.",
    "Changed only the incompatible Gradio arguments."
  ],
  "decisions": [
    {
      "decision": "Preserve the original tutorial structure.",
      "reason": "A large rewrite would hide the pipeline being studied.",
      "alternatives_considered": [
        "Rewrite the application around a different framework."
      ]
    },
    {
      "decision": "Use LiteLLM as the model adapter.",
      "reason": "The application could change model backends without changing the rest of the agent workflow.",
      "alternatives_considered": [
        "Call Ollama directly from every model-dependent component."
      ]
    }
  ],
  "trade_offs": [
    "The local model may be slower than a hosted endpoint.",
    "Preserving the tutorial structure limits architectural cleanup in this iteration."
  ],
  "result": "The Gradio interface successfully completed the local agent pipeline through smolagents, LiteLLM, Ollama, and Qwen3.",
  "lessons": [
    "Adapter layers reduce coupling between applications and model providers.",
    "Minimal compatibility changes make debugging easier.",
    "A working agent pipeline depends on clear boundaries between UI, framework, model adapter, and model runtime."
  ],
  "evidence": [
    "Ollama served the selected Qwen3 model locally.",
    "The Gradio interface returned a valid response.",
    "The final execution path was Gradio -> smolagents -> LiteLLM -> Ollama -> Qwen3."
  ],
  "audience": "AI engineers, software engineers, and technical recruiters",
  "metadata": {
    "project": "Local AI Agent",
    "language": "Python",
    "tools": [
      "smolagents",
      "LiteLLM",
      "Ollama",
      "Qwen3",
      "Gradio"
    ]
  }
}
```

---

## 9. Business logic

### 9.1 Main workflow

```text
1. User supplies one iteration JSON file.
2. The system loads the file.
3. Pydantic validates the schema.
4. Deterministic preprocessing normalizes the input.
5. The planner selects the central story.
6. The writer creates the first LinkedIn draft.
7. The evaluator scores the draft.
8. Code compares scores with fixed thresholds.
9. If required, the reviser performs one revision.
10. The system stores all artifacts.
11. The final Markdown draft is returned for human review.
```

### 9.2 Revision rule

Only one automatic revision is allowed in v0.1.

```text
Draft
  ↓
Evaluation
  ↓
Pass ───────────────→ Final
  ↓
Fail
  ↓
One revision
  ↓
Final
```

No autonomous infinite loop is permitted.

### 9.3 Evidence rule

Every factual claim in the generated post must be supported by the input.

The system must not invent:

- performance numbers
- user counts
- revenue
- deployment scale
- production usage
- hiring outcomes
- business impact
- development duration
- technologies not listed in the input

### 9.4 Privacy rule

The user is responsible for removing confidential information before input.

The system should include a final human-review warning reminding the user to check:

- secrets
- API keys
- employer-confidential information
- customer data
- private repository details
- unpublished business information

---

## 10. System architecture

```text
┌─────────────────────────────┐
│       Iteration JSON        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Input Loader + Validation   │  Deterministic
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Normalization               │  Deterministic
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Story Planner               │  LLM
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ LinkedIn Writer             │  LLM
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Draft Evaluator             │  LLM + fixed rubric
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Threshold Decision          │  Deterministic
└───────┬─────────────────────┘
        │
        ├── pass ────────────────┐
        │                        │
        ▼                        │
┌─────────────────────────────┐  │
│ Constrained Reviser         │  │ LLM
└──────────────┬──────────────┘  │
               │                 │
               └─────────────────┘
                         │
                         ▼
┌─────────────────────────────┐
│ Filesystem + SQLite Output  │  Deterministic
└─────────────────────────────┘
```

---

## 11. Agentic boundaries

### 11.1 Low-agentic components

These must be implemented as ordinary Python modules:

- configuration loading
- path handling
- JSON loading
- schema validation
- whitespace normalization
- run ID generation
- trace-directory creation
- output persistence
- content hashing
- SQLite metadata persistence
- score threshold comparison
- revision-count enforcement
- error handling
- logging

### 11.2 High-agentic components

These may use an LLM:

#### Planner

Purpose:

- identify the strongest evidence-grounded narrative
- determine the central engineering lesson
- select useful technical details
- avoid generic storytelling

Structured output:

```text
central_idea
hook
technical_points
decision_story
reader_value
ending
```

#### Writer

Purpose:

- convert the iteration and plan into a LinkedIn draft
- preserve technical accuracy
- communicate a useful engineering lesson
- avoid exaggerated language

#### Evaluator

Purpose:

- score the draft
- identify unsupported claims
- identify vague language
- provide actionable revision instructions

#### Reviser

Purpose:

- revise the draft based on evaluator feedback
- remove unsupported claims
- increase specificity using existing evidence
- preserve the original meaning

---

## 12. Evaluation strategy

### 12.1 Evaluation dimensions

Each draft receives a score from 1 to 10 for:

#### Technical accuracy

Are all technical claims supported by the input?

#### Specificity

Does the post contain concrete problems, decisions, tools, and results?

#### Readability

Is the post clear, concise, and easy to follow?

#### Reader value

Does the reader receive a transferable lesson or useful insight?

#### Evidence coverage

Does the draft use the most relevant supplied evidence without inventing new facts?

### 12.2 Hard-failure conditions

A draft must be revised if it contains:

- unsupported metrics
- invented business impact
- technologies absent from the evidence
- false production claims
- confidential-looking values
- contradictions with the iteration input

### 12.3 Suggested thresholds

```text
technical_accuracy >= 8
specificity >= 7
readability >= 7
reader_value >= 7
evidence_coverage >= 7
```

Technical accuracy is the highest-priority dimension.

### 12.4 Future evaluation improvements

Not required for v0.1:

- claim extraction
- claim-to-evidence mapping
- deterministic word-count checks
- cliché detection
- repeated-phrase detection
- human rating storage
- prompt-version comparison
- model comparison
- regression test dataset

---

## 13. Trace and observability

Every run must create a unique directory.

Example:

```text
runs/
└── 2026-07-27T19-30-12_local-agent-001/
    ├── 00_input.json
    ├── 01_normalized_input.json
    ├── 02_plan.json
    ├── 03_draft.md
    ├── 04_evaluation.json
    ├── 05_revised_draft.md
    ├── 06_final.md
    └── run_metadata.json
```

### `run_metadata.json`

Should contain:

```json
{
  "run_id": "2026-07-27T19-30-12_local-agent-001",
  "iteration_id": "local-agent-001",
  "model": "ollama_chat/qwen3",
  "prompt_versions": {
    "planner": "v1",
    "writer": "v1",
    "evaluator": "v1",
    "reviser": "v1"
  },
  "revision_performed": true,
  "status": "completed"
}
```

### Logging requirements

Logs should record:

- pipeline start
- validation success or failure
- each component start and completion
- model-call failure
- JSON parsing failure
- evaluation result
- revision decision
- final output path

Do not log secrets or full environment variables.

### Hybrid persistence

BuildLog v0.1 is not a disposable file-only script. It uses two persistence
mechanisms with separate responsibilities:

- the filesystem stores readable JSON and Markdown artifacts under `runs/`
- SQLite stores structured metadata, relationships, statuses, scores, paths,
  and SHA-256 content hashes

Required SQLite tables:

1. `projects`: `id`, `name`, `description`, `created_at`, `updated_at`
2. `iterations`: `id`, `project_id`, `title`, `goal`, `context`, `problem`,
   `audience`, `raw_input_json`, `created_at`
3. `runs`: `id`, `iteration_id`, `model`, `status`, `revision_performed`,
   `started_at`, `completed_at`, `error_message`, and four prompt-version
   foreign keys
4. `artifacts`: `id`, `run_id`, `artifact_type`, `file_path`, `content_hash`,
   `created_at`
5. `evaluations`: `id`, `run_id`, five rubric scores, `feedback_json`,
   `created_at`
6. `prompt_versions`: `id`, `prompt_name`, `version`, `file_path`,
   `content_hash`, `created_at`

Relationships:

- one project has many iterations
- one iteration has many runs
- one run has many artifacts and at most one evaluation
- each run records the exact planner, writer, evaluator, and reviser prompt
  versions available for that execution

Business logic must not depend directly on SQLAlchemy persistence models.
Domain records and a minimal repository protocol form the boundary between the
pipeline and persistence. The SQLAlchemy-backed repository is the only v0.1
implementation.

Creating tables on startup is acceptable for v0.1. Do not add Alembic, async
database access, repository factories, or an additional service layer.

---

## 14. Technical stack

### Required for v0.1

| Area | Technology |
|---|---|
| Language | Python |
| Data validation | Pydantic |
| Model abstraction | LiteLLM |
| Local model runtime | Ollama |
| Initial model | Qwen3 |
| Configuration | python-dotenv |
| Input format | JSON |
| Output format | Markdown |
| Metadata persistence | SQLite |
| Database access | SQLAlchemy 2.0 |
| Testing | Pytest |
| Logging | Python `logging` |
| Packaging | `pyproject.toml` |
| Version control | Git + GitHub |

### Optional later

| Area | Technology |
|---|---|
| API | FastAPI |
| UI | Gradio or Streamlit |
| External database | PostgreSQL |
| Workflow graph | LangGraph |
| Observability | LangSmith, OpenTelemetry, or custom traces |
| Cloud deployment | Docker + AWS/Azure/GCP |

### Framework decision

Do not introduce an agent framework in v0.1 unless the implementation clearly requires it.

A normal Python pipeline is preferred because:

- the workflow is mostly fixed
- only specific stages require model judgment
- explicit control improves reliability
- traces are easier to understand
- revision count must remain bounded

---

## 15. Planned repository structure

```text
BuildLog/
├── README.md
├── PROJECT.md
├── TASK.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── examples/
│   ├── local_agent_iteration.json
│   └── buildlog_architecture_iteration.json
├── prompts/
│   ├── planner_v1.md
│   ├── planner_v2.md
│   ├── writer_v1.md
│   ├── writer_v2.md
│   ├── evaluator_v1.md
│   ├── evaluator_v2.md
│   ├── reviser_v1.md
│   └── reviser_v2.md
├── src/
│   └── buildlog/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models.py
│       ├── domain.py
│       ├── hashing.py
│       ├── input_loader.py
│       ├── preprocessor.py
│       ├── llm_client.py
│       ├── planner.py
│       ├── writer.py
│       ├── evaluator.py
│       ├── reviser.py
│       ├── pipeline.py
│       ├── trace.py
│       ├── repository.py
│       ├── run_persistence.py
│       ├── persistence_models.py
│       ├── sqlalchemy_repository.py
│       └── exceptions.py
├── tests/
│   ├── test_models.py
│   ├── test_input_loader.py
│   ├── test_preprocessor.py
│   ├── test_threshold_logic.py
│   ├── test_repository.py
│   ├── test_pipeline.py
│   ├── test_prompt_loader.py
│   ├── test_trace.py
│   └── fixtures/
│       └── valid_iteration.json
├── runs/
│   └── .gitkeep
└── docs/
    ├── ideas.md
    └── output_quality_baseline.md
```

---

## 16. Module responsibilities

### `main.py`

- command-line entry point
- accepts input path
- starts pipeline
- prints final result path
- returns non-zero exit code on failure

### `config.py`

- loads environment variables
- exposes validated settings
- contains no business logic

### `models.py`

- defines Pydantic domain models
- validates required fields
- rejects blank list entries
- defines planner and evaluator output schemas

### `input_loader.py`

- checks path existence
- loads JSON
- returns validated `Iteration`

### `preprocessor.py`

- normalizes whitespace
- removes exact duplicate list entries
- preserves semantic content
- must not use an LLM

### `llm_client.py`

- wraps LiteLLM
- supports text and structured JSON output
- centralizes retries and errors
- does not contain prompts

### `planner.py`

- loads planner prompt
- generates structured `StoryPlan`

### `writer.py`

- loads writer prompt
- generates first Markdown draft

### `evaluator.py`

- loads evaluation prompt
- returns structured scores and feedback

### `reviser.py`

- performs one constrained revision

### `pipeline.py`

- coordinates components
- contains revision decision logic
- does not contain prompt text

### `trace.py`

- creates run directory
- writes readable JSON and Markdown artifacts
- writes run metadata
- computes artifact content hashes

### `domain.py`

- defines persistence-facing domain records
- contains no SQLAlchemy imports

### `hashing.py`

- computes deterministic SHA-256 hashes for files
- contains no persistence logic

### `repository.py`

- defines the minimal persistence protocol used by the pipeline
- exposes only current v0.1 use cases

### `run_persistence.py`

- maps validated pipeline data to persistence-facing domain records
- records artifact hashes and evaluation feedback through the repository
- contains no SQLAlchemy imports

### `persistence_models.py`

- defines SQLAlchemy table mappings
- contains no pipeline business logic

### `sqlalchemy_repository.py`

- creates the SQLite schema on startup
- implements the repository protocol
- stores run relationships, scores, paths, and hashes

### `exceptions.py`

Defines project-specific exceptions such as:

- `InputFileError`
- `ValidationError`
- `ModelResponseError`
- `StructuredOutputError`
- `TraceWriteError`

---

## 17. Prompt requirements

Prompts are source code and must be versioned.

### Planner prompt rules

The planner must:

- use only supplied evidence
- identify one central story
- prefer engineering decisions over generic motivation
- avoid presenting routine setup as a major breakthrough
- return structured JSON

### Writer prompt rules

The writer must:

- use first person
- begin with a concrete problem, observation, or decision
- explain what changed and why it mattered
- include supported technical details
- provide a reusable lesson
- avoid exaggerated language
- avoid fake metrics
- avoid unsupported production claims
- produce approximately 180–350 words
- use no more than five hashtags
- return only the post

Avoid phrases such as:

- thrilled to announce
- excited to share
- game changer
- revolutionary
- cutting-edge solution
- groundbreaking
- transformed everything

### Evaluator prompt rules

The evaluator must:

- compare the draft against the original iteration
- score every rubric dimension
- list unsupported claims
- identify vague sections
- provide actionable revision instructions
- return structured JSON

### Reviser prompt rules

The reviser must:

- follow evaluator feedback
- preserve supported facts
- remove unsupported claims
- improve specificity only from existing evidence
- return only the revised post

---

## 18. Coding standards

All coding agents must follow these rules.

### Architecture

- Prefer explicit pipelines over hidden autonomy.
- Use one responsibility per module.
- Keep domain models independent of model providers.
- Keep prompts outside Python source files.
- Keep model calls behind one client abstraction.
- Do not add frameworks without a demonstrated need.

### Python

- Use Python type hints.
- Use Pydantic for external data validation.
- Use `pathlib.Path` for file paths.
- Use custom exceptions for domain failures.
- Use small functions with clear names.
- Add docstrings to public functions and classes.
- Avoid global mutable state.
- Do not suppress exceptions without logging.
- Do not store secrets in source control.

### Reliability

- Validate all model-generated structured data.
- Fail clearly when JSON output is invalid.
- Store raw model output when parsing fails.
- Limit automatic retries.
- Limit revision to one pass.
- Never silently replace missing evidence.
- Never invent default facts.

### Testing

At minimum, test:

- valid input
- missing required field
- blank list values
- missing input file
- invalid JSON
- duplicate normalization
- evaluation threshold pass
- evaluation threshold fail
- one-revision limit
- trace-directory creation

LLM calls should be mocked in unit tests.

---

## 19. CLI behavior

Initial command:

```bash
python -m buildlog.main examples/local_agent_iteration.json
```

Expected output:

```text
BuildLog completed.

Run:
runs/2026-07-27T19-30-12_local-agent-001

Final draft:
runs/2026-07-27T19-30-12_local-agent-001/06_final.md

Evaluation:
technical_accuracy: 9
specificity: 8
readability: 8
reader_value: 8
evidence_coverage: 9

Revision performed: no
```

Failure example:

```text
BuildLog failed: input field "evidence" must contain at least one non-empty item.
```

The process must return:

- exit code `0` on success
- non-zero exit code on failure

---

## 20. Environment configuration

Suggested `.env.example`:

```env
BUILDLOG_MODEL=ollama_chat/qwen3
BUILDLOG_API_BASE=http://127.0.0.1:11434
BUILDLOG_TEMPERATURE=0.4
BUILDLOG_MAX_TOKENS=2200
BUILDLOG_PROMPT_VERSION=v1
BUILDLOG_EVAL_THRESHOLD_ACCURACY=8
BUILDLOG_EVAL_THRESHOLD_SPECIFICITY=7
BUILDLOG_EVAL_THRESHOLD_READABILITY=7
BUILDLOG_EVAL_THRESHOLD_VALUE=7
BUILDLOG_EVAL_THRESHOLD_EVIDENCE=7
BUILDLOG_DATABASE_URL=sqlite:///buildlog.db
```

No real secrets should be committed.

---

## 21. Definition of done for v0.1

v0.1 is complete when:

- [ ] The repository installs locally.
- [ ] A sample iteration JSON is included.
- [ ] Invalid input produces a clear error.
- [ ] The planner returns validated structured output.
- [ ] The writer produces a LinkedIn Markdown draft.
- [ ] The evaluator returns validated scores and feedback.
- [ ] Threshold logic is deterministic.
- [ ] At most one revision occurs.
- [ ] Every pipeline artifact is stored.
- [ ] SQLite tables are created on startup.
- [ ] Project, iteration, run, artifact, evaluation, and prompt metadata are persisted.
- [ ] Artifact and prompt paths and SHA-256 hashes are persisted.
- [ ] Domain and business logic do not import SQLAlchemy models.
- [ ] The final draft is written to Markdown.
- [ ] Unit tests cover deterministic behavior.
- [ ] The README explains how to run the project.
- [ ] No automatic LinkedIn publishing exists.
- [ ] No unsupported claims are present in the sample result.

---

## 22. Current implementation iteration

### Objective

Build the smallest complete local pipeline that transforms the existing local-agent development experience into a LinkedIn draft.

### Required sequence

```text
Create project structure
        ↓
Define Pydantic models
        ↓
Create sample iteration input
        ↓
Implement deterministic input pipeline
        ↓
Implement LiteLLM client
        ↓
Implement planner
        ↓
Implement writer
        ↓
Implement evaluator
        ↓
Implement one-pass revision
        ↓
Implement trace storage
        ↓
Implement SQLite metadata persistence
        ↓
Add tests
        ↓
Run the sample end to end
```

### Freeze rule

New product ideas must not change the current iteration unless they solve a blocking problem.

Store future ideas in:

```text
docs/ideas.md
```

---

## 23. Future direction

Possible future evidence sources:

- Git diffs
- commit history
- pull requests
- issues
- terminal logs
- screenshots
- architecture notes
- test reports
- deployment records

Possible future outputs:

- README updates
- portfolio case studies
- resume bullets
- interview stories
- technical articles
- presentation outlines
- video scripts

Possible product evolution:

```text
One iteration
      ↓
Structured engineering knowledge
      ↓
Multiple reusable outputs
```

These are long-term possibilities, not v0.1 requirements.

---

## 24. Instructions for Codex or another coding agent

When implementing this project:

1. Read this entire file before writing code.
2. Do not expand the v0.1 scope.
3. Implement deterministic components before LLM components.
4. Use the repository structure defined above unless a concrete technical conflict exists.
5. Keep prompts in separate versioned Markdown files.
6. Validate every external input and structured model output.
7. Create tests for deterministic business logic.
8. Store every major pipeline artifact.
9. Permit at most one automatic revision.
10. Do not implement LinkedIn publishing.
11. Use only the specified SQLite persistence layer; do not introduce
    LangGraph, PostgreSQL, Redis, Celery, RAG, or a web UI in v0.1.
12. Before making a significant architectural change, document the reason.
13. Prefer a simple working pipeline over abstract extensibility.
14. Never invent requirements not present in this document.
15. End implementation by running the sample input and reporting:
    - files created
    - tests run
    - test results
    - command used
    - final output path
    - any unresolved limitations

### Confirmed architecture revision

SQLite metadata persistence was explicitly added to v0.1 after the original
file-only design. This is a deliberate product decision, not permission to add
unrelated backend infrastructure. If a persistence design decision is not
specified here, choose the simplest implementation that satisfies v0.1.
