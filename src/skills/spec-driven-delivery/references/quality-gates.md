# Quality gates

Use the repository's local commands and collect enough evidence to check each acceptance criterion. Run the required local validation even when hosted checks pass.

## Critical workflows

Apply these checks when work adds or materially changes a workflow whose failure can block an essential user task, compromise access or data, affect billing, or require operator recovery. Reuse existing telemetry and admin tools where they meet the need.

In `plan`, name each affected workflow and include the applicable checks in its acceptance criteria. Give a reason when a check does not apply.

- **Telemetry.** Name the product events, logs, metrics, or traces that show success and help diagnose failure. Specify how to identify the environment and deployed version. Use a request or job ID to link related events, logs, and traces where needed. Document how agents query redacted data with scoped read-only access.
- **Admin operations.** When the workflow needs operator inspection or recovery, specify a documented API or command-line interface (CLI) for the supported operations. Define permissions, machine-readable results, and how to check the status of background work. Reuse the same application operation behind any admin screen. Define audit records for writes and safe retry behavior where relevant.
- **End-to-end verification.** Plan a success case and a representative failure through a real entry point with isolated test data. Include recovery when the workflow supports it. Specify the expected application state and telemetry for each case.

Carry the acceptance checks into `task` and `qa`. In QA, run the planned cases using the agent's tools and test identities that match the permission scopes in the plan. Query the emitted telemetry to diagnose the failure. Exercise the applicable admin API or CLI. Verify the expected application state and signals for each case. For writes, check that unauthorized calls fail and verify the audit record. Check retry behavior where relevant.

## Audit before implementation

Assign an independent Staff Engineer when work is high risk, ambiguous, unusually large, or touches security, tenancy, billing, or migrations. Apply stricter audit rules from the caller or repository. An assigned `auditor` uses the same [audit checklist](../../task-audit-breakdown/references/audit-checklist.md). Small routine work can use an inline plan and task breakdown.

The auditor reads the requirements, plan, tasks and applicable design directly from the registered work. Record findings, the owner of each correction and a `PASS` or `FAIL` in the dated `*-audit.md`. Any P1 or P2 finding requires a `FAIL`. After corrections, record a fresh verdict before implementation.

## Verify the implementation

1. Run focused tests for the changed area.
2. Update durable docs before recording the target for independent checks.
3. Have QA verify changed UI or interaction against the [design gates](design-gates.md). Exercise the real entry points for behavioral acceptance criteria. Applicable design and behavioral checks must both pass.
4. Complete one independent code review before publishing code or finishing automatic code delivery. Review the exact diff or commit with the applicable QA and design results.
5. Record any product acceptance the caller or repository requires for the same target.
6. Before merge, verify that the PR head passed the standard local validation command and all applicable gates. Reuse results for that head.

An integration may allow an interim checkpoint before review. Require the caller's explicit grant for that checkpoint and verify all applicable checks before reporting completion.

## Independent code review

Assign `staff-engineer` to the independent code review. The reviewer must be independent of the implementation and material decisions under review. A Staff Engineer who proposed the chosen architecture, authored the plan under audit, or contributed code returns that gate to the caller for another independent Staff Engineer. A read-only readiness audit alone does not make its author the implementer. If no independent engineer is available, record the open gate.

Inspect the exact diff, affected callers and tests. Record the target and base, findings with file and line references and impact, test gaps, and a `PASS` or `FAIL` verdict in the dated `*-code-review.md` in the registered `artifactFolder`. A P1 or P2 finding requires a `FAIL`. A required design or QA result must pass for the reviewed target. If the target changes, rerun the affected checks and review before claiming completion.

## Evidence and failures

Record the exact commands, results, and any unverified acceptance criteria. Follow the [artifact contract](../../../tool-instructions/shared/artifact-contract.md) for storage. Leave a required gate open if its evidence is missing or a run limit prevents verification. Keep credentials and customer data out of evidence and logs.
