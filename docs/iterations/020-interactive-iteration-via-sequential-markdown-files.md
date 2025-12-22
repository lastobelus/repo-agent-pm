# Iteration 020 — Interactive Iteration via Sequential Markdown Files

#status/finished

This is the *iteration log* for developing the spec/manual for “Sequential Iteration via Markdown Files”.

Spec/manual lives here:

- `docs/process/sequential-iteration-via-markdown-files.md`

## Goal

Split the previous “single doc that is both spec and discussion” into:

1. a stable spec/manual (the thing we’ll reference)
2. an iteration doc (this file) to carry the messy, evolving conversation

## What Changed In This Iteration

- Created the spec/manual at `docs/process/sequential-iteration-via-markdown-files.md`.
- Converted this file into the current iteration document.

## Notes / Requirements To Capture In The Spec

Ensure the spec clearly states:

- the flexible numbering / renumbering approach (layers like `1xx`, `2xx`, and finer granularity via `x1x`, `x2x`)
- the reason this lives in this repo (useful regularly, even if orthogonal to kit scope)
- why Markdown editing ergonomics matter (tag highlighting, quotes, action blocks, fast capture)
- agent responsibility: summarize key outcomes into the iteration doc (not only to screen) and capture chat-only insights

## Discussion

#discuss This process is orthogonal to the kit, but is it still OK to keep it here?

Working answer:

- Yes, as maintainer tooling. If it becomes consumer-facing, publish a simplified version under `payload/docs/process/`.

#recommend Should we add a short pointer in `README.md` under “Maintaining The Kit” to the new spec/manual?

> yep

## Recommendations

#recommendation Keep maintainers’ “how we iterate” docs in `docs/process/` + `docs/iterations/`, and avoid exporting them to consumers unless we intentionally simplify and publish them under `payload/docs/process/`.

> ok. we will develop it here, and either create a new project or incorporate into payload when baked. It's a squirrel within a squirrel. 

## Status Markers
- an iteration document with no status marker is assumed to be #status/draft 

## **Agent Action** blocks

