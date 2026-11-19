# Delivery workflow

Use the entry that matches the request.

| Entry | Scope |
|---|---|
| [`$spec-driven-delivery`](../../skills/spec-driven-delivery/SKILL.md) | Defines the delivery process. A direct request runs exactly one stage. |
| [`$goal-to-delivery`](../../skills/goal-to-delivery/SKILL.md) | Runs the applicable stages automatically for one selected goal. |
| [`$linear-delivery-loop`](../../skills/linear-delivery-loop/SKILL.md) | Picks or resumes one Linear issue per run and passes it to Goal to Delivery. |

When the user asks for a plan, such as "create a plan" or "plan this change", run `$spec-driven-delivery plan <goal>` unless they choose another entry. Return the plan and hand control back to the user.

Resume the same work one stage at a time when the user asks to continue. Use `clarify` to resolve open decisions, then `task` to break down the work after those decisions and any required design are complete. Follow the [delivery stages](../../skills/spec-driven-delivery/references/delivery-stages.md) for the remaining work.

For other non-trivial requests without a selected entry, use Spec-driven Delivery and run only the requested stage.

Follow user and system requirements, then stricter repository rules, then the authority granted by the active entry. The repository owns its local commands and acceptance checks. Resolve any conflict about authority before implementing or changing external state. Keep unrelated changes intact.

- Use the [artifact contract](artifact-contract.md) when saving plans and delivery evidence.
- Use the [completion boundaries](completion-boundaries.md) to verify what the current request authorizes.
- Use the [worktree policy](worktrees.md) before creating, resuming, or removing a linked Git worktree.
