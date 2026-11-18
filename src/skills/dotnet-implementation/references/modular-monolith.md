# Modular Monolith Architecture for .NET

Use this guide when a repository already uses a modular monolith with module-first vertical slices or its approved design specifies one. Follow the target repository's boundaries, stack, naming, and validation rules. For an existing service with another architecture, extend its own patterns. A new architecture or framework belongs in the approved design.

## Place the change

A modular monolith runs in one deployable service. Business modules own their use cases and persistence. Keep the host's composition root responsible for registration and wiring. A module can be a folder or a project; use the separation the repository already enforces.

This is an example layout. Use the target's actual module and file names.

```text
Modules/
  Orders/
    Order.cs
    OrderErrors.cs
    IOrderRepository.cs
    CreateOrder/
      CreateOrderEndpoint.cs
      CreateOrderRequest.cs
      CreateOrderValidator.cs
      CreateOrderCommand.cs
      CreateOrderHandler.cs
      CreateOrderResponse.cs
    GetOrder/
      GetOrderEndpoint.cs
      GetOrderQuery.cs
      GetOrderHandler.cs
      GetOrderResponse.cs
    Data/
      Entities/
      Configurations/
      Mappers/
      Repositories/
      Migrations/
      OrdersDbContext.cs
    Services/
Infrastructure/
Shared/
```

| Place | What belongs there |
|---|---|
| Module root | Application models, enums, errors, and contracts used by multiple slices. |
| Use-case folder | Transport types, validator when needed, command or query, handler, and response for one operation. |
| Module `Data/` | Persistence entities, mappings, repository implementations, configuration, and migrations owned by the module. Keep tracked EF entities out of application and API contracts. |
| Module `Services/` | Business behavior shared by multiple slices. Keep one-use behavior in its handler. |
| `Infrastructure/` | Cross-module technical integration such as identity wiring, outbound clients, email, storage, messaging, caching, and time. |
| `Shared/` | Small app-wide primitives such as result mapping, common behaviors, and shared configuration. Module-specific rules and persistence stay with the module. |

## Trace the use case

```text
Request  -> endpoint -> command/query -> handler -> module contract -> data
Response <- endpoint/result mapper <- application result <- handler
```

1. **Endpoint:** Bind and validate the HTTP request, apply the route's authorization policy, and dispatch with cancellation. Keep business decisions out of the endpoint.
2. **Handler:** Reuse the application authorization and validation needed by every caller. A command changes state; a query reads it. Apply the business rules, call the module's data contract, and return an application model or a typed result. Keep the handler independent of HTTP status codes and transport types.
3. **Data:** Filter and project in the database, map between application and persistence models, and preserve transactional invariants. Keep the context and schema history under the module's ownership. Modules may share a physical database; use the owning module's public contract or established events to collaborate.
4. **Response:** Map success and expected failures through the existing result mapper. Preserve validation, conflict, not-found, and denial semantics across related endpoints.

For a project that has chosen FastEndpoints, MediatR, Ardalis.Result, and EF Core with PostgreSQL, this means a FastEndpoint sends a MediatR command or query, the handler uses the module's EF-backed contract and returns an Ardalis result, and the shared mapper produces the HTTP response. Use the same boundaries with the target's chosen libraries.

## Keep access and ownership explicit

- **Tenant data:** Resolve the active tenant and the actor's permission for the requested operation before accessing data. If the route also names a tenant, require it to match the authorized context. Use the resolved tenant ID in reads, writes, updates, and deletes, including lookups by resource ID.
- **Identity:** Keep account use cases and their data in the account module. Keep middleware, Identity/OpenIddict wiring, token schemes, policy registration, and current-user adapters in the authentication infrastructure. Where an authorization server owns interactive sign-in, keep credential forms there and preserve authorization code with PKCE. APIs validate their intended access tokens and enforce resource permissions.
- **Privileged writes:** Preserve the real actor and effective user as separate identities when acting on behalf of someone else. Revalidate authority for sensitive mutations where required by the contract. Preserve database constraints, stale-write behavior, and any required audit event in the write's transaction.
- **Across modules:** Reference the other module's exposed contract. Keep its entities, repositories, and context private. Use the existing transaction or event boundary when a change spans modules; resolve new ownership and consistency decisions before introducing cross-module writes.

## Example: create and retrieve an order

1. Add the write under `Orders/CreateOrder/` and the read under `Orders/GetOrder/`. Use the existing host registration and endpoint conventions.
2. Pass input to `CreateOrderCommand` and take the tenant from authorized context. Enforce the order rules in the handler, write through `IOrderRepository`, and map the result with the existing HTTP adapter. Add schema changes through the owning module's migration path if needed.
3. Resolve the same access boundary in `GetOrderHandler`. Query by tenant and order ID and project the fields the caller is allowed to see. Keep the response shape and failure semantics consistent with the API.
4. Test the successful write and read, invalid input, and relevant denied or cross-tenant cases. For a denied write, assert that state is unchanged. If the change depends on SQL, a database constraint, or a migration, run the relevant test with the target provider and disposable data.
