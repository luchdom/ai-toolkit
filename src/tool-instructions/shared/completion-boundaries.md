# Completion boundaries

Stop at the boundary authorized by the active entry.

| Boundary | Required outcome |
|---|---|
| `artifact` | The requested non-code artifact exists and its acceptance checks pass. |
| `working-tree` | Scoped changes and required local checks are complete in the working tree. |
| `commit` | Working-tree requirements pass and an authorized scoped commit exists. |
| `pr` | The branch is pushed and one pull request exists. |
| `merge` | The PR head passes required local checks, applicable UI design conformance, applicable QA, and one independent code review. The provider confirms the merge into the configured default branch. |

Goal to Delivery defaults to `working-tree` for a direct request. A manual Spec-driven Delivery request needs a separate stage for `commit`, `pr`, or `merge`. Linear Delivery Loop passes `merge` for code and `artifact` for other work when repository policy allows.

For an OpenBot assignment, use the completion boundary and allowed actions from the owner's project configuration and verified claim. Report the evidence to the Workflow Coordinator before it releases the project's slot. [OpenBot handoff](../../skills/goal-to-delivery/references/openbot-handoff.md)

Use read-only Git inspection where repository rules allow it. Require the declared boundary or a separate grant before committing, pushing, opening a pull request, or merging. Provider settings changes, force-pushes, history rewrites, direct pushes to the default branch, and destructive cleanup require their own authorization.

Follow the [quality gates](../../skills/spec-driven-delivery/references/quality-gates.md) before publishing. Reuse validation for the verified PR head after merge unless the repository requires a post-merge check.

Use `$pr-description` and the repository's pull request template when drafting a PR.

Keep a linked issue active through implementation and in review while its PR is open. Move it to Done only after verifying its completion boundary.
