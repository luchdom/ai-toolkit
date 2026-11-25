---
name: dotnet-implementation
description: Implement or fix C#/.NET backend code, including ASP.NET Core APIs, EF Core queries and migrations, authorization, background workers, and backend tests. Follow the target repo's architecture and validation commands.
---

# .NET Implementation

1. **Route authorized implementation.** Delegate to the `dotnet` subagent when explicitly requested or when changing backend behavior, access rules, persistence, or service boundaries, if the role is available and delegation is allowed. Give it the target, bounded scope, acceptance criteria, and applicable delivery artifacts. Apply this skill inline for small mechanical edits or when delegation is unavailable. If you are already the `dotnet` subagent, implement directly. Planning and independent review keep their existing owners.
2. **Find the local pattern.** Read the target `AGENTS.md`, architecture and quality docs, and the closest comparable implementation and tests. Confirm the owning project, SDK, target framework, and package versions. When the repository uses module-first vertical slices or its approved design calls for them, read the bundled [modular monolith guide](references/modular-monolith.md) before placing or editing the slice. Extend the target's architecture and dependencies; surface material decisions the task has not authorized.
3. **Implement and verify.** Apply the checks below to the changed behavior. Run focused tests and the applicable repository gate. Report the tested behavior, including relevant denials or failure paths, and anything that could not be verified.

## Architecture checks

Follow the [repository-rule checks](../spec-driven-delivery/references/quality-gates.md#repository-rules). Reuse the repository's architecture tests. A dedicated test project can enforce stable rules about names, file layout, or dependencies as part of the normal solution validation.

## Implementation checks

- **Empty collections.** Use the C# collection expression `[]` in projects that support collection expressions. Declare an explicit target type as needed.
- **API and access:** Validate and map input at the boundary; keep business rules in the repo's application layer. Reuse its result/error mapping. Check the authenticated principal, required policy, and resource ownership before access. Resolve tenant access server-side, then constrain every affected query and mutation by that tenant. A request ID, route, or header alone grants no authority.
- **Persistence:** Filter, order, project, and page in the database where needed; use no-tracking reads when entities will not be updated. Match the owning context and migration conventions. Protect concurrent writes with the appropriate database constraint, transaction, or concurrency token. Preserve atomic state and audit writes when the existing contract requires them.
- **Async and dependencies:** Pass `CancellationToken` through dispatch, EF, and outbound I/O. Keep `DbContext` and other scoped dependencies inside a request or a worker's explicit scope for each unit of work. Use validated Options and the repo's `IHttpClientFactory` or equivalent client setup; retry writes only when the operation can safely repeat.
- **Errors and diagnostics:** Return expected failures through the existing error contract. Log useful operation and correlation information without credentials, tokens, personal data, or raw provider payloads.
- **Evidence:** Test the changed contract where it can fail: handler logic, HTTP authorization and response mapping, or database behavior. Use the real database provider in a disposable environment for SQL, migrations, constraints, or concurrency claims. Cover the applicable cross-tenant denial and confirm denied writes leave state unchanged.
