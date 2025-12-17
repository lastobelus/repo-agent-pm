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

### Why this works (practitioner note)

In real multi-agent use (e.g. 2 concurrent “todo implementer” loops plus an interactive feature session), you may still see occasional conflicts.

The reason conflicts are usually manageable:

- TODO changes are mechanically simple (move/mark/add lines).
- The file is “hot”, so agents tend to rebase frequently and land small slices.

Worst case, a todo item gets re-run from scratch once in a while. The workflow is designed so that outcome is low-cost.
