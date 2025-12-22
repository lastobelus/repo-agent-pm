---
kind: prompt
mode: clean-context
name: continue-topic
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/process/git-workflow.md
  - docs/process/topics/README.md
outputs:
  - one additional atomic slice implemented
  - meaningful commit(s)
  - pushed updates to origin
  - iteration doc updated (questions + outcomes)
stop_conditions:
  - git working tree not clean
  - not on topic branch
  - requirements unclear
  - tests failing
  - merge conflicts
  - rebase conflicts
---

You are a CLI coding agent working in a consumer project that uses this kit.

Your task: continue an existing **long-lived topic** on `topic/<slug>`.

Inputs include the process docs; you will also be given the chosen iteration document for this run.

Protocol:

1) **Preflight (must pass)**
   - Confirm you are in a git repo.
   - Confirm the working tree is clean (`git status --porcelain` is empty).
   - Confirm you are on a topic branch named `topic/<slug>`.

2) **Sync and rebase**
   - `git fetch origin`
   - Rebase onto the latest trunk (usually `origin/main`).
   - If you rebase, you may need `git push --force-with-lease` later.

3) **Read the iteration doc and ask questions**
   - If the next slice is unclear, ask 1–3 minimal clarifying questions in the iteration doc.
   - Do not proceed by guessing.

4) **Implement the next atomic slice**
   - Make one meaningful increment.
   - Add/update tests as needed.
   - Run the project verification command(s).

5) **Commit + push**
   - Commit with a meaningful message.
   - Push updates to origin.
     - If you rebased: use `git push --force-with-lease`.
     - If push is rejected because remote moved: fetch → rebase → force-with-lease again.

6) **Update the iteration doc**
   - Summarize what changed and what remains.
   - Mark completed action items.

Stop and ask the human if anything is ambiguous.
