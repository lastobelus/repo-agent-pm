#!/bin/bash
# Setup a Local Exchange (Shadow Remote) for multi-slot visibility.
# Run this from your project wrapper root (where slot-1, slot-2 live).

SLOT_DIRS="slot-1 slot-2 slot-3"
EXCHANGE_PATH="slots/exchange.git"

# 1. Initialize the bare repo
if [ ! -d "$EXCHANGE_PATH" ]; then
  echo "Initializing local exchange repo..."
  mkdir -p slots
  git init --bare "$EXCHANGE_PATH"
else
  echo "Exchange repo already exists."
fi

# 2. Configure remotes in each slot
for slot in $SLOT_DIRS; do
  if [ -d "$slot" ]; then
    echo "  Configuring $slot..."
    # Add remote if missing
    if ! git -C "$slot" remote | grep -q exchange; then
      git -C "$slot" remote add exchange ../$EXCHANGE_PATH
      echo "    + Added remote 'exchange'"
    else
      echo "    * Remote 'exchange' already exists"
    fi

    # Ensure pruning is on
    git -C "$slot" config remote.exchange.prune true
  fi
done

echo ""
echo "Setup complete!"
echo "Use 'scripts/gitx-wrapper.sh' to view the dashboard."
