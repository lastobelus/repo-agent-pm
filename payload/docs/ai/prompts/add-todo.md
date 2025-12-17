---
kind: prompt
mode: clean-context
name: add-todo
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/ai/playbooks/add-todo.md
  - docs/process/TODO.md
outputs:
  - new todos added to Inbox
  - two doc commits (introduce + tag)
stop_conditions:
  - working tree not clean
  - todo wording ambiguous
---

You are an operator/manager agent.

Your task: add new todo group(s) to `docs/process/TODO.md` in a way that produces stable origin tags.

Follow `docs/ai/playbooks/add-todo.md` exactly.

If the human provides todo text, copy it verbatim. If the human provides only an idea, ask 1–3 minimal questions and then propose 1–3 candidate todo lines for approval.

