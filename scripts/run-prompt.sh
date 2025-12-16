#!/bin/bash
# Usage: ./scripts/run-prompt.sh <task_name>
# Example: ./scripts/run-prompt.sh implement

TASK=$1
CONFIG="scripts/context.config.json"

if [ -z "$TASK" ]; then
  echo "Usage: $0 <task_name>"
  exit 1
fi

# Extract files list using python (standard on macos) to parse json
FILES=$(python3 -c "import sys, json; print(' '.join(json.load(open('$CONFIG'))['$TASK']))" 2>/dev/null)

if [ -z "$FILES" ]; then
  echo "Error: Task '$TASK' not found in $CONFIG"
  exit 1
fi

echo ""
echo ""

for file in $FILES; do
  if [ -d "$file" ]; then
    # If it's a directory, concat all markdown files inside
    for f in "$file"/*.md; do
      echo "---"
      echo "File: $f"
      echo "---"
      cat "$f"
      echo ""
    done
  elif [ -f "$file" ]; then
    echo "---"
    echo "File: $file"
    echo "---"
    cat "$file"
    echo ""
  else
    echo "Warning: $file not found." >&2
  fi
done
