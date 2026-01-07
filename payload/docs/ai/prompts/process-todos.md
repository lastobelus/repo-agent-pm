---
kind: prompt
mode: clean-context
name: process
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/ai/playbooks/todo-processor.md
  - docs/process/TODO.md
outputs:
  - updated TODO.md (triaged)
stop_conditions:
  - unclear prioritization
  - destructive rewording of tasks
---

You are a manager agent.

Your task: triage the TODO inbox and review sections.

Follow `docs/ai/playbooks/todo-processor.md`. When you are uncertain, stop and ask the human rather than guessing.

