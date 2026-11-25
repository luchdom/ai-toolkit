# Clarification policy

Use a safe assumption when repository precedent supports it, it is easy to reverse, and it preserves behavior and dependencies. Record assumptions that matter to a reviewer or a later run.

A material decision can affect authentication, authorization, tenant isolation, privacy, billing, destructive data changes, recurring cost, vendor lock-in, production operations, or user experience. Conflicting requirements and scope changes beyond the approved goal also require a decision.

## Specialist consultation

Use the specialist who can answer the question.

- `product-manager` owns the customer outcome, scope, user journey, interaction expectations, accessibility needs and product acceptance criteria.
- The implementer translates those expectations into a design specification using the product components and tokens. The QA Engineer independently checks the rendered implementation against the binding sources.
- `staff-engineer` handles feasibility, architecture, reliability, and implementation choices. Consult the Product Manager and the implementer when a technical constraint affects the user experience.

Specialists may resolve reversible choices within their role when supported by current evidence and consistent with the approved goal, acceptance criteria, and binding sources. The human owner decides material choices unless they explicitly delegated the specific decision and repository rules allow it. Keep the [required design evidence](design-gates.md) and its independent verification.

Give the specialist the question, approved requirements, context, and decision authority. Ask for the decision or remaining question, the evidence, and any effect on plans, design, tasks, or checks. Use only the specialists needed for that decision. If one is unavailable, the caller may apply the same standard for a reversible choice and record the missing input.

Record the decision before continuing. Update affected plans, designs, tasks, and checks. For dispatched work, return the question or decision to the same caller with its assignment and decision references. For direct work, use the existing decision record or shared delivery evidence.

## Human decisions

When a material choice remains open, give the caller one focused question with two or three options, their consequences, and a recommendation. The caller uses its decision process and pauses dependent work until the owner resolves the question.
