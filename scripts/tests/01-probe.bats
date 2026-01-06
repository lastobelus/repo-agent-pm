#!/usr/bin/env bats

load "helpers.bash"

@test "validate-cli-wrappers probe mode succeeds" {
  root_dir="$(cd "$(dirname "${BATS_TEST_FILENAME}")/../.." && pwd)"
  tmpdir="$(make_tmp_project "$root_dir")"

  run "$tmpdir/scripts/validate-cli-wrappers" --probe implement-one-todo
  [ "$status" -eq 0 ]
}
