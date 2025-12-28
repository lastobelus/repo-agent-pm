
## Agents Additions
read payload/AGENTS-additions, and any files it references. Discuss the following questions, without taking action:

1. Context Strategy section
    - If Agents must always read  `docs/ai/instructions/context-strategy.md` , should it be inline in `AGENTS.md`? or better as separate doc, but it will always be prepended to a prompt when using run-prompt?
    - is the following instruction relevant to agents, or is it documentation for humans?
  >- **Clean-context jobs:** Use the prompts in `docs/ai/prompts/` (via `scripts/run-prompt <name>`).
  
      - it does make sense for orchestrator agents that launch agents. But can every-code actually do that?
      - same question for the `## Core Workflows` section
2. Guided Install section -- pretty sure this belongs in human documentations, not AGENTS.md

## Local Exchange
"Local Exchange" concept/installer/scripts is fragmented. How can we consolidate & organize it, and clarify it for a person installing the kit?
