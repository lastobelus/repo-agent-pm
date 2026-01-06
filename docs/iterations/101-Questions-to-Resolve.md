#status/finished 


## Agents Additions
read payload/AGENTS-additions, and any files it references. Discuss the following questions, without taking action:

1. Context Strategy section
    - If Agents must always read  `docs/ai/instructions/context-strategy.md` , should it be inline in `AGENTS.md`? or better as separate doc, but it will always be prepended to a prompt when using run-prompt? #question
      - Answer: keep it as a separate doc and reference it from `AGENTS.md`. It is already included via `run-prompt` inputs and is easier to maintain/version than an inline block. Inline only if we need a tiny “must-read” summary (1-2 bullets), otherwise keep the source in `docs/ai/instructions/context-strategy.md`.
    - is the following instruction relevant to agents, or is it documentation for humans? #question
  >- **Clean-context jobs:** Use the prompts in `docs/ai/prompts/` (via `scripts/run-prompt <name>`).
  
      - Answer: relevant to agents. It is an instruction for how agents should invoke clean-context runs. Not just for orchestrators; any agent with shell access can run `scripts/run-prompt`. If an agent cannot run shell commands in the environment, it should ask the human to run it.
      - it does make sense for orchestrator agents that launch agents. But can every-code actually do that? #question
        - Answer: yes for CLI agents in this kit; they can run scripts. If a given agent instance is constrained (no shell), it should request a human to run the command and provide the output.
      - same question for the `## Core Workflows` section
        - Answer: relevant to agents as default workflow entry points. Keep them in `AGENTS-additions.md`, but consider adding a short note like “If you can’t execute shell commands, ask the human to run these.”
2. Guided Install section -- pretty sure this belongs in human documentations, not AGENTS.md? #question
    - Answer: agree. Guided install is a human/operator flow; it belongs in `payload/docs/process/README.md` and/or the installer playbook. In `AGENTS-additions.md`, it should only appear if we want agents to be aware that a guided install exists when explicitly asked.

## Local Exchange
"Local Exchange" concept/installer/scripts is fragmented. How can we consolidate & organize it, and clarify it for a person installing the kit?

- Answer: propose a single “Local Exchange” entry point doc + one installer script, then reference them consistently:
  - Make `payload/docs/process/local-exchange.md` the canonical human doc (overview, quick-start, out-of-band option, and dashboard note).
  - Keep `payload/docs/process/README.md` with a short summary + link to `docs/process/local-exchange.md`.
  - Ensure `scripts/install-local-exchange` installs from payload (no hidden `.rapm` dependency), so the artifact lives under `payload/` and is always present.
  - Keep the clean-context prompt `setup-local-exchange` focused on “run installer + explain wrapper root + out-of-band option,” and make it reference the canonical doc.
  - Optional: move maintainer-only notes (currently in `docs/local-exchange-out-of-band.md`) into the consumer doc as a clearly labeled “Operator / Out-of-Band” subsection, and keep a maintainer-only copy only if it needs extra detail.

## Decisions / Updates
- Keep `context-strategy.md` as a separate always-read doc; avoid inlining in `AGENTS.md` except possibly a tiny summary.
- Treat clean-context prompts and Core Workflows as agent-relevant instructions; add a “ask human if no shell” note if needed.
- Guided install is primarily human documentation; keep in process docs and playbooks, not in `AGENTS-additions.md` unless explicitly needed.
- Local Exchange docs/scripts now live in the default payload with a single canonical doc and setup scripts.

## Changes Made
- Answered all #question items inline.
- Added a human-facing docs entry point at `payload/docs/README.md` and an operator guide with examples at `payload/docs/process/agent-workflows.md`.
- Added `payload/docs/process/local-exchange.md` and aligned Local Exchange references to it.
- Added Local Exchange setup scripts (`payload/scripts/setup-exchange.sh`, `payload/scripts/gitx-wrapper.sh`) and simplified `payload/scripts/install-local-exchange`.
- Guarded Local Exchange setup to skip non-slot git repos and avoid hijacking unrelated remotes.
- Adjusted Local Exchange setup to prompt the operator to select slot repos when multiple clones exist.
- Added `--add-slots` support to create slot clones from a repo URL.
- Updated `payload/AGENTS-additions.md` to remove guided install and add a shell-availability note.
- Updated `payload/docs/process/README.md`, `payload/docs/ai/README.md`, `payload/docs/process/bus-factor.md`, `scaffold-project.py`, and maintainer notes to reflect the new docs/Local Exchange layout.

## Next Steps
- Review the new Local Exchange setup script assumptions (slot layout and wrapper root).
- Decide whether to keep `scripts/install-local-exchange` as a compatibility shim or remove it in a later cleanup.

**Agent Action**
- let's ensure there is clear human-facing documentation installed with the kit, with a clear starting point, and what to read next, what to read for various development scenarios. Provide an
- let's provide human-facing documentation for elements in AGENTS-additions, with examples of interactive sessions. 
  - rework guided install as you recommended
  - rework local exchange as you recommended
