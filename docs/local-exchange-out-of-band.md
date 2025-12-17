# Local Exchange: Out-of-Band Options

This document is for **kit maintainers / operators**.

Goal: keep the Local Exchange “dashboard” working while requiring **zero explicit knowledge** of it from coding agents.

## What “Out-of-Band” Really Means

There are two levels:

1. **Agents don’t have to mention `exchange`** (ideal).
2. **Agents never have to run `git push` at all** (hard; requires a daemon/watcher).

This kit targets (1) as the practical default.

## Practical Default: Make `git push` Go to Exchange

If agents run normal `git push` but never specify a remote, you can route those pushes to `exchange` via Git configuration.

Recommended operator setup (per repo clone/slot):

- Ensure `exchange` remote exists.
- Set push default:

```bash
git config remote.pushDefault exchange
```

- When creating a topic branch, set its upstream to `exchange` (tooling should do this):

```bash
git push -u exchange HEAD
```

After that, the agent’s normal `git push` updates Exchange, not GitHub.

## Guardrail: Block Accidental Pushes to `origin`

Add a `pre-push` hook (operator-managed) that rejects pushes to `origin` for ephemeral branches (e.g. `topic/*`).

This keeps agent defaults safe even if they try `git push origin`.

## True Out-of-Band (No Agent Pushes)

If you want zero pushes from agents, you need something watching the repo state and pushing to Exchange periodically.

Options:

- A cron/launchd job that runs every N seconds/minutes and does a best-effort sync of refs.
- A long-running watcher script that checks `git for-each-ref` output for changes.

Tradeoffs:

- more moving parts
- harder to prune deleted branches cleanly
- risk of pushing partially rebased states if the watcher syncs at the wrong moment

Recommendation: start with the push-default approach; upgrade to a watcher only if you truly need it.

