#status/finished
# Next Guardrails: TODO Tagging + Landing

This iteration captures follow-ups discovered while aligning The Kit with the link-snagger process.

## Recommendations / decisions to make

1) **Origin tags for new todos**
   - Today, the `todo-processor` playbook insists on `git blame` for missing origin tags.
   - In brand-new repos (or when todos are newly added but uncommitted), blame will be “Not Committed Yet”.

> #recommend would it be better to use a post-commit git hook to "blame" todos as they are committed? problem with that is it runs in-band for the agent doing the commit, and could produce confusion/churn. Maybe "local ci" setup in the local exchange repo? For now, the best I can think of is in new repos or for new todos, leave blank, and todo-processor looks for & adds missing blame shas. Git blame will be more or less correct so long as they haven't been moved around since they were added.

Feedback:

- I’d avoid post-commit hooks by default: they’re easy to forget, non-portable across clones, and they add “surprise writes” during commits (exactly the churn/confusion you called out).
- The simplest stable rule is procedural: **new todos can be added without origin tags, but they should not be moved between sections until a manager run tags them**.
  - If new todos are committed in-place (still in `Inbox`), `git blame` will be correct enough when the manager later tags them.
- If we want stronger guarantees later (esp. for brand-new repos), a dedicated `add-todo` flow that does a two-step doc commit is the most robust approach:
  1) commit adding todo lines (no tags)
  2) commit appending `#<shortsha>` tags using that first commit SHA (not blame)

> sounds good to me


I did **not** implement an `add-todo` prompt yet because the Agent Action is conditional (“If you confirm (1)”). See Questions below.

Decision: do we want a dedicated playbook/prompt for “add todos + tag them correctly” (two-step doc commit), so the manager agent doesn’t get stuck?

> if new todos go in inbox and only move from there during todo-processor sessions I think we're good? git blame won't be wrong up until todo-processor moves them. But we do need two step commit when landing to tag the **finished** todos

Feedback:

- Agree on the “don’t move before tagging” logic. I strengthened the `todo-processor` playbook to treat parent+children as a single group and to preserve nesting and tags strictly.
- The “two step commit when landing” is now explicitly enforced:
  - implementer playbook calls out the two-commit rhythm
  - finish-and-land playbook is now strict about identifying the implementation SHA and doing doc-only bookkeeping

2) **Finish-and-land guardrails**
   - Consider importing the same “non-negotiables + safety checks” tone into `docs/ai/playbooks/finish-and-land.md`.

> yes please

Implemented:

- Strengthened `payload/docs/ai/playbooks/finish-and-land.md` with non-negotiables + mechanical safety checks.

2) **Document the intentional TODO taxonomy difference**
   - We intentionally kept `Inbox/Review/Approved/...`.
   - Consider explicitly documenting how this maps to the old `Available/Future/Finished` model for people migrating from link-snagger.

> not a concern

Acknowledged; not pursuing.


## #discuss Todo Prompts

### Hierarchy in todos
#recommend Can/should we allow hierarchy in todo bullet list?  I think perhaps "Pick exactly one todo group" implies this, i.e, exactly one top-level todo bullet, and all it's children come along. How/where should we make this explicit for both humans & agents? Maybe the installed TODO.md should come with some example content?

Feedback:

- Yes: hierarchy is a feature, not a bug. The “todo group” concept is how we keep tasks atomic while still allowing a checklist of sub-steps.
- I made this explicit in two places:
  - `payload/docs/process/TODO.md` now defines “todo group” + tag invariants.
  - `payload/docs/ai/playbooks/todo-implementer.md` now explicitly says “parent + children move together; don’t split unless the human asks”.

I did not add a full example block of fake todos (to avoid template noise), but we can if you want.

### Git process

#advise does it matter that
```
Append `#base/<sha>` to the selected todo line (preserving the existing `#<sha>` origin tag).
```
comes before making the branch?

Feedback:

- Functionally it doesn’t matter for correctness, but it matters for **hygiene**: branching first keeps the `#base/...` annotation isolated to the feature branch and avoids accidental edits on `main`.
- I reordered the implementer playbook so branching happens before recording `#base/<sha>`.

## Future work
- added `docs/iterations/030-topic-implementer-prompt.md`

Not actioned in this iteration.

---

**Agent Action (proposed)**:
If you confirm (1), add a clean-context prompt like `add-todo` or extend the existing process docs to include a safe “new todo ingestion” flow that results in stable origin tags.

## Questions

1) Confirm (1): do you want me to implement an `add-todo` clean-context prompt now?
   - My recommendation: yes, as an optional “operator” prompt that establishes origin tags via a two-step doc commit (avoids `git blame` edge cases and avoids hooks).

> yes, please proceed
## Summary of work (this iteration)

- Updated consumer-installed docs and playbooks to explicitly support hierarchical todo groups and to make the closer/landing flow glm-safe.
- Reordered base-tagging to happen after branching to avoid dirtying `main`.

- Implemented an `add-todo` clean-context workflow (two-step doc commit) to create stable origin tags without relying on `git blame`:
  - `payload/docs/ai/prompts/add-todo.md`
  - `payload/docs/ai/playbooks/add-todo.md`
  - documented in `payload/docs/process/TODO.md` and `payload/docs/process/README.md`

---
