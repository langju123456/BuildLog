# Current Sprint

## Objective

Establish the BuildLog v0.2 LinkedIn Publishing Baseline.

Make one existing reviewed BuildLog final artifact publishable as a text-only
personal LinkedIn post through a secure, observable, testable, and explicitly
human-controlled downstream workflow.

## Current Task

- [x] Assess the existing repository and preserve generation boundaries
- [x] Research LinkedIn scopes, OAuth, identity, endpoint, headers, and token
  behavior from official documentation
- [x] Record the publishing architecture decision
- [x] Add isolated LinkedIn configuration and secret redaction
- [x] Implement Authorization Code flow with one-time CSRF state and localhost
  callback
- [x] Store tokens atomically in a restricted user-level credential directory
- [x] Add safe status, whoami, and logout behavior
- [x] Resolve only an intact completed final artifact under the configured
  runs directory
- [x] Add a minimal publisher boundary and LinkedIn text-post adapter
- [x] Add exact preview and explicit human approval
- [x] Block duplicate successful publication by default
- [x] Persist successful, failed, and indeterminate publication receipts
- [x] Append safe publication events to the existing run event stream
- [x] Add mocked OAuth, identity, HTTP, publishing, persistence, and CLI tests
- [x] Document setup, security, and the manual production smoke test
- [x] Complete real OAuth and one explicitly approved controlled publication
  smoke test

## Definition of Done

- [x] Existing pipeline prompts, thresholds, LLM calls, and artifact names are
  unchanged
- [x] Legacy generation CLI behavior remains valid
- [x] Tests run without LinkedIn credentials or network access
- [x] `.env` and local credentials remain outside Git
- [x] No token, secret, authorization code, ID token, full post, or
  Authorization header enters receipts or events
- [x] OIDC userinfo resolves the authenticated member without trusting an
  unverified JWT
- [x] Preview displays the complete exact post and never submits it
- [x] Publication requires `--confirm` and exact interactive `PUBLISH`
- [x] A prior successful platform/account/content hash blocks duplicates
- [x] Ambiguous post outcomes are indeterminate and block blind retries
- [x] Publication failure does not change completed generation status
- [x] Receipt persistence and append-only event sequencing are test-covered
- [x] Real OAuth and the first real post required separate explicit human
  approval
- [x] Full tests, compile check, and `git diff --check` pass

## Out of Scope

- Automatic, scheduled, background, or retry-queue publishing
- Media, article, document, carousel, or video posts
- Organization-page publishing
- Comments, likes, analytics, deletion, or post management
- Multi-user, multi-account, cloud-token, or web UI support
- Advertising, Lead Sync, Verified, or data-portability products
- MCP or tool-calling integration
- Other social platforms
- Prompt, evaluator, threshold, model, or generation behavior changes
- RAG, embeddings, retrieval, memory, or multimodal baselines
- Unapproved or autonomous real publication
