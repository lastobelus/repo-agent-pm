---
kind: playbook
mode: in-session
name: todo-processor
writes:
  - docs/process/TODO.md
stop_conditions:
  - unclear prioritization
---

# Todo Processor

**Role:** Manager Agent
**Goal:** Triage the `Inbox` and `Review` sections of `docs/process/TODO.md`.

## Workflow
1.  **Inbox**: Read new items.
    - If it's a bug report from `test/support/feedback/`, analyze any attached `trace.json`.
    - Move to **Review** or **Approved**.
2.  **Review**:
    - If a task is blocked, move to **Future**.
    - If a task is ready for an agent, move to **Approved**.
3.  **Tagging**: Ensure every line has an origin SHA tag (`#<sha>`) if it's missing.
