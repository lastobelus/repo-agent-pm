import os
import json

# Define the file structure and contents
files = {
    "AGENTS.md": """# AGENTS.md — Project Instructions

## Context Strategy
- **Agents must read** `docs/ai/instructions/context-strategy.md` to understand where to find specs.
- **Agents must use** the playbooks in `docs/ai/playbooks/` for specific tasks.

## Core Workflows
1. **Picking a Todo**: Run the `todo-implementer` playbook.
2. **Finishing a Task**: Run the `finish-and-land` playbook.
3. **Processing Feedback**: Run the `todo-processor` playbook to triage `docs/process/TODO.md`.

## The "Buffered Integration" Protocol
- **`main`** is the development trunk.
- **`stable`** is the deployed demo branch.
- Agents work on `topic/*` or short-lived feature branches.
- Feedback arrives as files in `test/support/feedback/` (see `docs/process/ash-roadmap.md`).
""",

    "docs/ai/instructions/context-strategy.md": """# Context Strategy

When working on this project, look for specifications in these specific folders:

1.  **`docs/specs/implemented/`**: Features that are already done. Treat these as the "Source of Truth" for existing behavior.
2.  **`docs/specs/pending/`**: Approved specs that are ready to be implemented.
3.  **`docs/specs/drafts/`**: Rough ideas. **Ignore these** when coding unless explicitly instructed to "work on a draft."

## Scripts
Use `scripts/run-prompt.sh <task_name>` to automatically load the relevant specs for your current task.
""",

    "docs/ai/playbooks/finish-and-land.md": """# Finish and Land Playbook

**Role:** Closer Agent
**Goal:** Safely land the current feature branch into `main` and update the Todo list.

## 1. Verification
- Run the full test suite: `mix test`.
- Ensure `git status` shows the working tree is clean (except for the Todo update below).

## 2. Bookkeeping (Critical)
1.  **Identify the Implementation Commit**: Get the short SHA of the commit you just made to implement the code.
    - `git rev-parse --short HEAD`
2.  **Update `docs/process/TODO.md`**:
    - Find the item you are working on.
    - Change `[ ]` to `[x]`.
    - Append `#done/<implementation_sha>` to the end of the line.
    - *Example:* `- [x] Fix login bug #a1b2c3 #done/9z8y7x`

## 3. Committing the Bookkeeping
- Commit the change to `docs/process/TODO.md`:
    - `git add docs/process/TODO.md`
    - `git commit -m "docs: mark <task> as done"`

## 4. Landing
- Push the feature branch.
- If you have permissions, merge to `main`.
- If not, request human review.
""",

    "docs/ai/playbooks/todo-implementer.md": """# Todo Implementer

**Role:** Coding Agent
**Input:** A single item from `docs/process/TODO.md` (Approved section).

## Protocol
1.  **Read Context**: Check `docs/specs/pending` for any relevant specs.
2.  **Branch**: Create a branch `topic/<task-slug>`.
3.  **Implement**: Write code + tests.
4.  **Verify**: Run `mix test`.
5.  **Commit**: Use Conventional Commits (`feat: ...`, `fix: ...`).
6.  **Handover**: Instruct the user to run the `finish-and-land` playbook.
""",

    "docs/ai/playbooks/todo-processor.md": """# Todo Processor

**Role:** Manager Agent
**Goal:** Triage the `Inbox` and `Review` sections of `docs/process/TODO.md`.

## Workflow
1.  **Inbox**: Read new items.
    - If it's a bug report from `test/support/feedback/`, analyze the `trace.json` (see `docs/process/ash-roadmap.md`).
    - Move to **Review** or **Approved**.
2.  **Review**:
    - If a task is blocked, move to **Future**.
    - If a task is ready for an agent, move to **Approved**.
3.  **Tagging**: Ensure every line has an origin SHA tag (`#<sha>`) if it's missing.
""",

    "docs/process/TODO.md": """# Project Coordination

## Inbox (New Feedback)
## Review (Pending Human Approval)

## Approved (Queue for Agents)
- [ ] Initial project scaffold setup #init

## Future / Icebox

## Finished (History)
""",

    "docs/process/git-workflow.md": """# Git Workflow: Buffered Integration

## Branches
- **`stable`**: Production/Demo. Only merges from `main` when manually released.
- **`main`**: Development trunk.
- **`topic/*`**: Agent workspaces.

## The Feedback Loop
1. User reports issue in Demo App.
2. App commits `report.yaml` and `trace.json` to `test/support/feedback/` via GitHub API.
3. **Forensic Agent** picks up the file, analyzes the Ash Event trace, and adds a coherent Todo item to `docs/process/TODO.md`.
""",

    "docs/process/ash-roadmap.md": """# Ash Events Roadmap

## Phase 1: The Black Box (Current)
- **Goal:** Ingest user reports as files in the repo.
- **Action:**
    - Use Ash Events in `audit` mode.
    - Serialize trace to JSON.
    - Commit to `test/support/feedback/<id>/trace.json`.

## Phase 2: The Replay (Next)
- **Goal:** Turn reports into regression tests.
- **Action:**
    - Create a "Replay Test" helper in Elixir.
    - Agent reads `trace.json` and generates a `test/bugs/issue_<id>_test.exs` file that replays the events.

## Phase 3: The Flight Recorder (Future)
- **Goal:** Full visual replay.
- **Action:** Rehydrate the state from events to show the developer exactly what the user saw.
""",

    "scripts/context.config.json": json.dumps({
        "implement": [
            "AGENTS.md",
            "docs/ai/playbooks/todo-implementer.md",
            "docs/process/git-workflow.md",
            "docs/specs/pending/"
        ],
        "land": [
            "AGENTS.md",
            "docs/ai/playbooks/finish-and-land.md",
            "docs/process/TODO.md"
        ],
        "process": [
            "AGENTS.md",
            "docs/ai/playbooks/todo-processor.md",
            "docs/process/TODO.md"
        ]
    }, indent=2),

    "scripts/run-prompt.sh": """#!/bin/bash
# Usage: ./scripts/run-prompt.sh <task_name>
# Example: ./scripts/run-prompt.sh implement

TASK=$1
CONFIG="scripts/context.config.json"

if [ -z "$TASK" ]; then
  echo "Usage: $0 <task_name>"
  exit 1
fi

# Extract files list using python (standard on macos) to parse json
FILES=$(python3 -c "import sys, json; print(' '.join(json.load(open('$CONFIG'))['$TASK']))" 2>/dev/null)

if [ -z "$FILES" ]; then
  echo "Error: Task '$TASK' not found in $CONFIG"
  exit 1
fi

echo ""
echo ""

for file in $FILES; do
  if [ -d "$file" ]; then
    # If it's a directory, concat all markdown files inside
    for f in "$file"/*.md; do
      echo "---"
      echo "File: $f"
      echo "---"
      cat "$f"
      echo ""
    done
  elif [ -f "$file" ]; then
    echo "---"
    echo "File: $file"
    echo "---"
    cat "$file"
    echo ""
  else
    echo "Warning: $file not found." >&2
  fi
done
"""
}

def create_project_structure():
    for path, content in files.items():
        # Handle directory creation
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Write the file
        with open(path, "w") as f:
            f.write(content)
            print(f"Created: {path}")

    # Create empty spec directories to ensure structure exists
    dirs = [
        "docs/specs/implemented",
        "docs/specs/pending",
        "docs/specs/drafts",
        "test/support/feedback"
    ]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created directory: {d}")

    # Make script executable
    os.chmod("scripts/run-prompt.sh", 0o755)
    print("Made scripts/run-prompt.sh executable")

if __name__ == "__main__":
    create_project_structure()
    print("\\n✅ Project scaffold complete.")
