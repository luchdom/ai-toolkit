---
name: refine
description: Pressure-test an early product goal, feature request, or engineering decision with the user and the Product Manager, Staff Engineer, or both. Use for a refinement interview that can end in a Linear issue, PRD, ADR, or RFC.
---

# Refine

Help the user settle one goal or decision before delivery. Use the [clarification policy](../spec-driven-delivery/references/clarification-policy.md) for decision authority and owner questions.

```text
$refine <goal-or-selected-issue> [--with pm|staff|both] [--output linear|prd|adr|rfc]
```

Accept the same choices in plain language. Read any selected issue or proposal and use [Repo Discovery](../repo-discovery/SKILL.md) for the relevant docs, code, and precedents in the selected project. Reuse answers and decisions from earlier turns.

## Choose the specialists

Honor the user's explicit role choice. If it excludes the author of a requested document below, ask which choice to change. For automatic selection, use the scope of the decision and include the requested document's author.

| Choice | Agent | Use for |
|---|---|---|
| `pm` | `product-manager` | Prioritizing customer problems, defining success, or clarifying acceptance when the engineering constraints are settled. |
| `staff` | `staff-engineer` | Architecture, internal refactors, reliability, performance, or migrations that preserve product commitments. |
| `both` | Both agents | Product goals, feature requests, or changes where feasibility, cost, or reliability may change what users get. |

Call the selected agents with the goal, sources, agreed decisions, and remaining questions. Ask each to return the most consequential assumption to test, a recommendation, and its tradeoffs in the conversation. With both, have Staff Engineer test the feasibility of the PM's proposed scope and have the PM assess the customer impact of technical constraints. If delegation is unavailable, apply the role guidance inline and disclose that fallback.

## Run the interview

1. Check the selected issue, repository, or other available evidence for answers. Bring the user decisions that need their knowledge or judgment.
2. Ask one focused question at a time. Start with the highest-impact decision whose prerequisites are settled. Challenge the premise or propose a concrete alternative where it changes the outcome. Use the clarification policy's question format and wait for the user's answer before advancing dependent decisions.
3. Keep one record in the conversation of agreed decisions, assumptions, and open questions. Reuse the selected agents as new answers change the tradeoffs, and combine overlapping questions. If an answer needs a prototype, measurement, or customer research, record the smallest check that would resolve it and keep the decision open.
4. Stop when the decisions support the requested output, progress depends on evidence you cannot gather, or the user ends the interview. Recap what was agreed and flag open decisions with their impact.

The interview draws on [AI Hero's Grill Me](https://www.aihero.dev/skills-grill-me).

## Produce the requested output

If the user leaves the format open, return the decision summary and recommend the lightest suitable artifact. Use the [project documentation standard](../project-docs/references/documentation-standard.md) and repository conventions for document placement, templates, and decision status. Use [the artifact contract](../../tool-instructions/shared/artifact-contract.md) for any evidence that belongs to an active delivery workflow.

| Output | When and how |
|---|---|
| Linear issue | Use for a bounded, testable item of work. Draft the problem, agreed scope, acceptance criteria, and links to owning decisions. Use the project's issue conventions. Create or update the issue through Linear when the user requests that write and the destination is clear. Check for an existing issue before creating one. If the integration is unavailable, return the draft and explain the blocker. |
| Product requirements document (PRD) | Ask `product-manager` to write or update the product requirements. Use the [Project Docs skill](../project-docs/SKILL.md) for its product guidance and template. |
| Architecture decision record (ADR) | Ask `staff-engineer` to record an architectural choice once the appropriate owner has made it. |
| Request for comments (RFC) | Ask `staff-engineer` to document a technical proposal when alternatives or tradeoffs still need review. State what feedback would resolve the choice. |

If there is no selected project or file destination, return a document draft in the conversation. Mark unresolved material questions in drafts. Return the document path, verified issue link, or draft, along with any remaining decisions. A separate delivery request can use the refined result as input.
