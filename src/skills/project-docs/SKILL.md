---
name: project-docs
description: Create or refine a repository's PRD, design system, architecture, and root AGENTS.md using repo evidence and focused questions. Use when establishing project documentation or improving those foundations; use project-docs-review for assessment without edits.
---

# Project Docs

Turn a project idea or existing repository into useful, agreed project documentation. A request to create or refine docs authorizes scoped documentation edits, not changes to the application.

```text
$project-docs
$project-docs refine the design system
$project-docs create the missing foundations for this repository
```

## Discover

Read [the documentation standard](references/documentation-standard.md), repository instructions, README, existing product/design/architecture docs, and the source/configuration needed to verify the requested scope. Identify the selected project and any monorepo boundaries before writing.

Produce a short map of each foundation to its actual path, coverage, and evidence. Reuse existing equivalents and their headings when established; use the templates below for new documents. Resolve competing owners before adding another source of truth. Root `AGENTS.md` is the shared project entry point.

## Refine

Work in dependency order: product intent, visual/interaction decisions where applicable, technical structure, then agent routing. For a targeted request, refine only that document and necessary links or contradictions in its dependents.

- Derive implemented facts from source files and verified commands. Cite repository paths beside significant claims. Existing behavior is evidence, not proof of the owner's product goals.
- Ask focused questions only for material gaps in users, scope, success, design direction, or technical constraints. Reuse decisions already supplied; continue evidence gathering and independent drafting while answers are pending.
- Present supported options when a decision needs refinement. Keep proposals separate from approved direction and current implementation. A request to draft docs permits the draft; it does not establish approval of invented product or design choices.
- Use the populated template examples to make the desired detail and format concrete. Replace fictional content with repository evidence; for a new project, suitable sample values can be a clearly labeled starting proposal to refine with the owner. Mark material unresolved points as `Decision needed` with their exact question and impact. Keep a document a draft while material decisions remain; finish supported work before returning the remaining questions.

## Write

Read only the templates needed for this invocation. Preserve the PDF's core structure, then adapt the added sections to the repository. Each template includes populated sample values/tables and minimum coverage notes; use those notes as the authoring checklist, then remove the template instructions and replace fictional examples in the project's docs:

| Document | Template | Read when |
|---|---|---|
| `docs/PRD.md` | [PRD](assets/PRD.md) | Establishing users, goals, scope, journeys, and acceptance |
| `docs/DESIGN_SYSTEM.md` | [Design system](assets/DESIGN_SYSTEM.md) | Defining or refining an actual UI |
| `docs/ARCHITECTURE.md` | [Architecture](assets/ARCHITECTURE.md) | Explaining structure, boundaries, and data flow |
| Root `AGENTS.md` | [Agent instructions](assets/AGENTS.md) | Connecting the verified docs, commands, and project rules |

For projects without a UI, record design-system applicability in the docs map instead of manufacturing a palette. Add optional documents only for a concrete need identified in the standard. Replace instructional placeholders with supported content or explicit open decisions; remove inapplicable optional sections.

For UI projects, read [the working design-system guide](references/working-design-system.md). Discover an existing runnable workshop/catalogue or choose a fitting internal route/HTML page. Reuse actual tokens/components and specify the minimum functional demonstrations. Implement it only within an already-authorized UI scope; for docs-only work, document the concrete proposal and remaining implementation. Record actual source, URL, startup command, access boundary, and checks when it exists.

Maintain a direct documentation map in root `AGENTS.md`, including the applicable PRD, design system, architecture, and working catalogue/source access instructions. Update existing project-specific tool routers to point to that map with paths relative to their own files. Keep existing instruction markers and surrounding custom rules intact; add project-specific context outside toolkit-managed blocks. Link shared workflows rather than reproducing them, and link docs from the README or existing human documentation index too.

## Verify and hand back

Check minimum coverage and the document set for conflicting scope, design values, architectural ownership, commands, and links. Follow each project instruction pointer to its actual document; check catalogue pointers/access instructions when applicable. Run the repository's documentation checks and lint every changed Markdown file. Report commands and working interactions as verified only when actually checked; label others unverified. Use `$project-docs-review` for a final coverage and consistency pass.

Return the actual documentation map, files changed, decisions incorporated, checks run, and material open questions. State whether the result is a draft or ready for use; do not call unresolved proposals final. Further owner feedback refines these same documents.
