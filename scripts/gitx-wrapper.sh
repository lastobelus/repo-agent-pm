#!/bin/bash
# gitx-wrapper.sh
# Fetches the Local Exchange then opens GitX with --all

echo "Fetching from local exchange..."
git fetch exchange >/dev/null 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "Opening GitX..."
  gitx --all "$@"
else
  echo "Warning: Failed to fetch from exchange. Does the remote exist?"
  gitx "$@"
fi
