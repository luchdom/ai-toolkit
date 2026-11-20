---
name: goal-to-delivery
description: Run Spec-driven Delivery for one goal selected by the user, the active Linear Delivery Loop, or an owner-enabled OpenBot Workflow Coordinator. Continue to the authorized boundary or return a decision or checkpoint to the caller.
---

# Goal to Delivery

Run [Spec-driven Delivery](../spec-driven-delivery/SKILL.md) automatically for one goal.

## Invocation

```text
$goal-to-delivery <goal-or-selected-issue> [--completion artifact|working-tree|commit|pr|merge]
```

For a direct request, use the goal or issue the user selected. Default to a local goal with scoped edits and local checks through the `working-tree` boundary. Follow repository policy for updates to a selected issue.

[Linear Delivery Loop](../linear-delivery-loop/SKILL.md) can call this skill with one selected issue, the permitted actions, a completion boundary, and run limits. Use that authority only when called by the active loop. Queue selection stays with the loop.

An owner-enabled OpenBot Workflow Coordinator can dispatch one issue it already claimed. Check the live assignment, its registered worktree and the actions allowed by the owner. Start or resume one Codex lead for that assignment. Return events to the same Coordinator. [OpenBot handoff](references/openbot-handoff.md)

## Run the stages

1. Confirm the goal, acceptance criteria, and [completion boundary](../../tool-instructions/shared/completion-boundaries.md). Read the repository rules and the [shared workflow](../../tool-instructions/shared/delivery-workflow.md).
2. Run the applicable Spec-driven Delivery stages in order. Keep routine planning and task breakdown short. Use its stage requirements, including any required audit, design work, and verification.
3. Ask the Product Manager about the user experience and the Staff Engineer about technical choices. The implementer owns the UI spec and implementation. QA checks the rendered result. Assign code review to a Staff Engineer who meets the independence requirements. [Clarification policy](../spec-driven-delivery/references/clarification-policy.md) · [Independent code review](../spec-driven-delivery/references/quality-gates.md#independent-code-review)
4. Send failures back to the stage that can fix them. Rerun any checks that the fix invalidates. If scoped retries or the run budget are exhausted, stop with the blocker and the next action.
5. Ask the user one focused question if a material decision is unresolved. For a Linear loop or OpenBot assignment, return the question, options and recommendation to that caller. Return a checkpoint through the same route when the run pauses.
6. Stop when the authorized boundary is verified. Report the outcome, checks, material assumptions, and any remaining work.
