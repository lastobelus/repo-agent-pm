#status/finished

This was originally extracted from the project at `/Users/lasto/clients/lastobelus-2025/link-snagger`

Review the process in that project by reading:
- `/Users/lasto/clients/lastobelus-2025/link-snagger/Agents.md`
- `/Users/lasto/clients/lastobelus-2025/link-snagger`
- `/Users/lasto/clients/lastobelus-2025/link-snagger/docs/ai/prompts/*`
- `/Users/lasto/clients/lastobelus-2025/link-snagger/docs/TODO.md`

That process was working well, over several iterations with Codex(gpt-5.1-codex-max, gpt-5.1-codex-mini, gpt-5.2) and opencode(glm-4-6).

---

**Agent Action**:
Please provide the following feedback by appending to this document (`docs/iterations/003-align-with-link-snagger-process.md`):
1. have we sufficiently captured the previously working process?
2. risks of our current additions/changes to the previously working process impacting how well it works?
3. does our current process provide sufficient guardrails for models like glm-4-6

---

## Findings (from link-snagger)

I reviewed the referenced working process in `/Users/lasto/clients/lastobelus-2025/link-snagger`:
- `AGENTS.md`
- `docs/TODO.md`
- `docs/ai/prompts/todo-processor.md`
- `docs/ai/prompts/todo-implementer.md`

Notable characteristics of that process:
- Very explicit **non-negotiables** + repo constraints up front.
- Very explicit **procedures** (inventory, blame tagging, classification rules, safety checks).
- Tight definition of **what file + which region** is being processed ("open todos at the top").
- Strong guardrails against ambiguous/destructive edits ("do not drop/merge/rewrite", "ask minimal questions").
- Two-commit rhythm: implementation commit then doc-only bookkeeping commit (`#done/<sha>`), and origin tags are treated as immutable.

## Feedback

### 1) Have we sufficiently captured the previously working process?

Partially, but not yet.

What *is* captured in The Kit today:
- A concept of **clean-context prompts** (`payload/docs/ai/prompts/*`) + a runner (`payload/scripts/run-prompt`).
- A concept of **todo processing** and **todo implementing** playbooks.
- A concept of **origin tags** (`#<sha>`) and **completion tags** (`#done/<sha>`).

What looks missing / materially different vs the working link-snagger process:
- **Specificity and safety checks**: our `payload/docs/ai/playbooks/todo-processor.md` is much less explicit than link-snagger’s `docs/ai/prompts/todo-processor.md` (classification rules, invariants, stop conditions, and safety checks are under-specified).
- **Todo file model mismatch**: link-snagger’s core artifact is `docs/TODO.md` with sections `Available/Future/Finished`, while The Kit currently uses `payload/docs/process/TODO.md` with `Inbox/Review/Approved/Future/Finished`.
  - This isn’t inherently wrong, but it’s not “capturing the previously working process” as-is.
- **Branch naming mismatch**: link-snagger centers `development` and requires a clean tree + branch creation; The Kit docs currently emphasize `main`/`stable`, and the implementer/lander playbooks don’t strongly enforce a clean-tree preflight.
- **Repo-specific testing leakage**: The Kit playbooks currently hardcode `mix test`, which is correct for Elixir repos but breaks the “generic kit” premise and diverges from link-snagger’s “run repo-specific tests / don’t claim manual testing unless done”.

### 2) Risks of our current additions/changes impacting how well it works?

Highest risks I see:

- **Weak invariants encourage entropy** (especially for todo triage): without explicit “don’t rewrite intent / don’t merge / don’t drop / preserve nesting” rules, manager models will gradually “summarize away” important detail.
- **`mix test` breaks trust**: if an agent follows the playbook in a non-Elixir repo, it will fail immediately or (worse) hallucinate success. This undermines the kit’s reliability.

> we decided to specifically target this process to new Phoenix/Elixir/Ash projects, and make it generic later. #advise how can we capture this temporary decision so new clean-context agents pick it up on future iterations?

Captured by:
- adding a “Current Scope (Temporary)” section to `payload/AGENTS-additions.md` (so it lands in the consumer project’s `AGENTS.md`), and
- adding the same scope note to `docs/ai/instructions/context-strategy.md` (an always-loaded input in clean-context prompts), and
- adding a scope note to the consumer process README (`docs/process/README.md`) and kit maintainer overview (`docs/Overview.md`).


- **Competing todo taxonomies**: Inbox/Review/Approved can be great for throughput, but it’s a different mental model than Available/Future. Switching models without clear mapping invites inconsistent behavior across agents and across iterations.
- **Prompt format drift**: the Kit’s YAML-frontmatter prompt format is fine, but if we don’t also keep the “human-readable procedure” as explicit as link-snagger’s prompts, weaker models will follow the metadata and miss the behavioral constraints.

### 3) Does our current process provide sufficient guardrails for models like glm-4-6?

Not yet, primarily in the todo processing/triage layer.

The link-snagger `todo-processor` prompt is basically a set of rails designed *for* glm-class behavior:
- clear scope boundaries (what to edit)
- strict non-negotiables
- explicit, mechanical steps
- explicit “ask rather than guess” points

Our kit’s `todo-processor` playbook is currently too short and leaves too much discretion to the model.

## Questions (process + intent)

1) The Agent Action text references `docs/003-align-with-link-snagger-process.md`, but this file lives at `docs/iterations/003-align-with-link-snagger-process.md`. Should we treat this as a typo and standardize references to the `docs/iterations/` path?

> yes. I moved the iteration docs to docs/iterations manually in #sha/8ea4b56e70a7d8b6ddd49a7f1fcd4e89d6436e0b and neglected to update references.


2) Do we want The Kit to **adopt the link-snagger todo taxonomy** (`Available/Future/Finished`) verbatim, or keep `Inbox/Review/Approved/...` and just bring over the stronger invariants + blame-tag discipline?

> keep `Inbox/Review/Approved/...` . This is an intentional improvement. Yes to bringing over stronger invariants + blame-tag discipline

3) Is the target “alignment” mainly about:
   - (a) prompt/playbook content and guardrails, or
   - (b) repository structure + filenames (`docs/TODO.md` vs `docs/process/TODO.md`), or
   - (c) both?

> repo structure is intended as an improvement on the original process. Target alignment is attempting to bring along as much of what worked when iterating on the link-snagger project to the newly defined process before actually trying it in a new project. Retrofitting link-snagger later would be nice, but new projects are the focus


## Summary of work (this iteration)

- Reviewed the working link-snagger process artifacts and compared them to The Kit’s current consumer-facing prompts/playbooks and TODO model.
- Identified concrete mismatches and risk areas (guardrails strength, todo taxonomy drift, repo-specific test command leakage).
