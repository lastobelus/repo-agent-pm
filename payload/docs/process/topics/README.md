# Topics (Long-Lived, Iterative Work)

Topics are for work that is **too large or uncertain** for a single “one-shot” TODO implementer run.

- **TODOs** are intended to be completed in **one session**.
- **Topics** are intended to be worked **iteratively**, across multiple clean-context agent runs, on a long-lived branch.

## Directory naming (maps to branch)

Create one directory per topic under `docs/process/topics/`:

```
docs/process/topics/
  001-<slug>/
  002-<slug>/
  ...
```

Rules:

- The topic directory name is `NNN-<slug>`.
- The git branch name is `topic/<slug>`.
- The `<slug>` must appear **verbatim** in the directory name so tools can map between them.

Recommended: keep the numeric prefix **only** in the directory name (not the branch).

## Single-worker assumption (current policy)

For now, assume **only one worker** (human or agent) operates on a given `topic/<slug>` at a time.

Implications:

- Do not treat `origin/topic/<slug>` as a shared integration branch.
- You generally do **not** need to pull from `origin/topic/<slug>`.
- Keep “nice-to-haves” and follow-up ideas as **TODOs** to do after the topic lands.

## Iteration docs

Each topic directory holds one or more iteration documents.

- Iteration docs are just Markdown.
- Use `#status/*` tags to mark state:
  - `#status/draft`
  - `#status/active`
  - `#status/discussing`
  - `#status/finished`

Selection rule (used by `continue-topic`):

- Any `.md` file in the topic directory is eligible **unless** it is `#status/finished`.
- If multiple docs are eligible, `continue-topic` uses `fzf` to pick.
- After a pick, `continue-topic` ensures **exactly one** `#status/active` doc.
- Any file missing a `#status/` tag is normalized to `#status/draft`.

## Workflow

1) Create an initial iteration doc by copying the example:

- Start from `docs/process/topics/000-example/000-initial-iteration.md`.

2) Generate a clean-context agent prompt:

```bash
./scripts/start-topic -t docs/process/topics/001-<slug>
```

3) After the first slice lands (still on `topic/<slug>`), continue iteratively:

```bash
./scripts/continue-topic -t docs/process/topics/001-<slug>
```

Notes:

- `continue-topic` requires `fzf`.
- These scripts print to stdout so you can pipe the output into your agent runner.
- If you rebase a published topic branch, push with `git push --force-with-lease` (never plain `--force`).
