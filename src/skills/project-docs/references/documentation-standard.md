# Project Documentation Standard

Use a small, maintained brief that explains product intent, UI rules, technical structure, and how agents work in the repository. This standard adapts the four-file structure in Max Johnson's *The 4 Files That Make AI Build Your App Properly*, with conditional additions for acceptance, accessibility, security, and operation. The bundled templates are self-contained; the original PDF is not a runtime dependency.

## Placement and ownership

For a new project, start here:

```text
project/
├── AGENTS.md
└── docs/
    ├── PRD.md
    ├── DESIGN_SYSTEM.md
    └── ARCHITECTURE.md
```

| Foundation | Owns | Consult before |
|---|---|---|
| `docs/PRD.md` | Users, problem, goal, scope, success, journeys, acceptance | Product planning or changing behavior |
| `docs/DESIGN_SYSTEM.md` | Brand direction, tokens, typography, spacing, components, icons, responsive behavior, UI states, accessibility | Designing or changing a UI |
| `docs/ARCHITECTURE.md` | System, stack, folders, boundaries, data flow, growth constraints, security, operations | Adding files, dependencies, storage, or service boundaries |
| Root `AGENTS.md` | Actual docs map, task-based reading, commands, project rules, uncertainty handling | Working in the repository |

These are defaults for new documentation. Equivalent existing files, a design-system directory, or a repository-defined docs root can already satisfy them. Record actual links in `AGENTS.md`; keep one owner for each concern. Recommend a move only when the current location causes a concrete discovery or ownership problem, and carry out moves only within an authorized docs scope, updating inbound links. Split long documents into linked sections when that improves use.

Use root `AGENTS.md` as the shared project entry point, with scoped instructions where a monorepo needs them. Project documentation setup does not create a tool-specific wrapper. Preserve existing tool files and their custom rules when encountered.

For a monorepo, map shared foundations and project-specific overrides; avoid duplicating an entire shared PRD or design system into every package. For a service, library, CLI, or other project without a UI, mark the design system `not applicable` in the map with a short reason. API/CLI behavior belongs in product and technical docs.

## Evidence and decisions

Separate these states at the section or decision level:

- **Implemented:** supported by a source/configuration path or an executed check.
- **Approved direction:** an explicit owner decision or a clearly approved project specification; cite that source.
- **Proposal:** a recommendation awaiting a decision.
- **Decision needed:** a specific unresolved question, with its impact.

Record document status, scope, and evidence links near the top of the three foundation docs. Use project roles for ownership when known. Cite the owner decision or source rather than adding an unsupported approval date. A draft can be useful, but unresolved proposals are not binding requirements. Code/docs conflicts need an explicit finding; confirm intent before changing either to match the other.

Use the actual stack, conventions, design tokens, and commands. The templates prescribe questions and headings, not a framework, palette, font, database, or package manager. Goals and success metrics need owner evidence; implementation cannot establish them by itself. Reference source token/configuration files as the authoritative values when available, rather than maintaining a competing catalogue.

## Minimum coverage and examples

The bundled templates include populated fictional examples to show the expected specificity. Their **Minimum** notes are authoring criteria: replace examples with project facts or explicit proposals, supply that coverage, and remove template instructions from the project output. Minimum coverage is about usable content, not copying headings or a sample stack.

| Foundation | Minimum usable content |
|---|---|
| PRD | Named product/users/problem, a measurable goal, core scope and exclusions, success targets with measurement methods, acceptance for each core journey, constraints, and explicit open decisions |
| Design system for a UI | Exact or resolvable semantic colour roles; typography with size/weight/line height; spacing/radius scales with usage; actual component variants/states and behavior; icon and responsive rules; accessibility requirements/checks; authoritative source links; working-catalogue status |
| Architecture | System boundaries and entry points, stack responsibilities/evidence, actual directory ownership, at least one end-to-end flow including failures, relevant data/security/operational constraints, and material decisions |
| Agent instructions | Valid direct links to the applicable foundations, task-based reading rules, actual commands/directories and verification state, project conventions/security rules, and working-catalogue source/access instructions when one exists |

For a new UI, an example palette/type scale can be a clearly labeled proposal rather than an unexplained blank. For an existing UI, inspect its tokens and components first. Mark genuinely inapplicable coverage with a reason and unresolved coverage as a decision; do not call the set ready while material questions are disguised as filled examples.

## Working design system

