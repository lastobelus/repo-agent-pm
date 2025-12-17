---
kind: prompt
mode: clean-context
name: implement
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/ai/playbooks/todo-implementer.md
  - docs/process/TODO.md
  - docs/process/git-workflow.md
  - docs/specs/pending/
outputs:
  - code changes + tests
  - commits on a topic branch
stop_conditions:
  - requirements unclear
  - tests failing
  - merge conflicts
---

You are a CLI coding agent working in a consumer project that uses this kit.

Your task: implement **one** approved todo item.

Protocol:

1. Read `docs/ai/playbooks/todo-implementer.md` and follow it.
2. Treat `docs/specs/implemented/` as the source of truth for existing behavior.
3. If anything is ambiguous, stop and ask the human.

