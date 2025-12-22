#status/finished
# Updated Intent (Round 2)

This document records the clarified intent from your annotations in `docs/iterations/001-initial-feedback.md`.

## Scope (Now)

- Target audience is effectively **one experienced human dev** running **multiple concurrent CLI agents**.
- Immediate consumer target is **Elixir/Phoenix** (so Elixir-specific defaults are acceptable for now).
- Third-party feedback ingestion (from the live demo app) is **out of scope** for the next iteration, but should remain a first-class future capability.

## Process Commitments 

### Human-readable artifacts

- Process artifacts should be human-readable/editable (Markdown + YAML).
- If machine tags/ids are needed, they should be attached inline to the relevant line/block (not stored in opaque side files).

---

**Agent Action**: 
- provide a new prompt in payload called `process-improver` that can be used to improve/iterate-on the process in-project.

---

### TODO checkpoint stays central

- Keep a single coordination file (`docs/process/TODO.md` in the consumer project).
- Concurrency is allowed: multiple agents can edit the TODO file.
- Constraints that make this viable:
  - edits are line-oriented
  - `#<shortsha>` origin tags and `#done/<shortsha>` completion tags are treated as persistent
  - agents frequently rebase/fast-forward before landing

---

**Agent Action**: 
- ensure this is appropriately documented for humans and agents working on this project
- ensure this is appropriately documented in what is installed in target projects
- meta: add instruction to this project AGENTS.md distinguishing between documentation for humans/agents iterating on the process, and for humans/agents using the process in a target project, and requiring all refactors/refinements etc. to include both types of documentation.
  - prefer `README.md`s in each folder that is installed in target projects, but for documenting the process work itself prefer appropriately named documents in docs/
---

### Optional improvement: record base SHA

You liked the idea of recording the base SHA used when an agent starts from `origin/main` (e.g. `#base/<sha>`). This is a good future addition because it makes debugging “worked on stale main” situations much faster.

---

**Agent Action**: 
- go ahead and add this to the process, with appropriate documentation both in this project and for target projects

---
## Local Exchange (Clarifications)

- Local Exchange is not “optional” in the sense that the dashboard requires refs to be pushed there.
- What can be optional is **agent awareness** of Exchange.

Recommended direction:

- Keep Exchange as an operator-managed mechanism.
- Make “normal `git push`” go to Exchange by default (set branch upstream / `remote.pushDefault=exchange`), so agents don’t have to learn or mention it.

See `docs/local-exchange-out-of-band.md`.

---

**Agent Action**: 
- provide an agent prompt to setup local exchange in a target project (to be run separately from the main install, but the main install should emit a reference to it)

---
## Installer Direction

- The static installer should remain the baseline.
- An “agent installer” is feasible and potentially better for interactive reconciliation, but should be added as an optional guided workflow (not the only installation path).

See `docs/iterations/100-Installation.md`.

## New Feedback / Recommendations

### “Tell me more” on reducing shared-file collisions

The sharding idea is not “replace TODO.md”, it’s to reduce write pressure on it.

Practical patterns if TODO conflicts get annoying:

- Keep `docs/process/TODO.md` as the queue, but have agents write detail into per-task files like `docs/process/tasks/<slug>.md` and only update the queue line.
- For large features on long-lived branches, keep a branch-local checklist in the spec file itself, and only promote items into the main TODO when they’re ready to be worked as independent slices.

This preserves the core “TODO checkpoint” while keeping most high-churn writing out of the shared hotspot.

---
**Agent Action**: 
- provide documentation of the idea & suggestions how/when to do it, in `docs/`, & a pointer to that documentation in what is installed in target process (likely the README.md in payload/docs/process)
- payload/docs organization tweaks:
	- move `payload/docs/process/ash-roadmap.md` out of `payload/docs/process.md` and into `docs/`
	- move the `Future` section out of `payload/docs/process/git-workflow.md` and integrate into `payload/docs/process/ash-roadmap.md`
	- don't add `payload/docs/process/local-exchange.md` with the main installer, but add it with the (new) local-exchange.md setup installer referenced earlier
	- remove `payload/docs/process/using-gitx-as-a-dashboard`. Add a section to `payload/docs/process/local-exchange.md`  suggesting how the local-exchange setup enables using gitx as a sort of dashboard showing a linear history of what was worked on, with the branch labels acting as pointers to allow a human to quickly view what was done

---

### YAML preference implemented

The prompt context mapping now lives in `payload/scripts/context.config.yaml` and `payload/scripts/run-prompt` parses it without external dependencies.

### Prompts vs playbooks

The kit now distinguishes:

- **Prompts** (`payload/docs/ai/prompts/`): clean-context job starters.
- **Playbooks** (`payload/docs/ai/playbooks/`): mid-session procedures.
- **Instructions** (`payload/docs/ai/instructions/`): always-on navigation/policy.

`scripts/context.config.yaml` starts empty and exists only to add **project-specific extra inputs**. Baseline inputs live in YAML frontmatter on the prompt/playbook files.
