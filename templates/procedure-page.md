---
title: "{{procedure_title}}"
created: "{{date}}"
updated: "{{date}}"
type: procedure
category: "{{category}}"
subcategory: "{{subcategory}}"
tags: []
sources: []
related: []  # ≥2 items for procedure pages
supersedes: null
superseded_by: null
status: active
confidence: high
version: "1.0"
---

# {{procedure_title}}

## Purpose

What this procedure accomplishes and when to use it.

## Prerequisites

- Requirement 1
- Requirement 2

## Steps

### Step 1: {{step_name}}

{{step_description}}

```bash
# Command or code if applicable
```

### Step 2: {{step_name}}

{{step_description}}

...

## Verification

How to confirm the procedure succeeded:
- Check 1
- Check 2

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Issue 1 | Cause | Resolution |

## Related Procedures

- [[related-procedure-1]]
- [[related-procedure-2]]

## Sources

{% for source in sources %}
- [{{source.title}}]({{source.url}}) — {{source.date}}
{% endfor %}

## Changelog

- {{date}} v1.0 — Created