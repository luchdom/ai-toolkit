# Clarification policy

Use a safe assumption when repository precedent supports it, it is easy to reverse, and it preserves behavior and dependencies. Record assumptions that matter to a reviewer or a later run.

A material decision can affect authentication, authorization, tenant isolation, privacy, billing, destructive data changes, recurring cost, vendor lock-in, production operations, or user experience. Conflicting requirements and scope changes beyond the approved goal also require a decision.

## Specialist consultation

Use the specialist who can answer the question.

- `product-manager` handles product goals, customer outcomes, product behavior, and interpretation of scope and acceptance criteria.
- `product-designer` handles UI, accessibility, interaction, and design decisions. The design specification and rendered conformance review belong to this role.
- `staff-engineer` handles feasibility, architecture, reliability, and implementation choices. Include product or design input when a technical constraint affects user experience.

Specialists may resolve reversible choices within their role when supported by current evidence and consistent with the approved goal, acceptance criteria, and binding sources. The human owner decides material choices unless they explicitly delegated the specific decision and repository rules allow it. A required design spec or conformance review still needs product-designer input.

Give the specialist the question, approved requirements, context, and decision authority. Ask for the decision or remaining question, the evidence, and any effect on plans, design, tasks, or checks. Use only the specialists needed for that decision. If one is unavailable, the caller may apply the same standard for a reversible choice and record the missing input.

Record the decision before continuing. Update affected plans, designs, tasks, and checks. For a Linear loop run, return the decision to the loop so it can record it in the issue. For other runs, use the existing decision record or shared delivery evidence.

## Human decisions

When a material choice remains open, give the caller one focused question with two or three options, their consequences, and a recommendation. The caller uses its decision process and pauses dependent work until the owner resolves the question.
