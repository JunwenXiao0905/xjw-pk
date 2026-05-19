---
name: knowledge-note-writer
description: Add or revise knowledge points inside an existing personal knowledge-base note. Use when the user says a concept, syntax point, API detail, framework behavior, engineering rule, GIS workflow, frontend mechanism, example, or pitfall should be added to a document and Codex must place it in the correct section, keep headings retrieval-friendly, and write concise reference-style content instead of tutorial filler or chatty prose.
---

# Knowledge Note Writer

Use this skill for personal knowledge-base notes that are meant for later lookup.

## Primary Goal

When the user says a knowledge point should be added:

1. Find the most appropriate existing section.
2. Insert the content there directly.
3. Keep the note compact, searchable, and structurally stable.

Do not default to appending at the end of the document.

## Writing Target

Treat the document as:

- a personal reference note,
- a lookup-oriented knowledge base,
- a long-term accumulation file.

Do not treat it as:

- a beginner-facing textbook chapter,
- a lecture transcript,
- a chat-style explanation,
- or a motivational tutorial article.

## Heading Rule

Headings must be retrieval-oriented.

Prefer:

- `位置参数与关键字参数`
- `列表解包`
- `TypedDict`
- `useEffect 的执行时机`
- `GeoJSON 与 WGS84`
- `PostGIS SRID`
- `model_dump()`

Avoid:

- `Python 是什么`
- `理解 React 的核心思想`
- `初识地图投影`
- `从案例看列表展开`

## Placement Rule

Classify the new knowledge point before writing. Common categories include:

- language syntax,
- framework behavior,
- runtime mechanism,
- API usage,
- data model,
- frontend interaction,
- GIS data / projection / coordinate system,
- database / storage,
- engineering practice,
- debugging or pitfall notes.

Insert the new content into the nearest correct category.

If no suitable section exists:

1. Add a new section only if it clearly fits the note's long-term structure.
2. Use a concise, index-like heading.

## Content Rule

Write for fast lookup. Keep only high-value information:

1. the concrete point that needs to be remembered;
2. the minimum code, syntax, API shape, data shape, or rule;
3. the key mechanism, condition, or constraint when it matters;
4. the pitfall or boundary when it is easy to get wrong.

Do not add broad introductions unless they are necessary for retrieval.

Do not force every section into the same template. Explain enough to make the point understandable on later lookup.

## Explanation Rule

Prefer explanation that is anchored to the actual mechanism in the domain.

For Python, prefer:

- inheritance
- method lookup
- `__init__`
- `**data`
- class creation
- instance method binding

For frontend, prefer:

- render timing
- event flow
- state update timing
- prop flow
- effect execution conditions
- DOM / browser behavior when relevant

For GIS, prefer:

- coordinate system
- projection
- geometry type
- spatial reference
- data format constraints
- analysis workflow steps

For engineering practice, prefer:

- process order
- source of truth
- build / runtime boundary
- environment variable loading point
- interface contract

Do not hide the mechanism behind empty phrases such as:

- "the framework handles it"
- "the library takes over"
- "the parent provides the logic"
- "the map engine processes it automatically"

If such a phrase is used, immediately follow it with the concrete mechanism that makes it true.

When introducing a new internal term such as `metaclass`, `schema`, `effect`, `SRID`, or `projection`, define it in relation to already-known concepts. If the term is not needed for the current level of understanding, defer it.

## Method Rule

When documenting a method, hook, API, or inherited behavior:

1. Say where it comes from.
2. Show how the call or behavior is reached.
3. Show the equivalent direct shape when useful.
4. Explain what receives the input and what happens next.

For example:

- parent method resolution in Python,
- hook execution conditions in React,
- coordinate conversion requirements in GIS,
- request / response shape in API notes.

## Style Rule

Use:

- concise prose;
- direct statements;
- small examples;
- terminology-first writing;
- explanation that stays close to the code, data, or mechanism.

Avoid:

- abstract metaphors;
- analogies that do not map directly to code or data;
- anthropomorphic language for libraries, frameworks, or methods;
- long narrative descriptions of runtime behavior when a short mechanism-focused explanation will do.

When possible, explain behavior with:

- the relevant code;
- the relevant data shape;
- the actual mechanism that executes it;
- a short direct statement tied to the code or data.

## Structural Rule

Use textbook-like organization only at the directory level, not at the prose level.

That means:

- categories may resemble a good technical book;
- section bodies should behave like a compact reference manual.

## Output Expectation

When editing:

1. choose the correct insertion point;
2. write the new content in concise reference style;
3. preserve heading consistency;
4. optimize for future retrieval.
