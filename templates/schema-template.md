# Wiki Schema

> This schema defines the structure, conventions, and tag taxonomy for the knowledge vault.
> **Categories and subcategories are defined in `knowledge_structure.md` (SSOT).**
> Update this schema when domain scope changes.

## Domain

Technical knowledge for hardware, software, programming, electronics, networking, OS, and AI.
Covers devices, libraries, frameworks, protocols, algorithms, procedures, and comparisons.

## Conventions

- **File names:** lowercase, hyphens, no spaces (e.g., `esp32-pinout.md`, `transformer-architecture.md`)
- **Every page starts with YAML frontmatter** (see schema below)
- **Use `[[wikilinks]]`** to link between pages (minimum 2 outbound links per active page; exactly 1 for device entities: board ↔ MCU)
- **Bump `updated` date** on every modification
- **Every new page must be added** to the correct category index AND master index
- **Every action appended to log** (not implemented in this version — per-page changelog used)
- **Provenance markers:** On pages synthesizing 3+ sources, append `^[sources/source-file.md]` at end of paragraphs tracing to specific source

## Frontmatter Schema

```yaml
---
title: Page Title                    # Required: Human-readable title
created: YYYY-MM-DD                  # Required: Creation date
updated: YYYY-MM-DD                  # Required: Last modification date
type: entity | concept | procedure | comparison | query | archive-note  # Required
category: devices | software | programming | electronics | networking | operating-systems | ai  # Required
subcategory: string                  # Required: Per knowledge_structure.md subcategories
tags: [tag1, tag2]                   # Required: From tag taxonomy below
sources:                             # Required: At least 1 for non-obvious claims
  - title: "Source Title"
    url: "https://example.com"
    date: "YYYY-MM-DD"
    type: article | paper | doc | video | spec | repo
related: [page-slug]                 # Required for active: exactly 1 for device entities (board ↔ MCU), ≥2 for all other types
supersedes: page-slug                # Optional: Page this replaces
superseded_by: page-slug             # Optional: Page that replaces this
status: active | archived | draft    # Required
confidence: high | medium | low      # Required: How well-supported claims are
version: "1.0"                       # Optional: For procedures/comparisons
---
```

### Status Values

- `active` — Current, maintained, discoverable
- `archived` — Superseded or out of scope (moved to archive/, placeholder remains)
- `draft` — Incomplete, not yet indexed

### Confidence Values

- `high` — Multiple independent sources, well-established
- `medium` — Few sources or some uncertainty
- `low` — Single source, speculative, or rapidly changing

## Tag Taxonomy

**Categories (from knowledge_structure.md — SSOT):**

| Category | Subcategories (examples) |
|----------|--------------------------|
| devices | microcontroller, sbc, sensor, actuator, tool, instrument |
| software | os, library, framework, tool, application, driver |
| programming | language, algorithm, pattern, architecture, api, protocol |
| electronics | component, circuit, pcb, power, signal, measurement |
| networking | protocol, topology, security, wireless, wired, monitoring |
| operating-systems | kernel, shell, filesystem, process, memory, container |
| ai | model, training, inference, dataset, framework, application |

**Cross-cutting Tags (use in addition to category tags):**

| Tag | When to Use |
|-----|-------------|
| `tutorial` | Step-by-step how-to |
| `reference` | Spec, datasheet, API docs |
| `comparison` | Side-by-side analysis |
| `troubleshooting` | Common issues & fixes |
| `best-practice` | Recommended patterns |
| `deprecated` | Superseded but still referenced |
| `security` | Security-related |
| `performance` | Optimization, benchmarks |
| `integration` | Connecting systems |

**Rule:** Every tag on a page must appear in this taxonomy. If new tag needed, add here first.

## Page Thresholds

- **Create a page** when entity/concept appears in 2+ sources OR is central to 1 source
- **Add to existing page** when source mentions something already covered
- **DON'T create page** for passing mentions, minor details, or out-of-domain items
- **Split page** when exceeds ~200 lines — break into sub-topics with cross-links
- **Archive page** when fully superseded — move to `archive/`, remove from indexes

## Entity Pages

One page per notable entity (device, software, person, organization).
Include: Overview, Key Facts, Details, Relationships, Sources.

## Concept Pages

One page per concept/topic (algorithm, protocol, pattern, architecture).
Include: Definition, Explanation, Key Properties, Related Concepts, Open Questions, Sources.

## Procedure Pages

One page per how-to / setup guide / workflow.
Include: Purpose, Prerequisites, Steps (with commands), Verification, Troubleshooting, Related.

## Comparison Pages

Side-by-side analyses for decision support.
Include: Purpose, Items Compared, Dimensions (table), Verdict, Related, Sources.

## Query Pages

Filed answers to research questions worth keeping.
Include: Question, Answer, Supporting Details, Related Queries, Sources, Confidence Assessment.

## Update Policy

When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older
2. If genuinely contradictory, note both positions with dates and sources
3. Mark in frontmatter: `supersedes: [old-page]` and `superseded_by: [new-page]`
4. Flag for review in lint report (contested pages surfaced)

## Raw Sources (inbox/ → documentation/ → knowledge/)

Raw sources are immutable. They live in `inbox/` during processing, then `documentation/` for reference.
Only the compiled wiki pages (this vault) are agent-owned and mutable.
Raw source frontmatter (for drift detection):
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of body only>
---
```