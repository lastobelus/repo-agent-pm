# `.rapm/` — Optional Repo-Agent-PM Add-ons

`./.rapm/` contains **optional** process components that are shipped with repo-agent-pm but **not installed into the consumer project by default**.

## Why this exists

Some workflows (like Local Exchange) are:

- operator-specific
- environment-specific (wrapper roots, multiple clones/slots, GUI tooling)
- not required for the core “TODO checkpoint + prompts/playbooks” workflow

Shipping them under `.rapm/` lets the main install remain minimal and predictable while still keeping advanced tooling available.

## About the name

**repo-agent-pm (rapm)** is a lightweight, in-repo coordination kit for **one human running multiple concurrent agents**. It is a *terrible* substitute for multi-human project management tooling, but it provides just enough back-pressure to keep a solo operator and several agents aligned.

## Local Exchange

- Source: `.rapm/local-exchange/`
- Installer: `scripts/install-local-exchange`

The Local Exchange install copies docs/scripts into their standard locations (`docs/process/` and `scripts/`) without overwriting existing files.
