#!/bin/bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./scripts/setup-exchange.sh [--wrapper-root <path>] [--exchange-path <path>] [--set-push-default] [--add-slots <n>] [--slot-prefix <name>] [--repo-url <url>]

Creates a local Exchange bare repo and wires it as a remote in each slot repo.
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

WRAPPER_ROOT=""
EXCHANGE_DIR=""
SET_PUSH_DEFAULT=0
WRAPPER_ROOT_PROVIDED=0
ADD_SLOTS=0
SLOT_PREFIX=""
REPO_URL=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wrapper-root)
      WRAPPER_ROOT="$2"
      WRAPPER_ROOT_PROVIDED=1
      shift 2
      ;;
    --exchange-path)
      EXCHANGE_DIR="$2"
      shift 2
      ;;
    --set-push-default)
      SET_PUSH_DEFAULT=1
      shift 1
      ;;
    --add-slots)
      ADD_SLOTS="$2"
      shift 2
      ;;
    --slot-prefix)
      SLOT_PREFIX="$2"
      shift 2
      ;;
    --repo-url)
      REPO_URL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [ -z "$WRAPPER_ROOT" ]; then
  WRAPPER_ROOT="$(cd "$REPO_ROOT/.." && pwd)"
fi

if [ -z "$EXCHANGE_DIR" ]; then
  EXCHANGE_DIR="$WRAPPER_ROOT/exchange.git"
fi

if ! [[ "$ADD_SLOTS" =~ ^[0-9]+$ ]]; then
  echo "Invalid --add-slots value: $ADD_SLOTS" >&2
  exit 1
fi

if [ "$ADD_SLOTS" -gt 0 ]; then
  if [ -z "$REPO_URL" ]; then
    if git -C "$REPO_ROOT" remote | grep -q '^origin$'; then
      REPO_URL="$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)"
    fi
  fi

  if [ -z "$REPO_URL" ]; then
    echo "No repo URL available. Pass --repo-url <url> or ensure 'origin' exists in the current repo." >&2
    exit 1
  fi

  if [ -z "$SLOT_PREFIX" ]; then
    SLOT_PREFIX="$(basename "$REPO_ROOT")"
  fi

  idx=1
  while [ "$idx" -le "$ADD_SLOTS" ]; do
    target="$WRAPPER_ROOT/$SLOT_PREFIX-$idx"
    if [ -e "$target" ]; then
      echo "Skip (exists): $target"
    else
      echo "Cloning slot: $target"
      git clone "$REPO_URL" "$target"
    fi
    idx=$((idx + 1))
  done
fi

if [ ! -d "$WRAPPER_ROOT" ]; then
  echo "Wrapper root not found: $WRAPPER_ROOT" >&2
  exit 1
fi

if [ ! -d "$EXCHANGE_DIR" ]; then
  git init --bare "$EXCHANGE_DIR"
  echo "Created exchange repo: $EXCHANGE_DIR"
else
  echo "Exchange repo already exists: $EXCHANGE_DIR"
fi

repos=()

for child in "$WRAPPER_ROOT"/*; do
  if [ -d "$child/.git" ]; then
    repos+=("$child")
  fi
done

if [ ${#repos[@]} -eq 0 ]; then
  echo "No git repos found under: $WRAPPER_ROOT" >&2
  if [ "$WRAPPER_ROOT_PROVIDED" -eq 0 ]; then
    echo "Pass --wrapper-root to the directory that contains your slot clones (e.g., slot-1, slot-2)." >&2
  fi
  exit 1
fi

selected=()

if [ ${#repos[@]} -eq 1 ]; then
  selected+=("${repos[0]}")
else
  echo "Found multiple git repos under $WRAPPER_ROOT."
  echo "Select which ones are slots to wire into Exchange:"

  idx=1
  for repo in "${repos[@]}"; do
    remote_name=""
    remote_url=""
    if git -C "$repo" remote | grep -q '^origin$'; then
      remote_name="origin"
      remote_url="$(git -C "$repo" remote get-url origin 2>/dev/null || true)"
    else
      first_remote="$(git -C "$repo" remote | head -n 1)"
      if [ -n "$first_remote" ]; then
        remote_name="$first_remote"
        remote_url="$(git -C "$repo" remote get-url "$first_remote" 2>/dev/null || true)"
      fi
    fi

    if [ -n "$remote_name" ]; then
      echo "$idx) $repo ($remote_name: $remote_url)"
    else
      echo "$idx) $repo (no remotes)"
    fi
    idx=$((idx + 1))
  done

  if [ ! -t 0 ]; then
    echo "Non-interactive shell detected. Re-run with a TTY to choose repos." >&2
    exit 1
  fi

  read -r -p "Enter repo numbers (e.g. 1 3) or 'all': " selection
  if [ -z "$selection" ]; then
    echo "No selection provided. Aborting." >&2
    exit 1
  fi

  if [ "$selection" = "all" ]; then
    selected=("${repos[@]}")
  else
    for token in $selection; do
      if ! [[ "$token" =~ ^[0-9]+$ ]]; then
        echo "Invalid selection: $token" >&2
        exit 1
      fi
      if [ "$token" -lt 1 ] || [ "$token" -gt ${#repos[@]} ]; then
        echo "Selection out of range: $token" >&2
        exit 1
      fi
      selected+=("${repos[$((token - 1))]}")
    done
  fi
fi

for slot in "${selected[@]}"; do
  if git -C "$slot" remote | grep -q '^exchange$'; then
    git -C "$slot" remote set-url exchange "$EXCHANGE_DIR"
    echo "Updated exchange remote in: $slot"
  else
    git -C "$slot" remote add exchange "$EXCHANGE_DIR"
    echo "Added exchange remote to: $slot"
  fi

  if [ "$SET_PUSH_DEFAULT" -eq 1 ]; then
    git -C "$slot" config remote.pushDefault exchange
    echo "Set pushDefault=exchange in: $slot"
  fi
done

echo ""
echo "Next steps:"
echo "- For each active branch, set upstream once: git push -u exchange HEAD"
if [ "$SET_PUSH_DEFAULT" -eq 0 ]; then
  echo "- If you want out-of-band pushes, re-run with --set-push-default"
fi
