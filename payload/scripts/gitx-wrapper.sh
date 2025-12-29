#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

WRAPPER_ROOT="${1:-$(cd "$REPO_ROOT/.." && pwd)}"
EXCHANGE_DIR="${EXCHANGE_DIR:-$WRAPPER_ROOT/exchange.git}"

if [ ! -d "$EXCHANGE_DIR" ]; then
  echo "Exchange repo not found: $EXCHANGE_DIR" >&2
  echo "Run ./scripts/setup-exchange.sh first." >&2
  exit 1
fi

if command -v gitx >/dev/null 2>&1; then
  gitx "$EXCHANGE_DIR"
  exit 0
fi

if command -v open >/dev/null 2>&1; then
  open -a GitX "$EXCHANGE_DIR" >/dev/null 2>&1 || open "$EXCHANGE_DIR" >/dev/null 2>&1 || true
  echo "Opened exchange repo (if GitX is installed): $EXCHANGE_DIR"
  exit 0
fi

echo "Open this repo in your git GUI: $EXCHANGE_DIR"
