# Ash Events Roadmap

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
