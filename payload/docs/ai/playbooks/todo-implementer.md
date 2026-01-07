---
kind: playbook
mode: in-session
name: todo-implementer
depends_on:
  - playbook/prepare-slot-for-work
inputs: []
writes: []
stop_conditions:
  - requirements unclear
  - tests failing
---

# Todo Implementer

This playbook is for **one-shot TODO work** (complete one Approved todo group in a single run).

If the work is long-lived or needs multiple sessions, use the **topic** workflow instead (see `docs/process/topics/README.md`).

**Role:** Coding Agent
**Input:** A single item from `docs/process/TODO.md` (the `Approved` section).

This playbook is optimized for new Phoenix/Elixir projects.

## Protocol
### 0) Preflight (do not skip)

Complete `prepare-slot-for-work` first. If already done, continue.

### 1) Select exactly one todo

- Pick exactly one todo group from `docs/process/TODO.md` under `## Approved (Queue for Agents)`.
- Do not “bundle” multiple Approved todos.
- If requirements or acceptance criteria are unclear, stop and ask 1–3 minimal clarifying questions.

### 2) Branch

If you are on `main` or `stable`, create a new `todo/<task-slug>` branch.
If you are already on a non-trunk branch, do not create a new branch.

### 3) Record base SHA + mark the selected todo group (recommended)

After branching, record the base you started from so stale-branch debugging is easy:

```bash
git rev-parse --short origin/main
```

Append `#base/<sha>` to the selected **parent** todo line (preserving the existing `#<sha>` origin tag). Treat the parent line plus any nested children as one “todo group”; do not split children into separate tasks unless the human explicitly asks.

### 4) Implement

- Make the smallest change that fully completes the selected todo.
- Add/update tests where reasonable.
- Avoid refactors unrelated to the todo.

### 5) Verify

Run the standard Elixir test suite:

```bash
mix test
```

If tests fail, stop and fix or ask.

### 6) Commit (implementation)

Make an implementation commit using Conventional Commits:

- `feat: ...` for new behavior
- `fix: ...` for bug fixes

### 7) Handover + bookkeeping (two-commit rhythm)

This kit uses a two-commit rhythm:

1. Implementation commit (you just made)
2. Doc-only bookkeeping commit updating `docs/process/TODO.md` with `#done/<implementation_sha>`

If you are not also acting as the closer, stop here and instruct the human (or closer agent) to run the `finish-and-land` playbook (via `./scripts/run-prompt land`).