For UI projects, assess a runnable component workshop, internal page, or HTML catalogue alongside the Markdown guide. Reuse an existing one where available; follow [the working design-system guide](working-design-system.md) for stack-aware placement, minimum functional demonstrations, access, and browser verification. Shared tokens/components must drive both the catalogue and the application. A docs-only scope can finish with a concrete implementation proposal; catalogue implementation follows the authorized UI scope and its design/verification gates.

## Tool instruction routing

Global guidance routes the agent to root `AGENTS.md`. That project file must link the actual PRD, design system, architecture equivalents, and any working catalogue source/access instructions, with a condition for reading each. Maintain this map when documentation edits are in scope. Default filenames in a global rule do not replace these project-specific links.

Existing project-specific tool routers point to this root map, avoiding another copy of the project brief. For example, `.github/copilot-instructions.md` can say `Follow [the project instructions](../AGENTS.md) and their task-specific documentation links.` Resolve relative links from each instruction file's location, including scoped files. Root `AGENTS.md` remains the shared project entry point.

Verify the full route from each relevant project instruction file through the map to the actual documents. For a working catalogue, verify the source link and record the real local URL, startup command, and access boundary. A proposed catalogue is recorded as a proposal in the design-system document, not as a link to a nonexistent page.

## Discovery and suggestions during ordinary work

For substantive planning or implementation, locate the foundations relevant to the task and read only the needed sections. Lightweight discovery is enough when coverage is clear. Load `$project-docs-review` when a relevant foundation is missing, misplaced, stale, or conflicting, or the user requests an assessment.

Offer a specific next action such as: "The existing architecture guide covers the service, but product scope is undocumented. Use `$project-docs` to draft `docs/PRD.md` from the known requirements and refine the open decisions."

Make the suggestion once per project context unless the user asks again or the gap materially changes. Respect earlier declines. Continue authorized work when the gap is nonblocking. Missing foundation files alone are not a reason to stop a small fix or generate an unsolicited documentation suite; ask only when an unresolved decision prevents the requested work.

An explicit create/refine request authorizes the selected documentation edits. An assessment request produces findings and suggestions; it does not move or rewrite files. Preserve repository-specific rules and the caller's active delivery stage.

## Conditional extensions

Add a section to its current owner first. Create a separate page when readers need a substantial independent reference, not simply because a template exists.

| Concern | Add when | Typical owner and content |
|---|---|---|
| Human onboarding | Setup or navigation is hard to find | `README.md`: purpose, quick start, verified commands, docs links |
| Code conventions | Important naming or organization rules are not enforced or obvious from the code | Existing contributing guide or `docs/CODE_STYLE.md`: exceptions and representative examples; link formatter/linter config |
| Security | Auth, tenancy, sensitive data, or threat boundaries need explanation | Architecture section or `docs/SECURITY.md`: trust, permissions, data lifecycle, secrets, threat mitigations; preserve root `SECURITY.md` for disclosure policy if present |
| Testing and acceptance | Test responsibilities or required checks need a stable guide | `docs/TESTING.md`: risk-based coverage, commands, fixtures, local versus external checks; PRD owns user acceptance |
| Operations | Deployment, recovery, or monitoring needs a runbook | Existing operations docs: environments, configuration names, deployment, observability, rollback, recovery |
| Durable decisions | An architectural choice has meaningful alternatives or consequences | Existing ADR convention or `docs/decisions/`: context, decision, status, consequences, supersession |
| Domain vocabulary | Ambiguous terms cross features or teams | Existing glossary or `docs/GLOSSARY.md`: terms, boundaries, links |

Keep secrets and personal data out of documentation; configuration examples name variables and use synthetic values. Refer to external providers with verified links when their current behavior matters.

## Maintenance and completion

Product changes update the PRD; UI rules update the design system and its source tokens/working catalogue within the active scope; changes to structure, stack, or boundaries update architecture. Refresh `AGENTS.md` and existing tool-router pointers when paths, commands, or project rules change. Keep human navigation linked from the README or established index. Use `$docs-as-code` for change-related maintenance and `$luchdom-docs` for Luchdom's additional ownership map. Record catalogue implementation work that is outside the docs stage as an exact follow-up.

Store reusable foundations in curated docs. Keep feature plans, reviews, and QA evidence in the active workflow's exact registered `artifactFolder`; a project PRD or design system does not replace those workflow artifacts or design gates.

A document set is ready for use when each applicable foundation has a clear owner/path, significant claims have evidence or an explicit decision state, links resolve, available Markdown/docs checks pass, and no material decision is presented as settled while still open. State gaps and unrun checks precisely.
