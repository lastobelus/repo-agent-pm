#status/finished 

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

**Agent Action**
1. Review the entire kit, reading whatever files necessary to ensure:
    - kit is ready to start using in a project (don't be too nit-picky, prefer to let details be uncovered by iterating with real work in a project)
2. ensure `scaffold-project.py` is complete
3. add optional “guided install” playbook that an agent can run to tailor the kit (e.g., `docs/ai/playbooks/installer.md`).
4. Install to `../liftanvil/liftanvil-one`, fixing any issues. Some directories may already exist; prompt if any files would be overwritten

## Agent Updates (2025-12-22)

### Decisions
- Added a guided install playbook for agent-led tailoring.
- Documented the guided install in both maintainer and consumer-facing docs.

### Changes
- Added `payload/docs/ai/playbooks/installer.md` (guided install playbook).
- Updated `payload/docs/ai/playbooks/README.md` to list the installer playbook.
- Updated `payload/docs/process/README.md` with a guided install section.
- Updated `payload/AGENTS-additions.md` with a guided install entry.
- Updated `docs/Overview.md` to reference the guided install playbook.

### Install Attempt
- Tried `python3 scaffold-project.py ../liftanvil/liftanvil-one`.
- Blocked by OS permissions when creating `../liftanvil/liftanvil-one/.rapm` (Operation not permitted).

#agent-question
Can you grant write access or run the installer from your user account?
Suggested command:

```bash
python3 scaffold-project.py ../liftanvil/liftanvil-one
```
