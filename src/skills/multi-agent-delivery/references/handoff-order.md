# Specialist roles

The caller entry policy controls advancement and authority throughout.

| Owner | Owns | Must not own |
|---|---|---|
| `planner` | Discovery-backed plan and clarification record | Tasks, audit verdict, implementation |
| `product-manager` | User journeys, UX and acceptance criteria, product decisions, requested PRDs and product acceptance | Code changes, weakening criteria, technical approval |
| `staff-engineer` | Technical advice, requested engineering docs, independent readiness audit, independent review of the exact diff | Implementation, fixes or sign-off on its own material decisions |
| `tasker` | Ordered execution tasks and completeness notes | Independent audit verdict |
| `auditor` when explicitly assigned | Independent pre-implementation audit | Tasks, code changes, code review |
| Implementer | Required UI spec, shared components and tokens, scoped changes, focused tests and changed files | Approval of its own work or publication authority |
| `senior-full-stack-engineer` in OpenBot | The selected issue's plan, clarification, UI spec when needed, task breakdown, implementation and fixes | Queue selection, independent audit, QA or code review |
| `qa` | Independent rendered design conformance and acceptance-mapped runtime results for the same revision | Code fixes, code review or product acceptance |
| docs skills | Durable docs update or no-impact record | Review/QA substitution |

Hand back a failed artifact to its owner. Return failed post-build design conformance to the implementer, then rerun the affected review on the new implementation identity. Do not silently let one specialist absorb another's independence contract.

Use the [clarification policy](../../spec-driven-delivery/references/clarification-policy.md) for decisions. Assign a separate Staff Engineer if prior material involvement would compromise the [independent review](../../spec-driven-delivery/references/quality-gates.md#independent-code-review). In OpenBot, the Product Manager evaluates the user journey after engineering review and returns any unmet criteria before handoff.

Specialists return their results to the caller. The caller handles tracking, Git, and publication.
