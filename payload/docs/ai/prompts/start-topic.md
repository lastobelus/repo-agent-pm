---
kind: prompt
mode: clean-context
name: start-topic
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/process/git-workflow.md
  - docs/process/topics/README.md
outputs:
  - topic branch created + pushed
  - one atomic slice implemented
  - iteration doc updated (questions + plan + outcomes)
stop_conditions:
  - git working tree not clean
  - topic slug or iteration doc missing
  - requirements unclear
  - tests failing
  - merge conflicts
  - rebase conflicts
---

You are a CLI coding agent working in a consumer project that uses this kit.

Your task: start a **long-lived topic** (iterative work across multiple clean-context runs).

Inputs include the process docs; you will also be given the current topic iteration document.

Protocol:

1) **Preflight (must pass)**
   - Confirm you are in a git repo.
   - Confirm the working tree is clean (`git status --porcelain` is empty).
   - Sync trunk:
     - `git fetch origin`
     - checkout trunk (usually `main`)
     - `git pull --ff-only`

2) **Derive topic slug + create branch**
   - Determine the topic `<slug>` from the topic directory name `NNN-<slug>`.
   - Create `topic/<slug>` from the synced trunk HEAD.

3) **Record the base SHA**
   - Record the trunk base SHA you branched from (the synced trunk HEAD) into the iteration doc under a “Base” section.

4) **Plan in the iteration doc**
   - Write a concise plan and any blocking questions in the iteration doc.
   - Keep the process lightweight: do not invent a new process layer.

5) **Implement one atomic slice**
   - Implement the smallest meaningful increment aligned with the iteration doc.
   - Add/update tests as needed.
   - Run the project’s verification command(s).

6) **Commit + push**
   - Create a meaningful commit (avoid “wip”).
   - Push `topic/<slug>` to origin.

7) **Update the iteration doc**
   - Summarize what changed, what remains, and any new follow-ups.
   - If you completed the action checklist, mark it done in the doc.

If anything is ambiguous, stop and ask the human (in the iteration doc).
