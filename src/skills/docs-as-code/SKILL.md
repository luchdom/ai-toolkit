---
name: docs-as-code
description: Maintain durable, searchable repository documentation as a distinct delivery stage. Use when implementation or artifact work changes behavior, architecture, setup, operations, workflow, or troubleshooting guidance and the nearest curated docs must be updated or explicitly declared unaffected.
---

# Docs as Code

Own the documentation stage without replacing planning, code review, or runtime QA.

For changes to product scope, UI rules, or technical structure, locate their owners using [the project documentation standard](../project-docs/references/documentation-standard.md). Update the existing PRD, design system, or architecture equivalent when affected, and refresh root `AGENTS.md` links/commands when needed. Use `$project-docs-review` for uncertain coverage and suggest `$project-docs` for missing foundations; keep that suggestion proportional to the change and within the caller's active scope.

Verify project tool instructions still route to the actual docs map. For a working UI catalogue, update its documented source/access instructions when affected and identify any component/token/demo changes belonging to an implementation stage. Keep written UI rules and working examples consistent without claiming out-of-scope code work was completed.

## Contract

1. Read repository instructions and the smallest relevant curated documentation set.
2. Read the approved work artifacts from the exact `artifactFolder` recorded by the active work descriptor/registry and inspect the implemented change; do not infer behavior from the task title alone.
3. Record docs impact as exact pages to update or `none` with a concrete reason.
4. Update the nearest durable source of truth. Prefer an existing page and links over a competing explanation.
5. Verify commands, links, navigation, and any repository documentation gate available locally.
6. Return changed pages, checks performed, and residual gaps. Do not claim code review or behavioral QA.

Use the [artifact contract](../../tool-instructions/shared/artifact-contract.md) to locate the registered work and historical evidence.

Keep evidence separate from durable knowledge:

- Store plans, decisions, task breakdowns, audits, review reports, QA evidence, and completion records in the workflow's exact registered `artifactFolder`.
- Store reusable concepts, how-tos, references, ADRs, runbooks, and troubleshooting under the curated `docs/` tree or repository-defined equivalent.
- Write setting how-tos with prerequisites, steps, verification, rollback, and troubleshooting.
- Link useful evidence; do not add raw run logs or whole workflow folders to primary documentation navigation.
- Keep Linear comments concise and link artifacts rather than copying full documents.

Link to the [shared delivery rules](../../tool-instructions/shared/delivery-workflow.md). Use repository docs for local commands and requirements.

Edit docs only when the caller's active stage and repository authority allow it. A docs-only artifact can finish at the `artifact` boundary after its acceptance and documentation checks pass; never create an empty code change merely to publish evidence.
