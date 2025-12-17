#status/finished
# Initial Feedback on `simple-agentic-process-setup`

Date: 2025-12-16

This document is meant to be annotated. Each quoted block (`> ...`) captures feedback; add your response immediately below it.

## What This Project Is

> This repo is a “process kit” / template generator: it’s not an app, it’s a set of process artifacts (docs + playbooks + scripts) plus an installer (`scaffold-project.py`) that writes those artifacts into some other project.

Response:
correct. What's missing is a top level overview. Below are some notes from the original discussion that will help:

**NOTE**: the part regarding third-party feedback should be considered out-of-scope for the inital round of iterations on this project, but kept in mind as a future integral addition to the process

```
<team>

- solo human developer

- multiple CLI coding agents (codex cli, opencode, gemini cli, claude cli)

</team>

<current-development-habits>

- these are habits that have worked well on smaller projects

- frequently running multiple coding agents concurrently:

- interactive feature development session

- atomic todos/cleanup-task, running in a loop, new clean context agent per todo item, in transient branch that is fastforwarded & merged to land.

- Usually prompts for human review before landing, with recommended further todos

- uses <todo-checkpoint/> to coordinate

<todo-checkpoint>

- single in-project todos document with Review, Approved, Future, and Finished sections

- Review Todos moved to Approved (or Future) by human developer after review

- todo agent works on TODOs from Approved

- when todo agent prompts for "recommended todos" it adds those the human developer approved to Available section directly

- if running non-interactively, todo agent adds recommended todos to Review section, or to Future TODOs if the human developer indicates

- todo agent ensures that todos in Review section have the short git sha where they were added appended with `#SHORTSHA`, so that when they are moved between sections, they retain a pointer to when they were first added

- when landing a todo, todo agent moves the todo to Finished. Then a final commit before landing appends `#done/SHORTSHA` to the todo with the short sha of the commit that finished the work

</todo-checkpoint>

- review agent reviewing commits as they land in development branch

- ensures test coverage & up-to-date documentation

</current-development-habits>

  

<whats-new-about-this-project>

- need to maintain a stable branch that is deployed, for demoing / personal-use

- probably this means using long-lived feature branches, although minor todos could still be folded immediately into development

- need a way to ingest todos/ideas/feedback from third-parties

- preferrably from within the running demo app. third-parties are non-technical, so not github issues

</whats-new-about-this-project>

  

<considerations>

- prefer as much as possible to be viewable in the project git repo

- must use human readable / editable format for process artifacts.

- yaml or markdown

- If process needs machine generated ids etc., they should be attached to the line or hierarchical block of markdown or yaml for ease of human editing

- would consider using github process tools if there is a strong enough case, and if it is easy to consume them from terminal and/or within an interactive cli coding agent

