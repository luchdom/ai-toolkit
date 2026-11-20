---
name: spec-driven-delivery
description: Define and run the delivery stages from plan to publication. A direct request runs exactly one named stage. Goal to Delivery uses the same stages for automatic delivery.
---

# Spec-driven Delivery

Use the [stage order and prerequisites](./references/delivery-stages.md) for manual and automatic delivery. Plan, clarify the open decisions, break down the work, audit when required, implement, run quality assurance (QA), then review. Include the applicable design and documentation stages. Publish only to the [authorized boundary](../../tool-instructions/shared/completion-boundaries.md).

## Run one stage manually

```text
$spec-driven-delivery <stage> <goal|selected-issue|exact-work-selector>
```

Check the named stage's prerequisites, perform it, and report the result. Return control to the user at the end of the stage. For `clarify`, ask one focused question at a time when a material decision remains open. For `implement`, make scoped edits and run focused tests. For `commit`, `pr`, or `merge`, require an explicit request for that stage.

## Use the same stages in automatic delivery

[Goal to Delivery](../goal-to-delivery/SKILL.md) runs these stages in order for the user, the active Linear loop, or an operator-enabled OpenBot Workflow Coordinator with a verified [issue handoff](../goal-to-delivery/references/openbot-handoff.md). Each run keeps the assignment, permitted actions and completion boundary from its caller. The caller chooses when to advance, retry, ask for a decision, or stop. An issue label or saved artifact alone grants no authority to advance.

## Follow the rules for the current stage

- Use the [clarification policy](./references/clarification-policy.md) when a decision blocks progress.
- Use the [design gates](./references/design-gates.md) for UI work. Initialize or resume the registered `artifactFolder` before design or implementation when they apply.
- Use the [quality gates](./references/quality-gates.md) to plan critical workflows and guide audit, QA, review, and validation.
- Use [Multi-agent Delivery](../multi-agent-delivery/SKILL.md) when handing a stage to a specialist.
- Follow the [artifact contract](../../tool-instructions/shared/artifact-contract.md) when saving evidence and the [worktree policy](../../tool-instructions/shared/worktrees.md) when using a linked worktree. Keep one concise work note when requested, useful across sessions, or required by a stage.
