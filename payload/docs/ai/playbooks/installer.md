---
kind: playbook
mode: clean-context
name: installer
inputs:
  - docs/ai/instructions/context-strategy.md
writes:
  - docs/process/README.md
  - scripts/context.config.yaml
stop_conditions:
  - requirements unclear
  - target repo path not confirmed
  - installer would overwrite existing files without approval
---

# Guided Install (Tailored)

This playbook is a **guided install** for the Process Kit. It uses the static installer to copy the payload, then reconciles project-specific conventions (branch names, test commands, etc.).

## 0) Confirm target + safety

1. Ask the human for the **target repo path**.
2. Ask whether the target repo has any existing process docs (e.g., `docs/`, `AGENTS.md`, or `scripts/`).
3. If the target repo is dirty, ask whether to proceed or pause for cleanup.

## 1) Collect project conventions

Ask for the minimum needed conventions:

- Trunk branch name (default `main`)
- Test command (default `mix test`)
- Agent branch prefix (default `topic/`)
- Any existing TODO system or file location

If the project is **not** Phoenix/Elixir/Ash, ask for the stack and note it for the process docs.

## 2) Run the static installer

From the kit repo root:

```bash
python3 scaffold-project.py <target-path>
```

If the installer reports conflicts or skips, **pause** and confirm whether to overwrite or keep existing files.

## 3) Reconcile docs (tailor the defaults)

Update the target repo’s `docs/process/README.md` to reflect the collected conventions:

- Trunk branch name
- Test command
- Agent branch prefix
- Project stack (if not Phoenix/Elixir/Ash)

Keep the edits minimal: change values, don’t rewrite the structure.

## 4) Seed project-specific context inputs

Update `scripts/context.config.yaml` with any critical project docs that should always be in agent context, for example:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/ADR/`

Keep the file small; prefer a few high-signal inputs.

## 5) Install report (brief)

Create `docs/process/INSTALLATION-REPORT.md` with:

- date and installer (guided install)
- key conventions recorded
- any skipped or preserved files
- optional next steps (e.g., set up Local Exchange)

## 6) Verify basics

Run a quick sanity check:

```bash
./scripts/run-prompt start-topic
```

Confirm the output renders without errors.
