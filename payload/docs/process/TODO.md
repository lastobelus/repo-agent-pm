# Project Coordination

Conventions:

- A “todo group” is a parent checklist item plus any nested checklist children.
- Implementers pick exactly one todo group (one parent item + its children) from `Approved`.
- Preserve tags at the end of todo lines:
  - origin: `#<shortsha>` (or `#init` for scaffolded items)
  - optional base: `#base/<shortsha>`
  - completion: `#done/<shortsha>`

When adding new todos, it is acceptable to add them without origin tags as long as they stay in `Inbox` until a triage run attaches tags.
If you want stable origin tags immediately, run:

```bash
./scripts/run-prompt.sh add-todo
```

## Inbox (New Feedback)
## Review (Pending Human Approval)

## Approved (Queue for Agents)
- [ ] Initial project scaffold setup #init

## Future / Icebox

## Finished (History)
