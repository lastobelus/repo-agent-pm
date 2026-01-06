# Scripts (Installed)

This folder contains helper scripts installed into a consumer project.

## Prompt / Playbook Printers

- `run-prompt <name>` prints a clean-context prompt plus its declared inputs.
- `run-playbook <name>` prints a playbook plus its declared inputs (no AGENTS/context injection).

Use `run-prompt` when starting a **fresh** agent session. Use `run-playbook` when you are already in an interactive session and just need the mid-session procedure.

## CLI Wrappers

Wrappers generate a prompt and pass it to the CLI via stdin:

- `coder`
- `qwen`
- `gemini`
- `opencode`
- `claude`

Example:

```bash
./scripts/claude implement-one-todo --model claude-3-5-sonnet
```

These wrappers assume your CLI is already configured to read `AGENTS.md` on launch.

### If your CLI does NOT read `AGENTS.md`

You have two options:

1. Set an environment variable when invoking the wrapper:

```bash
RUN_PROMPT_INCLUDE_AGENTS=1 ./scripts/claude implement-one-todo
```

2. Permanently change the wrapper to inject AGENTS by adding `--with-agents` to
`RUN_PROMPT_FLAGS` near the top of the script.

Notes:
- The Claude wrapper injects `-p <prompt>` internally, so avoid passing `-p/--print` yourself.
- The OpenCode wrapper uses `opencode run <prompt>` internally; extra args are appended after the prompt.

## Wrapper Validation Harness

Use `validate-cli-wrappers` to automate wrapper checks:

```bash
./scripts/validate-cli-wrappers --probe implement-one-todo
```

Probe mode replaces the CLI with a stub that captures stdin, so you can confirm
that each wrapper pipes the prompt correctly. For real CLI runs, omit `--probe`.

Optional environment variables for real runs:

- `CLAUDE_ARGS`, `CODER_ARGS`, `QWEN_ARGS`, `GEMINI_ARGS`, `OPENCODE_ARGS`

## Topics

- `start-topic -t docs/process/topics/NNN-<slug>`
- `continue-topic -t docs/process/topics/NNN-<slug>`

These wrap `run-prompt` for long-lived, multi-session work.
