---
name: qa-verification
description: Independently verify implemented work with repository-owned local commands and real runtime behavior mapped to acceptance criteria. Use after implementation for QA evidence; report defects and unverified work without fixing production code or substituting for code review.
---

# QA Verification

Verify the exact implementation target against observable acceptance criteria. When the work changes rendered UI or interaction, use the [design gates](../spec-driven-delivery/references/design-gates.md) and [UI Review Spec](../ui-review-spec/SKILL.md) to record your independent design conformance verdict first. A shared browser run can support both the design and behavior results.

## Discover the local gate

- Read `AGENTS.md`, `README`, relevant docs, and manifests/scripts to discover the repository's real build, test, lint, type, documentation, and aggregate validation commands.
- Derive commands from the repository. Never hardcode machine paths, ports, URLs, tokens, or environment identifiers.
- Identify the exact working tree or SHA under test and fail on ambiguity.

## Exercise behavior

1. Run the smallest relevant checks first, then the full repository-required local aggregate.
2. Map every acceptance criterion to a concrete observed result.
3. Use real HTTP/browser/CLI/user flows for behavioral criteria. Mock only true boundaries.
4. Use environment guards, non-default values, isolated disposable data, bounded readiness predicates, and verified cleanup. Avoid fixed sleeps.
5. Run the applicable [critical workflow checks](../spec-driven-delivery/references/quality-gates.md#critical-workflows) using the planned tools and test identities.
6. Treat skipped required checks, cleanup failures, identity mismatch, or an unexercised behavior path as incomplete verification.

## Report, do not fix

Write the dated `*-qa.md` in the exact `artifactFolder` recorded by the active work descriptor/registry with target identity, commands/results, pass/fail counts, acceptance mapping, cleanup evidence, blockers, and residual risk. Follow the [artifact contract](../../tool-instructions/shared/artifact-contract.md).

QA does not implement fixes, perform the pre-implementation audit, or replace exact-diff code review. Route defects to the caller for a separately authorized implementation pass. Do not mutate Linear or perform Git/provider actions.

Read [qa-checklist.md](./references/qa-checklist.md) before reporting and the canonical quality contract in `../spec-driven-delivery/references/quality-gates.md`.
