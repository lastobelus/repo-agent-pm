> 🛑 **Human Context Only**
> This document describes workflows for human operators to visualize agent slots.
> **AI Agents:** Ignore this file unless tasked with `sysops` or process design.

# Process: Local Exchange Repo (God Mode)

**Goal:** Provide a real-time, visual dashboard of all active and past work without polluting GitHub.

## 1. Intention & Philosophy
In this workflow, **branches are labels**.
Because we fast-forward merges, the linear history in `main` can sometimes obscure *which* agent worked on *what* task at a specific time.

This kit optimizes for a working style where:

- Multiple agents (and sometimes a human) work concurrently in separate clones/slots.
- Work is landed in small, fast-forwarded slices, so the trunk stays readable.
- Ephemeral branches are still valuable as a *timeline* and *labeling system*, even if they’re not pushed to GitHub.

The **Local Exchange** solves this by acting as a **private dashboard**:
1.  **Branches as Labels:** Every agent slot pushes its current task to this exchange. A branch named `feat/fix-login-race-condition` tells you exactly what is happening in that slot, right now.
2.  **GitX as Dashboard:** By fetching from the exchange, you get a "God Mode" view in `gitx`. You can see:
    * **Current Work:** Active branches sitting ahead of `main`.
    * **Past Work:** "Parked" or finished branches that provide a historical breadcrumb trail of *how* a feature landed, even if the final merge was a fast-forward.
    * **The Timeline:** A sequential overview of who did what, when, accessible from any slot.

This effectively replicates the visibility of a "Team Board" (like Jira/Linear) but entirely within Git, and safe from "bus factor" risks because the history is preserved locally.

## 2. Setup (One Time)

Run this in the project wrapper root:

```bash
./scripts/setup-exchange.sh
```

## 3. Agent Scripts Update

### `bin/slot-start`
When creating a branch, the agent/script must upstream it to `exchange`:

```bash
branch="$(git symbolic-ref --short HEAD)"

# Push the current branch to the exchange dashboard and set upstream
git push -u exchange HEAD

# Keep the dashboard fresh for other slots
git fetch exchange --prune
```

If `exchange` is missing, rerun `./scripts/setup-exchange.sh` from the wrapper root.

### `bin/slot-finish`
When a task is landed or abandoned, remove the **topic branch** from Exchange to reduce noise.

If you already switched to `main`, pass the branch name explicitly (do not delete `main`).

```bash
branch="${1:-$(git symbolic-ref --short HEAD)}"

if [ "$branch" = "main" ] || [ "$branch" = "stable" ]; then
  echo "Refusing to delete $branch from Exchange. Pass the topic branch name explicitly." >&2
  exit 1
fi

# Delete the branch from the dashboard
git push exchange :"$branch" || true

# Prune the refs locally so GitX stays clean
git fetch exchange --prune
```

If you want to keep a historical breadcrumb for a complex feature, leave the branch in Exchange; otherwise, delete it to keep the view focused on current work.

## 4. Using the Dashboard

From any slot, fetch the Exchange and open GitX with all refs:

```bash
./scripts/gitx-wrapper.sh
```

If GitX is not installed, run `git fetch exchange` and use your preferred visualizer (`gitk --all`, Fork, etc.).

## 5. Out-of-Band Visibility (Optional)

To make Exchange pushes the default without changing agent behavior, set a push default in each slot after running setup:

```bash
git config remote.pushDefault exchange
git push -u exchange HEAD
```

With this in place, a normal `git push` updates the Exchange dashboard. Add an operator-managed `pre-push` hook to block accidental pushes of ephemeral branches to `origin` if needed.
