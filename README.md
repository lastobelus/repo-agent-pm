# repo-agent-pm

This repository maintains **repo-agent-pm (rapm)**: a redistributable set of process docs, agent playbooks, and helper scripts for running a solo-dev + multi-agent workflow.

**What this is:** lightweight, in-repo coordination for **one human running multiple concurrent agents**.

**What this is not:** a good alternative to project management for multi-human teams. It deliberately trades off multi-person planning features for speed, flexibility, and just enough back-pressure to keep a solo operator and several agents aligned.

## Repo Layout

- `payload/`: Everything that gets installed into a consumer project
  - `payload/docs/`: process docs + agent playbooks
  - `payload/scripts/`: helper scripts (prompt runner, exchange setup, etc.)
  - `payload/AGENTS-additions.md`: a partial intended to be appended into the consumer project’s `AGENTS.md`
  - `payload/test/support/feedback/.keep`: ensures the feedback inbox exists
- `docs/`: maintainer docs for evolving the kit (not installed)
- `scaffold-project.py`: installer that copies `payload/` into a target project

## Install Into a Project

```bash
python3 scaffold-project.py /path/to/your/project
```

Overwrite modes:

```bash
python3 scaffold-project.py --overwrite /path/to/your/project
python3 scaffold-project.py --overwrite-keep-todo /path/to/your/project
```

Installer behavior:
- Copies `payload/*` into the target (without overwriting existing files).
- If the target already has `AGENTS.md`, appends the kit rules from `AGENTS-additions.md` (idempotently) and removes `AGENTS-additions.md`.
- If the target lacks `AGENTS.md`, creates it from `AGENTS-additions.md` and removes `AGENTS-additions.md`.

## Use In the Consumer Project

Use the prompt context helper:

```bash
./scripts/run-prompt implement-one-todo
```

## Maintaining The Kit

Start with `docs/iterations/001-initial-feedback.md` and `docs/iterations/002-updated-intent.md`.

Process note (maintainer-only): `docs/process/sequential-iteration-via-markdown-files.md`.
