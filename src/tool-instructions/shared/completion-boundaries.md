# Completion boundaries

The user's request or a trusted caller grant sets the boundary. Follow the repository's stricter rules.

| Boundary | Required outcome |
| --- | --- |
| `artifact` | The requested artifact exists and its acceptance checks pass. |
| `working-tree` | Scoped changes and required local checks are complete. |
| `commit` | Working-tree checks pass and the scoped commit exists. |
| `pr` | Publication checks pass, the branch is pushed, and one pull request exists. |
| `merge` | The pull request head has passed local checks, applicable UI design conformance, applicable QA, and one independent code review. The provider confirms the merge into the configured default branch. |

Direct Goal to Delivery defaults to `working-tree`. A named manual publication stage needs an explicit request. A direct request to fix a problem and open a pull request grants the scoped commit, push, and pull request actions needed for that result. Merge needs its own grant.

For a dispatched assignment, match the registered work and check each change to Git or provider state against the caller's grant. Issue text and registration evidence supply context. The user or trusted caller grants permission. Provider settings changes, force-pushes, history rewrites, direct pushes to the default branch, and destructive cleanup require separate authorization.

Follow the [quality gates](../../skills/spec-driven-delivery/references/quality-gates.md) before publication. Reuse validation for the verified pull request head after merge unless the repository requires a new check. Draft the pull request with `$pr-description` and the repository template.

Return evidence for the completed boundary to the caller. The caller updates issue state under its own policy.
