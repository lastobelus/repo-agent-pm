#!/usr/bin/env bats

load "helpers.bash"

setup() {
  root_dir="$(cd "$(dirname "${BATS_TEST_FILENAME}")/../.." && pwd)"
  TMPDIR_LOCAL="$(make_tmp_project "$root_dir")"
  TOKEN_LOCAL="TOKEN-$(date +%s)-$RANDOM"
  write_echo_prompt "$TMPDIR_LOCAL" "$TOKEN_LOCAL"
}

run_wrapper() {
  local wrapper="$1"
  local bin
  local args
  bin="$(default_cli_bin "$wrapper")"
  if ! cli_available "$bin"; then
    skip "Missing CLI: $bin"
  fi

  if [ "$wrapper" = "claude" ] && [ "${RUN_CLAUDE:-0}" != "1" ]; then
    skip "claude disabled (set RUN_CLAUDE=1 to enable)"
  fi

  args="$(default_cli_args "$wrapper")"
  IFS=' ' read -r -a cli_args <<< "$args"

  echo "--- $wrapper debug ---" >&2
  echo "bin=$bin" >&2
  echo "args=$args" >&2
  echo "cwd=$TMPDIR_LOCAL" >&2

  if [ "$wrapper" = "coder" ] && [ -n "${CODER_FORK_BIN:-}" ]; then
    run bash -c "cd '$TMPDIR_LOCAL' && CODER_BIN='$CODER_FORK_BIN' ./scripts/coder echo-context ${cli_args[*]}"
  else
    run bash -c "cd '$TMPDIR_LOCAL' && ./scripts/$wrapper echo-context ${cli_args[*]}"
  fi

  if [ "$status" -ne 0 ]; then
    if echo "$output" | grep -Fq "Attempted to create a NULL object"; then
      skip "coder crashed (system configuration); rerun after fixing local install"
    fi
    if echo "$output" | grep -Fq "Please visit the following URL to authorize"; then
      skip "$wrapper needs interactive auth"
    fi
    if echo "$output" | grep -Fq "Authorization code is required"; then
      skip "$wrapper needs interactive auth"
    fi
    if echo "$output" | grep -Fq "Failed to authenticate"; then
      skip "$wrapper needs interactive auth"
    fi
    if echo "$output" | grep -Fq "[API Error: Connection error.]"; then
      skip "$wrapper needs credentials or network access"
    fi
    if echo "$output" | grep -Fq "EPERM: operation not permitted, open ''"; then
      skip "$wrapper needs log dir permissions"
    fi
    if echo "$output" | grep -Fq "EPERM: operation not permitted, open '/Users/"; then
      skip "$wrapper needs config file permissions"
    fi
    echo "--- $wrapper output ---" >&2
    echo "$output" >&2
    return 1
  fi

  if [[ "$output" != *"$TOKEN_LOCAL"* ]]; then
    if echo "$output" | grep -Fq "Please visit the following URL to authorize"; then
      skip "$wrapper needs interactive auth"
    fi
    if echo "$output" | grep -Fq "Authorization code is required"; then
      skip "$wrapper needs interactive auth"
    fi
    if echo "$output" | grep -Fq "Failed to authenticate"; then
      skip "$wrapper needs interactive auth"
    fi
    if echo "$output" | grep -Fq "[API Error: Connection error.]"; then
      skip "$wrapper needs credentials or network access"
    fi

    echo "--- $wrapper output (token missing) ---" >&2
    echo "$output" >&2
    return 1
  fi
}

@test "real echo prompt works with coder" {
  run_wrapper "coder"
}

@test "real echo prompt works with qwen" {
  run_wrapper "qwen"
}

@test "real echo prompt works with gemini" {
  run_wrapper "gemini"
}

@test "real echo prompt works with opencode" {
  run_wrapper "opencode"
}

@test "real echo prompt works with claude" {
  run_wrapper "claude"
}
