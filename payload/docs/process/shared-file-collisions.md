# Shared File Collisions (TODO.md)

`docs/process/TODO.md` is intentionally central, which also makes it the most likely merge-conflict file.

This process assumes you can tolerate occasional conflicts, but if it becomes noisy, use sharding to reduce write pressure.

## Pattern: Queue + Per-Task Notes

- Keep `docs/process/TODO.md` as the *queue*.
- Create per-task notes at `docs/process/tasks/<slug>.md` (or similar).

Then TODO lines remain short and stable, while details churn elsewhere.

## When to Use It

- When multiple long-lived branches are active.
- When agents frequently add “recommended todos” and the human is also triaging.
- When you want richer context/history per task without bloating TODO.

## Minimal Convention

- TODO entry contains a pointer to the note file:
  - e.g. `- [ ] Improve onboarding docs (see docs/process/tasks/onboarding.md) #abc123`
- Notes can contain checklists, links, reproduction steps, and sub-todos.

