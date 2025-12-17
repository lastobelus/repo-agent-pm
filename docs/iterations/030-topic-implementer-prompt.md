
- longer-lived iterations, may require multiple clean-context agent runs
	- ok to split: start-topic prompt & continue-topic prompt
- we want commits of atomic/meaningful phases, not just final
- we should (unless changes too complex) ff rebase each time
- we should push topic branches to origin; we don't want to lose a large chunk of work, where as with todos we don't care, we can just re-run them

---

**Agent Action (proposed)**:
Draft two clean-context prompts for long-lived work:

1) `start-topic`
   - clean-tree preflight
   - create `topic/<slug>`
   - record base SHA
   - plan + implement first atomic slice
   - push branch to origin

2) `continue-topic`
   - clean-tree preflight
   - pull/ff-only + rebase/ff policy guidance
   - implement next slice with meaningful commit
   - push updates to origin

Also decide:
- how we want to do “ff rebase each time” in practice (rebase onto `origin/main` vs merge main)
- whether to require a local exchange push for topics (recommended: no; origin push is enough)

---
