---
name: linear-delivery-loop
description: Pick or resume one Linear issue and run Goal to Delivery for it. Use when a scheduled task or an attended pilot explicitly invokes this skill. Keep queue state, checkpoints, and decisions in Linear.
---

# Linear Delivery Loop

Use Linear as the autonomous queue. Run [Goal to Delivery](../goal-to-delivery/SKILL.md) for at most one issue per invocation.

## Setup

Read `.ai/loop.json` from the target repository and compare it with [project-config.example.json](./references/project-config.example.json). Stop without mutation if the file is missing, invalid, or disabled. Follow repository rules and the [shared delivery workflow](../../tool-instructions/shared/delivery-workflow.md). Keep API keys and notification topics private.

The normal state mapping is Backlog for eligible intake, In Progress for the single active issue, and Done only after the configured completion boundary.

## Acquire the run lease

After validating that `.ai/loop.json` exists and is enabled, acquire the deterministic cross-run lease before reading or mutating Linear, Git, notifications, or repository work. Run `python <this-skill-directory>/scripts/loop_lock.py acquire --repo-root <repository-root>` and retain the returned token only for release.

- Exit `0` with `status: acquired`: continue this invocation.
- Exit `3` with `status: busy`: another invocation owns this Linear queue; stop immediately without comments, notifications, or repository mutation.
- Any other result: fail closed and report the local lock error without attempting delivery.

The helper scopes the lock by repository key plus Linear team/project, so worktrees and separate local checkouts of the same queue contend. Its lease is `maxRunMinutes + 15` minutes. An expired valid lease is recovered atomically; malformed state is never overwritten.

On Windows, the default lease root is `%LOCALAPPDATA%\Luchdom\ai-toolkit`. Set `LUCHDOM_AI_STATE_HOME` to an absolute user-state path only when an installation requires an explicit override; never point it at this repository or its `docs` directory.

Before every return after acquisition—including completion, checkpoint, decision request, validation failure, or unexpected error—run `python <this-skill-directory>/scripts/loop_lock.py release --repo-root <repository-root> --token <token>`. Never store the token in Linear, Git, docs, or notifications. If the process is killed before release, a later invocation recovers the lease after expiry.

## Select or resume one issue

Query the configured Linear team/project and re-read the result immediately before claiming:

1. If more than one issue is in the active state, comment on none and stop with a human-attention result.
2. If one active issue lacks the configured autonomous label, assume attended work is in progress and stop.
3. If one active autonomous issue has the configured human-decision label, inspect only newer owner comments that match `DECIDE <ISSUE> <OPTION>` or `DECIDE <ISSUE> CUSTOM <SUGGESTION>`. For a listed option, acknowledge the decision, remove the label, and continue. For `CUSTOM`, use the remaining non-empty text as the owner's proposed direction; continue only when it resolves the latest question safely, otherwise keep the label, post one focused follow-up, and stop. Ignore ordinary comments as authorization.
4. If one eligible active autonomous issue exists, resume it.
5. Otherwise select the highest-priority backlog issue with the autonomous label and without the human-decision label. Break ties by oldest creation time. Select no work when none is eligible.

Before claiming new work, confirm the issue states one achievable, bounded, locally testable goal with acceptance criteria. External-only setup, unclear product behavior, and oversized work are not eligible. Move one eligible issue to the active state, assign it to the configured owner when present, and add a short claim comment. Re-query active work; if the one-issue invariant no longer holds, stop.

## Archive quiet standalone runs

A quiet run is a standalone scheduled invocation that finds an expected no-work condition, produces no new actionable result, and makes no Linear, Git/GitHub, repository, pull-request, or notification mutation. Transient lease acquisition and release do not make a run non-quiet. Expected quiet outcomes are: the loop is disabled; the lease is busy; attended work is active; no eligible backlog issue exists; or an active `needs-human` issue has no newer valid owner decision and needs no new follow-up.

After releasing any acquired lease, archive only the current quiet standalone scheduled run when the host exposes a native current-task archival capability. In Codex, call `set_thread_archived`; never emit a raw archive directive, automate the app UI, archive another task, or invent a filesystem workaround. If native archiving is unavailable, return one concise no-op result normally.

Never archive an attended pilot, a scheduled task attached to an existing long-lived chat, or a run that claimed or resumed delivery work. Keep the run visible when it created or changed anything, requested or refined a decision, sent a notification, checkpointed work, encountered an error or invalid configuration, found multiple active issues, or discovered another condition that needs attention.

## Run Goal to Delivery

Pass the selected issue, approved decisions, permitted actions, and run limits to Goal to Delivery. For code, set the boundary to `merge` and authorize the branch, push, pull request, and merge actions allowed by the configuration and repository. Prefer one branch and pull request per issue. For other work, set the boundary to `artifact`. Record any new decisions in the issue before dependent work continues.

Use `maxRunMinutes` for the run and `maxTestMinutes` for tests. Use `maxFiles` and `maxChangedLines` as planning thresholds. Finish a coherent edit before deciding whether to split the remaining scope.

## Checkpoint or split the work

When the run or test limit is reached or work is interrupted, commit and push coherent work when safe and allowed. Add the branch or PR, completed checks, and next action to a Linear checkpoint. Keep the issue active and stop. If scoped retries leave a technical blocker, use the decision process below.

Create at most one linked continuation issue when a limit is reached and the remainder is too large for another normal run. Split only at a reviewable boundary with independently testable acceptance criteria. Preserve the original goal across the two issues. Record what is complete and what remains. Use the same project and priority, add the autonomous label only when the continuation is eligible, and leave it in Backlog for a later run. Checkpoint the current issue or request a decision if no safe split exists.

## Ask for a decision

Use this path when Goal to Delivery returns an unresolved choice. Include the specialist recommendation and evidence. Resume a human-decision pause only on a newer matching reply from the owner.

Keep the issue active and add the configured human-decision label. Include these details in the Linear comment.

- The blocked decision
- Two or three concrete options and consequences
- One recommendation
- How to choose an option with `DECIDE <ISSUE> <OPTION>` or supply a direction with `DECIDE <ISSUE> CUSTOM <SUGGESTION>`

When enabled, send one best-effort ntfy notification. Use the Linear issue URL as the notification click target and include the URL in the message. Keep the decision request in Linear if the notification fails. Stop after requesting the decision.

## Complete

Verify that Goal to Delivery reached the [completion boundary](../../tool-instructions/shared/completion-boundaries.md). For code, use the configured merge method and confirm the provider reports a merge into the configured default branch. For an artifact, confirm the acceptance checks passed. Then move the issue to Done, add a short result comment, release the lease, and end the run.
