# Finish and Land Playbook

**Role:** Closer Agent
**Goal:** Safely land the current feature branch into `main` and update the Todo list.

## 1. Verification
- Run the full test suite: `mix test`.
- Ensure `git status` shows the working tree is clean (except for the Todo update below).

## 2. Bookkeeping (Critical)
1.  **Identify the Implementation Commit**: Get the short SHA of the commit you just made to implement the code.
    - `git rev-parse --short HEAD`
2.  **Update `docs/process/TODO.md`**:
    - Find the item you are working on.
    - Change `[ ]` to `[x]`.
    - Append `#done/<implementation_sha>` to the end of the line.
    - *Example:* `- [x] Fix login bug #a1b2c3 #done/9z8y7x`

## 3. Committing the Bookkeeping
- Commit the change to `docs/process/TODO.md`:
    - `git add docs/process/TODO.md`
    - `git commit -m "docs: mark <task> as done"`

## 4. Landing
- Push the feature branch.
- If you have permissions, merge to `main`.
- If not, request human review.
