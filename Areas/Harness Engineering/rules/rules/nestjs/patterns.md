---
paths:
  - "src/**/*.ts"
  - "apps/**/*.ts"
  - "libs/**/*.ts"
---
# NestJS Coding Patterns

> Preferred implementation patterns for NestJS projects using modular architecture and clear separation between request handling, business logic, and background execution.

## DTO Pattern

- Use class-based DTOs for controller request and response boundaries.
- Do not use interfaces as controller input types when validation or transformation is expected.
- Put validation decorators on DTO fields, not inside controllers or services.
- Keep request DTOs focused on transport validation, not domain orchestration.
- Prefer dedicated response DTOs when output shape should differ from persistence shape.

## Controller Pattern

- Keep controllers thin:
  - accept request data
  - delegate to services
  - return service results
- Do not place database queries, queue job construction details, or complex branching in controllers.
- Keep request metadata close to handlers with decorators such as route decorators, auth decorators, and Swagger decorators.
- Let guards, pipes, interceptors, and filters handle cross-cutting concerns instead of duplicating them in handlers.

## Service Pattern

- Put business decisions and orchestration in services.
- Inject dependencies through the constructor; do not instantiate infrastructure classes manually.
- Keep services transport-agnostic; do not depend on `req`, `res`, headers, route params objects, or HTTP status handling.
- Services may coordinate:
  - repositories / database services
  - helper services
  - queue producers
  - external adapters
- Services should return domain data or DTO-compatible objects, not handcrafted HTTP wrapper objects unless the project explicitly uses a specific generic response DTO.
- Put business rules in services/domain code, not in DTO validators.

## Database Access Pattern

- Centralize persistence access through the project’s database abstraction, such as `DatabaseService`.
- Prefer explicit query intent over generic helper indirection when the query is domain-specific.
- Keep persistence concerns in services or repository-style abstractions, not in controllers.
- Do not leak raw persistence models directly when response contracts should hide internal fields.
- Use transactions for multi-write flows or state changes that must succeed or fail together.

## Error Handling Pattern

- Throw framework exceptions for expected business failures.
- Do not catch and rethrow the same error without adding value.
- Let global exception filters shape HTTP error responses.
- Keep domain failure checks near the business rule they protect.

## Auth and Request Boundary Pattern

- Use decorators plus guards for route access policy.
- Treat request metadata as declarative policy:
  - public/private route markers
  - role requirements
  - custom auth decorators
- Do not scatter auth checks across services when the rule belongs in the request pipeline.

## Response Pattern

- Let interceptors and serializers shape outbound HTTP responses.
- Keep controllers and services focused on returning meaningful data, not formatting global envelopes.
- Use response decorators consistently so runtime behavior and generated API docs stay aligned.

## Worker Pattern

- Services produce background jobs.
- Worker processors consume jobs.
- Do not perform long-running or retry-prone side effects directly inside latency-sensitive HTTP handlers when a queue is appropriate.
- Treat worker classes as Nest providers with extra runtime semantics; inject dependencies normally.
- Keep worker methods focused on one job type or one tightly related responsibility.

## Module Boundary Pattern

- Place domain-specific code in domain modules or domain libs.
- Place reusable platform capabilities in shared/common modules or libs.
- Avoid mixing domain logic, transport concerns, and infrastructure concerns in one file.
- When adding new code, prefer extending the nearest existing module boundary before introducing a new top-level abstraction.
- Keep `helper` code generic; do not move domain logic into helper utilities.

## Testing Alignment Pattern

- Unit tests should verify the colocated unit’s behavior and boundary assumptions.
- Prefer mocking external boundaries in unit tests:
  - database
  - queues
  - network clients
  - cloud SDKs
- Use broader integration or e2e suites for cross-module wiring and full request flow validation.
