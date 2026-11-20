# Frontend and UI design gates

Use these gates for work that changes a rendered screen, user flow, navigation, layout, component choice, interaction, responsive behavior, accessibility behavior, UI state presentation, visual styling, design token, or content hierarchy.

## Binding design sources

Before making a UI decision, identify the applicable repository sources in this order:

1. repository instructions and product-specific design rules;
2. an issue-tied approved design spec or frozen visual reference;
3. the repository design system, theme, tokens, component catalog, and established feature patterns;
4. approved framework or component-library primitives.

Record the exact paths or tools consulted. A stricter repository rule wins. If binding sources conflict and repository precedent does not resolve the conflict, stop for clarification. Do not silently replace an existing design system with personal preference or a new visual direction.

Use a frozen reference as the acceptance standard. Compare the implementation at the same viewport, state, content, and theme. Record any unavoidable deviation.

## Before implementation

The planning owner records whether the work changes rendered UI and whether a design specification is required.

When these gates apply, the caller initializes or resumes the workflow descriptor and its registered `artifactFolder` before the implementer writes a design specification or edits UI code. Use that folder for the spec and later design review.

The implementer writes a design specification with [UI Review Spec](../../ui-review-spec/SKILL.md) when any of these conditions apply.

- a screen, flow, navigation path, layout, component composition, interaction, responsive rule, accessibility behavior, state presentation, visual style, or content hierarchy is added or changed;
- the implementer would need to choose between plausible UI behaviors or visual treatments;
- a new component, primitive, token, pattern, or exception to the existing design system is proposed;
- the available product/design sources are missing, ambiguous, conflicting, or do not cover the requested state;
- the user explicitly requests UI/UX design, review, redesign, fidelity, or design-system alignment.

A mechanical change can proceed without a new spec when a binding source already settles every UI decision. Examples include a specific copy correction in an existing layout or restoring documented behavior. Record the binding source and why it covers the change.

Record the affected user journey, binding source paths, shared components and tokens, responsive layout, accessibility and interaction states, and the criteria QA can observe. The Product Manager resolves product and UX choices within the agreed scope. Take material choices outside that authority to the owner through the caller. Finish the required spec before tasking, audit or implementation.

## During implementation

The implementer reads the recorded design-gate decision, binding design sources, and approved design specification before editing UI code. Implement the specified components and tokens. Do not add one-off styling, a new primitive, or a visual/interaction deviation that the approved artifacts do not authorize.

When a constraint changes the approved design, consult the Product Manager about the user outcome and the Staff Engineer about feasibility under the [clarification policy](clarification-policy.md). Record the agreed revision in a new dated design spec, then update the affected tasks before editing code. Keep previous versions.

Exercise the affected UI in a real browser during implementation when the environment permits it. Return the exact routes, states, themes, and representative viewports needed for conformance review. Keep optional screenshots in disposable evidence storage unless the user or registered workflow explicitly requires another destination.

## After implementation

The independent QA Engineer owns the design conformance review for every change to rendered UI or interaction, including mechanical changes that did not need a new design specification.

The QA Engineer inspects the exact implementation identity in a real browser and compares the affected routes, states, themes, and representative mobile and desktop viewports against the binding design sources and approved specification. The result is a dated `*-design-review.md` with `PASS` or `FAIL`, exact evidence, deviations, and required corrections. Use the base dated name for the first result; if that name already exists, insert deterministic `--02`, `--03`, and later sequences before `-design-review.md`. Never overwrite historical evidence.

Run the affected UI in a real browser. If rendering is unavailable, record the limitation and leave conformance unverified. An unresolved mismatch with a binding design source or approved acceptance criterion produces `FAIL`. Record optional improvements separately.

Any implementation change that affects rendered UI, interaction, responsive or accessibility behavior, or a reviewed state invalidates the previous design-review result. Route a failed result to the implementer, then rerun the affected conformance review. QA can reuse the same browser run for the design and behavioral checks. Record each verdict against its own criteria and link the shared evidence. The Staff Engineer reviews the exact code separately.
