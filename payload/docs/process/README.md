# Process Docs

This folder contains the core process artifacts that coordinate work between a human operator and multiple CLI agents.

## Current Scope (Temporary)

This kit is currently optimized for **new Phoenix/Elixir/Ash projects**. Some playbooks assume:

- tests are run with `mix test`
- trunk branch is `main`
- agent branches are `topic/*`

## Guided Install (Optional)

If you want to tailor the kit to your project’s conventions (branch names, test command, etc.), run the guided install playbook:

```bash
./scripts/run-prompt installer
```

## The TODO Checkpoint

The coordination “nervous system” is `docs/process/TODO.md`.

Conventions (line-oriented, designed for concurrent edits):

- Every todo line should have an origin tag `#<shortsha>`.
- When a todo is completed, append `#done/<shortsha>` (the implementation commit).
- When an agent starts work from trunk, it may also record a base tag `#base/<shortsha>` (the `origin/main` base it started from).

### Why this works in practice

This process intentionally allows multiple agents (and the human) to edit `docs/process/TODO.md` concurrently.

It stays workable because:

- Most changes are **whole-line edits** (add a line, move a line, mark a line done).
- Tags like `#<shortsha>`, `#base/<shortsha>`, and `#done/<shortsha>` are treated as **persistent** and not “cleaned up”.
- Agents frequently fast-forward/rebase before landing, so TODO drift stays small.

Worst case, an occasional conflict means re-doing one small todo. That’s acceptable because the loop is optimized for atomic, small tasks.

## Topics (Iterative Work)

If a task is too large or uncertain for a one-shot TODO run, use a **topic**.

- Topics live under `docs/process/topics/` (one directory per topic).
- Topic work is iterative across multiple clean-context runs.

See `docs/process/topics/README.md`.

Quick start:

```bash
./scripts/start-topic -t docs/process/topics/001-<slug>
./scripts/continue-topic -t docs/process/topics/001-<slug>
```

## Adding Todos (Origin Tags)

When adding new todos, you can either:

- add them quickly (without origin tags) and let the `todo-processor` session attach missing tags later, **as long as the new todos remain in `Inbox` until tagged**, or
- use the clean-context prompt that produces stable origin tags via a two-step doc commit:

```bash
./scripts/run-prompt add-todo
```

## Reducing TODO Conflicts (Optional)

If `TODO.md` becomes a merge-conflict hotspot, keep it as the queue but move high-churn detail into per-task notes.

See `docs/process/shared-file-collisions.md`.

## Local Exchange (Optional)

Local Exchange is an operator workflow for “branches as labels” visibility without pushing ephemeral branches to GitHub.

It is not installed by default. To set it up in a project:

```bash
./scripts/run-prompt setup-local-exchange
```
