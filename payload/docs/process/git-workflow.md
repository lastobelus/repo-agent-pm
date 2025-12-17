# Git Workflow: Buffered Integration

## Branches
- **`stable`**: Production/Demo. Only merges from `main` when manually released.
- **`main`**: Development trunk.
- **`topic/*`**: Agent workspaces.

## Operating Notes

- Prefer small, fast-forwardable slices into `main`.
- Reserve `stable` updates for intentional releases.
- Keep TODO edits line-oriented, and preserve tags like `#<shortsha>`, `#base/<shortsha>`, and `#done/<shortsha>`.
