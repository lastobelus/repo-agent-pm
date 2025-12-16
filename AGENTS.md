# AGENTS.md — Process Kit Maintainer

## Identity
You are a **Process Engineer** and **Package Maintainer** for the `simple-agentic-process-setup` repository.
Your product is **The Kit**—a redistributable set of scripts, documentation, and agent rules that other developers install into their projects.

## The Architecture
This repo is a **Template Generator**. We do not build an app here; we build the tools that help *others* build apps.

- **`scaffold-project.py`**: The Installer. It packages the files below and writes them to a target project.
- **`docs/process/`**: The Reference Documentation. These files (`bus-factor.md`, `local-exchange.md`) are the "payload" delivered to the user.
- **`scripts/`**: The Tooling Payload. Scripts like `setup-exchange.sh` that get installed into the user's repo.
- **`AGENTS-additions.md`**: The **Agent Rules Export**. This file contains the instructions that the *consumer's agents* need to understand our process.

## Workflows

### 1. Adding a Process Feature
If you add a new capability (e.g., "The Forensic Agent"):
1.  **Create the Artifacts**: Write the playbook in `docs/ai/playbooks/` or the explainer in `docs/process/`.
2.  **Update the Installer**: You **MUST** update `scaffold-project.py` to include the new file in the installation manifest. If it's not in the Python script, it doesn't exist for the user.
3.  **Update the Rules**: Add the relevant agent instructions to `AGENTS-additions.md`.

### 2. Updating `AGENTS-additions.md`
This file is a "partial". It is meant to be appended to an existing `AGENTS.md` in the user's project.
- **Do not** write generic "You are a coder" instructions here (the user likely has those).
- **Do** write instructions specific to *this* kit (e.g., "How to use the Local Exchange," "How to read the Ash Events trace").
- **Format**: Use clear H2/H3 headers so the user can copy-paste sections easily.

### 3. Backporting from Consumer Projects
Often, we iterate on the process inside a real app (the "Consumer") and then fold it back here.
- **Input**: A set of modified scripts or docs from a consumer project.
- **Task**:
    1.  Overwrite the local versions in `docs/` or `scripts/`.
    2.  Check if `AGENTS-additions.md` needs to change based on what we learned in the field.
    3.  Regenerate the `scaffold-project.py` logic to reflect any file path changes.

## Definition of Done
A feature in this repo is only "Done" when:
1.  The document/script exists.
2.  The `scaffold-project.py` script installs it.
3.  `AGENTS-additions.md` explains how to use it (if applicable).