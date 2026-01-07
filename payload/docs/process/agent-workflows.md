# Operator Guide: Agent Workflows

This document translates the agent rules (from `AGENTS.md`) into human-facing instructions and examples.

## Context Strategy (What Agents Read)

Agents should always read `docs/ai/instructions/context-strategy.md`. It explains where specs live and how to use prompts/playbooks.

If an agent is starting from a fresh session, run `./scripts/run-prompt <name>` and paste the output into the agent.

If you are already mid-session (AGENTS loaded), use `./scripts/run-playbook <name>` to avoid duplicating AGENTS/context-strategy.

## Current Scope (Temporary Defaults)

Playbooks assume Phoenix/Elixir/Ash and use `mix test` by default. If your stack differs:

- Update `docs/process/README.md` with your real test command and branch names.
- Add stack-specific docs to `scripts/context.config.yaml` so agents always see them.

## Context Safety (Human-Only Docs)

Files marked with `> 🛑 Human Context Only` are for humans, not agents. If an agent is working, do not provide those files unless the task is specifically about changing that process document.

## Core Workflows (Examples)

The clean-context workflows are the default entry points for agents. If an agent cannot run shell commands, you run the prompt and paste it.

### Example: Add a TODO

```bash
./scripts/run-prompt add-todo
```

Then paste the printed prompt into a fresh agent session. The agent will ask for the todo text and will add origin tags.

### Example: Implement One TODO

```bash
./scripts/run-prompt implement-one-todo
```

Expected interaction:

```
Agent: I need the current TODO queue and relevant specs.
Human: (pastes prompt output, which includes docs/process/TODO.md and specs)
Agent: I'll pick the next approved TODO and implement it.
```

### Example: Land Work

```bash
./scripts/run-prompt land
```

The agent should run tests, update `docs/process/TODO.md` with `#done/<sha>`, and push/prepare for merge.

### Example: Triage the Queue

```bash
./scripts/run-prompt process-todos
```

Use this when Inbox grows or TODO ordering needs cleanup.

### Example: Start / Continue a Topic

```bash
./scripts/start-topic -t docs/process/topics/001-some-topic
./scripts/continue-topic -t docs/process/topics/001-some-topic
```

Topics are for multi-session, higher-uncertainty work.

## Topics vs TODOs

- **TODOs** are one-shot tasks intended to finish in a single clean-context run.
- **Topics** are multi-session tasks with evolving notes and decisions.

## TODO Discipline (Why Tags Matter)

The queue lives at `docs/process/TODO.md`.

- Every todo line has an origin tag `#<shortsha>`.
- Completed todos get a completion tag `#done/<shortsha>`.
- If an agent starts from trunk, it may add `#base/<shortsha>`.

These tags keep concurrent edits safe and provide traceability.

## Buffered Integration (Branching Protocol)

- `main` is the development trunk.
- `stable` is the deployed/demo branch.
- Agents work on `topic/*` (or whatever prefix you set).

If you use Local Exchange, agent pushes can be routed to a local-only remote instead of GitHub.

## Guided Install (Operator-Only)

If you need to tailor conventions (test command, branches), run:

```bash
./scripts/run-prompt installer
```

That playbook will walk you through the install steps and document the project-specific defaults.

## Local Exchange (Optional)

See `docs/process/local-exchange.md` for setup and out-of-band options.
