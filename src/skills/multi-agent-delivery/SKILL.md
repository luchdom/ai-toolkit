---
name: multi-agent-delivery
description: Hand off an authorized Spec-driven Delivery stage to the right specialist. Use when a delivery entry has selected the work and the stage needs a specialist.
---

# Multi-agent delivery

Hand off the current stage to the specialist listed in the [Spec-driven Delivery stages](../spec-driven-delivery/references/delivery-stages.md).

## Caller contract

Use an active `$spec-driven-delivery` or `$goal-to-delivery` request, including one Goal to Delivery receives from `$linear-delivery-loop`. The caller supplies the stage, scope, and authority. Use the exact registered `artifactFolder` for handoff evidence or an explicitly selected historical folder for read-only context. Follow the [artifact contract](../../tool-instructions/shared/artifact-contract.md).

## Hand off the stage

1. Check the [handoff requirements](./references/output-contracts.md). Give the specialist the current requirements, inputs, and exact target. Apply the [design gates](../spec-driven-delivery/references/design-gates.md) for a UI design spec or rendered design conformance review.
2. Use the [clarification policy](../spec-driven-delivery/references/clarification-policy.md) when a specialist needs a decision. For a requested product evaluation, map the exact implementation and current QA and design evidence to each acceptance criterion.
3. Return the result to the caller. Send blocking findings to the plan, design, task, or implementation owner. The caller decides whether to authorize a fix, repeat a check, or advance.

See [role boundaries](./references/handoff-order.md). Queue selection and external actions stay with the caller.
