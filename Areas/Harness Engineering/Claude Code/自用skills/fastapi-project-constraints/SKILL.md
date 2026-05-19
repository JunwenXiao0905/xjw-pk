---
name: fastapi-project-constraints
description: Follow FastAPI project structure and engineering conventions for Python backend work. Use when Codex is creating, editing, refactoring, or reviewing FastAPI codebases that use layered modules, dependency injection, database sessions, Pydantic schemas, and request-scoped services. Trigger for tasks involving routers, services, repositories, dependencies.py, main.py, SQLAlchemy session handling, response models, exception handlers, or FastAPI tests.
---

# FastAPI Project Constraints

## Core rules

- Keep HTTP details in `router.py`.
- Keep business logic in `service.py`.
- Keep persistence logic in `repository.py`.
- Keep request and response models in `schema.py`.
- Keep dependency assembly in `dependencies.py`.
- Keep `main.py` focused on app assembly: `FastAPI(...)`, `include_router(...)`, middleware, exception handlers, lifespan.

## Directory layout conventions

- Use `modules/<domain>/` to organize business code by domain.
- Keep `modules/<domain>/router.py` for HTTP entrypoints only.
- Keep `modules/<domain>/service.py` for business rules and orchestration.
- Keep `modules/<domain>/repository.py` for persistence and data access.
- Keep `modules/<domain>/schema.py` for request and response models.
- Keep `dependencies.py` for dependency assembly and shared providers.
- Keep `core/` for infrastructure such as config, database, security, and shared utilities.
- Keep `middleware/` for cross-cutting request/response behavior.
- Keep `tests/` aligned with API behavior and module boundaries.

## Router conventions

- Parse request inputs in routers, then delegate to services.
- Use `response_model` for structured JSON responses unless there is a clear reason to return a raw `Response`.
- Keep route handlers thin; avoid embedding business rules or persistence details.
- Use `Annotated[..., Depends(...)]` for injected runtime objects when editing modern code.
- Treat path/query/body inputs as request data, not dependencies.

## Dependency conventions

- Use `Depends(...)` for runtime objects such as settings, database sessions, current user, repositories, and services.
- Prefer small dependency functions that construct or return one thing clearly.
- Keep dependency chains explicit and readable.
- For request-scoped database access, use a `get_db()` style dependency that yields a `Session` and closes it in `finally`.
- If app infrastructure is initialized in lifespan, read shared objects from `app.state`.

## Database conventions

- Treat `Engine` as application infrastructure, not a per-request object.
- Treat `Session` as the per-request unit of database work.
- Create the engine and session factory once during startup, then inject sessions per request.
- Keep raw SQL, ORM access, and transaction-sensitive persistence logic out of routers.
- Prefer repository or service boundaries over direct session usage in many route handlers.

## Schema conventions

- Use Pydantic models for request and response contracts.
- Separate create, update, partial update, and response schemas when the shapes differ.
- Do not mix database entities, HTTP response shapes, and domain input shapes into one model unless they are truly identical.

## Error handling conventions

- Raise domain-specific exceptions from service or repository layers when appropriate.
- Convert exceptions to HTTP responses through registered FastAPI exception handlers.
- Keep error response shape consistent across endpoints.

## Testing conventions

- Cover endpoints with API tests.
- Cover business rules with service-level tests when logic is non-trivial.
- Override dependencies in tests when replacing repositories, sessions, or external services.
- Prefer testing behavior and response shape over testing internal implementation details.

## Review checklist

- Does the router contain only HTTP-facing logic?
- Is dependency injection used for runtime objects rather than request data?
- Is database session lifetime request-scoped and cleaned up?
- Are schemas separated by API role when needed?
- Are exceptions mapped consistently to HTTP responses?
- Are changes aligned with the existing module layout and naming style?

## Output style

- Preserve existing project structure unless the task explicitly asks for a refactor.
- When introducing a new module, mirror the established layout under `modules/<domain>/`.
- Prefer concise comments and explicit naming over framework cleverness.
