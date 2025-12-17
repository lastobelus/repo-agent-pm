# TODO Checkpoint (Coordination Convention)

This kit is built around a single in-repo coordination document (the “TODO checkpoint”).

## The File

In consumer projects, the canonical file is:

- `docs/process/TODO.md`

## Sections

Typical sections:

- Inbox: raw inputs (notes, bug reports, ideas)
- Review: items awaiting human approval/triage
- Approved: queue for agents
- Future: intentionally deferred
- Finished: historical record

## Tagging

- Every todo line should carry an origin tag `#<shortsha>` pointing to the commit where it was first introduced.
- When starting work from `origin/main`, consider also recording `#base/<shortsha>` on the todo line.
- When a todo is completed, the bookkeeping commit appends `#done/<shortsha>` (the short SHA of the implementation commit).

## Concurrency Note

This process assumes multiple agents may edit `docs/process/TODO.md` concurrently. The constraint that makes it workable is:

- edits are line-oriented
- `#<shortsha>` and `#done/<shortsha>` tags are treated as persistent
- branches are rebased/fast-forwarded frequently
