# Delivery workflow

Use the entry that matches the request.

| Entry | Scope |
|---|---|
| [`$spec-driven-delivery`](../../skills/spec-driven-delivery/SKILL.md) | Defines the delivery process. A direct request runs exactly one stage. |
| [`$goal-to-delivery`](../../skills/goal-to-delivery/SKILL.md) | Runs the applicable stages automatically for one selected goal. |
| [`$linear-delivery-loop`](../../skills/linear-delivery-loop/SKILL.md) | Picks or resumes one Linear issue per run and passes it to Goal to Delivery. |

When a non-trivial request names no entry, use Spec-driven Delivery and run only the requested stage. For a planning request, run `plan`.

Follow user and system requirements, then stricter repository rules, then the authority granted by the active entry. The repository owns its local commands and acceptance checks. Resolve any conflict about authority before implementing or changing external state. Keep unrelated changes intact.

- Use the [artifact contract](artifact-contract.md) when saving plans and delivery evidence.
- Use the [completion boundaries](completion-boundaries.md) to verify what the current request authorizes.
- Use the [worktree policy](worktrees.md) before creating, resuming, or removing a linked Git worktree.
