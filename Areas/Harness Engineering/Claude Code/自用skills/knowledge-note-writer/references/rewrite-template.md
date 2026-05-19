# Insertion Checklist

## Purpose

Use this checklist when adding a new knowledge point into an existing knowledge-base note.

## Core Rule

Do not append by default. Place the new content where a later lookup would most naturally expect to find it.

## Steps

1. Determine what kind of point is being added:
   - syntax
   - mechanism
   - API
   - framework behavior
   - data shape
   - pitfall
   - workflow step
2. Find the nearest correct existing section.
3. Insert the content there.
4. Keep heading depth and terminology consistent with surrounding content.
5. Explain only as much as is needed for later retrieval and understanding.

## Section Pattern

Do not force every section into a fixed template.

A good entry usually contains some combination of:

- the exact concept name;
- the concrete code, API, or data shape;
- the mechanism or condition that explains the behavior;
- the pitfall or boundary when it is easy to get wrong.

## Mechanism Rule

When a point depends on hidden behavior, explain the actual mechanism instead of using abstract phrases.

Prefer:

- inheritance and method lookup for Python;
- render / effect / event flow for frontend;
- coordinate system / projection / geometry constraints for GIS;
- build-time / runtime / environment boundary for engineering notes.

## Editorial Rule

If a note is intended for long-term accumulation, every new knowledge point must be placed according to concept hierarchy, not according to the order in which it was learned.
