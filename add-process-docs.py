import os
import stat
import zipfile

# --- CONSTANTS TO PREVENT UI RENDERING BUGS ---
# We use these variables so the Chat UI doesn't interpret
# the backticks inside the strings as Markdown formatting.
TICK = "`"
BLOCK = TICK * 3

# --- FILE CONTENT DEFINITIONS ---

LOCAL_EXCHANGE_MD = f"""> 🛑 **Human Context Only**
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

{BLOCK}bash
./scripts/setup-exchange.sh
{BLOCK}

## 3. Agent Scripts Update

### `bin/slot-start`
When creating a branch, the agent/script must upstream it to `exchange`:

{BLOCK}bash
# ... create branch ...
git push -u exchange HEAD
{BLOCK}

### `bin/slot-finish`
When finishing, clean up the exchange to keep the dashboard clean:

{BLOCK}bash
# ... after merging/parking ...
git push exchange --delete <branch_name>
{BLOCK}

## 4. Visibility (GitX Wrapper)
To view the dashboard, use a wrapper that fetches the latest state before launching the GUI:

{BLOCK}bash
./scripts/gitx-wrapper.sh
{BLOCK}
"""

BUS_FACTOR_MD = f"""> 🛑 **Human Context Only**
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
"""

SETUP_EXCHANGE_SH = """#!/bin/bash
# Setup a Local Exchange (Shadow Remote) for multi-slot visibility.
# Run this from your project wrapper root (where slot-1, slot-2 live).

SLOT_DIRS="slot-1 slot-2 slot-3"
EXCHANGE_PATH="slots/exchange.git"

# 1. Initialize the bare repo
if [ ! -d "$EXCHANGE_PATH" ]; then
  echo "Initializing local exchange repo..."
  mkdir -p slots
  git init --bare "$EXCHANGE_PATH"
else
  echo "Exchange repo already exists."
fi

# 2. Configure remotes in each slot
for slot in $SLOT_DIRS; do
  if [ -d "$slot" ]; then
    echo "  Configuring $slot..."
    # Add remote if missing
    if ! git -C "$slot" remote | grep -q exchange; then
      git -C "$slot" remote add exchange ../$EXCHANGE_PATH
      echo "    + Added remote 'exchange'"
    else
      echo "    * Remote 'exchange' already exists"
    fi

    # Ensure pruning is on
    git -C "$slot" config remote.exchange.prune true
  fi
done

echo ""
echo "Setup complete!"
echo "Use 'scripts/gitx-wrapper.sh' to view the dashboard."
"""

GITX_WRAPPER_SH = """#!/bin/bash
# gitx-wrapper.sh
# Fetches the Local Exchange then opens GitX with --all

echo "Fetching from local exchange..."
git fetch exchange >/dev/null 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "Opening GitX..."
  gitx --all "$@"
else
  echo "Warning: Failed to fetch from exchange. Does the remote exist?"
  gitx "$@"
fi
"""

# --- ZIP CREATION LOGIC ---


def create_zip():
    filename = "process-docs.zip"

    # Define file mapping
    files = {
        "docs/process/local-exchange.md": LOCAL_EXCHANGE_MD,
        "docs/process/bus-factor.md": BUS_FACTOR_MD,
        "scripts/setup-exchange.sh": SETUP_EXCHANGE_SH,
        "scripts/gitx-wrapper.sh": GITX_WRAPPER_SH,
    }

    try:
        with zipfile.ZipFile(filename, "w") as zf:
            for path, content in files.items():
                # Add file to zip
                zf.writestr(path, content)

                # Set permissions for scripts (Unix only)
                if path.endswith(".sh"):
                    # Get ZipInfo object
                    zi = zf.getinfo(path)
                    # Set executable permission (0o755 << 16)
                    zi.external_attr = 0o755 << 16

        print(f"✅ Successfully created {filename}")
        print(f"   Contains: {', '.join(files.keys())}")

    except Exception as e:
        print(f"❌ Error creating zip: {e}")


if __name__ == "__main__":
    create_zip()
