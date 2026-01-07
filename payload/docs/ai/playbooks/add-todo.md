---
kind: playbook
mode: in-session
name: add-todo
depends_on:
  - playbook/prepare-slot-for-work
writes:
  - docs/process/TODO.md
stop_conditions:
  - unclear todo wording
  - working tree not clean
---

# Add Todo (Origin-Tag Safe)

**Role:** Operator / Manager Agent
**Goal:** Add new todo groups to `docs/process/TODO.md` without relying on `git blame`.

This playbook uses a **two-step doc commit** so origin tags are stable and deterministic.

## Non-Negotiables

- Do not rewrite or reorder existing todos.
- Add new items to `## Inbox (New Feedback)` unless the human explicitly requests another section.
- Use checklist items (`- [ ] ...`).
- A “todo group” is a parent checklist item plus any nested checklist children.
- Every new checklist line you add must end with exactly one origin tag: `#<shortsha>`.

## Procedure

### 1) Preflight

Complete `prepare-slot-for-work` first. If already done, continue.

### 2) Edit: add new todos (no tags yet)

- Add the new todo group(s) under `## Inbox (New Feedback)`.
- Do **not** add any `#...` tags yet.

### 3) Commit A: “introduce todos”

Commit the new todo lines:

```bash
git add docs/process/TODO.md
git commit -m "docs: add todo items"
```

Capture the short SHA of this commit:

```bash
git rev-parse --short HEAD
```

Call this value `<origin_sha>`.

### 4) Edit: append origin tags using `<origin_sha>`

- For every new checklist line you added in Commit A (including nested sub-todos), append ` #<origin_sha>`.
- Do not tag unrelated existing todos.

### 5) Commit B: “tag todos”

```bash
git add docs/process/TODO.md
git commit -m "docs: tag new todos"
```

### 6) Safety checks

- Confirm every newly-added checklist line ends with exactly one `#<origin_sha>` tag.
- Confirm you did not alter existing tags.
