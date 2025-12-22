# Git Workflow: Buffered Integration

## Branches
- **`stable`**: Production/Demo. Only merges from `main` when manually released.
- **`main`**: Development trunk.
- **`topic/*`**: Agent workspaces.

## Operating Notes

- Prefer small, fast-forwardable slices into `main`.
- Reserve `stable` updates for intentional releases.
- Keep TODO edits line-oriented, and preserve tags like `#<shortsha>`, `#base/<shortsha>`, and `#done/<shortsha>`.

## Topic branch policy (long-lived work)

- Topic branches are `topic/<slug>`.
- Keep topics **iterative**: each session lands one meaningful commit.
- Prefer rebasing topic branches onto `origin/main` to stay close to trunk.
  - If you rebase a published topic branch, push with `git push --force-with-lease`.
