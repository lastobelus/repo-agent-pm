**FUTURE PLAN. Do not implement yet**

## Raw notes

I'm going to add a wrinkle. The app will be a phoenix/elixir app using [Ash Framework](https://github.com/ash-project). We will use the [Ash Events plugin](https://github.com/ash-project/ash_events). To minimize initial learning curve, we will first use Ash Events in auditing mode, and refactor to replayable events when ready. In the first case, user reports can include a complete audit trail of what the user was doing when they reported the issue. In the second case, we will be able to replay their actions in-app for testing debugging.

### Gemini thoughts
Here is how to adapt the **Buffered Integration** strategy to leverage this "Flight Recorder" capability.

### 1. The "Black Box" Workflow

Since your goal is to have artifacts in the repo, you should treat user reports not just as text, but as **Test Fixtures**.

Instead of a generic `feedback/inbox`, move the ingestion point to your test directory structure. This prepares you for Phase 2 (Replay), where these reports literally become your regression tests.

**Directory Structure:**

```
test/
└── support/
    └── feedback/
        └── 2023-10-27-issue-a1b2/
            ├── report.yaml      # User's written complaint + metadata
            └── trace.json       # The Ash Events dump (Audit or Replay data)
```

**The Flow:**

1. **User Action:** User encounters a bug and submits feedback via the "Report Issue" form.
    
2. **System Action:**
    
    - The app captures the `AshEvents` history for that `actor`.
        
    - The app uses the GitHub API to commit a new folder to `test/support/feedback/` containing the report and the trace.
        
3. **Forensic Agent:** Your "Review Agent" (or a dedicated "Forensic Agent") detects the new file. It reads `trace.json` to understand _exactly_ what happened, rather than relying on the user's possibly vague description.
    

### 2. Implementation: The Forensic Agent

You will need to update your agent's system prompt to handle this new data source.

**Role:** `forensic_analyst` **Trigger:** New folder in `test/support/feedback/`

**Phase 1 (Audit Mode) Workflow:** When the agent picks up a ticket, it performs a "Reality Check":

1. **Read:** `report.yaml` (What the user _said_ happened).
    
2. **Read:** `trace.json` (What _actually_ happened).
    
3. **Analyze:** The agent compares the two.
    
    - _Example:_ User says "Login failed," but Trace shows "ResourceNotFound: Tenant ID missing."
        
4. **Output:** The agent writes a simplified summary into `TODO.md` and links the specific line in the code likely responsible (Ash resources make this easy because the trace points to specific Actions).
    

**Phase 2 (Replay Mode) Workflow:** This is where the ROI explodes.

1. The agent takes `trace.json`.
    
2. The agent generates a **new ExUnit test file** (`test/bugs/issue_a1b2_test.exs`).
    
3. The test file is bootstrapped to load the events from `trace.json` and replay them against the `Ash` resources.
    
4. Now you have a failing test case. The coding agent can now iterate on the code until this specific test passes.
    

### 3. Pros & Cons of the "Ash Wrinkle"

|**Feature**|**Pros**|**Cons**|
|---|---|---|
|**Repo-as-Database**|Your test suite grows automatically with real-world user paths. You build a massive regression suite for free.|**Repo Bloat:** `trace.json` files can get large. You may need to prune old ones or use a separate "feedback-data" branch (orphan branch) to avoid cloning history forever.|
|**Ash Introspection**|Ash resources/actions are declarative. AI Agents understand them much better than imperative controller code. The agent can map a trace error to the exact Resource definition file easily.|**Privacy Risk:** `AshEvents` might capture PII. You need to configure a scrubber (Ash has capabilities for this) before the JSON leaves the app.|
|**Replayability**|Removes "Works on my machine" entirely.|**Complexity:** Setting up the "Replay" harness in `test_helper.exs` is non-trivial initially.|

### 4. Updated Git Setup for Data Hygiene

To prevent your `main` branch from becoming 5GB of JSON files, I recommend a **Hybrid Branch Strategy** for the data.

**The "Orphan Feedback" Branch:** Configure your Committer Bot (the API call in your app) to commit the `trace.json` files to a branch named `feedback-data`, _not_ `main`.

- **`main`**: Contains the code and the `report.yaml` (lightweight).
    
- **`feedback-data`**: Contains the heavy `trace.json` files.
    

**Agent Workflow Adjustment:** When the Forensic Agent runs:

1. It checks `main` for new `report.yaml` files.
    
2. It does a `git checkout feedback-data -- path/to/trace.json` to temporarily pull the heavy data for analysis.
    
3. It deletes the JSON file after analysis/test-generation is done, keeping your local dev environment clean.