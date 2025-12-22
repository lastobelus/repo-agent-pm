#status/active

- start by reading `payload/docs/ai/README.md`

## Add a topic process
- topics are longer-lived iterations, may require multiple clean-context agent runs
	- we'll use a start-topic prompt & continue-topic prompt
- we want commits of atomic/meaningful phases, not just final
- we should (unless changes too complex) ff rebase each time
- we should push topic branches to origin; we don't want to lose a large chunk of work, where as with todos we don't care, we can just re-run them
- when working on topics, we want to use the sequential iteration via markdown files strategy in [[sequential-iteration-via-markdown-files]]. But since this was getting complicated, we decided to put a pin in it for now and spend some time working with just a very simple lose version. Leave [[sequential-iteration-via-markdown-files]] as is, and for now the topic implementer prompts need to instruct to use the simple version in [[020.1-discuss-fears-of-antipattern#Option 1 Put a pin in the spec]]
- this means topics need a place to live in process, as they will acquire multiple working documents.
- Topics & specs are connected, but loosely. The work of a topic will typically refer to one or more specs.
- a topic should have a directory in `payload/docs/process/topics` that matches the branch name, but prefaced with a serial `001-` etc., so that they naturally appear in implementation order
- ensure `payload/docs/process/topics` has a README.md explaining how it is used
- to illustrate the process, add `payload/docs/process/topics/000-example/000-initial-iteration.md`
- to work on a topic, the user will create clone `payload/docs/process/topics/000-example/000-initial-iteration.md` and add notes about the first steps to start the work, referencing any necessary specs
- then it will start an agent with the `start-topic` prompt & the contents of the initial iteration doc
    - let's have a script to do this. You can run it without arguments in the `topic/00X-some-topic` branch or run it elsewhere with `-t path/to/topic`
    - it outputs to STDOUT so can be used with coder etc.
- agent will respond by planning & asking questions in the current iteration doc, performing `AGENT Action` blocks. 
- continue-topic script when run in the topic dir figures out the correct iteration doc based on `#status/` tags. If ambiguous, it prompts using fzf. When choice confirmed, it updates `#status/` tags as necessary, and emits the `continue-topic` prompt concatenates with the contents of the chosen iteration doc
---
## Ask Questions and Clarifications here

### Topic directory ↔ branch mapping

#question For a topic branch named `topic/<slug>`, what should the corresponding directory name be under `payload/docs/process/topics/`?

#answer this one: Option A: `001-<slug>/` (recommended: simplest + grep-friendly)
- Option B: `001-topic-<slug>/`
- Option C: `001-topic__<slug>/` (explicitly encodes the `/`)

#question Do we want to **require** the `<slug>` to appear verbatim in the directory name (so scripts can infer the topic dir from the branch name without extra metadata), or is it OK to introduce a tiny metadata file like `topic.meta.md`/`topic.yaml` inside the topic dir?
> #answer: require slug in dir name

### Status tags + continue-topic selection rules

#question Which status tags are “eligible” for `continue-topic` to pick as the current iteration doc?

- only `#status/active`
- `#status/active` else fallback to `#status/draft`
- include `#status/discussing` as eligible
> #answer: everything that's NOT `#status/finished`, then mark the current `#status/active` as `#status/finished` and any file missing a `#status/` as `#status/draft`


#question If `continue-topic` finds **multiple** `#status/active` iteration docs in the topic dir, do we:

- fail hard and ask the human to fix it
- #answer this one: prompt to select (fzf), then automatically demote the others to `#status/finished`
- prompt to select but do not auto-edit other files

#question When the human selects an iteration doc via `fzf`, should `continue-topic` automatically ensure exactly one active doc (i.e., set selected to `#status/active` and all others to `#status/finished`), or should it only edit the chosen file? #answer automatically ensure exactly one active document, set other actives to finished, with a note. User can always change them back to  `#status/discussing` if they want.

### Prompt semantics + git policy

#question For long-lived topics, do we want to recommend **rebasing** a published `topic/<slug>` branch?

- If yes, do we explicitly endorse `git push --force-with-lease` (after a rebase), or do we prefer merge-based updating to avoid rewriting remote history?
- > #clarify can we do rebase/push/rebase-again until push succeeds? We'll only have a single digit number of agents operating concurrently, and they typically take at least a few minutes to run, so collisions won't churn long

#answer Yes — if we recommend rebase for topic branches, the safe loop is:

- `git fetch origin`
- `git rebase origin/main` (or whatever trunk is)
- `git push --force-with-lease`
- if push is rejected (remote moved), repeat: fetch → rebase → force-with-lease

This only works safely if we *always* use `--force-with-lease` (never plain `--force`). It also assumes low concurrency on the same topic branch (which matches your stated policy).

#question The Agent Action text says “pull/ff-only + rebase/ff policy guidance — prefer rebase onto origin/main, fallback to merge if churning”. Confirm the canonical guidance we want in the consumer docs:

- `git pull --ff-only` from `origin/topic/<slug>` 
- rebase `topic/<slug>` onto `origin/main` regularly
- land via fast-forwardable slices into `main`

> #clarify we don't need to pull from `origin/topic` — for now policy is only one agent working on a topic. not-in-scope & nice-to-haves will become todos to be done after the topic is merged main
> does that clarify sufficiently?

#answer Yes — that’s sufficient. We can write the policy as:

- “Assume a single worker on a topic branch.”
- “Do not routinely pull from `origin/topic/<slug>`; just `git fetch origin`, rebase onto `origin/main`, and push updates.”

If we later relax this to multi-worker-per-topic, we can add a follow-up todo to support `origin/topic/<slug>` sync + conflict policy.

### Script UX + naming

#question Should the installed scripts be:

- `scripts/start-topic` and `scripts/continue-topic` (no extension)
- `scripts/start-topic.sh` and `scripts/continue-topic.sh` (consistent with `run-prompt.sh`)
> #answer I prefer not to have `.sh`, can we also rename the other scripts please.

#question Confirm scope for “rename the other scripts”:

- rename `scripts/run-prompt.sh` → `scripts/run-prompt`
- rename `scripts/install-local-exchange.sh` → `scripts/install-local-exchange`

Any others in-scope right now?

#answer Implemented as:

- `scripts/run-prompt.sh` → `scripts/run-prompt`
- `scripts/install-local-exchange.sh` → `scripts/install-local-exchange`
- New: `scripts/start-topic` and `scripts/continue-topic`

Not touched (still `.sh`) because they are Local-Exchange internals that get installed later: `scripts/setup-exchange.sh`, `scripts/gitx-wrapper.sh`.

### Branch naming (numeric prefix)

#question Earlier notes mention running in a branch like `topic/00X-some-topic`. Do we want the numeric prefix in the **branch name** too, or only in the **topic directory** (recommended: only in the dir, branch stays `topic/<slug>`) ?

#answer Implemented the recommended approach: numeric prefix only in the topic directory (`NNN-<slug>`), and the branch is `topic/<slug>`.

#question Is `fzf` a hard dependency for `continue-topic` (required), or should we provide a fallback picker when `fzf` is missing?

> #answer hard dependency

#question For `start-topic`, should the script:

- require the human to have already created the topic directory + initial iteration doc, and only generate the prompt
- #answer this one: or optionally scaffold missing topic files (create the topic dir + seed `000-initial-iteration.md` from the example)

### Backwards compatibility (rename implement prompt)

#question When renaming `payload/docs/ai/prompts/implement.md` → `implement-one-todo.md`, do we want to keep a compatibility shim `implement.md` (that just points to `implement-one-todo`) for new installs, or do we want a clean break and update all references to the new name? 
> #answer clean break

---

## Proposed Plan (after questions answered)

1. **Clarify naming + mapping rules**
   - Decide the canonical topic directory naming scheme under `payload/docs/process/topics/`.
   - Decide the status-tag rules for selecting the “current” iteration doc.

2. **Make Topics a first-class consumer doc area**
   - Add `payload/docs/process/topics/README.md` explaining:
     - what topics are vs TODOs
     - how topic dirs are named
     - how iteration docs work (`#status/*` tags)
     - how to start/continue a topic using scripts
   - Add `payload/docs/process/topics/000-example/000-initial-iteration.md` as the seed template.

3. **Split TODO implement prompt naming**
   - Rename `payload/docs/ai/prompts/implement.md` → `payload/docs/ai/prompts/implement-one-todo.md`.
   - Update all references in:
     - `payload/AGENTS-additions.md`
     - `README.md` (repo + consumer-facing copy where applicable)
     - `payload/scripts/run-prompt` header comment/example
     - any other docs mentioning `run-prompt implement`
   - Decide whether to keep a compatibility shim `payload/docs/ai/prompts/implement.md` (only if we explicitly want it).
       - #answer not needed

4. **Add clean-context topic prompts**
   - Create `payload/docs/ai/prompts/start-topic.md` and `payload/docs/ai/prompts/continue-topic.md` with YAML frontmatter.
   - Ensure they:
     - run clean-tree preflight
     - enforce branch naming `topic/<slug>`
     - record base SHA (where + how is documented)
     - implement one atomic slice per run
     - push to origin (and document rebase/merge guidance)

5. **Add scripts to generate prompts from a topic directory**
   - Create `payload/scripts/start-topic` (or `.sh`) that:
     - resolves the topic directory from `-t <path>` OR current branch name (if on `topic/<slug>`)
     - prints the `start-topic` prompt + the initial iteration doc contents to stdout
   - Create `payload/scripts/continue-topic` (or `.sh`) that:
     - resolves topic directory
     - selects the iteration doc via `#status/*` tags (fzf if ambiguous)
     - updates tags as needed
     - prints the `continue-topic` prompt + chosen iteration doc contents

6. **Doc pass + verification**
   - Confirm `scaffold-project.py` copies all new payload files as expected (it should, but verify).
   - Run a local dry-run install into a temp folder and validate:
     - `./scripts/run-prompt start-topic` and `continue-topic` output are sensible
     - `./scripts/start-topic` and `./scripts/continue-topic` work end-to-end in a toy git repo
---

## **Agent Action**:

### Topics & TODOs are different processes
- rename `payload/docs/ai/prompts/implement.md` to `payload/docs/ai/prompts/implement-one-todo.md`, and update references
- scan the project for references to todo, and ensure it is clear that:
    - todos are intended to be "one-shot", finished in a single session.
    - topics are intended to be worked on iteratively, possibly over multiple work sessions, in long-lived branches
### Draft two clean-context prompts for long-lived work:

1) `start-topic`
   - clean-tree preflight
   - create `topic/<slug>`
   - record base SHA
   - plan + implement first atomic slice
   - push branch to origin

2) `continue-topic`
   - clean-tree preflight
   - pull/ff-only + rebase/ff policy guidance
       - prefer rebase onto origin/main, fallback to merge if churning
   - implement next slice with meaningful commit
   - push updates to origin

### Setup Topics
1. create `payload/docs/process/topics/000-example/000-initial-iteration.md`
2. write  `payload/docs/process/topics/README.md`

### Write scripts
1. create `payload/scripts/start-topic`
2. create `payload/scripts/continue-topic`
