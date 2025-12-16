# Todo Implementer

**Role:** Coding Agent
**Input:** A single item from `docs/process/TODO.md` (Approved section).

## Protocol
1.  **Read Context**: Check `docs/specs/pending` for any relevant specs.
2.  **Branch**: Create a branch `topic/<task-slug>`.
3.  **Implement**: Write code + tests.
4.  **Verify**: Run `mix test`.
5.  **Commit**: Use Conventional Commits (`feat: ...`, `fix: ...`).
6.  **Handover**: Instruct the user to run the `finish-and-land` playbook.
