# Bats Tests

Run from repo root:

```bash
bats scripts/tests
```

The real echo test uses sane defaults, but you can override per-CLI args, e.g.:

```bash
CODER_ARGS="exec - --skip-git-repo-check" \
OPENCODE_ARGS="--model zai-coding-plan/glm-4.7" \
bats scripts/tests
```

To verify the coder fork works with codex-style args, set `CODER_FORK_BIN` (the
real echo test covers this when `CODER_ARGS` is set too):

```bash
CODER_ARGS="exec -" \
CODER_FORK_BIN="/path/to/coder" \
bats scripts/tests/02-real-echo.bats
```

Note: the Claude wrapper always injects `-p <prompt>` internally, so avoid
passing `-p`/`--print`/`--prompt` yourself; use flags like `--output-format` instead.

The real echo test skips CLIs that are installed but not yet authenticated.

Claude is skipped by default; set `RUN_CLAUDE=1` to include it in the real echo test.
