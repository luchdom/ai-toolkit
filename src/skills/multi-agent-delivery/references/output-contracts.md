# Handoff requirements

## Product and engineering consultation

- Input: specific question or requested document/review, approved goal and AC, relevant constraints and evidence, affected target, and the caller's decision authority.
- Output: resolved decision or remaining question, rationale and alternatives, sources, customer/engineering consequences, affected artifacts and validation, and the owner of the next action.
- PM implementation evaluation: exact implementation and requirement revision, every AC mapped to evidence and `MET`, `GAP`, or `UNVERIFIED`, and required corrections separated from optional improvements.
- A staff engineer can perform the independent review when they meet the [review requirements](../../spec-driven-delivery/references/quality-gates.md#independent-code-review).
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
- Current applicable design-review result for the same identity
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

Per-work evidence uses the descriptor's exact registered `artifactFolder`; durable documents use the repository's curated locations under the canonical artifact contract. An explicitly supplied historical layout is readable fallback only and remains unchanged.
