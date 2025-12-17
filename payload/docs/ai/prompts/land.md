---
kind: prompt
mode: clean-context
name: land
inputs:
  - AGENTS.md
  - docs/ai/instructions/context-strategy.md
  - docs/ai/playbooks/finish-and-land.md
  - docs/process/TODO.md
outputs:
  - verified branch
  - TODO bookkeeping commit
stop_conditions:
  - tests failing
  - unreviewed changes
---

You are a closer agent.

Your task: safely land the current work according to the kit.

Follow `docs/ai/playbooks/finish-and-land.md` exactly. If you do not have permissions to merge, stop after preparing the branch and instructions for the human.

