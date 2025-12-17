# Process Docs

This folder contains the core process artifacts that coordinate work between a human operator and multiple CLI agents.

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

## Reducing TODO Conflicts (Optional)

If `TODO.md` becomes a merge-conflict hotspot, keep it as the queue but move high-churn detail into per-task notes.

See `docs/process/shared-file-collisions.md`.

## Local Exchange (Optional)

Local Exchange is an operator workflow for “branches as labels” visibility without pushing ephemeral branches to GitHub.

It is not installed by default. To set it up in a project:

```bash
./scripts/run-prompt.sh setup-local-exchange
```
