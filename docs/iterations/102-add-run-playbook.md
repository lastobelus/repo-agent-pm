#status/active

   - In interactive sessions (like Codex/Code), AGENTS.md and context-strategy.md are already loaded, so run-prompt currently duplicates them.
   - run-prompt is still useful to use interactively during agent sessions because it bundles the playbook/prompt + inputs + TODO, reducing round trips.
   - Proposed fix: add run-playbook for in-session use that bundles only the playbook and its declared inputs (no AGENTS/context-strategy).
   - Also add a configurable switch for run-prompt to include or skip AGENTS injection depending on agent runtime (needed for some CLIs, not for Codex/
   Code).
   - if AGENTS.md already points to `payload/docs/ai/instructions/context-strategy.md`, do we need to specify it in prompt requirements? #question
   - Update top-level instructions so interactive agents are guided to use run-playbook rather than run-prompt, unless they are actually launching a subagent
   - provide wrappers in scripts/ for:
     - coder
     - qwen
     - gemini
     - opencode
     - claude
   - these wrappers should assume the argument is the name of a prompt and run it through run-prompt then pass the result and all other arguments/switches to the specified cli
   - OMM all these tools are configured to read AGENTS.md, so none of them need to prepend AGENTS.md. In scripts/README.md document how to change them to tell run-prompt to prepend AGENTS.md for users who don't wish to configure their cli's thusly

## Decisions
- #question: if AGENTS.md already points to `payload/docs/ai/instructions/context-strategy.md`, do we need to specify it in prompt requirements?
  - Answer: keep `context-strategy.md` listed in prompt inputs for clean-context runs; AGENTS references are not guaranteed in every CLI. In-session runs now use `run-playbook`, which omits instructions and avoids duplication.

## Changes
- Added `payload/scripts/run-playbook` for in-session playbook loading (playbook + declared inputs only).
- Added `--with-agents/--no-agents` switch to `payload/scripts/run-prompt` (optional AGENTS injection).
- Added CLI wrappers in `payload/scripts/` for coder/qwen/gemini/opencode/claude.
- Added `payload/scripts/validate-cli-wrappers` test harness (probe mode + optional CLI args).
- Added `scripts/test-harness` maintainer helper to install the kit into a temp repo and run wrapper checks there (probe or real echo test).
- Added Bats-based tests under `scripts/tests/` covering probe and real echo flows.
- Added `payload/scripts/README.md` documenting wrappers and AGENTS injection toggles.
- Updated consumer docs to guide in-session use of `run-playbook` and mention wrappers.
- Updated `scaffold-project.py` to mark new scripts as executable.

## Next Steps
- Validate wrapper behavior with each CLI in a consumer repo.
- Confirm any CLI-specific flags needed for stdin prompt ingestion and adjust wrappers if necessary.
- Consider adding a per-CLI config file if env-based args prove too limiting.
