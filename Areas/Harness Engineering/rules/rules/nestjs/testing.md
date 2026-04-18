---
paths:
  - "src/**/*.ts"
  - "apps/**/*.ts"
  - "libs/**/*.ts"
  - "src/**/*.spec.ts"
  - "src/**/*.test.ts"
  - "apps/**/*.spec.ts"
  - "apps/**/*.test.ts"
  - "libs/**/*.spec.ts"
  - "libs/**/*.test.ts"
  - "apps/**/*e2e*.ts"
  - "e2e/**/*.ts"
---
# NestJS Testing Rules

> Testing rules for NestJS projects in Nx-style single-repo setups. Prefer colocated unit tests and separate end-to-end suites.

## Test Placement

- Unit tests must be colocated with the source file they verify.
- Place unit test files beside the runtime file using `*.spec.ts`.
- Do not create or expand a top-level catch-all `test/` directory for ordinary unit tests.
- End-to-end tests should live in dedicated e2e projects or directories, not beside source files.
- Cross-module integration tests that are broader than one unit should live with e2e/integration suites, not be disguised as colocated unit tests.

## Expected Layout

- Colocated unit test examples:
  - `libs/server/user/src/lib/user.service.ts`
  - `libs/server/user/src/lib/user.service.spec.ts`
  - `libs/server/auth/src/lib/jwt-access.guard.ts`
  - `libs/server/auth/src/lib/jwt-access.guard.spec.ts`
- Separate e2e examples:
  - `apps/api-e2e/src/auth/signup.e2e-spec.ts`
  - `e2e/auth/signup.e2e-spec.ts`

## What To Test Where

- Service, helper, guard, interceptor, pipe, and worker logic should usually have colocated unit tests.
- Controller tests may be colocated when they are true unit tests with mocked dependencies.
- Full HTTP flow, module wiring, persistence flow, or cross-boundary tests belong in e2e/integration suites.
- Do not label cross-module, database-backed, or queue-backed behavior tests as unit tests.

## Agent Behavior

- When modifying a source file, first look for its colocated `*.spec.ts`.
- When adding a new source file with meaningful logic, create a colocated unit test by default unless the project clearly uses another local convention.
- Do not move existing tests just for style unless the task explicitly includes test-structure refactoring.
- Prefer incremental migration: old centralized tests may remain, but new unit tests should follow colocated placement.

## Naming and Scope

- Name colocated unit tests after the runtime file: `foo.service.ts` -> `foo.service.spec.ts`.
- Keep unit tests narrow and dependency-light; mock external services, queues, network calls, and persistence where appropriate.
- Avoid mixing e2e concerns into unit specs.
