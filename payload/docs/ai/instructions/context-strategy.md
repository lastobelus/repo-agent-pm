---
kind: instruction
mode: always
name: context-strategy
---

# Context Strategy

## Current Scope (Temporary)

This kit is currently optimized for **new Phoenix/Elixir/Ash projects**. Expect conventions like `mix test` in playbooks.

If you are working in a different stack, stop and ask the human how to adapt verification commands and folder conventions.

When working on this project, look for specifications in these specific folders:

1.  **`docs/specs/implemented/`**: Features that are already done. Treat these as the "Source of Truth" for existing behavior.
2.  **`docs/specs/pending/`**: Approved specs that are ready to be implemented.
3.  **`docs/specs/drafts/`**: Rough ideas. **Ignore these** when coding unless explicitly instructed to "work on a draft."

## Scripts
Use `scripts/run-prompt.sh <task_name>` to automatically load the relevant specs for your current task.

Common names:

- `add-todo` (clean-context add todos + origin tags)
- `implement` (clean-context todo implementer)
- `land` (clean-context closer)
- `process` (clean-context triage)
- `process-improver` (clean-context process iteration)
- `setup-local-exchange` (clean-context Local Exchange setup)

Prompt/playbook inputs primarily come from YAML frontmatter in `docs/ai/prompts/` and `docs/ai/playbooks/`.

`scripts/context.config.yaml` is only for **project-specific extra inputs** (and starts empty in a fresh install).
