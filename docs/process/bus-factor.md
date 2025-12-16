> 🛑 **Human Context Only**
> This document is a high-level overview for human developers.
> **AI Agents:** Ignore this file.

# Bus Factor: Project Overview & Recovery

**Welcome.** If you are reading this, the primary developer is likely unavailable. This document explains the **Human-in-the-Loop AI Orchestration** system used to build this project.

## 1. The Core Concept
This is not a standard solo-dev project. It is built by a "team" consisting of **one human orchestrator** and **multiple AI agents** (running via CLI tools like Codex/Claude).

* **You (The Human):** Act as the Lead Architect and Code Reviewer. You define *what* to do.
* **The Agents:** Act as Junior Developers. They implement features, run tests, and manage boilerplate.

## 2. The Nervous System: `docs/process/TODO.md`
This file is the source of truth. It is not just a text file; it is a **state machine** for the agents.
* **`Available/Approved`**: Tasks waiting for an agent.
* **`Review`**: Code written by an agent waiting for your approval.
* **`Inbox`**: Raw feedback or bug reports (often from the "Flight Recorder", see below).

**Emergency Action:** If you don't know what to do next, read `docs/process/TODO.md`.

## 3. The "Buffered Integration" Git Strategy
We use a specific branching model to prevent AI-generated chaos from breaking the demo.
* **`stable`**: The "Production" branch. Deploys to the live demo. **Never push directly here.**
* **`main`**: The "Development Trunk". Agents merge here. It is generally stable but moves fast.
* **`topic/*`**: Feature branches where agents work.

**The "Dashboard" (Local Exchange):**
If you want to see what work is in flight *right now* across different agent "slots", run the `gitx` wrapper. We use a local-only remote called `exchange` to broadcast active branches between directory slots without cluttering GitHub.

## 4. How to Drive the Agents
You don't just "chat" with the bot. You use **Playbooks** to give them specific roles.
* **To Code:** Run the `todo-implementer` playbook. It reads specs from `docs/specs/pending` and code from `docs/specs/implemented`.
* **To Land:** Run the `finish-and-land` playbook. It runs tests, updates the Todo list with completion hashes (`#done/sha`), and pushes code.
* **To Triage:** Run the `todo-processor` playbook.

*See `AGENTS.md` for the master instructions provided to every agent.*

## 5. The Architecture: Ash Framework + "Flight Recorder"
The app is built on **Elixir/Phoenix + Ash Framework**.
* **Ash Events:** We use this to capture user actions.
* **The Workflow:**
    1.  A user reports a bug in the demo.
    2.  The app captures the `AshEvents` trace.
    3.  It commits a file to `test/support/feedback/`.
    4.  An agent reads this trace (Audit Mode) to fix the bug or generates a regression test (Replay Mode).

*See `docs/process/ash-roadmap.md` for the evolution of this system.*
