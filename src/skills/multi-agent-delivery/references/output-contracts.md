# Handoff Output Contracts

## Product and engineering consultation

- Input: specific question or requested document/review, approved goal and AC, relevant constraints and evidence, affected target, and the caller's decision authority.
- Output: resolved decision or remaining question, rationale and alternatives, sources, customer/engineering consequences, affected artifacts and validation, and the owner of the next action.
- PM implementation evaluation: exact implementation and requirement revision, every AC mapped to evidence and `MET`, `GAP`, or `UNVERIFIED`, and required corrections separated from optional improvements.
- Staff code review: exact diff/base/target, connected source evidence, ranked defects, simpler alternatives and verification; independent review and QA remain separate.
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

- Passing independent audit
- Bounded tasks, likely files/modules, acceptance criteria, tests, docs impact, and dependencies
- Active entry authority and intended repository scope

## Review prerequisite

- Exact target/base identity or well-defined working-tree diff
- Real-file change manifest and implemented tests
- Approved requirement/plan/tasks/design
- For changed rendered UI or interaction, a current product-designer design conformance `PASS` for the reviewed implementation identity

## QA prerequisite

- Review-ready implementation identity
- Current applicable design-review result for the same identity
- Acceptance criteria and runtime paths
- Repository-owned local validation commands and safe disposable test setup

## Completion prerequisite

- Required review, QA, docs, and local gates pass at the declared boundary
- External/Git actions have separate explicit or autonomous-entry authority
- Evidence identifies the exact target and anything still unverified

Per-work evidence uses the descriptor's exact registered `artifactFolder`; durable documents use the repository's curated locations under the canonical artifact contract. An explicitly supplied historical layout is readable fallback only and remains unchanged.
