---
title: "{{comparison_title}}"
created: "{{date}}"
updated: "{{date}}"
type: comparison
category: "{{category}}"
subcategory: "{{subcategory}}"
tags: []
sources: []
related: []  # ≥2 items for comparison pages
supersedes: null
superseded_by: null
status: active
confidence: high
---

# {{comparison_title}}

## Purpose

Why this comparison matters and what decision it informs.

## Items Compared

| Item | Description |
|------|-------------|
| [[item-1]] | Description |
| [[item-2]] | Description |

## Dimensions

| Dimension | [[item-1]] | [[item-2]] |
|-----------|------------|------------|
| Dimension 1 | Value | Value |
| Dimension 2 | Value | Value |

## Verdict

Synthesis and recommendation based on the comparison.

## Related

- [[related-item-1]]
- [[related-item-2]]

## Sources

{% for source in sources %}
- [{{source.title}}]({{source.url}}) — {{source.date}}
{% endfor %}

## Changelog

- {{date}} — Created