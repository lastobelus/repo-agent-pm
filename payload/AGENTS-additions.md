## Context Strategy
- **Agents must read** `docs/ai/instructions/context-strategy.md` to understand where to find specs.
- **Clean-context jobs:** Use the prompts in `docs/ai/prompts/` (via `scripts/run-prompt <name>`).
- **Mid-session procedures:** Use the playbooks in `docs/ai/playbooks/`.
- If you cannot run shell commands in this environment, ask the human to run `scripts/run-prompt` and paste the output.

## Current Scope (Temporary)

This kit is currently optimized for **new Phoenix/Elixir/Ash projects**.

- Default verification uses `mix test`.
- Do not generalize the process to other stacks unless the human explicitly asks.

## Context Safety
- **Human-Only Documents:** If you encounter a document starting with `` or the blockquote `> 🛑 Human Context Only`, stop reading it immediately unless your current task is explicitly about modifying that specific process.


## Core Workflows
0. **Adding Todos (clean-context)**: Run `./scripts/run-prompt add-todo`.
1. **Picking a Todo (clean-context)**: Run `./scripts/run-prompt implement-one-todo`.
2. **Finishing a Task (clean-context)**: Run `./scripts/run-prompt land`.
3. **Processing Feedback (clean-context)**: Run `./scripts/run-prompt process`.
4. **Starting a Topic (clean-context)**: Use `./scripts/start-topic -t docs/process/topics/NNN-<slug>`.
5. **Continuing a Topic (clean-context)**: Use `./scripts/continue-topic -t docs/process/topics/NNN-<slug>`.

## Topics vs TODOs

- **TODOs** are intended to be **one-shot** (finish in a single session / clean-context run).
- **Topics** are intended to be worked **iteratively** over multiple runs, on a long-lived `topic/<slug>` branch.

## TODO Discipline (glm-safe rails)

The coordination artifact is `docs/process/TODO.md`. Follow these invariants:

- Do not drop, merge, or materially rewrite todo intent during triage.
- Preserve nesting (parent + sub-todos move together).
- Treat tags as persistent:
  - origin tag: `#<shortsha>` (or `#init` for scaffolded items)
  - optional base tag: `#base/<shortsha>`
  - completion tag: `#done/<shortsha>`
- Use the playbooks exactly:
  - triage: `docs/ai/playbooks/todo-processor.md`
  - implement: `docs/ai/playbooks/todo-implementer.md`
  - land/bookkeep: `docs/ai/playbooks/finish-and-land.md`

## The "Buffered Integration" Git Protocol
- **`main`** is the development trunk.
- **`stable`** is the deployed demo branch.
- Agents work on `topic/*` or short-lived feature branches.
- Feedback may arrive as files in `test/support/feedback/`.
