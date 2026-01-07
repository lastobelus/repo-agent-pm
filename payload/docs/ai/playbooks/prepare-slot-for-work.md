---
kind: playbook
mode: in-session
name: prepare-slot-for-work
stop_conditions:
  - working tree not clean
  - branch choice unclear
  - missing exchange remote
---

# Prepare Slot for Work

**Role:** Any Agent
**Goal:** Ensure clean git state, correct branch setup, and exchange tracking before doing slot work.

This playbook prevents branch-off-branch and standardizes branch naming by slot type.

## Branch Prefixes

- `todo/<slug>` for one-shot TODO work.
- `spec/<slug>` for spec slot work.
- `topic/<slug>` for general feature threads.
- `process/<slug>` for process-improver work.

## Procedure

### 1) Clean tree (required)

```bash
git status --porcelain
```

If anything is dirty, stop and ask the human.

### 2) Ensure exchange remote exists

```bash
git remote
```

If `exchange` is missing, run:

```bash
./scripts/setup-exchange
```

### 3) Sync trunk (only when on trunk)

```bash
git fetch origin
```

If you are on `main` or `stable`, sync `main`:

```bash
git checkout main
git pull --ff-only origin main
```

### 4) Branch (no branch-off-branch)

Check current branch:

```bash
git rev-parse --abbrev-ref HEAD
```

Rules:

- If you are on `main` or `stable`, create a new branch with the correct prefix:

```bash
git checkout -b <prefix>/<slug>
```

- If you are already on a non-trunk branch, **do not create a new branch**.
  - If the current branch matches the intended slot, continue.
  - If it does not match, stop and ask the human which branch to use.

### 5) Set upstream to exchange

```bash
git push -u exchange HEAD
```

### 6) Record base SHA (recommended)

```bash
git rev-parse --short origin/main
```

Use this `#base/<sha>` when required by the task playbook.
