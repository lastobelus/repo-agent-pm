---
kind: playbook
mode: in-session
name: finish-and-land
depends_on:
  - playbook/prepare-slot-for-work
writes:
  - docs/process/TODO.md
stop_conditions:
  - tests failing
  - working tree not clean
---

# Finish and Land Playbook

**Role:** Closer Agent
**Goal:** Safely land the current feature branch into `main` and update the Todo list.

This playbook is intentionally strict and mechanical to reduce “closer drift” and to be safe for weaker models.

## Non-Negotiables

- Never claim tests passed unless you ran them.
- Never mark a todo done without identifying the implementation commit SHA.
- Do not rewrite todo intent during bookkeeping; only mark done and add `#done/<sha>`.
- Preserve existing tags (`#<shortsha>`, `#base/<sha>`) exactly.
- If anything is ambiguous or the working tree is dirty, stop and ask the human.

## 1. Verification

1. Ensure the working tree is clean:

```bash
git status --porcelain
```

2. Run the full test suite:

```bash
mix test
```

## 2. Bookkeeping (Critical)

1. **Identify the implementation commit** (the code commit, not the bookkeeping commit):

```bash
git rev-parse --short HEAD
```

If `HEAD` is not the implementation commit (e.g. you already did some doc commits), locate the correct one and stop if unsure.

2. **Update `docs/process/TODO.md`**:

- Find the todo group you are finishing.
- Change the checkbox on the parent line from `[ ]` to `[x]`.
- Append `#done/<implementation_sha>` to the end of the parent line.
- Do not remove or alter existing tags (keep the origin tag and optional base tag).

Example:

`- [x] Fix login bug #a1b2c3 #base/7f00ba4 #done/9z8y7x`

3. **Safety check**: ensure the only uncommitted change is the TODO update.

```bash
git status --porcelain
```

## 3. Committing the Bookkeeping
- Commit the change to `docs/process/TODO.md`:
    - `git add docs/process/TODO.md`
    - `git commit -m "docs: mark <task> as done"`

## 4. Landing

1. Push the feature branch to exchange:

```bash
git push -u exchange HEAD
```

2. Fast-forward `main` locally from `origin/main`:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
```

3. Fast-forward `main` to the feature branch:

```bash
git merge --ff-only <feature-branch>
```

If this is **not** a clean fast-forward, stop and ask the human (do not attempt a non-ff merge unless explicitly instructed).

4. Push the fast-forwarded `main` to exchange:

```bash
git push exchange main
```
