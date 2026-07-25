# Knowledge Vault Index

> Master content catalog. Every knowledge page listed under its category with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: {{date}} | Total pages: {{total_count}} | Categories: {{category_count}}

## Categories

{% for category in categories %}
### {{category.name}} ({{category.count}} pages)

#### Entities
{% for page in category.entities %}
- [[{{page.path}}|{{page.title}}]] — {{page.summary}}
{% endfor %}

#### Concepts
{% for page in category.concepts %}
- [[{{page.path}}|{{page.title}}]] — {{page.summary}}
{% endfor %}

#### Procedures
{% for page in category.procedures %}
- [[{{page.path}}|{{page.title}}]] — {{page.summary}}
{% endfor %}

#### Comparisons
{% for page in category.comparisons %}
- [[{{page.path}}|{{page.title}}]] — {{page.summary}}
{% endfor %}

#### Queries
{% for page in category.queries %}
- [[{{page.path}}|{{page.title}}]] — {{page.summary}}
{% endfor %}

{% endfor %}

## Recent Additions (last 10)

{% for page in recent %}
- [[{{page.path}}|{{page.title}}]] ({{page.category}}/{{page.type}}) — {{page.date}}
{% endfor %}

---

**Scaling rule:** When total entries exceed 200, create `_meta/topic-map.md` grouping pages by theme for faster navigation.