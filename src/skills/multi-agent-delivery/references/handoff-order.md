# Specialist roles

The caller entry policy controls advancement and authority throughout.

| Owner | Owns | Must not own |
|---|---|---|
| `planner` | Discovery-backed plan and clarification record | Tasks, audit verdict, implementation |
| `product-manager` | Scoped product decisions, requested PRDs, benchmark interpretation with PD, and AC-based product evaluation | Code changes, weakening AC, independent QA/design/code-review substitution |
| `staff-engineer` | Scoped technical decisions, feasibility with PM/PD, simplification and code review, requested RFCs/ADRs/diagrams | Implementation, fixes, or independent approval of its own technical proposal |
| `product-designer` before implementation | Binding design-source analysis and design spec when required | Implementation, code review, QA |
| `tasker` | Ordered execution tasks and light audit notes | Independent audit verdict |
| `auditor` | Independent pre-implementation audit | Tasks, code changes, code review |
| implementer | Scoped changes, tests, real-file manifest | Independent gates or external authority |
| `product-designer` after UI implementation | Real-browser design-system and approved-spec conformance verdict | Code fixes, code review, QA substitution |
| `qa` | Acceptance-mapped runtime evidence | Fixes or code-review substitution |
| `code-reviewer` | Independent code review of the exact diff or commit | Fixes, plan audit, runtime QA |
| docs skills | Durable docs update or no-impact record | Review/QA substitution |

Hand back a failed artifact to its owner. Return failed post-build design conformance to the implementer, then rerun the affected review on the new implementation identity. Do not silently let one specialist absorb another's independence contract.

Use the [clarification policy](../../spec-driven-delivery/references/clarification-policy.md) for decisions. For independent code review, use the [same requirements for either reviewer](../../spec-driven-delivery/references/quality-gates.md#independent-code-review).

Specialists return their results to the caller. The caller handles tracking, Git, and publication.
