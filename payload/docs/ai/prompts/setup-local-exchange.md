---
kind: prompt
mode: clean-context
name: setup-local-exchange
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/process/README.md
  - .kit/local-exchange/docs/process/local-exchange.md
  - scripts/install-local-exchange.sh
outputs:
  - local-exchange docs + scripts installed
stop_conditions:
  - repo layout differs (no wrapper root / no slots)
---

You are helping a human operator set up the Local Exchange workflow.

Goals:

1. Install the Local Exchange docs/scripts into their standard locations in this project.
2. Explain how to run the one-time setup and how it affects day-to-day pushing.

Steps:

1. Run `./scripts/install-local-exchange.sh`.
2. Ask the human where their wrapper root is (the directory that contains `slot-1`, `slot-2`, etc.).
3. In that wrapper root, run `./scripts/setup-exchange.sh`.
4. Explain the “out-of-band” option (make `git push` default to exchange) if they want agents to remain unaware of Exchange.

