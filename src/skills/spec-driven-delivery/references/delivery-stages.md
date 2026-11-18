# Delivery stages

Run the applicable stages in the order shown. Revisit the plan when clarification changes the scope, design, or acceptance criteria. A stage starts when its required inputs are ready.

| Stage | Typical owner | Result |
|---|---|---|
| `discover` | active agent with `$repo-discovery` | Relevant instructions, patterns, and commands |
| `plan` | planner or active agent | Scope, approach, acceptance criteria, risks, and checks |
| `clarify` | planner or active agent with the relevant specialist | Recorded decision or one unresolved question |
| `design` | product-designer when a spec is required | UI decisions and binding design sources |
| `task` | tasker or active agent | Ordered changes and checks based on the plan and any required design |
| `audit` | independent auditor when required | Plan and task verdict. Resolve blocking findings before implementation. |
| `implement` | matching implementer or active agent | Scoped changes and focused tests |
| `design_review` | product-designer for changed UI or interaction | Design conformance verdict based on the rendered UI in a real browser |
| `qa` | qa with `$qa-verification` | Observed behavior against the acceptance criteria |
| `review` | independent reviewer | Code review of the exact diff with the applicable QA and design results |
| `docs` | `$docs-as-code` and `$luchdom-docs` where applicable | Updated durable docs or a record that no docs need changes |
| `commit` | authorized caller | Scoped commit after the required local checks |
| `pr` | authorized caller | Pushed branch and pull request at the authorized boundary |
| `merge` | authorized caller | Verified merge into the configured default branch |
| `post_merge` | authorized caller | Any follow-up verification the user or repository requires |

## Stage requirements

- During `plan`, apply the [critical workflow checks](quality-gates.md#critical-workflows) to affected workflows.
- Before task breakdown, resolve open material decisions and finish any required design spec. Use the [clarification policy](clarification-policy.md) to record decisions. If a later stage reveals a gap, return to the stage that owns it and update any affected evidence.
- For UI work, use the [design gates](design-gates.md) to decide whether a spec is required. Every change to rendered UI or interaction requires a current design conformance verdict before QA or code review can pass.
- Use the [quality gates](quality-gates.md) to decide when an independent pre-build audit or behavior QA applies, and to verify the evidence needed for code review and publication.
- For authorized C#/.NET backend changes, use [`$dotnet-implementation`](../../dotnet-implementation/SKILL.md) to select the `dotnet` specialist or apply the same guidance inline. In mixed work, route only the .NET portion this way.
- Follow the [completion boundaries](../../../tool-instructions/shared/completion-boundaries.md) for Git, pull requests, merge, and issue closure.
