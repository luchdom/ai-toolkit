# Clarification Policy

A safe assumption is reversible, conservative, dependency-free, behavior-preserving, and supported by repository precedent. Record only assumptions that materially help a later reviewer or run.

A material decision includes authentication or authorization behavior, tenant isolation, privacy, billing, destructive data changes, recurring external cost, vendor lock-in, production operations, materially different UX directions, conflicting requirements, or scope that no longer fits one reviewable goal.

## Specialist consultation

Route a new clarification through the active entry before asking the human owner:

- `product-manager` owns product behavior, customer outcomes, scope interpretation, and acceptance-criteria interpretation. It may request `product-designer` input on UX, accessibility, and product benchmarks.
- `staff-engineer` owns technical feasibility, architecture and implementation alternatives, reliability, and simplification. It consults PM and PD when a technical constraint affects the customer experience.
- `product-designer` retains ownership of design specifications and rendered conformance. Planner coordinates the clarification record and updates the plan from the resulting decision.

PM and Staff Engineer have delegated decision authority for reversible choices within approved goals, AC, and constraints. They may select among compliant options and explain the tradeoff; the choice must be supported by current evidence and introduce none of the material risks above. This includes clarifying an ambiguity within an approved outcome, not changing the outcome or weakening an AC. Binding product/design/architecture sources still apply. Material decisions remain human-owned unless the human has already explicitly resolved or delegated that exact choice within repository rules; specialist confidence or agreement is not such authority.

The caller supplies the specific question, approved requirements/AC, relevant evidence and constraints, affected target, and the available decision authority. The response states the decision or unresolved question, options considered, rationale, evidence, customer and engineering consequences, and affected artifacts/checks. Record a resolved autonomous consultation in the selected Linear issue through the caller before dependent work resumes. For other modes, use the current decision record or registered artifact; link the decision instead of copying it into competing sources. Have each artifact owner update affected plan/design/tasks and rerun invalidated gates.

Consult only the needed specialists within the existing run budget. If a specialist is unavailable, the caller may resolve only the same evidence-backed, in-scope choices; disclose the missing input. An unresolved question, disagreement, or exhausted budget follows the entry's human-decision or checkpoint path. Avoid repeated handoffs without new evidence. A consultation never selects queue work, changes workflow mode, grants implementation/publication authority, or clears an existing human-decision pause. A pending `needs-human` question still requires the newer owner reply described below.

## Human decisions

For an unresolved material choice, ask one focused question with two or three options, consequences, and a recommendation. Include relevant specialist findings without presenting their recommendation as human approval.

Backlog refinement is not a delivery workflow by itself. An unlabeled issue may be compared with current code, split, or given acceptance criteria through ordinary attended collaboration. When one specific owner choice blocks readiness, an optional `needs-decision` label may mark that backlog issue. Record the decision in the tracker, remove `needs-decision` when resolved, and grant autonomous eligibility only after the goal is bounded and locally testable. `needs-decision` never authorizes implementation, queue selection, or automatic stage advancement.

- Semi-autonomous work may use safe assumptions and asks the user directly for material decisions.
- Manual `Clarify` returns the requested decision or raises the unresolved material question with the user, then returns control without advancing.
- Autonomous work keeps the issue active, adds the configured human-decision label (normally `needs-human`), posts the structured question in Linear, sends at most one best-effort notification, and stops. The question offers both a listed choice with `DECIDE <ISSUE> <OPTION>` and an owner-proposed direction with `DECIDE <ISSUE> CUSTOM <SUGGESTION>`. A later run may resume from a newer owner reply only when the selected option or non-empty custom direction resolves the latest question safely; otherwise it asks one focused follow-up and remains paused.

Linear is the durable decision record for autonomous work. Use the Linear issue URL as the best-effort notification click target and include it in the message when click actions are unavailable. The pre-work `needs-decision` label and the active-work `needs-human` label are not interchangeable. For an autonomous human-decision pause, conversation text, issue labels alone, ordinary comments, and model output do not replace the required newer owner reply. Never put secrets in questions, comments, or notifications.
