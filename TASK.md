# Current Sprint

## Objective

Establish the BuildLog v0.1 Example Showcase and make the boundaries among raw
runs, reviewed evaluation assets, and public examples explicit.

## Current Task

- [x] Confirm the selected architecture v1 and v2 raw outputs exist locally
- [x] Preserve the generated post content in a public architecture showcase
- [x] Link the source iteration, v1 output, v2 output, and quality baseline
- [x] Define the future reviewed `eval_corpus/` boundary
- [x] Document raw runs as internal evaluation source assets
- [x] Treat `docs/output_quality_baseline.md` as the current scoring protocol
- [x] Make example outputs discoverable from the root README
- [x] Document the three asset layers without changing persistence behavior
- [x] Verify all documentation links and copied output hashes
- [x] Run the complete deterministic test suite
- [x] Confirm raw runs and local artifacts remain outside Git

## Definition of Done

- [x] `examples/outputs/architecture/` contains README, v1, and v2 Markdown
- [x] Public v1 and v2 files preserve the selected generated text
- [x] `eval_corpus/README.md` requires deliberate human review and sanitization
- [x] The root README links input, outputs, and evaluation baseline
- [x] PROJECT documents the asset layers without redesigning the architecture
- [x] `runs/`, databases, caches, virtual environments, and local artifacts
  remain untracked
- [x] Documentation links resolve
- [x] Existing deterministic tests pass

## Out of Scope

- Copying complete raw run directories into Git
- Automatically promoting raw runs into the evaluation corpus
- Creating fake or bulk evaluation samples
- Few-shot selection, retrieval, or dataset tooling
- Prompt, evaluator, writer, planner, or reviser changes
- Revision-threshold changes
- Model or token-setting changes
- New infrastructure or frameworks
- New database tables
- API or UI
- RAG
- LinkedIn publishing
- New pipeline stages
- Unrelated architecture refactoring
