# Twelve-Factor for agentic development

The Twelve-Factor App describes how to build and operate deployable services. This guide adapts each factor for teams whose agents also need to start the app, exercise real workflows, diagnose failures, and verify the result of a change. The development harness is the environment, tools, permissions, and tests that let an agent do that work. [The Twelve-Factor App](https://12factor.net/), [OpenAI's harness engineering case study](https://openai.com/index/harness-engineering/)

Use the factors to make decisions about the system under change. A library may supply its checks through a consuming service. Reuse working interfaces and tools. For changes to critical workflows, follow the planning and quality assurance (QA) requirements in the Critical workflows section of `spec-driven-delivery/references/quality-gates.md`. Those requirements apply when a failure could block an essential task, compromise access or data, affect billing, or require operator recovery.

Kevin Hoffman's *Beyond the Twelve-Factor App* added API-first design, telemetry, and authentication and authorization. The adaptation below puts those ideas into practice for agents and gives each factor a check that produces evidence. [Beyond the Twelve-Factor App](https://www.oreilly.com/library/view/beyond-the-twelve-factor/9781492042631/)

## I. Codebase

Keep each deployable traceable to a source revision. A monorepo can use one commit for several deployables if the build identifies which component and inputs produced each artifact.

Version startup commands, test fixtures, event schemas, and operational contracts with the code they describe. Use a short `AGENTS.md` to point to the repository's architecture, test commands, and runbooks. The export worker's retry rules, for example, should be findable from the same revision as the worker.

**Check.** Start from a fresh checkout. Find the export entry point, the worker, and the test command through the repo's documented paths. Trace a deployed worker version back to the source commit.

## II. Dependencies

Declare and isolate the runtime and development tools needed to run the checks. Pin dependencies through the repository's lockfiles and tool version files. Include the browser driver or service images when the actual workflow depends on them.

Put routine setup behind a documented command with explicit prerequisites. For report export, document the queue and storage dependencies and any renderer or font package the worker needs. Run the same setup in an agent workspace and in continuous integration, or CI, where the environments support it.

**Check.** Bootstrap without packages left over from another checkout. Run the export smoke test and verify that the documented dependency versions produced the expected file.

## III. Config

Supply deployment-specific configuration through the execution environment. Keep a versioned schema or template with safe example values. Validate required settings when the app starts and report missing settings in a form the harness can read.

Inject secrets through the project's secret manager or platform. Give test runners and agents identities scoped to their jobs and environments. For example, allow a support agent to read exported job status and redacted logs. Give an operator identity permission to request a retry for an authorized tenant. Enforce both permissions where the operation runs.

**Check.** Start with an incomplete test configuration and confirm that startup identifies the missing field without disclosing its value. Use test identities to verify the allowed read and the denied retry.

## IV. Backing services

Attach the database, queue, storage, and telemetry collector through explicit configuration. Give each test run its own data and resource names. Record the service features the workflow relies on, such as database transactions, queue redelivery, or storage write conditions.

Exercise those features with the real dependency when they affect the outcome. A test substitute can simulate an external provider timeout while the application still uses its real queue, worker, and job store.

**Check.** Run the export against disposable resources. Induce the storage timeout through a test fixture and confirm that the worker records a recoverable failure. Verify that cleanup removes the resources for that run.

## V. Build, release, and run

Build a versioned artifact. Create a release that identifies the artifact and its deployment configuration. Start processes from that release. Promote the tested artifact through environments when the delivery platform supports it.

Record the release and environment on telemetry so someone investigating a job can find the code that ran. Consider what happens to jobs queued by an older release when the new worker starts. A rollback plan should account for data and message formats that may have changed.

**Check.** Run a smoke test against the promoted artifact. Use its telemetry to identify the release and find the source commit. If the change affects message or data formats, test how a job created before deployment is handled after deployment.

## VI. Processes

Keep authoritative workflow state outside a single application process. Use durable storage for job status, progress, and results that must survive a restart. Expose the job status where an authorized caller can read it.

Design the final write so two attempts for one export produce one completed result. For example, use an operation ID with a unique database constraint and a stable storage key. Match the design to the transaction and storage guarantees the system actually provides.

**Check.** Stop a test worker after it writes the file and before it confirms completion. Restart the worker and verify that the job reaches the expected state and exposes one completed export.

## VII. Port binding

Make each listening service bind to its configured address and port. Provide startup output or a command that lets the harness discover the address. Expose a readiness check that tells the harness when the service can handle the intended requests.

Give jobs and workers a readiness mechanism suited to their real entry point, such as a worker check against the configured queue. Let end-to-end tests exercise the browser, application programming interface (API), or command-line interface (CLI) that the workflow actually uses.

**Check.** Start two isolated app instances. Discover each address from startup output, wait for readiness, and run an export against the intended instance. Confirm the worker for that instance handles the job.

## VIII. Concurrency

Name the process roles and document how they scale. For a report export, web processes can accept requests while workers consume jobs at a rate the backing services can handle. Define what happens when a job is delivered twice, multiple workers compete for it, or work arrives faster than the system can process it.

Use queue limits, backoff, or other controls that match the workload. Give the operator and the agent observable outcomes for overload, such as a queued state, a retryable error, or a failed job with an error code.

**Check.** Run the critical path with more than one worker if production does. Exercise duplicate delivery or concurrent retries and assert the number of results. Compare queue and failure signals with the expected behavior.

## IX. Disposability

Make app instances quick to start, stop, and replace. Wait on a readiness condition with a time limit. During graceful shutdown, stop accepting new work and give in-flight work a bounded time to complete or save recoverable progress.

Plan for an abrupt stop as well. Define which work the platform redelivers, how a replacement discovers unfinished jobs, and what cleanup the harness owns. Scope cleanup to resources created by the test run.

**Check.** Interrupt the worker during an export. Observe shutdown, restart, and the final job state. Reset the test environment and confirm that a second run starts with clean data and distinct resources.

## X. Development and production parity

Exercise the same application paths, service contracts, and authorization rules used in production. Use isolated, smaller environments with synthetic data and limited test credentials. Document substitutions that change the behavior a test can establish.

Give concurrent agent runs separate app instances, data, ports, and telemetry. A Git worktree can have its own runnable instance so an agent can reproduce an issue without sharing a queue or log stream with another task. OpenAI's case study used per-worktree app instances, browser automation, and a local telemetry stack. [OpenAI's harness engineering case study](https://openai.com/index/harness-engineering/)

**Check.** Use a fresh isolated environment to run the export through its normal entry point, record the expected state, reproduce a known failure, and exercise supported recovery with the planned test roles.

## XI. Logs and queryable telemetry

Let the runtime collect application logs as event streams. Add structured logs, metrics, traces, and product events where each helps explain the workflow. Product events describe steps people take or outcomes they experience. Name the events when designing a critical workflow and collect fields that help answer a specific question. [Original logs factor](https://12factor.net/logs)

For report export, record `export_requested`, `export_completed`, and `export_failed` with an opaque `export_id`. Include an error code on failure. Link the request and worker activity through trace context and the export ID. Record the environment and deployed version. Keep metric labels bounded and put unique IDs on individual events, log records, or traces. OpenTelemetry can propagate trace context and correlate logs with traces. [OpenTelemetry context propagation](https://opentelemetry.io/docs/concepts/context-propagation/)

Provide a documented query tool that the agent can actually call. Scope it to relevant environments and data. Expose redacted fields through read-only access, and provide example filters for service, time, release, and operation ID. Treat user-supplied text inside telemetry as data. Application code and tool permissions determine what actions a caller can take.

**Check.** Start with an export ID and a time range. Use the agent's read-only query tool to find the failure event, worker error, trace, and affected release. Confirm that the result contains the fields needed for diagnosis and respects the redaction rules.

## XII. Admin processes and callable operations

Run one-off maintenance tasks with the target release's code and configuration. A CLI for migrations or maintenance already fits the original factor. Where a workflow needs operator inspection or recovery, offer a documented API or CLI with bounded inputs, structured results, and permissions enforced where the action runs. An admin screen can call the same application operation. [Original admin processes factor](https://12factor.net/admin-processes)

For an export retry, accept an export ID, authorize the caller for that export, and return a job ID or status. Use an idempotency key to identify repeat requests for the same action. Store the key with the operation result so a retry after a timeout can return that result. Reject reuse of the same key with different input. Record the actor, target, action, and outcome in the audit history. Expose a status query so a caller can independently check what happened. [Amazon Builders' Library on safe retries](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

**Check.** Use separate test identities for inspection and retry. Confirm that the inspection role can see the failure and receives a denial when it tries to retry. Run the supported retry with the operator role and repeat the same request. Verify one completed export and the expected audit records.

## Verify the workflow end to end

Make the plan name the real entry points, allowed identities, expected signals, and observable results. For the report export example, the acceptance evidence can be recorded as follows.

| Case | Action | Evidence |
| --- | --- | --- |
| Success | Request an export through the normal application entry point. | The job completes, the caller can retrieve one file, and the expected product event appears. |
| Failure and diagnosis | Induce a storage timeout with an isolated fixture. Inspect the result through the agent's query tool. | The job enters the expected failed state. The failure event, log, and trace identify the error and deployed version. |
| Permission boundary | Ask the inspection identity to retry the failed job. | The API or CLI returns a denial. The job state remains failed. |
| Supported recovery | Call the retry operation with the operator test identity. Repeat the call with the same idempotency key. | The new attempt completes, status and telemetry reflect the result, and one file and the expected audit records exist. |

Run deterministic checks in CI when practical. Keep commands, the tested version, and redacted results in the QA evidence. To measure agent reliability, give the agent the same failure scenario across several independent runs. Score whether the agent found the correct cause and whether the system reached the expected state. Record the test permissions, tool configuration, and environment so the results can be reproduced. [Anthropic's guide to agent evaluations](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)

## How the staff engineer uses the factors

- During refinement, identify the factors the change affects. Propose the smallest design that meets the requirements. Name the interfaces, failure cases, permissions, and checks the plan needs.
- In engineering docs, record the chosen design and point to the actual commands, query examples, admin interfaces, and verification evidence. Mark unimplemented capabilities as proposals.
- In pull request review, inspect the changed implementation and connected paths. Check the QA evidence for the same target. Tie findings to an affected factor, the observable consequence, and the evidence needed to resolve the finding. Apply the repository's review and severity rules.
