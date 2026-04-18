---
paths:
  - "src/**/*.ts"
  - "apps/**/*.ts"
  - "libs/**/*.ts"
  - "prisma/**/*.prisma"
---
# NestJS Security Rules

> Security constraints for NestJS backends using DTO validation, DI, JWT auth, queues, and external service integrations.

## Secrets and Configuration

- Never hardcode secrets, API keys, JWT secrets, passwords, Redis URLs, database URLs, or cloud credentials.
- Read sensitive configuration through environment variables and the project’s config layer.
- Fail fast when required security-sensitive config is missing.
- Validate required env/config at startup, not lazily in late request paths.

## Input Validation

- Validate external input at the request boundary with DTO classes and validation decorators.
- Prefer strict request validation with whitelist-style behavior when the project supports it.
- Do not trust client-supplied fields that affect authorization or privileged state, such as roles, ownership, internal status flags, or audit fields.
- Keep validation logic near transport boundaries; do not rely on frontend validation alone.

## Authentication and Authorization

- Keep authentication in guards, strategies, and request decorators rather than scattering token parsing across controllers/services.
- Use route metadata and guards for access control decisions whenever possible.
- Distinguish authentication from authorization:
  - authentication proves identity
  - authorization checks permissions
- Never trust client-claimed identity fields when authoritative request user context is available from auth middleware/guards.

## Password and Token Handling

- Never store plaintext passwords.
- Use established password hashing helpers/services rather than custom crypto for password storage.
- Do not log raw tokens, passwords, refresh tokens, session secrets, or authorization headers.
- Treat token creation and verification as infrastructure concerns; avoid ad hoc token logic in unrelated modules.

## Response and Error Exposure

- Do not expose internal stack traces, raw database errors, secrets, or provider-specific failure details in production responses.
- Let centralized exception handling sanitize errors for clients.
- Avoid leaking internal-only fields in response DTOs.
- Prefer explicit response DTOs over returning persistence models directly.

## Database Safety

- Prefer ORM/query builder APIs over unsafe string-built queries.
- Enforce ownership and permission checks before update/delete operations.
- Do not trust client input for ownership fields such as `userId`, `authorId`, or tenant identifiers when the server can derive them from authenticated context.
- Be careful with soft-delete behavior and ensure deleted records are not unintentionally treated as active.

## External Service Calls

- Isolate cloud SDK, email, storage, payment, and network calls behind services or adapters.
- Use queues/workers for side effects that are slow, retry-prone, or operationally fragile.
- Sanitize logs and error paths around external requests so secrets and PII are not emitted.

## Queue and Worker Safety

- Treat queued payloads as durable data; do not place secrets in job payloads unless there is a clear operational reason.
- Keep job payloads minimal and purpose-specific.
- Validate or defensively check job data at consumption boundaries if payload correctness is not fully guaranteed.
- Make worker handlers idempotent or retry-tolerant when feasible.

## Logging and Observability

- Log enough context for debugging, but redact or omit secrets, tokens, passwords, cookies, and sensitive headers.
- Be careful when attaching request bodies, headers, or job payloads to logs or monitoring tools.
- Prefer structured logging through the project logging layer over ad hoc console logging.
- Add structured logs for key async jobs, external calls, and important state transitions.

## File and Upload Handling

- Validate file metadata and access intent before generating upload/download URLs.
- Do not assume client-provided filenames, content types, or storage keys are trustworthy.
- Keep storage access behind dedicated file/storage services.

## Change Discipline

- When adding new endpoints, ask:
  - what inputs are untrusted?
  - who is allowed to call this?
  - what fields must be server-derived?
  - what data must never be returned or logged?
- Prefer using existing auth, validation, and response infrastructure before introducing custom security behavior.
