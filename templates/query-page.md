---
title: "{{query_title}}"
created: "{{date}}"
updated: "{{date}}"
type: query
category: "{{category}}"
subcategory: "{{subcategory}}"
tags: []
sources: []
related: []  # ≥2 items for query pages
supersedes: null
superseded_by: null
status: active
confidence: high
---

# {{query_title}}

## Question

The original question that prompted this research.

## Answer

Direct answer to the question.

## Supporting Details

Evidence, examples, and reasoning behind the answer.

## Related Queries

- [[related-query-1]]
- [[related-query-2]]

## Sources

{% for source in sources %}
- [{{source.title}}]({{source.url}}) — {{source.date}} — {{source.type}}
{% endfor %}

## Confidence Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Source quality | High/Medium/Low | |
| Recency | Recent/Aged | |
| Consensus | Strong/Mixed/Uncertain | |

## Changelog

- {{date}} — Created