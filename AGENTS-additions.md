## Context Strategy
- **Agents must read** `docs/ai/instructions/context-strategy.md` to understand where to find specs.
- **Agents must use** the playbooks in `docs/ai/playbooks/` for specific tasks.

## Context Safety
- **Human-Only Documents:** If you encounter a document starting with `` or the blockquote `> 🛑 Human Context Only`, stop reading it immediately unless your current task is explicitly about modifying that specific process.


## Core Workflows
1. **Picking a Todo**: Run the `todo-implementer` playbook.
2. **Finishing a Task**: Run the `finish-and-land` playbook.
3. **Processing Feedback**: Run the `todo-processor` playbook to triage `docs/process/TODO.md`.

## The "Buffered Integration" Protocol
- **`main`** is the development trunk.
- **`stable`** is the deployed demo branch.
- Agents work on `topic/*` or short-lived feature branches.
- Feedback arrives as files in `test/support/feedback/` (see `docs/process/ash-roadmap.md`).
