# Shared File Collisions (Design Note)

This document explains why `docs/process/TODO.md` is both powerful and a merge-conflict hotspot, and suggests mitigation patterns.

## Why it happens

When you run multiple agents concurrently, they naturally want to:

- claim items
- add follow-up items
- mark items done

If all of that happens in one file, you get more merges in the same region.

## The sharding idea

The goal is not to replace the TODO checkpoint. It’s to reduce write pressure on it.

Practical patterns:

1. **Queue + per-task notes**
   - TODO.md stays small.
   - Each task gets a notes file under `docs/process/tasks/`.

2. **Spec-local checklists for long-lived branches**
   - Large features often have a checklist embedded in the spec.
   - Only promote items to the main TODO when they become independent slices.

## Tradeoffs

- Pros: fewer TODO conflicts, richer per-task context, easier reviews.
- Cons: more files, slightly more “where is the detail?” overhead.

## What the kit installs

Consumer projects get a short version of this guidance in `payload/docs/process/shared-file-collisions.md`.

