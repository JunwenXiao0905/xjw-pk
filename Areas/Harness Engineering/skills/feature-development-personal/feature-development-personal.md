# Feature Development Workflow

A structured approach to developing features from ambiguous requirements to concrete implementation.

## When to Use

Invoke this skill when:
- Starting a new feature from scratch
- Requirements are vague or need clarification
- You need to track development progress across multiple sessions

## Workflow Stages

### Stage 1: Requirements Concretization (需求具象化)

**Goal**: Transform vague requirements into clear, actionable specifications.

**Steps**:
1. Clarify user intent through targeted questions
2. Identify core use cases and edge cases
3. Define acceptance criteria
4. Document technical constraints

**Output**: A PRD-like document with:
- Feature overview
- User stories
- Technical requirements
- Out of scope items

### Stage 2: Architecture Design (架构设计)

**Goal**: Design the technical architecture before coding.

**Steps**:
1. Identify affected components/modules
2. Design data flow and state management
3. Plan API contracts (if applicable)
4. Consider scalability and performance

**Output**: Architecture document with:
- Component diagram
- Data flow diagram
- API specifications
- Key technical decisions

### Stage 3: Implementation Planning (实现规划)

**Goal**: Break down the work into actionable tasks.

**Steps**:
1. Create implementation plan with file paths
2. Identify dependencies between tasks
3. Estimate complexity (not time)
4. Define testing strategy

**Output**: Task list with:
- File paths
- Function/method names
- Dependencies
- Test cases

### Stage 4: Incremental Implementation (增量实现)

**Goal**: Implement the feature step by step.

**Principles**:
- Start with core functionality
- Add enhancements iteratively
- Test after each significant change
- Update documentation as you go

### Stage 5: Debugging & Refinement (调试优化)

**Goal**: Fix issues and polish the implementation.

**Common Debugging Approaches**:
- Use browser dev tools for UI issues
- Add logging for state tracking
- Isolate components to test independently
- Check for race conditions in async code

## Document Templates

### Feature Document Template

```markdown
# [Feature Name]

## Overview
Brief description of the feature.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Technical Implementation

### Files Modified
- `path/to/file.tsx` - Description of changes

### Key Functions
- `functionName()` - Purpose

## Status
- [x] Requirements clarified
- [x] Architecture designed
- [x] Implementation complete
- [ ] Testing complete

## Known Issues
- Issue description and workaround
```

### Technical Document Template

```markdown
# [Technical Topic]

## Problem Statement
What problem does this solve?

## Solution Overview
High-level approach.

## Implementation Details

### Key Code
```typescript
// Relevant code snippet
```

### Dependencies
- Library/package name

## Edge Cases
- Case 1: How it's handled

## References
- Related documentation links
```

## Decision Records (ADR)

For significant technical decisions, create an ADR:

```markdown
# ADR-XXX: [Decision Title]

## Context
What is the issue being addressed?

## Decision
What is the change being made?

## Consequences
What are the trade-offs?

## Status
Accepted | Deprecated | Superseded
```

## Debugging Checklist

When encountering issues:

1. **Reproduce**: Can you consistently reproduce the issue?
2. **Isolate**: What's the minimal case that shows the problem?
3. **Hypothesize**: What could be causing this?
4. **Verify**: Test your hypothesis with targeted changes
5. **Fix**: Implement the solution
6. **Document**: Update docs if the fix reveals new information

## Session Continuity

When work spans multiple sessions:

1. **End of session**: Update feature document with current progress
2. **Start of session**: Review last session's progress and next steps
3. **Use compact**: Ensure context is preserved across long conversations