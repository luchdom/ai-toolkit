# Delivery workflow

Use the entry and stopping point the user requested.

| Request | Route and stopping point |
| --- | --- |
| Create a plan | Run [Spec-driven Delivery](../../skills/spec-driven-delivery/SKILL.md) `plan` and return control. |
| Run a named stage or continue a manual delivery | Run the requested or next applicable stage. Check its prerequisites and return control. |
| Fix a problem | Use Goal to Delivery for scoped working-tree changes and local checks. |
| Fix a problem and open a pull request | Use Goal to Delivery, complete the required checks, and stop at the pull request. |
| Run Goal to Delivery | Use [Goal to Delivery](../../skills/goal-to-delivery/SKILL.md) for one selected goal. |

The [stage order](../../skills/spec-driven-delivery/references/delivery-stages.md) defines the prerequisites. Follow the repository's commands and stricter rules. Protect unrelated changes.

An external runner selects the work and manages scheduling, decisions, and issue state. It supplies a verified assignment and the allowed actions for that run. The toolkit reports the result for the assigned work.

- Save plans and evidence using the [artifact contract](artifact-contract.md).
- Check the [completion boundaries](completion-boundaries.md) before publishing.
- Follow the [worktree policy](worktrees.md) when creating, resuming, or removing a linked Git worktree.
