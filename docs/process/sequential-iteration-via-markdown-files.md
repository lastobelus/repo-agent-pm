# Sequential Iteration via Markdown Files (Spec / Manual)

#status/draft

This is a lightweight workflow for iterating with an AI assistant by maintaining a *sequence* of Markdown files.

This document is a *field guide*, not a contract:

- Keep it lightweight; use what helps and ignore the rest.
- The “rules” are descriptive (what worked), not prescriptive (what must be).
- If formalization starts to reduce usage, delete sections until it feels effortless again.

It is designed to be:

- **ad hoc and flexible** (no hard-coded rules)
- **ordered-as-needed** (you can renumber freely)
- **resilient to context loss** (a clean-context agent can pick up later)

This doc is orthogonal to the “kit” itself, but it has proven useful enough in this repo that we keep it here (instead of spinning up a separate project).

Iteration log for developing this spec:

- `docs/iterations/020-interactive-iteration-via-sequential-markdown-files.md`

## What This Is For

Use this when you want to:

- work in small chunks with clear boundaries
- preserve rationale and decisions alongside the work
- reduce “round trips” caused by losing or re-deriving context
- park out-of-scope items without losing them

This is especially useful for topics/features that span multiple sessions. For truly atomic tasks (single-pass changes), a TODO list or a single **Agent Action** block is often enough.

## The Core Workflow

1. Humans create a new numbered iteration doc under `docs/iterations/`.
2. The doc accumulates:
   - discussion (`#discuss`, `#question`)
   - recommendations (`#recommendation`)
   - decisions (`#decide`)
   - clarifications requested (`#clarify/*`)
   - executable work items (**Agent Action** blocks)
3. The agent responds in chat *and* summarizes the important bits back into the iteration doc.
4. When the round is complete, the current doc is marked `#status/finished`, and the next round starts in a new file that captures the “current truth.”

## Why Markdown Files Beat Chat Scrollback (Human Ergonomics)

This approach works well for humans because:

- Adding commentary in a Markdown editor is far more fluid than bouncing between a TUI chat buffer and an input box.
- Tags, headings, quotes, and action blocks are visually distinct in a proper editor.
- Important pieces of the interactive conversation can be preserved *in the same artifact* as the work, instead of relying on copy/paste or memory.

## Status Markers

Put a simple, machine-searchable status marker near the top:

- `#status/draft`
- `#status/active`
- `#status/finished`

Conventions:

- Treat the newest `#status/active` file as the current source of truth.
- Finished files should not receive new decisions or new actions (except minor corrections).

## Numbering: Big Layers, Small Granularity, and Renumbering

The numbering is intentionally informal.

### Layered numbering (a useful mental model)

- Use **`1xx`, `2xx`, ...** to represent “big layers” or major workstreams.
- Use **`x1x`, `x2x`, ...** to insert smaller-granularity work within a layer.
- Fill in with smaller steps as needed.

This helps you:

- capture out-of-scope items now without derailing the current work
- come back later and expand them into smaller iterations

### Renumbering rule of thumb

You can renumber freely as you learn more.

The only invariant that matters:

> Numbers for “work to be done” should remain **higher** than numbers for “work that is done.”

That keeps the sequence intuitive even if it is ad hoc.

## Tags: How Humans Request and Agents Respond

Humans use tags to express intent:

- `#question` ask for an answer
- `#discuss` explore tradeoffs or uncertainty
- `#advise` ask for judgment / warnings
- `#recommend` ask for a recommended course of action

### Agent-emitted tags

To make scanning reliable, all agent-emitted tags should start with `#agent-`.

Examples:

- `#agent-answer`
- `#agent-recommendation`
- `#agent-considerations`
- `#agent-decide`
- `#agent-question`
- `#agent-clarification/intent`, `#agent-clarification/platform`, `#agent-clarification/target`

Keep the tag set small and consistent. Too many tags reduces scanability.

### Suggested tag pairs (request → response)

