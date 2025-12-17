# Installation

This kit currently ships a Python installer (`scaffold-project.py`) that copies `payload/` into a target repository and merges the agent rules into `AGENTS.md`.

## Feasibility: “Agent Installer” Instead of Python

An “agent installer” (i.e., run a CLI agent to install and reconcile process artifacts) is feasible, and it could be strictly better than a static copier in a few ways:

- It can ask interactive questions (branch model, test command, whether the project already has `AGENTS.md`, preferred TODO format, etc.).
- It can detect and reconcile conflicts with existing conventions, rather than clobbering.
- It can produce a human-readable “installation report” (what changed, why, and what to do next).

However, it also has real tradeoffs:

- **Determinism / auditability:** A static installer is reproducible; an agent installer can drift unless tightly constrained.
- **Dependency surface:** It requires the user to have an agent runtime available and trusted.
- **Failure modes:** Partial installs, or installs that vary by model/tooling.

### Recommendation

Use a hybrid:

- Keep `scaffold-project.py` as the always-available baseline (copy + minimal merge).
- Add an optional “guided install” playbook that an agent can run to tailor the kit (e.g., `docs/ai/playbooks/installer.md`).

This keeps the kit installable everywhere, while still enabling a richer interactive experience when desired.

