---
name: goal-to-delivery
description: Run Spec-driven Delivery automatically for one goal selected by the user or by Linear Delivery Loop. Continue through the applicable stages and stop at the authorized boundary or an unresolved decision.
---

# Goal to Delivery

Run [Spec-driven Delivery](../spec-driven-delivery/SKILL.md) automatically for one goal.

## Invocation

```text
$goal-to-delivery <goal-or-selected-issue> [--completion artifact|working-tree|commit|pr|merge]
```

For a direct request, use the goal or issue the user selected. Default to a local goal with scoped edits and local checks through the `working-tree` boundary. Follow repository policy for updates to a selected issue.

[Linear Delivery Loop](../linear-delivery-loop/SKILL.md) can call this skill with one selected issue, the permitted actions, a completion boundary, and run limits. Use that authority only when called by the active loop. Queue selection stays with the loop.

## Run the stages

1. Confirm the goal, acceptance criteria, and [completion boundary](../../tool-instructions/shared/completion-boundaries.md). Read the repository rules and the [shared workflow](../../tool-instructions/shared/delivery-workflow.md).
2. Run the applicable Spec-driven Delivery stages in order. Keep routine planning and task breakdown short. Use its stage requirements, including any required audit, design work, and verification.
3. At the stage where a question comes up, use the [clarification policy](../spec-driven-delivery/references/clarification-policy.md). Call `product-manager` for the goal or product behavior, `product-designer` for UI and user experience, and `staff-engineer` for technical choices. For code review, use `code-reviewer` by default. A separate `staff-engineer` can review when technical depth is needed and they meet the same [independent review requirements](../spec-driven-delivery/references/quality-gates.md#independent-code-review).
4. Send failures back to the stage that can fix them. Rerun any checks that the fix invalidates. If scoped retries or the run budget are exhausted, stop with the blocker and the next action.
5. Ask the user one focused question if a material decision is unresolved. If the loop called this skill, return the question, options, and recommendation to the loop. Return a checkpoint the same way when the run needs to pause.
6. Stop when the authorized boundary is verified. Report the outcome, checks, material assumptions, and any remaining work.
