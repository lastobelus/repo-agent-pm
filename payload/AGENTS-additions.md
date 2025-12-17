## Context Strategy
- **Agents must read** `docs/ai/instructions/context-strategy.md` to understand where to find specs.
- **Clean-context jobs:** Use the prompts in `docs/ai/prompts/` (via `scripts/run-prompt.sh <name>`).
- **Mid-session procedures:** Use the playbooks in `docs/ai/playbooks/`.

## Context Safety
- **Human-Only Documents:** If you encounter a document starting with `` or the blockquote `> 🛑 Human Context Only`, stop reading it immediately unless your current task is explicitly about modifying that specific process.


## Core Workflows
1. **Picking a Todo (clean-context)**: Run `./scripts/run-prompt.sh implement`.
2. **Finishing a Task (clean-context)**: Run `./scripts/run-prompt.sh land`.
3. **Processing Feedback (clean-context)**: Run `./scripts/run-prompt.sh process`.

## The "Buffered Integration" Protocol
- **`main`** is the development trunk.
- **`stable`** is the deployed demo branch.
- Agents work on `topic/*` or short-lived feature branches.
- Feedback may arrive as files in `test/support/feedback/`.
