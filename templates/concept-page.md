---
title: "{{concept_name}}"
created: "{{date}}"
updated: "{{date}}"
type: concept
category: "{{category}}"
subcategory: "{{subcategory}}"
tags: []
sources: []
related: []  # ≥2 items for concept pages
supersedes: null
superseded_by: null
status: active
confidence: high
---

# {{concept_name}}

## Definition

Precise, one-paragraph definition of the concept.

## Explanation

Extended explanation with context, significance, current state of knowledge.
Use subsections for complex concepts.

## Key Properties

| Property | Description |
|----------|-------------|
| Property 1 | Description |
| Property 2 | Description |

## Related Concepts

- [[related-concept-1]]
- [[related-concept-2]]

## Open Questions

- Question 1
- Question 2

## Sources

{% for source in sources %}
- [{{source.title}}]({{source.url}}) — {{source.date}} — {{source.type}}
{% endfor %}

## Changelog

- {{date}} — Created