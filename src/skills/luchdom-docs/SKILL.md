---
name: luchdom-docs
description: Apply Luchdom repository-specific documentation ownership when architecture, workflow, setup, tooling, validation, tracking, or operations change. Use with docs-as-code to update the nearest durable source without duplicating the canonical shared delivery protocol.
---

# Luchdom Docs

Apply `$docs-as-code` with the Luchdom documentation ownership map.

1. Read repository `AGENTS.md`, `README.md`, and the smallest relevant curated docs set.
2. Inspect the implementation and approved artifacts using the [artifact contract](../../tool-instructions/shared/artifact-contract.md).
3. Use [doc-targets.md](./references/doc-targets.md) to select the existing source of truth.
4. Update that source and remove contradictions instead of adding another explanation.
5. Link to the [shared delivery rules](../../tool-instructions/shared/delivery-workflow.md) for workflow policy. Keep local commands and requirements in the repository's docs.
6. Run the available local docs/drift checks and report exact pages, checks, and gaps.

Do not put reusable guidance only in the per-work artifact folder. Do not add full workflow records to curated navigation. Prefer concise task-oriented how-tos with prerequisites, steps, verification, rollback, and troubleshooting.

If documentation and implementation disagree and the correct source cannot be proven, report the conflict and fail the docs stage rather than choosing silently.
