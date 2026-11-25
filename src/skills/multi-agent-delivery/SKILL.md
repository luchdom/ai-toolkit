---
name: multi-agent-delivery
description: Hand off an authorized Spec-driven Delivery stage to the right specialist.
---

# Multi-agent delivery

Use an active `$spec-driven-delivery` or `$goal-to-delivery` request. The caller supplies the stage, scope, and allowed actions. Queue selection and external actions stay with the caller.

1. Choose the specialist from the [stage order](../spec-driven-delivery/references/delivery-stages.md) and [role boundaries](references/handoff-order.md).
2. Give the specialist the requirements, exact target, and [required inputs](references/output-contracts.md). Follow the [artifact contract](../../tool-instructions/shared/artifact-contract.md) and the [design gates](../spec-driven-delivery/references/design-gates.md) for a design spec or design conformance review.
3. Return results to the caller. Send blocking findings to the owner of the affected work. The caller decides whether to authorize a fix or move to the next stage.
