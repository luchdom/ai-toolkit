# Agent Instructions

> Adapt this template to the actual repository. The Taskboard paths and npm commands are illustrative; keep only valid links and commands for this project. Remove template notes and example-only wording after adaptation.

## 01 Purpose

**Example:** this repository contains Taskboard, a personal task app. These instructions connect its product requirements, UI rules, architecture, and local checks.

## 02 Before You Start

**Minimum:** maintain a direct map to every applicable foundation, using existing equivalents and valid relative paths. For projects without a UI, replace the design rows with a short applicability reason.

| Source | Actual project link | Read / use when |
|---|---|---|
| Product brief | [PRD](docs/PRD.md) | Planning behavior, scope, journeys, and acceptance |
| UI rules | [Design system](docs/DESIGN_SYSTEM.md) | Designing or changing the UI; follow linked tokens/components |
| Technical structure | [Architecture](docs/ARCHITECTURE.md) | Adding files, dependencies, persistence, or boundaries |
| Working UI catalogue | [Example source](src/app/design-system/page.tsx) | Inspecting component variants/interactions; keep this row only when the source exists |

**Example catalogue access:** `/design-system` on the existing development server, started with the verified dev command below. Replace with the real source, URL, command, and access conditions. If no catalogue exists, record its proposal in the design-system doc instead of adding a broken link here.

- Check nearby instructions and existing patterns for the area being changed.
- Open the working catalogue for shared UI work when one exists; check the real implementation as well as the written guide.

## 03 General Rules

- Keep behavior within the agreed PRD scope and acceptance criteria; surface unresolved product decisions.
- Reuse the documented components, tokens, and technical boundaries before creating alternatives.
- Update the owning docs and working examples when an authorized change affects their rules.

**Minimum:** retain only project-specific rules that affect decisions. Keep shared workflow policy linked to its canonical source.

## 04 Code Guidelines

**Example:** shared UI belongs in the existing component library. The internal catalogue imports those components and shared tokens. Formatting/naming follow the repository's lint/formatter configuration and nearby patterns.

**Minimum:** link actual configuration, any code-style guide, and representative files for important conventions that tooling does not enforce.

## 05 Security

**Example:** catalogue fixtures use synthetic local data. They do not contact live services or bypass existing access controls. Follow the architecture's data/secret-handling boundaries.

**Minimum:** record project-specific authorization, tenancy, data, or secret-handling rules, with a link to the detailed owner.

## 06 Useful Commands

| Task | Command and working directory | Verification |
|---|---|---|
| Install | Example: `npm ci` from repository root | Unverified example; confirm the actual package manager/lockfile |
| Run / catalogue | Example: `npm run dev` from root, then open `/design-system` | Unverified example; confirm script, URL, and access boundary |
| Build | Example: `npm run build` from root | Unverified example; retain only if defined |
| Test | Example: `npm test` from root | Unverified example; use the actual unit/browser commands |
| Lint | Example: `npm run lint` from root | Unverified example; use the repository-owned check |

**Minimum:** give actual applicable commands and working directories; label commands unverified until run safely. Include the working catalogue's startup instructions when it exists.

## 07 When Unsure

- Follow the docs map above and inspect the nearest implementation before assuming behavior.
- Treat `Proposal` and `Decision needed` sections as unresolved direction; clarify material choices with the owner.
- Report code/docs/catalogue conflicts with source paths and continue independent work where possible.

**Minimum:** identify where evidence lives and which product, design, or technical decisions require owner input. Existing project-specific tool instructions should link this root map using paths relative to their own files.
