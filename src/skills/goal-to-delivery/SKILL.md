---
name: goal-to-delivery
description: Run Spec-driven Delivery automatically for one selected goal. Stop at the authorized boundary or return a decision, checkpoint, or blocker to the caller.
---

# Goal to Delivery

```text
$goal-to-delivery <goal-or-selected-issue> [--completion artifact|working-tree|commit|pr|merge]
```

1. Confirm the selected goal, acceptance criteria, repository, scope, and [completion boundary](../../tool-instructions/shared/completion-boundaries.md). Follow the [shared workflow](../../tool-instructions/shared/delivery-workflow.md). A direct request defaults to `working-tree`. For dispatched work, verify the assignment and allowed actions from the trusted caller. Honor its run limits. The caller owns queue selection, scheduling, and tracker updates.
2. Run the applicable [Spec-driven Delivery stages](../spec-driven-delivery/SKILL.md) in order. Keep routine planning and task breakdown short. Apply [the clarification policy](../spec-driven-delivery/references/clarification-policy.md) and [quality gates](../spec-driven-delivery/references/quality-gates.md).
3. Return a failed check to the role that can fix it and repeat affected checks. When a material decision blocks progress, ask a direct user one focused question. For a dispatched assignment, return the question, options, and recommendation to the caller. Return a checkpoint or blocker with the completed work and next action when the run needs to pause.
4. Stop when the authorized boundary is verified. Report the result, checks, material assumptions, and remaining work.

Follow the integration guide for caller-specific checks and results. [OpenBot handoff](references/openbot-handoff.md)