- `#question` → `#agent-answer`
- `#recommend` → `#agent-recommendation`
- `#discuss` → `#agent-considerations` (and optionally `#agent-recommendation`)
- `#agent-question` → human `#answer`
- `#clarify/<x>` → `#agent-clarification/<x>`

Notes:

- The exact vocabulary is less important than “agent output is visually distinct.”
- If you change the tags later, update the spec once and continue.

## Mode Markers (Optional)

If you find yourself forgetting and accidentally triggering work, add a mode marker near the top:

- `#mode/discuss` (questions and feedback only)
- `#mode/execute` (approved actions allowed)

If you don’t want a persistent mode marker, a one-off prefix works too:

- `#noactions` or “Discussion only — no Agent Actions yet.”

## “Agent Action” Blocks (Executable Work)

**Agent Action** blocks are where work becomes executable.

Minimal checklist:

- Goal
- Files to touch
- Definition of done (including validation)
- Non-goals / scope boundaries

If you include one line that always appears on refactors, make it:

- “Update references + validate install”

### Proposed vs approved vs done

To keep a single file readable, keep action blocks in one of these states:

- `**Agent Action (proposed)**` (discussion is ongoing; not approved)
- `**Agent Action**` (approved; safe to execute)
- `**Agent Action (done)**` (completed; outcomes summarized)

## Agent Responsibilities (Important)

Agents should:

- Summarize key outcomes back into the iteration doc (not only to screen).
- Capture any chat-only interaction worth remembering (decisions, caveats, rationale) into the iteration doc.
- When starting a new iteration doc, carry forward:
  - the “current truth”
  - unresolved `#decide` items
  - the next **Agent Action** blocks

## Quote Blocks

Quote blocks have two common uses:

1. **Quoted reference + response** (classic review mode)
   - Quote the specific line being answered, then respond underneath.
2. **Inline rejoinders inside existing content** (annotation mode)
   - Use quotes to insert short parenthetical comments/requests inside a section.

If you need to quote nested replies, use a double quote marker:

```md
> original thing said
rejoinder
>> rejoinder to the rejoinder
```

It should usually be obvious which quoting mode is happening; when it isn’t, prefer rewriting the section rather than piling on more quotes.

## AGENTS Snippet (Minimal)

This is the smallest set of instructions to add to an `AGENTS.md` to make this flow work.

```md
## Iteration Docs (Optional)

When iterating with an AI assistant, prefer sequential Markdown files under `docs/iterations/`.

- Add a status marker near the top: `#status/draft`, `#status/active`, `#status/finished`.
- Treat the newest `#status/active` file as the current source of truth.
- Put executable work in **Agent Action** blocks with: goal, files to touch, definition of done, non-goals.
- Agent-emitted tags should start with `#agent-` to keep scanning reliable.
- The agent summarizes outcomes into the iteration doc (not only to screen) and captures chat-only decisions/rationale.
```

## Worked Example (Tiny)

> #question Should this process be maintainer-only, or installed into consumer projects?

Agent response:

- #recommendation Keep the detailed process in maintainer docs (`docs/iterations/`). If teaching consumers, publish a simplified version under `payload/docs/process/`.

Example “Agent Action” block (kept in a code fence so it won’t be mistaken for executable work):

```md
**Agent Action (Example Only — do not execute)**

- Goal: Draft consumer-safe version of this process.
- Files to touch: `payload/docs/process/iteration-docs.md`, `payload/docs/process/README.md`.
- Definition of done: Consumer doc exists, is linked from navigation, and does not reference maintainer internals.
- Non-goals: Changing existing scripts.
```

## Scope Placement (Where This Belongs)

This workflow is useful beyond this kit repo.

Keeping it here is reasonable if:

- you intend to use it regularly
- you want it versioned and close to the work it supports

If/when it becomes a consumer-facing process (installed into other repos), extract a simplified version into `payload/docs/process/` and reference it from consumer navigation.
