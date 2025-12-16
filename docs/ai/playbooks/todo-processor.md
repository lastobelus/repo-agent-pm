# Todo Processor

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