Important to only do one pass of Agent Actions, or the iteration doc becomes too confusing to parse
Implies:
- human should avoid adding Agent Action blocks until discussion has settled, **or**
- human should indicate in the round trip "more discussion, don't do actions yet" (#recommend: terser/clearer way to say that?)
- I like the `**Agent Action (proposed)**:` convention you invented; let's formalize that. And when the human approves, they just remove the `(proposed)`

## Tags

- you used the `#recommend` tag to **ask me** for a recommendation, which is fine, but we need a way to distinguish (i.e., when I read I'm looking for new content, and might gloss over content that I think was tagged by me).

- maybe prefacing with `agent/` e.g. `#agent/recommend`, but it doesn't read right.
- Common markdown requires tags to start with a letter, so can't use < or !.
- #recommend ideas?
- my original idea was I write in markdown and agent replies in quote blocks, but this didn't really work because we both need to write headings, code blocks, etc. and it is cumbersome to do that inside quote blocks. So having either agent or human respond directly to tags/questions with quote blocks is better. Just adding more markdown headings/sections to works for bigger responses if we don't spend too long in any one document, though it does lose a little bit of the process (no way to tell what was added when etc.)
- we probably shouldn't overthink this. The ad hoc way we've been doing it works well enough

## Agent Commentary (2025-12-17)

> an iteration document with no status marker is assumed to be #status/draft

Agree. Two small tweaks that reduce ambiguity later:

- Treat “missing status” as `#status/draft`, but *prefer* always writing a status line anyway (so search is reliable). 
  >> I'll prefer as hard as I can but I can also promise I'll forget
- Consider one more status for your mode concern: `#status/discussing` (or `#mode/discuss`) vs `#status/active` (or `#mode/execute`).

> Important to only do one pass of Agent Actions, or the iteration doc becomes too confusing to parse

Agree with the underlying pain: mixing discussion + execution output in one file gets noisy fast.

#recommendation Separate “discussion” from “execution” without adding process overhead:

- Put a single line near the top like `#mode/discuss` or `#mode/execute`.
- During `#mode/discuss`, allow only `#question` / `#discuss` / `#recommend` and prohibit approved actions.
- During `#mode/execute`, require that all actions are either clearly marked `(proposed)` or explicitly approved.

> human should indicate in the round trip "more discussion, don't do actions yet" ( #recommend: terser/clearer way to say that? )

Options that read clearly and are hard to misinterpret:

- `#mode/discuss` (my favorite; least English, most machine-like)
- `#noactions` (very explicit)
- `#hold` (short, but might be too ambiguous without a convention)

If you want to keep it in plain English:

- “Discussion only — no Agent Actions yet.”

> I like the `**Agent Action (proposed)**:` convention ... when the human approves, they just remove the `(proposed)`

This is good because it’s visually obvious and low ceremony.

#recommendation Add one more terminal marker to reduce “did we do it?” ambiguity:

- `**Agent Action (done)**` once completed (or append `#status/done` inside the block)

That gives you a 3-state lifecycle: proposed → approved → done.

> we need a way to distinguish ... tags asked *of* the agent vs tags emitted *by* the agent

Yes — without this, skimming fails because your eyes will “pattern match” on `#recommend` and you’ll miss content.

Two conventions that stay tag-like, read ok, and obey “starts with a letter”:

1. **Namespace by actor** (simple + explicit)
   - Human asks: `#human/question`, `#human/recommend`, `#human/discuss`
   - Agent outputs: `#agent/recommendation`, `#agent/clarify/*`, `#agent/decide`

2. **Namespace by intent** (cleaner for scanning)
   - Requests: `#ask/recommend`, `#ask/question`, `#ask/discuss`
   - Responses: `#answer`, `#recommendation`, `#clarify/*`, `#decide`

If you want minimal change from what you already do: keep your tags, but require that *agent-emitted* tags always start with `#agent/`.

> replying in quote blocks didn’t really work ... both need headings, code blocks, etc.

Agree. Quote blocks are best used surgically:

- quote *just* the sentence/question being answered
- respond normally underneath

That gives you the “this is what I’m responding to” affordance without forcing full Markdown structure inside quotes.

**Agent Action**
Goal: capture decisions in the spec
- add a section ## AGENTS Snippet that distills the spec into necessary instructions to add to AGENTS, but keep it minimal. If the system fails with e.g. glm_4_6 we may expand, but mostly I use glm_4_6 for todos & atomic tasks, whereas this process is only for topics or features with multi-session work lengths
- agent-emitted tags always start with `#agent-`. This instead of `#agent/` because it reads a little less wrong, and agent prefix is the most viable/visible/convenient solution 
- having to mark the document `#mode/discuss` or not will probably result in a lot of wasted round trips because I'll forget. But happy to use `#mode/discuss` and/or `#noaction` to preface asking questions or asking for a read-give-feedback round trip in the chat. So capture that as a recommendation in the spec, and instructions if required
- formalize tag pairs: 
    - #question => #agent-answser 
    - #recommend => #agent-recommendation 
    - #discuss => #agent-considerations and/or #agent-recommendation 
    - #agent-question => #answer 
    - #clarify/xxx => #agent-clarification/xxx
    - etc.
- formalize: **Two** uses for quotes:
    - **either** the way used them above, in a comments section to quote things referenced **or**
    - the opposite, to insert parenthetical comments/requests in the body of existing markdown. 
    - It should mostly be contextually obvious which is occurring, and simple enough to resolve when not.
    - use double quotes when necessary, e.g.:

```
> original thing said
rejoinder
>> rejoinder to the rejoinder
```

**Agent Action (done)**

Summary of what changed:

- Updated `docs/process/sequential-iteration-via-markdown-files.md` with:
  - `#agent-` tag prefix convention + suggested request/response pairs
  - optional `#mode/discuss` / `#mode/execute` and `#noactions` guidance
  - action block lifecycle: `(proposed)` → approved → `(done)`
  - quote-block guidance (two uses + nested `>>` example)
  - a minimal “AGENTS snippet” section you can copy/paste
