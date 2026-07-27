# Current Sprint

## Objective

Establish the BuildLog v0.1 Agent Observability Baseline.

Make every BuildLog run explainable and reproducible without changing any
pipeline behavior.

## Current Task

- [x] Define validated Run, Step, LLM-call, Error, and Artifact Dependency
  observation schemas
- [x] Record all ten fixed steps exactly once, including explicit skipped states
- [x] Record step duration and attempt count without adding retry behavior
- [x] Record model configuration, prompt hashes, provider token usage, finish
  reason, and LLM-call duration
- [x] Preserve unavailable token counts as `null` with an availability reason
- [x] Record structured revision triggers and whether revision changed the draft
- [x] Mark revision improvement as `not_measured` without a post-revision
  evaluation
- [x] Record producing steps and direct artifact dependencies
- [x] Classify and sanitize observed errors without swallowing business failures
- [x] Add `run_metadata.json`, `timeline.json`, and `events.jsonl`
- [x] Add SQLite query projections for observations without changing existing
  business-table meaning
- [x] Keep observability failure isolated from generation behavior
- [x] Add deterministic tests for the observability contract
- [x] Run one complete local Qwen3 workflow and inspect its observation outputs
- [x] Complete the final regression, scope, prompt-hash, and artifact-contract
  review

## Definition of Done

- [x] Pipeline, observability, and reproducibility statuses are independent
- [x] Every fixed step has status, timestamps, duration, attempts, and skip reason
- [x] The run identifies its slowest step and highest-token step when measurable
- [x] Every LLM call belongs to a step and records replay-relevant metadata
- [x] Revision execution or skipping is explained by structured evidence
- [x] Final artifact lineage points directly to Draft or Revised Draft
- [x] Error records use the frozen category taxonomy and stable error codes
- [x] Replay completeness is based on an explicit checklist and configuration
  fingerprint
- [x] Existing artifact filenames and pipeline behavior remain unchanged
- [x] Filesystem payloads remain authoritative and SQLite remains a query
  projection
- [x] No prompt or model-response body is stored in SQLite telemetry
- [x] Observability failure cannot cause a new LLM call or change business output
- [x] A real local run produces inspectable metadata, timeline, events, and
  SQLite observations
- [x] All tests pass and `git diff --check` reports no errors

## Out of Scope

- Prompt, evaluator, writer, planner, or reviser behavior changes
- Revision-threshold or revision-count changes
- Retry-policy changes
- Additional LLM calls or post-revision evaluation
- Moving or renaming existing generated artifacts
- Full prompt, response, or post-body storage in telemetry tables
- Token estimation when the provider does not return usage
- Byte-identical output guarantees at nonzero temperature
- Dashboards, external tracing services, or OpenTelemetry
- New business outputs beyond `linkedin_post`
- API or UI
- RAG
- LinkedIn publishing
- Performance or output-quality optimization
