# AI Process Artifacts

This folder contains artifacts intended for use by AI agents (and the human operator).

## Mental Model

There are three layers:

1. **Instructions** (`docs/ai/instructions/`)
   - Always-on policy and navigation: where truth lives, how to find specs, safety rules.
   - These are stable and referenced by everything else.

2. **Playbooks** (`docs/ai/playbooks/`)
   - “Procedures”: checklists/protocols used mid-session.
   - Assumes some working context exists (current branch, diffs, local state).
   - Can still be referenced from clean-context jobs, but they are not the “starting prompt”.

3. **Prompts** (`docs/ai/prompts/`)
   - Clean-context job starters: the initial message you feed to a fresh agent invocation.
   - Must declare inputs/outputs/stop conditions because they cannot rely on previous chat context.

## YAML Frontmatter

Prompts and playbooks may start with YAML frontmatter:

- `kind`: `prompt` | `playbook` | `instruction`
- `mode`: `clean-context` | `in-session`
- `inputs`: paths to include as context (files or directories)
- `outputs`: what the agent should produce
- `writes`: expected files to modify
- `stop_conditions`: when to stop and ask a human

The frontmatter is metadata for tooling; it is not meant to be shown to the agent as part of the prompt.

## Tooling

Use `scripts/run-prompt <name>` to print a prompt/playbook plus its inputs (and any project-specific inputs from `scripts/context.config.yaml`).

## YAML Spec (Tiny)

This kit intentionally supports a **very small YAML subset** so it can be parsed with standard shell tools.

### Frontmatter (`--- ... ---`)

Supported keys:

- `kind`: `prompt` | `playbook` | `instruction`
- `mode`: `clean-context` | `in-session` | `always`
- `name`: string
- `inputs`: list of paths (strings)
- `outputs`: list of strings (optional)
- `writes`: list of paths (optional)
- `stop_conditions`: list of strings (optional)

Rules:

- Frontmatter must start on the first line with `---` and end at the next `---`.
- Lists must be written as one-item-per-line using `- `.
- No nested objects are supported.

### `scripts/context.config.yaml`

Purpose: add **project-specific extra inputs** without editing kit prompt files.

Supported keys:

- `instructions`: list of extra paths applied to all runs
- `global_inputs`: list of extra paths applied to all runs
- `task_inputs`: mapping of task name → list of extra paths

Rules:

- `task_inputs` only supports one level deep (task name keys).
- Values must be lists written as `- ` items.
- Duplicate paths are deduped by `scripts/run-prompt`.
