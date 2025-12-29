# Local Exchange (Optional)

Local Exchange is an operator workflow for “branches as labels” visibility without pushing ephemeral branches to GitHub.

It creates a **local-only remote** (named `exchange`) that every slot/repo can push to. You can then open the bare repo in a git GUI to see all in-flight work in one place.

## When To Use It

- You run multiple local clones (“slots”) and want a single dashboard.
- You want agents to push without publishing to GitHub.
- You prefer a clean, linear view of branch labels over the full GitHub history.

## Quick Setup

1. Pick a **wrapper root**: the directory that contains your slot folders (e.g., `slot-1`, `slot-2`, ...).
2. From any slot repo, run:

```bash
./scripts/setup-exchange.sh
```

This will:

- create a bare repo at `<wrapper-root>/exchange.git`
- prompt you to choose which sibling repos are “slots”
- add a remote named `exchange` to the selected repos only

If your layout is unusual, pass the wrapper root explicitly:

```bash
./scripts/setup-exchange.sh --wrapper-root /path/to/wrapper
```

## Adding Slots (Optional)

If you want the script to create new slot clones for you:

```bash
./scripts/setup-exchange.sh --add-slots 3
```

Defaults:

- Uses the current repo's `origin` URL as the clone source.
- Names slots as `<repo-name>-1`, `<repo-name>-2`, etc.

Overrides:

```bash
./scripts/setup-exchange.sh --add-slots 3 --slot-prefix project --repo-url git:some/repo
```

Note: `--add-slots` clones repos; it does not validate credentials or network access. If cloning fails, re-run with a reachable URL.

## Out-Of-Band Option (Agents Stay Unaware)

If you want normal `git push` to go to Exchange by default, set:

```bash
./scripts/setup-exchange.sh --set-push-default
```

That sets `remote.pushDefault=exchange` in each slot repo so agents can keep using plain `git push`.

For new branches, the first push should establish the upstream:

```bash
git push -u exchange HEAD
```

## Dashboard View (Git GUI)

You can open the Exchange repo in your preferred git GUI to view all branch labels in a single timeline.

If you use GitX and want a helper:

```bash
./scripts/gitx-wrapper.sh
```

## Troubleshooting

- **No repos found:** ensure your slot directories are direct children of the wrapper root.
- **Nothing wired but git repos exist:** the script requires you to select which repos are slots. Re-run and pick the correct entries.
- **Remote exists but wrong path:** re-run setup; it will update the `exchange` URL.
- **Agents should not push to GitHub:** set `remote.pushDefault=exchange` (see above).
