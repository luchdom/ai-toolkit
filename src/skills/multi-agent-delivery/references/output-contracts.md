# Handoff requirements

## Product and engineering consultation

- Input includes the question, approved goal and acceptance criteria, target, evidence, and decision authority.
- Output: resolved decision or remaining question, rationale and alternatives, sources, customer/engineering consequences, affected artifacts and validation, and the owner of the next action.
- For product acceptance, match each criterion to evidence for the exact revision and mark it `MET`, `GAP`, or `UNVERIFIED`. Identify required corrections.
- A Staff Engineer performs the readiness audit and the independent code review as separate assignments. Check [reviewer independence](../../spec-driven-delivery/references/quality-gates.md#independent-code-review) for the material under each review.
- Requested PRDs, RFCs, ADRs, and diagrams use repository conventions and distinguish proposals from authorized decisions. Routine answers may be inline; substantial per-work evidence uses the registered artifact contract.

Consultations follow the canonical clarification policy. A missing specialist or unresolved choice is reported to the caller; it never creates approval or clears a human-decision pause.

## Tasking prerequisite

- Concrete plan with exact sources
- Material decisions resolved or explicitly paused
- Frontend/UI classification with exact binding design sources
- Design spec when `design-gates.md` requires one, otherwise a mechanical-change reason tied to a binding source
- Required post-implementation design-conformance path for changed rendered UI or interaction
- Acceptance and local validation strategy

## Implementation prerequisite

- Passing independent audit when required
- Bounded tasks, likely files/modules, acceptance criteria, tests, docs impact, and dependencies
- Active entry authority and intended repository scope

## QA prerequisite

- Review-ready implementation identity
- Binding sources and applicable design spec for changed UI. QA writes the design-review verdict for that identity before concluding behavioral QA. One observed browser run can support both reports.
- Acceptance criteria and runtime paths
- Repository-owned local validation commands and safe disposable test setup

## Review prerequisite

- Exact target and base or well-defined working-tree diff
- Changed files, implemented tests, and approved requirements, plans, tasks, and design
- Applicable passing QA and design conformance results for the reviewed target

## Completion prerequisite

- Required review, QA, docs, and local gates pass at the declared boundary
- External/Git actions have separate explicit or autonomous-entry authority
- Evidence identifies the exact target and anything still unverified
- Record product acceptance for that target when the caller or repository requires it.

Use the [artifact contract](../../../tool-instructions/shared/artifact-contract.md) for delivery evidence and durable docs.
