---
name: multi-agent-delivery
description: Route one already-selected delivery workflow through planner, PM, PD, Staff Engineer, tasker, auditor, implementer, code-reviewer, QA, and documentation specialists. Use for explicit specialist handoffs; never use it to choose a workflow mode, select Linear work, or expand caller authority.
---

# Multi-Agent Delivery

Coordinate the shared specialist set for the entry policy that invoked you. This skill is a handoff primitive, not a fourth delivery entry.

## Caller contract

Require an active `$goal-to-delivery`, `$spec-driven-delivery`, or `$linear-delivery-loop` policy plus one registered work descriptor or explicitly selected historical artifact folder. Read the canonical protocol under `../goal-to-delivery/references/`, especially `delivery-stages.md`, `design-gates.md`, `artifact-contract.md`, and `quality-gates.md`.

Do not choose or change the workflow policy. Do not select queue work, infer autonomous mode from a label, auto-advance a manual caller, or expand Git/tracking/provider authority. The caller decides which applicable stages may run and when to stop.

## Shared handoff order

1. `planner` discovers context, writes the plan, and coordinates the clarification record.
2. `product-designer` writes the design spec when `design-gates.md` requires one and records binding design-system sources.
3. `tasker` creates execution-ready tasks.
4. Independent `auditor` judges plan/task readiness before implementation.
5. Matching implementer(s) produce scoped code/artifacts, tests, a real-file manifest, and the affected UI evidence matrix.
6. For changed rendered UI or interaction, `product-designer` performs the required real-browser design conformance review against the exact implementation identity.
7. `code-reviewer` inspects the exact implementation diff/head and current design-review result when applicable.
8. `qa` verifies real behavior and local repository gates without substituting for design review.
9. `$docs-as-code`, with `$luchdom-docs` where applicable, updates durable documentation or records no impact.

At the point a question arises, consult `product-manager` for product/AC decisions or `staff-engineer` for technical decisions under the canonical [clarification policy](../goal-to-delivery/references/clarification-policy.md). Include PD for experience and benchmark work and PM/PD/Staff Engineer together when feasibility affects the product direction. Request PRDs, engineering documents, staff code reviews, or PM acceptance evaluations only when the user or work needs that output; these consultations are not extra mandatory gates. PM evaluation uses the exact implementation/requirements and current QA/design evidence, and any unresolved required AC remains a completion blocker.

Loop a failed audit to its named artifact owner. During implementation, return an uncovered decision through this consultation route before coding that decision; PD owns any resulting design revision. Loop scoped design-review, code-review, or QA defects to an implementer only when the caller still grants implementation authority and its retry policy permits it. PM and Staff Engineer return decisions, docs, or findings; they do not implement fixes. Never let product-designer, code-reviewer, or QA fix code in place.

Use the exact `artifactFolder` recorded by the active work descriptor/registry for every handoff. Do not reconstruct it from a root literal or select it by recency or a similar slug. New/current registered work resolves under `.ai/work`; an exactly registered legacy workflow continues in its exact registered folder. Explicitly supplied unregistered or tracked historical artifacts are read-only fallback; never adopt, migrate, or rewrite them.

Read [handoff-order.md](./references/handoff-order.md) for role boundaries and [output-contracts.md](./references/output-contracts.md) for handoff prerequisites.
