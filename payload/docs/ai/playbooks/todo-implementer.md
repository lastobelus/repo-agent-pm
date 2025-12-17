---
kind: playbook
mode: in-session
name: todo-implementer
inputs: []
writes: []
stop_conditions:
  - requirements unclear
  - tests failing
---

# Todo Implementer

**Role:** Coding Agent
**Input:** A single item from `docs/process/TODO.md` (Approved section).

## Protocol
1.  **Read Context**: Check `docs/specs/pending` for any relevant specs.
2.  **Record Base** (recommended):
    - Get the base SHA: `git rev-parse --short origin/main`.
    - Add `#base/<sha>` to the todo line you are working on (preserving the existing `#<sha>` origin tag).
3.  **Branch**: Create a branch `topic/<task-slug>`.
4.  **Implement**: Write code + tests.
5.  **Verify**: Run `mix test`.
6.  **Commit**: Use Conventional Commits (`feat: ...`, `fix: ...`).
7.  **Handover**: Instruct the user to run the `finish-and-land` playbook.
