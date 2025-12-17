# Interactive Iteration via Sequential Markdown Files

This document captures a lightweight workflow for iterating on process/tooling with an AI assistant by maintaining a sequence of annotated Markdown files.

Goal: make it easy to work in small chunks, preserve rationale, and enable a clean-context agent (or forgetful human) to pick up later.

## The Core Pattern

1. Create a numbered iteration doc (e.g. `docs/001-...md`).
2. Paste feedback as quoted blocks (`> ...`).
3. Respond inline under each quote.
4. Add explicit action items as **Agent Action** blocks.
5. When a new round begins, write a new file (e.g. `docs/002-...md`) that summarizes the *current truth* and adds new actions.

This repo currently uses:

- `docs/001-initial-feedback.md`
- `docs/002-updated-intent.md`

## Status Lines

A simple, machine-searchable status marker at the top of a file works well.

Example:

- `#status/finished`

Why it helps:

- an agent can quickly ignore closed iteration docs
- humans can tell what is “done” at a glance

Recommendation:

- Use a small fixed vocabulary like `#status/draft`, `#status/active`, `#status/finished`.

## Why This Reduces Round Trips

This approach reduces repeated clarification because:

- decisions are written once and persist
- out-of-scope boundaries are explicit
- actions are listed in one place and can be executed in batches

It also makes the workflow resilient to model variance: an assistant that is less adept at inferring intent (or has less context loaded) can still follow explicit Agent Actions.

## Common Gotchas

### 1) Actions that are underspecified

Bad:

- “make it better”

Better:

- “add `payload/docs/ai/prompts/process-improver.md` with YAML frontmatter and update `run-prompt.sh` to include it”

### 2) Secondary references get missed

Refactors often require updating:

- installer references
- README pointers
- scripts/config references

Mitigation: include a standard “update references + validate install” line in Agent Actions when appropriate.

### 3) Conflicting “truth” across files

Older iteration docs may contain decisions that are superseded.

Mitigation:

- treat the latest “updated intent” doc as the current source of truth
- use status markers to indicate older docs are finished

## Suggested Minimal Template for Agent Actions

You don’t need to formalize this in the process, but it’s a useful mental checklist:

- Goal
- Files to touch
- Definition of done (including validation)
- Non-goals / scope boundaries

## Notes from Current Repo Evolution

This repo used the approach successfully to:

- split consumer payload into `payload/` vs maintainer docs in `docs/`
- introduce prompts vs playbooks with YAML frontmatter
- make `scripts/run-prompt.sh` parse a tiny YAML subset and dedupe inputs
- move Local Exchange into `.kit/` as an optional add-on, installed via `scripts/install-local-exchange.sh`

