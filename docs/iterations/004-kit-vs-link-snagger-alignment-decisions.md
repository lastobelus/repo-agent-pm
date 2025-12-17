#status/finished
# Alignment Decisions: Kit ↔ link-snagger

This iteration captures decisions and recommended next actions arising from `003-align-with-link-snagger-process.md`.

## Decisions (confirmed)

1) **TODO taxonomy**
   - Keep The Kit’s `docs/process/TODO.md` with `Inbox/Review/Approved/Future/Finished`.
   - Import link-snagger’s stronger invariants + mechanical procedures.

2) **Branch naming + landing**
   - Keep `main` + `topic/*` branches, and keep `stable` as “deploy-only”.

3) **Test command defaults**
   - Elixir-first: keep `mix test` as the default for now.

## Recommendation (default)

- Keep the kit’s `Inbox/Review/Approved` flow (good for throughput + human gating), but **lift the link-snagger guardrails verbatim** into kit prompts/playbooks where applicable:
  - explicit “do not drop/merge/rewrite intent”
  - explicit “preserve nesting”
  - explicit “what region of the TODO file is in-scope”
  - explicit “origin tags are immutable”
  - explicit safety checks

## Proposed work (once decisions are confirmed)

---

**Agent Action**:
1) Strengthen `payload/docs/ai/playbooks/todo-processor.md` by importing the mechanical procedure + safety checks from link-snagger’s `docs/ai/prompts/todo-processor.md`, adapted to The Kit’s TODO sections.
2) Strengthen `payload/docs/ai/playbooks/todo-implementer.md` to include:
   - clean-tree preflight
   - explicit branch naming rules
   - explicit two-commit bookkeeping rhythm
3) Make test execution guidance align with the kit’s chosen scope (generic vs Elixir-first).
4) Update `payload/AGENTS-additions.md` to point at the strengthened procedures (glm-safe rails).
5) update all references to `docs/0..` iteration docs to `docs/iterations/0..`
6) capture intent to target  new Phoenix/Elixir/Ash projects specifically, and make `The Kit` generic later.

---

## Summary of work completed

- Strengthened the consumer-installed `Todo Processor` rails to match the link-snagger style (explicit scope, non-negotiables, mechanical steps, and safety checks): `payload/docs/ai/playbooks/todo-processor.md`.
- Strengthened the consumer-installed `Todo Implementer` playbook with clean-tree preflight, explicit branch naming, and an explicit two-commit rhythm: `payload/docs/ai/playbooks/todo-implementer.md`.
- Added glm-safe reminders and pointers to the strengthened procedures in `payload/AGENTS-additions.md`.
- Updated stale iteration doc references from `docs/00..` to `docs/iterations/00..`.
- Captured the temporary Elixir/Phoenix/Ash scope in both maintainer and consumer-installed docs (`docs/Overview.md`, `payload/docs/process/README.md`, and `payload/docs/ai/instructions/context-strategy.md`).