</considerations>
```

**Agent Action:**
1. produce a project README.md and/or docs/Overview.md that captures the intent and goals

## What It Contains (As Designed)

> **Agent operating model:** a small “human orchestrator + multiple agents” loop, with explicit playbooks in `docs/ai/playbooks/` and a context-loading helper `scripts/run-prompt.sh` driven by `scripts/context.config.yaml`.

Response:
correct.
**Action:**
convert `scripts/context.config.yaml` to yaml. I am and always will be a yaml dude.


> **State machine:** a single coordination file `docs/process/TODO.md` with sections (Inbox/Review/Approved/Finished) acting as the shared queue and audit trail.

Response:
correct

> **Buffered integration:** branch model `topic/*` → `main` (fast-moving trunk) → `stable` (manual release), plus a “Local Exchange” concept to visualize multiple working slots without pushing everything to GitHub.

Response:
correct. The "local exchange" idea comes out of wanting to abandon a bare repo + worktree "slots" setup and switch to just cloning as many local repos as needed to accomodate concurrent human + agents. However, one thing I valued from the bare repo + worktree setup was being able to run gitx and see all the ephemeral branches, since we did not delete them locally. Visually in gitx they are like labels in time order of the work. Since they are fastforward rebased on development before merging, any other commits involved in a branch's work are immediately after the commit with the branch label, and the history is linear and simple to reason about, and quickly inspect what happened/changed in a branch's work. So the local exchange repo that "slot" repos push to is intended to accomplish that.

**Agent Action:**
1. Better documentation of the why

## Initial Criticisms / Gaps

> **Single source of truth problem:** the repo had “real” files under `docs/` and `scripts/`, but `scaffold-project.py` embedded its own copies of several documents/scripts as Python strings. That drifts easily unless you generate one from the other.

Response:
correct, scaffold-project.py got out-of-date in attempting to clumsily iterate on the idea with gemini via webchat
I think it might be better to use an agent prompt to do the installation, allowing the opportunity to ask questions of the installing user, and flexibly handle potential conflicts with existing agent instruction in the app being installed to and/or existing project docs/artifacts

**Agent Action**:
comment on the feasibility of an Agent installer in docs/iterations/100-Installation.md


> **Definition-of-done mismatch:** your maintainer rules say some artifacts are payload, but the installer didn’t actually install all of them (e.g. `bus-factor.md`, `local-exchange.md`, and `AGENTS-additions.md`).

Response:
correct, installer needs work, see above.


> **Cross-project specificity leaks:** playbooks hardcode `mix test` (Elixir), and GitX/macOS assumptions appear in the dashboard path. As a general-purpose kit, you probably want a configurable “test command” and a more platform-neutral dashboard option (or at least label GitX as optional).

Response:
correct. However my immediate next need is for an Elixir/Phoenix project, and I don't feel the overall idea is mature enough to make it generic yet. So, let's keep the immediate focus on an Elixir/Phoenix project and make it generic at a later date.


> **Concurrency hotspot:** `docs/process/TODO.md` is intentionally central, but that makes it the most likely merge-conflict file when multiple agents run concurrently.

Response:
Yes, but I've done variation's on it across three small projects, and it works. The highest concurrency I got up to was 2 concurrent "todo implementer" loops running while working with a larger feature with an interactive agent. The todo implementer agents were still interactive, so occasionally paused with questions and paused before feedback before landing. We had one conflict which took some sorting, but chatgpt-codex handled it with no problem (opencode with glm_4_6 not so adept, but the worst case is that a particular todo item needs to be run from scratch once in a while)

## Team Fit

> Best fit: **1 tech lead / product owner** who actively “operates” the system (triage, approve, land), plus **2–6 contributors** (human and/or agent) doing implementation work in parallel.

Response:
Correct. Exactly what this is, me (25 years web developer experience, much of it as solo or lead), and however many agents I feel like running on a given day


> Works well for teams that are **Git-fluent**, comfortable with **branch discipline**, and want **lightweight coordination** without Jira/Linear overhead.

Response:
I'm reasonably git-fluent, and have been practicing bnanch discipline since before git existed. And chatgpt-codex's adpetpness with git is *chef's kiss*


> Poor fit / higher friction: larger orgs needing formal approvals/audit trails outside Git, or teams that can’t enforce “single-writer” rules for coordination artifacts.

Response:
correct. If project gets to that point, this whole process is trivial to rip out & replace with an external pm system

## Multi-Agent Concurrency (2–4 Agents)

> This can work well with 2–4 agents concurrently if you treat concurrency as a first-class constraint and adopt a few hard rules.

Response:
yep. Already tested.


> **Use `origin/main` as an immutable starting snapshot per agent run.** Each agent should branch from a specific `origin/main` SHA and record it on the TODO item (e.g., `#base/<sha>`).

Response:
Hadn't thought of recording the base sha on the todo. It's a good idea


> **Enforce “single-writer” for coordination files.** If multiple agents edit `docs/process/TODO.md`, you’ll get avoidable conflicts. A clean pattern is: only the “manager/closer” role edits TODO; implementers don’t touch it.

Response:
nope, disagree. everyone edits todo. edits always change whole lines, #sha tags are treated as persistent/untouchable, everyone fast-forward rebases before merging, and because todo implementers work on & land a single todo in a branch per run, TODO on the head is rarely far behind. If the long-lived topic branches end up creating/finishing TODO items while they are unmerged, that could be a problem—but usually they are working off a spec, and can use their own todo list for that spec, adding todos to the mainlist when they land, after first fast-forwarding. If fast-forwarding when landing topic branches becomes painful, it is simply resolved by having them organize the work such that it can be fast-forwarded one piece at a time. If we ever have a topic branch where that is difficult, well, we're no worse off than any other way of doing things in that situation.


> **Reduce shared-file collisions.** Your feedback-as-files approach is good because it’s naturally sharded by path. You want the same sharding property for other agent outputs if TODO conflicts become a tax.

Response:
I think I understand what you are saying, but tell me more.


> **Local Exchange helps visibility, but keep it optional.** It assumes a wrapper-directory slot structure and local Git GUI habits. Great for the operator; not required for agents to function.

Response:
It can't really be optional though, because everyone needs to push their work branches to the local exchange repo for it to work. Although, that could be done out-of-band by watcher or git-hook?

**Agent Action**
1. capture anything in the feedback/responses necessary for clean context agent (or forgetful human a month from now) understanding the project from scratch in appropriated docs in docs/ (without the integer prefix, we'll keep that for ordering our work on iterating on this)
2. advise on handling the local exchange out-of-band (no agent knowledge of it necessary). Do this in a document in docs/
