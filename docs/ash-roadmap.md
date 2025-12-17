# Ash Events Roadmap

Note: third-party feedback ingestion from a deployed demo app is not part of the next iteration of this kit, but remains a planned future capability.

## The Feedback Loop (Future)

1. A user reports an issue in the demo app.
2. The app captures an event trace.
3. The trace is committed into the repo under `test/support/feedback/`.
4. A “forensic” workflow turns the report into a coherent todo item (and later a regression test).

## Phase 1: The Black Box (Current)
- **Goal:** Ingest user reports as files in the repo.
- **Action:**
    - Use Ash Events in `audit` mode.
    - Serialize trace to JSON.
    - Commit to `test/support/feedback/<id>/trace.json`.

## Phase 2: The Replay (Next)
- **Goal:** Turn reports into regression tests.
- **Action:**
    - Create a "Replay Test" helper in Elixir.
    - Agent reads `trace.json` and generates a `test/bugs/issue_<id>_test.exs` file that replays the events.

## Phase 3: The Flight Recorder (Future)
- **Goal:** Full visual replay.
- **Action:** Rehydrate the state from events to show the developer exactly what the user saw.
