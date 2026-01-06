#!/bin/bash

set -euo pipefail

make_tmp_project() {
  local root_dir
  root_dir="$1"
  local tmpdir
  tmpdir="$(mktemp -d)"

  python3 "$root_dir/scaffold-project.py" --overwrite "$tmpdir" >/dev/null
  printf "%s" "$tmpdir"
}

write_echo_prompt() {
  local tmpdir
  tmpdir="$1"
  local token
  token="$2"

  local context_path
  local prompt_path
  context_path="$tmpdir/docs/process/sample-context.txt"
  prompt_path="$tmpdir/docs/ai/prompts/echo-context.md"

  mkdir -p "$(dirname "$context_path")" "$(dirname "$prompt_path")"
  printf 'Echo token: %s\n' "$token" > "$context_path"

  cat > "$prompt_path" <<EOF
---
kind: prompt
mode: clean-context
name: echo-context
inputs:
  - docs/process/sample-context.txt
outputs:
  - token echoed exactly
stop_conditions:
  - file missing
---

Read the file at \`docs/process/sample-context.txt\`. It contains a line with a token.

Output the token **exactly**, on a single line, with no other text.
EOF
}

default_cli_args() {
  case "$1" in
    coder)
      printf "%s" "${CODER_ARGS:-exec - --skip-git-repo-check}"
      ;;
    qwen)
      printf "%s" "${QWEN_ARGS:-}"
      ;;
    gemini)
      printf "%s" "${GEMINI_ARGS:-}"
      ;;
    opencode)
      printf "%s" "${OPENCODE_ARGS:---model zai-coding-plan/glm-4.7}"
      ;;
    claude)
      printf "%s" "${CLAUDE_ARGS:---output-format text}"
      ;;
    *)
      printf "%s" ""
      ;;
  esac
}

default_cli_bin() {
  case "$1" in
    coder)
      if [ -n "${CODER_FORK_BIN:-}" ]; then
        printf "%s" "$CODER_FORK_BIN"
      else
        printf "%s" "${CODER_BIN:-coder}"
      fi
      ;;
    qwen)
      printf "%s" "${QWEN_BIN:-qwen}"
      ;;
    gemini)
      printf "%s" "${GEMINI_BIN:-gemini}"
      ;;
    opencode)
      printf "%s" "${OPENCODE_BIN:-opencode}"
      ;;
    claude)
      printf "%s" "${CLAUDE_BIN:-claude}"
      ;;
    *)
      printf "%s" ""
      ;;
  esac
}

cli_available() {
  local bin
  bin="$1"
  if [ -z "$bin" ]; then
    return 1
  fi
  command -v "$bin" >/dev/null 2>&1
}
