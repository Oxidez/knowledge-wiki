---
title: "{{entity_name}}"
created: "{{date}}"
updated: "{{date}}"
type: entity
category: "{{category}}"
subcategory: "{{subcategory}}"
tags: []
sources: []
related: []  # Exactly 1 item: for boards → its MCU; for MCUs → its primary board
supersedes: null
superseded_by: null
status: active
confidence: high
---
# {{entity_name}}

## Overview

One-paragraph canonical description of what this entity is and why it matters.

## Key Facts

| Property | Value |
|----------|-------|
| Type | {{entity_type}} |
| Category | {{category}} |
| Subcategory | {{subcategory}} |
| Status | {{status}} |

## Details

Extended description with technical specifications, history, variants, etc.
Use subsections as needed.

## Relationships

- **Related:** [[related-entity]]  # Single bidirectional link: board ↔ its MCU only

## Sources

{% for source in sources %}
- [{{source.title}}]({{source.url}}) — {{source.date}} — {{source.type}}
{% endfor %}

## Changelog

- {{date}} — Created