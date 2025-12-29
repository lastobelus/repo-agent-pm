# Process Kit Docs (Start Here)

This folder is the human-facing documentation installed with the kit.

## Start Here

1. Read `docs/process/README.md` for the core workflow and conventions.
2. Skim `docs/ai/README.md` to understand prompts/playbooks and how agents are invoked.
3. Keep `docs/process/TODO.md` open while you work; it is the coordination hub.

## What To Read Next (By Scenario)

- **I want to add work quickly** → `docs/process/TODO.md` + `docs/ai/prompts/add-todo.md`
- **I need an agent to implement a task** → `docs/ai/prompts/implement-one-todo.md` + `docs/ai/playbooks/todo-implementer.md`
- **I need to triage the queue** → `docs/ai/prompts/process.md` + `docs/ai/playbooks/todo-processor.md`
- **I want to close out work** → `docs/ai/prompts/land.md` + `docs/ai/playbooks/finish-and-land.md`
- **This task needs multiple sessions** → `docs/process/topics/README.md`
- **We just installed the kit** → `docs/process/agent-workflows.md` (examples) + `docs/ai/playbooks/installer.md` (optional)
- **I want Local Exchange visibility** → `docs/process/local-exchange.md`

## Operator Quickstart (Clean-Context Run)

1. Run a prompt printer:

```bash
./scripts/run-prompt implement-one-todo
```

2. Copy the printed prompt into a fresh agent session.
3. If the agent asks for missing context, add the relevant files to `scripts/context.config.yaml` and re-run.

