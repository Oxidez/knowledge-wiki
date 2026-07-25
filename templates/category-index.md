# {{category_name}} Index

> Content catalog for **{{category_name}}** category. Every page in this category listed under its type with a one-line summary.
> Read this first to find relevant pages for any query in this category.
> Last updated: {{date}} | Total pages: {{total_count}}

## Entities

<!-- Alphabetical within section -->

{% for page in entities %}
- [[{{page.title}}]] — {{page.summary}}
{% endfor %}

## Concepts

{% for page in concepts %}
- [[{{page.title}}]] — {{page.summary}}
{% endfor %}

## Procedures

{% for page in procedures %}
- [[{{page.title}}]] — {{page.summary}}
{% endfor %}

## Comparisons

{% for page in comparisons %}
- [[{{page.title}}]] — {{page.summary}}
{% endfor %}

## Queries

{% for page in queries %}
- [[{{page.title}}]] — {{page.summary}}
{% endfor %}

---

**Scaling rule:** When any section exceeds 50 entries, split into sub-sections by first letter or sub-domain.