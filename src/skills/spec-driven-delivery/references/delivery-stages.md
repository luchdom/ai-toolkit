# Delivery stages

Start a stage when its inputs are ready. Run the applicable stages in order. When a decision or fix changes an earlier result, update that result and repeat affected checks.

| Stage | Typical owner | Result |
| --- | --- | --- |
| `discover` | active agent with `$repo-discovery` | Relevant rules, patterns, and commands |
| `plan` | planner or active agent | Goal, scope, acceptance criteria, risks, and checks. For a saved plan, use a dated `*-plan.md`. |
| `clarify` | planner or active agent with the relevant specialist | Recorded decision or an open question |
| `design` | implementer with `$ui-review-spec`, when required | UI behavior, components, and acceptance checks |
| `task` | tasker or active agent | Ordered changes and checks |
| `audit` | independent Staff Engineer, or an assigned `auditor` | Readiness verdict when required. Resolve blockers before implementation. |
| `implement` | matching implementer or active agent | Scoped changes and focused tests |
| `docs` | `$docs-as-code` and `$luchdom-docs` where applicable | Updated durable docs or a reason no update is needed |
| `design_review` | `qa` for changes to rendered UI or interaction | Independent design conformance verdict from a real browser |
| `qa` | `qa` with `$qa-verification` | Observed behavior against acceptance criteria |
| `review` | independent Staff Engineer | Code review of the exact diff with the applicable QA and design results |
| `commit` | authorized caller | Scoped commit after required checks |
| `pr` | authorized caller | Pushed branch and pull request |
| `merge` | authorized caller | Verified merge into the configured default branch |
| `post_merge` | authorized caller | Follow-up checks required by the user or repository |

## Prerequisites

- In `plan`, cover affected [critical workflows](quality-gates.md#critical-workflows).
- Resolve material decisions with the [clarification policy](clarification-policy.md) and finish any required [design specification](design-gates.md) before task breakdown.
- Finish tracked docs before design review, QA, and code review record the target. Use the [quality gates](quality-gates.md) to decide which checks apply.
- Use [completion boundaries](../../../tool-instructions/shared/completion-boundaries.md) for Git and publication. A caller or repository can require product acceptance in addition to the shared checks.

## Implementation

For authorized C#/.NET backend work, use [`$dotnet-implementation`](../../dotnet-implementation/SKILL.md). Route only the .NET work this way in a mixed task.

Follow the repository's dependency policy and the approved scope. When both are silent, reuse an existing option if practical. If the change needs a new dependency, ask the caller to approve it before adding it.
