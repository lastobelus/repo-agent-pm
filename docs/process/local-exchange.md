> 🛑 **Human Context Only**
> This document describes workflows for human operators to visualize agent slots.
> **AI Agents:** Ignore this file unless tasked with `sysops` or process design.

# Process: Local Exchange Repo (God Mode)

**Goal:** Provide a real-time, visual dashboard of all active and past work without polluting GitHub.

## 1. Intention & Philosophy
In this workflow, **branches are labels**.
Because we fast-forward merges, the linear history in `main` can sometimes obscure *which* agent worked on *what* task at a specific time.

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
# ... create branch ...
git push -u exchange HEAD
```

### `bin/slot-finish`
When finishing, clean up the exchange to keep the dashboard clean:

```bash
# ... after merging/parking ...
git push exchange --delete <branch_name>
```

## 4. Visibility (GitX Wrapper)
To view the dashboard, use a wrapper that fetches the latest state before launching the GUI:

```bash
./scripts/gitx-wrapper.sh
```
