# Quality gates

Use the repository's local commands and collect enough evidence to check each acceptance criterion. Run the required local validation even when hosted checks pass.

## Audit before implementation

Use an independent auditor when work is high risk, ambiguous, unusually large, or touches security, tenancy, billing, or migrations. Small routine work can use an inline plan and task breakdown.

## Verify the implementation

1. Run focused tests for the changed area.
2. For changed rendered UI or interaction, obtain a current product-designer `PASS` using the [design gates](./design-gates.md).
3. Run QA for behavioral acceptance criteria. Exercise the real HTTP, browser, CLI, or other runtime path and record the result.
4. Complete one independent code review for automatic code delivery. Review the exact diff or commit with the applicable QA and design results.
5. Update durable docs when behavior, architecture, setup, or operations changed.
6. Before merge, verify that the PR head passed the standard local validation command and all applicable gates. Reuse results for that head.

## Independent code review

Use `code-reviewer` by default. When `staff-engineer` reviews, choose one who was independent of the decisions and implementation under review. Apply the same review requirements to either role.

Record the target and base, findings with file references and impact, and a `PASS` or `FAIL` verdict. A P1 or P2 finding requires a `FAIL`. A required design or QA result must pass for the reviewed target. If the target changes, rerun the affected checks and review before claiming completion.

## Evidence and failures

Record the exact commands, results, and any unverified acceptance criteria. Follow the [artifact contract](../../../tool-instructions/shared/artifact-contract.md) for storage. Leave a required gate open if its evidence is missing or a run limit prevents verification. Keep credentials and customer data out of evidence and logs.
