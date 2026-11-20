# Delivery stages

Run the applicable stages in the order shown. Revisit the plan when clarification changes the scope, design, or acceptance criteria. A stage starts when its required inputs are ready.

| Stage | Typical owner | Result |
|---|---|---|
| `discover` | active agent with `$repo-discovery` | Relevant instructions, patterns, and commands |
| `plan` | planner or active agent | Scope, approach, acceptance criteria, risks, and checks |
| `clarify` | planner or active agent with the relevant specialist | Recorded decision or one unresolved question |
| `design` | implementer with `$ui-review-spec` when a spec is required | UI behavior, components and acceptance checks tied to binding design sources |
| `task` | tasker or active agent | Ordered changes and checks based on the plan and any required design |
| `audit` | independent `staff-engineer` when required | Readiness verdict on the plan, design and tasks. Resolve blocking findings before implementation. |
| `implement` | matching implementer or active agent | Scoped changes and focused tests |
| `design_review` | `qa` for changed UI or interaction | Independent comparison of the rendered UI with the binding sources in a real browser |
| `qa` | qa with `$qa-verification` | Observed behavior against the acceptance criteria |
| `review` | independent `staff-engineer` | Code review of the exact diff with the applicable QA and design results |
| `docs` | `$docs-as-code` and `$luchdom-docs` where applicable | Updated durable docs or a record that no docs need changes |
| `commit` | authorized caller | Scoped commit after the required local checks |
| `pr` | authorized caller | Pushed branch and pull request at the authorized boundary |
| `merge` | authorized caller | Verified merge into the configured default branch |
| `post_merge` | authorized caller | Any follow-up verification the user or repository requires |

In OpenBot, one `senior-full-stack-engineer` owns `plan`, `clarify`, any required `design`, `task` and `implement` for the selected issue. An independent Staff Engineer checks readiness before implementation. After engineering review, the Product Manager checks the delivered user journey against the acceptance criteria before handoff. Other entries can continue to use their planner, tasker, stack implementers or an explicitly assigned `auditor` for the pre-build audit.

Older project prompts may ask the toolkit for a designer or a separate reviewer. Route a product or UX decision to the Product Manager, a design specification to the implementer, an independent rendered check to QA and an independent code review to the Staff Engineer. Keep any project requirement for a named human approval.

## Stage requirements

- During `plan`, apply the [critical workflow checks](quality-gates.md#critical-workflows) to affected workflows.
- Before task breakdown, resolve open material decisions and finish any required design spec. Use the [clarification policy](clarification-policy.md) to record decisions. If a later stage reveals a gap, return to the stage that owns it and update any affected evidence.
- For UI work, use the [design gates](design-gates.md) to decide whether a spec is required. Every change to rendered UI or interaction requires a current design conformance verdict before QA or code review can pass.
- Use the [quality gates](quality-gates.md) to decide when an independent pre-build audit or behavior QA applies, and to verify the evidence needed for code review and publication.
- For authorized C#/.NET backend changes, use [`$dotnet-implementation`](../../dotnet-implementation/SKILL.md) to select the `dotnet` specialist or apply the same guidance inline. In mixed work, route only the .NET portion this way.
- Follow the [completion boundaries](../../../tool-instructions/shared/completion-boundaries.md) for Git, pull requests, merge, and issue closure.
