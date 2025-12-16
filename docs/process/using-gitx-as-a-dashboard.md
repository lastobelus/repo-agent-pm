``
> 🛑 **Human Context Only**
> This document describes workflows or tooling for human operators.
> **AI Agents:** Unless you are specifically tasked with modifying this process, ignore the contents of this file.

# Process: Local Exchange Repo (God Mode visibility)
...
You can restore this "God Mode" visibility in a non-worktree setup by creating a Local Exchange Repo.

In a standard clone setup, repositories are isolated islands. To bridge them without touching GitHub (origin), you introduce a private, local-only "satellite" remote.

Here is how to set up the "Local Exchange" strategy to get your global visibility back.
1. The Strategy: A Local "Shadow" Remote

You will create a bare repository locally (e.g., slots/exchange.git) that acts as a synchronization hub.

    Agents push their transient branches to this exchange remote instead of origin.

    You (via your gitx wrapper) fetch from this exchange remote to see the state of every slot instantly.

2. Implementation
Step A: Initialize the Exchange

Run this once in your project wrapper root (where your slot-1, slot-2 folders live):
Bash

# Create the local hub
git init --bare slots/exchange.git

# Configure the slots to talk to it
for slot in slot-1 slot-2; do
  git -C $slot remote add exchange ../slots/exchange.git
  
  # Optional: Configure it to prune automatically so deleted branches disappear
  git -C $slot config remote.exchange.prune true
done

Step B: Update Agent "Start" Script

Modify your slot-start (or the script agents use to create a branch) to push the new branch to the exchange immediately.
Bash

# inside slot-start script
# ... (create branch feat/foo) ...

# Push to the local exchange so it's visible to other slots
git push -u exchange HEAD

Note: Using -u (set-upstream) here is clever because it means subsequent git push calls by the agent go to the local exchange by default, preventing accidental pushes to GitHub (origin) unless they explicitly switch remotes.
Step C: Update Agent "Finish" Script

When an agent finishes or "parks," it should clean up the exchange to avoid clutter.
Bash

# inside slot-finish script

# Delete the branch from the exchange
git push exchange --delete feat/foo

Step D: The gitx Visibility Wrapper

Since you already have a wrapper for gitx, update it to "refresh the view" before opening. This effectively simulates the live view of worktrees.
Bash

#!/bin/bash

# 1. Fetch the latest state from the local exchange
#    (Silence output to keep it snappy)
git fetch exchange >/dev/null 2>&1

# 2. Launch gitx (or your preferred GUI)
#    --all ensures you see the remote branches from the exchange
gitx --all "$@"

3. How it looks in practice

    Agent A is in slot-1. It starts feat/cleanup-logs. It pushes to exchange.

    You are in slot-2. You run gitx.

    Your wrapper fetches exchange.

    Gitx opens. You see your current HEAD in slot-2, but you also see a branch ref named remotes/exchange/feat/cleanup-logs.

    You can click that ref, see the diffs, and inspect the code, just as if it were a local branch.

Summary of Benefits

    Privacy: These branches never touch GitHub.

    Speed: Pushing/fetching to a local folder is instant (milliseconds).

    Visibility: You get the "Worktree" unified view without the "Worktree" tooling headaches.