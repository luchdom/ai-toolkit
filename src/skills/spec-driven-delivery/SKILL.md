---
name: spec-driven-delivery
description: Define and run the delivery stages. A direct stage request runs exactly one stage. Goal to Delivery can run the same stages for one goal.
---

# Spec-driven Delivery

Use the [stage order and prerequisites](references/delivery-stages.md).

```text
$spec-driven-delivery <stage> <goal|selected-issue|exact-work-selector>
```

For a manual request, check prerequisites, perform the named stage, and return control. Ask one focused question in `clarify` when a material decision blocks progress. During `implement`, make scoped edits and run focused checks. For `commit`, `pr`, or `merge`, require an explicit request for that stage.

[Goal to Delivery](../goal-to-delivery/SKILL.md) uses the same stages. The caller sets the scope, allowed actions, and stopping point.

- Use the [clarification policy](references/clarification-policy.md) and [quality gates](references/quality-gates.md).
- For UI work, follow the [design gates](references/design-gates.md). Initialize or resume the registered `artifactFolder` before design or implementation when required.
- Use [Multi-agent Delivery](../multi-agent-delivery/SKILL.md) when handing a stage to a specialist.
- Follow the [artifact contract](../../tool-instructions/shared/artifact-contract.md), [completion boundaries](../../tool-instructions/shared/completion-boundaries.md), and [worktree policy](../../tool-instructions/shared/worktrees.md).
