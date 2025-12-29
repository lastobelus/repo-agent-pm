---
kind: prompt
mode: clean-context
name: setup-local-exchange
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/process/README.md
  - docs/process/local-exchange.md
  - scripts/setup-exchange.sh
  - scripts/gitx-wrapper.sh
outputs:
  - exchange repo created + slot remotes configured
stop_conditions:
  - repo layout differs (no wrapper root / no slots)
---

You are helping a human operator set up the Local Exchange workflow.

Goals:

1. Ensure Local Exchange docs/scripts are present.
2. Explain how to run the one-time setup and how it affects day-to-day pushing.

Steps:

1. Confirm `docs/process/local-exchange.md` and the Local Exchange scripts exist (they are installed with the kit).
2. Ask the human where their wrapper root is (the directory that contains `slot-1`, `slot-2`, etc.).
3. From any slot repo, run `./scripts/setup-exchange.sh --wrapper-root <path>`.
4. Explain the “out-of-band” option (`--set-push-default`) if they want agents to remain unaware of Exchange.
