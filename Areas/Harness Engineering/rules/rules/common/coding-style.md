# Coding Style

## Immutability (CRITICAL)

ALWAYS create new objects, NEVER mutate existing ones:

```
// Pseudocode
WRONG:  modify(original, field, value) → changes original in-place
CORRECT: update(original, field, value) → returns new copy with change
```

Rationale: Immutable data prevents hidden side effects, makes debugging easier, and enables safe concurrency.

## File Organization

MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large modules
- Organize by feature/domain, not by type

## Error Handling

ALWAYS handle errors comprehensively:
- Handle errors explicitly at every level
- Provide user-friendly error messages in UI-facing code
- Log detailed error context on the server side
- Never silently swallow errors
- **Fail fast and loudly**: Do not write fallback logic unless explicitly required. Throw errors immediately.
- **Let errors bubble up**: Do not handle errors inside business logic layers. Let them propagate to a unified error handler at the system boundary.
- **Valid tests**: Tests must prove bugs exist by failing. Tests that only pass prove nothing.

## Input Validation

ALWAYS validate at system boundaries:
- Validate all user input before processing
- Use schema-based validation where available
- Fail fast with clear error messages
- Never trust external data (API responses, user input, file content)

## Mock Data Restrictions

  NEVER use mock data unless explicitly requested:
  - Default to real data sources (APIs, databases, files)
  - Mock data introduces drift from production behavior
  - Tests with mocks pass but production may fail

  If mock data appears necessary due to business or code constraints:
  - STOP and ASK the user before proceeding
  - Explain why mock is needed and what alternatives exist
  - Get explicit approval before implementing any mock

  Rationale: Mocks hide real-world edge cases, create maintenance burden, and mask integration failures.


## Code Quality Checklist

Before marking work complete:
- [ ] Code is readable and well-named
- [ ] Functions are small (<50 lines)
- [ ] Files are focused (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Proper error handling
- [ ] No hardcoded values (use constants or config)
- [ ] No mutation (immutable patterns used)
