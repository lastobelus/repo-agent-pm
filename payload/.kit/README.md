# `.kit/` — Optional Kit Add-ons

`./.kit/` contains **optional** process components that are shipped with the kit but **not installed into the consumer project by default**.

## Why this exists

Some workflows (like Local Exchange) are:

- operator-specific
- environment-specific (wrapper roots, multiple clones/slots, GUI tooling)
- not required for the core “TODO checkpoint + prompts/playbooks” workflow

Shipping them under `.kit/` lets the main install remain minimal and predictable while still keeping advanced tooling available.

## Local Exchange

- Source: `.kit/local-exchange/`
- Installer: `scripts/install-local-exchange.sh`

The Local Exchange install copies docs/scripts into their standard locations (`docs/process/` and `scripts/`) without overwriting existing files.

