# Overview

This repository builds and maintains **The Kit**: a set of process artifacts for a workflow where a solo human developer runs multiple CLI coding agents concurrently.

## Goals

- Keep the workflow **Git-native**: coordination is visible in the repository.
- Keep artifacts **human-editable**: Markdown + YAML (and minimal machine tags embedded inline when needed).
- Support **concurrent agents** without requiring heavy external PM tooling.
- Maintain a **stable deployed branch** (`stable`) while development continues on `main`.

## The Model

### Team Shape

- One experienced human developer (operator / lead / reviewer).
- Multiple CLI agents (Codex CLI / Claude CLI / Gemini CLI / etc.), sometimes 2+ in parallel.

### Coordination: TODO Checkpoint

The core coordination artifact is a single TODO document (`docs/process/TODO.md` in the consumer project) with sections like Inbox / Review / Approved / Future / Finished.

Conventions:
- Todos carry an origin tag like `#<shortsha>` (the commit where the todo first entered the list).
- When a todo is completed, the final bookkeeping commit appends `#done/<shortsha>`.

### Branching

- `main`: development trunk
- `stable`: deployed/demo branch (only updated intentionally)
- short-lived branches for atomic todos; longer-lived branches for larger spec-driven work

### Visibility: Local Exchange

Local Exchange is a local-only git remote used as a dashboard for “what’s in flight” across multiple clones/slots.

The intent is to preserve the “branches as labels” visualization without pushing ephemeral branches to GitHub.

## What Gets Installed

Everything under `payload/` is what the installer copies into the consumer project.

