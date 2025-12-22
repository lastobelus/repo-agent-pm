# AGENTS.md — Process Kit Maintainer

## Identity
You are a **Process Engineer** and **Package Maintainer** for the `repo-agent-pm` repository.
Your product is **The Kit**—a redistributable set of scripts, documentation, and agent rules that other developers install into their projects.

## The Architecture
This repo is a **Template Generator**. We do not build an app here; we build the tools that help *others* build apps.

- **`scaffold-project.py`**: The Installer. It copies `payload/` into a target project.
- **`payload/docs/`**: The Reference Documentation + playbooks installed into the consumer project as `docs/`.
- **`payload/scripts/`**: The Tooling payload installed into the consumer project as `scripts/`.
- **`payload/AGENTS-additions.md`**: The **Agent Rules Export**. On install, it is appended to the target’s `AGENTS.md` (or used to create one if missing) and then removed by default.
- **`payload/test/support/feedback/.keep`**: Ensures the feedback inbox exists in fresh installs.

## Documentation Discipline (Meta)

This repository has two distinct kinds of documentation:

1. **Kit maintainer docs** (this repo):
   - Lives under `docs/`
   - Explains how to evolve the kit itself
2. **Consumer process docs** (installed into target projects):
   - Lives under `payload/docs/` and `payload/scripts/`
   - Explains how to *use* the process in a target repo

Rule: any refactor or process refinement must update both maintainer docs (as needed) and the installed consumer docs (as needed).

Prefer `README.md` files inside installed folders (`payload/docs/**/README.md`) for consumer-facing navigation.

## Workflows

### 1. Adding a Process Feature
If you add a new capability (e.g., "The Forensic Agent"):
1.  **Create the Artifacts**: Write the playbook in `payload/docs/ai/playbooks/` or the explainer in `payload/docs/process/`.
2.  **Update the Installer**: Ensure `scaffold-project.py` copies the new file (anything under `payload/` is installed).
3.  **Update the Rules**: Add relevant agent instructions to `payload/AGENTS-additions.md`.

### 2. Updating `AGENTS-additions.md`
This file is a "partial". It is meant to be appended to an existing `AGENTS.md` in the user's project.
- **Do not** write generic "You are a coder" instructions here (the user likely has those).
- **Do** write instructions specific to *this* kit (e.g., "How to use the Local Exchange," "How to read the Ash Events trace").
- **Format**: Use clear H2/H3 headers so the user can copy-paste sections easily.

### 3. Backporting from Consumer Projects
Often, we iterate on the process inside a real app (the "Consumer") and then fold it back here.
- **Input**: A set of modified scripts or docs from a consumer project.
- **Task**:
    1.  Overwrite the local versions in `payload/docs/` or `payload/scripts/`.
    2.  Check if `payload/AGENTS-additions.md` needs to change based on what we learned in the field.
    3.  Verify `scaffold-project.py` still installs everything expected.

## Definition of Done
A feature in this repo is only "Done" when:
1.  The document/script exists.
2.  The `scaffold-project.py` script installs it.
3.  `AGENTS-additions.md` explains how to use it (if applicable).
