# Git Workflow: Buffered Integration

## Branches
- **`stable`**: Production/Demo. Only merges from `main` when manually released.
- **`main`**: Development trunk.
- **`topic/*`**: Agent workspaces.

## Future
### The Feedback Loop 
1. User reports issue in Demo App.
2. App commits `report.yaml` and `trace.json` to `test/support/feedback/` via GitHub API.
3. **Forensic Agent** picks up the file, analyzes the Ash Event trace, and adds a coherent Todo item to `docs/process/TODO.md`.
