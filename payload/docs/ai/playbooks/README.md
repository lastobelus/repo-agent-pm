# Playbooks (Procedures)

Playbooks are mid-session procedures/checklists.

They are often referenced by clean-context prompts, but they are meant to describe *how* to do work once the agent is engaged.

Use `scripts/run-playbook <name>` to print a playbook and its declared inputs during an active session.

## Available Playbooks

- `add-todo` — add todos with stable origin tags.
- `todo-processor` — triage and reorder the TODO queue.
- `todo-implementer` — implement one approved todo group.
- `finish-and-land` — land work + perform bookkeeping.
- `installer` — guided install to tailor the kit.
