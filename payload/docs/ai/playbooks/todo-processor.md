---
kind: playbook
mode: in-session
name: todo-processor
writes:
  - docs/process/TODO.md
stop_conditions:
  - unclear prioritization
---

# Todo Processor

**Role:** Manager Agent
**Goal:** Triage the `Inbox` and `Review` sections of `docs/process/TODO.md` into `Review`, `Approved`, or `Future`.

This playbook is intentionally strict and mechanical to reduce “manager drift” and to be safe for weaker models.

## Non-Negotiables

- Do not drop, merge, or materially rewrite any todo’s intent.
- Preserve nesting (a parent todo and its children move together).
- Prefer moving todo groups between sections over editing wording.
- Never “clean up” or replace existing origin tags.
- When unsure, ask 1–3 minimal clarifying questions and leave the todo in `Review`.

## Scope: What to Process

Only process todos under these headings in `docs/process/TODO.md`:

- `## Inbox (New Feedback)`
- `## Review (Pending Human Approval)`

Do not touch items under `Approved`, `Future / Icebox`, or `Finished` unless the human explicitly asks.

Treat each “todo group” as a parent checklist line plus its nested checklist children.

## Procedure

### 1) Inventory todo groups

- Read `docs/process/TODO.md`.
- Identify todo groups under `Inbox` and `Review`.
- Preserve ordering unless there is a strong reason to re-order; if you re-order, keep it minimal.

### 2) Attach origin tags (only when missing)

For each checklist line (`- [ ] ...`) in the in-scope sections:

- If the line already ends with `#...`, keep it.
- Otherwise, append an origin marker at the end:
  - Preferred: `#<shortsha>` from `git blame`.
  - Acceptable for scaffolded items: `#init`.

How to get the origin tag:

1. Determine the line number.
2. Run:

```bash
git blame -L <line>,<line> docs/process/TODO.md
```

3. Extract the short commit hash and append ` #<shortsha>` to the end of the line.

Guardrails:

- If blame reports “Not Committed Yet” (or is otherwise unclear), stop and ask the human what origin tag to use.
- Never add a second `#...` if one already exists.
- Treat existing origin tags as immutable.

### 3) Classify each todo group

For each todo group in `Inbox` / `Review`, choose one destination:

- **Review**: needs a human decision, acceptance criteria, or risk call.
- **Approved**: can be implemented now by an agent as an atomic slice.
- **Future / Icebox**: blocked by a dependency or deliberately deferred.

Guidelines:

- If the item is a bug report from `test/support/feedback/`, read any referenced artifacts (e.g. a `trace.json`) before classifying.
- Prefer `Review` over guessing.

### 4) Rewrite TODO sections (move groups, don’t rewrite)

- Move whole todo groups to the correct section.
- Keep checklist formatting intact.
- Keep tags at line ends.

### 5) Safety checks

- Confirm every todo group from `Inbox` and `Review` still exists somewhere (none lost).
- Confirm nesting is preserved.
- Confirm each checklist line in the processed sections ends with exactly one trailing `#...` tag.
- Confirm you did not change items outside `Inbox` / `Review`.

## Deliverable

- Updated `docs/process/TODO.md` with:
  - todo groups triaged into `Review` / `Approved` / `Future / Icebox`
  - origin tags present (or clarified questions asked when blame is ambiguous)
