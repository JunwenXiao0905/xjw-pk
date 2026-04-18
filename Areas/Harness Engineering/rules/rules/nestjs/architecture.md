---
paths:
  - "src/**/*.ts"
  - "prisma/**/*.prisma"
  - "apps/**/*.ts"
  - "libs/**/*.ts"
---
# NestJS Architecture Rules

> NestJS module and layering rules for Nx-style monorepos and modular NestJS backends.

## Directory Boundaries

- Keep app bootstrap and composition thin.
- Keep domain logic in domain-focused modules or libs.
- Keep cross-cutting infrastructure in shared/common modules or libs.
- Keep async execution in dedicated worker/background modules or libs.
- Keep Prisma schema and migrations in their dedicated persistence layer.

## Module Placement

- Put code in a domain module/lib when it primarily serves one business domain.
- Put code in a shared/common module/lib only when it is reusable infrastructure or a cross-cutting concern.
- Place auth where it best fits your system boundary; keep the choice consistent across the repo.
- Avoid `forwardRef`; fix module boundaries first. Use it only as a last resort.
- Keep module internals explicit and predictable, typically with `controllers`, `services`, `dtos`, and related interfaces/types when needed.

## Controller Rules

- Controllers should stay thin: accept request data, call services, return service results.
- Do not embed database logic, queue orchestration details, or response envelope shaping in controllers.
- Use DTO classes for request/response boundaries. Do not use interfaces for runtime validation inputs.
- Keep route metadata close to handlers with decorators such as `@Post`, `@Get`, `@PublicRoute`, Swagger decorators, and response decorators.

## Service Rules

- Services hold business rules and orchestration.
- Prefer injecting `DatabaseService`, helper services, and queues instead of instantiating dependencies manually.
- Services should return domain data or DTO-compatible objects, not handcrafted global success/error envelopes.
- Throw Nest HTTP exceptions for business failures; let global filters/interceptors format the HTTP response.

## Request/Response Conventions

- Respect the existing global request pipeline.
- Put cross-cutting request behavior in middleware, guards, decorators, pipes, or interceptors rather than duplicating checks in controllers/services.
- Preserve the existing global response model.
- Reuse existing response decorators and serialization conventions where present.

## Data Access Rules

- Access the database through the project’s chosen database abstraction.
- Keep Prisma schema changes and migrations in the project’s persistence layer.
- Favor Prisma queries over ad hoc raw SQL unless there is a clear need.
- Follow existing soft-delete patterns such as `deletedAt` where the domain already uses them.

## Async and Worker Rules

- Produce jobs from services; consume jobs in worker/background processors.
- Keep queue registration in modules and queue consumption in processors.
- Put scheduled background logic in dedicated scheduler/background code, not in controllers or domain services.
- Worker classes are still Nest providers; inject dependencies instead of constructing them manually.

## Config and Security Rules

- Read configuration via `ConfigService` and the repo’s config layer.
- Never hardcode secrets, tokens, credentials, bucket names, or environment-specific URLs.
- Reuse existing auth, throttling, and request guard patterns before introducing new access-control logic.

## Testing Rules
- Follow the dedicated NestJS testing rules in `rules/nestjs/testing.md`.
- Keep architectural decisions independent from where tests happen to live.

## Change Strategy

- Match the existing layering before creating new abstractions.
- Prefer extending an existing module or helper when the responsibility already fits there.
- Export the minimum provider surface; do not expose internal module implementation by default.
- Do not move code across `common`, `modules`, and `workers` without a clear architectural reason.
- Keep changes minimal, consistent, and aligned with the current project structure.
