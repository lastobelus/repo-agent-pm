---
kind: prompt
mode: clean-context
name: process-improver
inputs:
  - AGENTS.md
  - docs/ai/README.md
  - docs/ai/instructions/context-strategy.md
  - docs/process/README.md
  - docs/process/TODO.md
outputs:
  - improved process docs and/or prompts/playbooks
stop_conditions:
  - changes would break installed workflow
  - unclear desired behavior
---

You are improving the process artifacts in this repository.

Scope:

- Prefer small, reversible edits.
- Keep the workflow Git-native and human-editable.
- If you change how agents are expected to work, update both:
  - human-facing docs under `docs/process/`
  - agent-facing prompts/playbooks under `docs/ai/`

Deliverable:

- Make a concrete improvement (docs, prompt clarity, conflict reduction, etc.).
- Summarize what changed and why.

