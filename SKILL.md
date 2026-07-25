---
name: knowledge-wiki
description: Index and maintain knowledge vault for agent navigation.
category: knowledge-management
tags:
  - wiki
  - indexing
  - knowledge-base
  - duplicate-detection
  - validation
---

# knowledge-wiki

## Purpose

Maintains a searchable, navigable, consistent knowledge vault using portable path resolution via `config_loader.py`.
Provides explicit handoff interface for `knowledge_workflow.md` Step 5 (indexing after page creation/update).

## Operations

### index_update(page_path, category, action) → IndexResult

**Called by knowledge_workflow.md Step 5** after creating/updating a knowledge file.
Performs incremental index update for single page and returns discoverability confirmation.

**Parameters:**
- `page_path`: Relative path from vault root (e.g., `devices/entities/arduino-uno.md`)
- `category`: One of 7 categories from knowledge_structure.md (devices, software, programming, electronics, networking, operating-systems, ai)
- `action`: `"create"` | `"update"` | `"archive"`

**Returns:** `IndexResult` with discoverability verification for workflow Step 6.

### full_rebuild() → IndexResult

Complete vault scan → rebuild master index + all category indexes.

### validate_all() → ValidationReport

Run all quality gates: frontmatter schema, wikilinks, related links, tags, orphans, supersedes chains, page size.

### find_duplicates() → DuplicateReport

Detect duplicate entities/concepts:
- Exact title match (normalized)
- Same entity_type + category + title similarity (Levenshtein < 3)
- Similar content (simhash Hamming distance ≤ 3)
- Naming conflicts (same kebab-case filename in same folder)

### find_inconsistencies() → InconsistencyReport

Detect inconsistencies:
- Broken wikilinks
- Missing required frontmatter fields
- Tag taxonomy violations
- Orphan pages (0 inbound wikilinks)
- <2 related links for active pages
- Broken supersedes chains
- Frontmatter schema violations

### verify_discoverable(page_path) → bool

Confirm page is reachable from master index → category index → page.

## File Placement (per workspace_rules.md)

- Pages: `knowledge/<category>/<type>/<kebab-case>.md`
- Category index: `knowledge/<category>/index.md`
- Master index: `knowledge/index.md`
- Archive: `archive/<category>/<type>/...` (per archive_rules.md)
- Inbox processing: `inbox/` → `documentation/` → `knowledge/`

## Vault Path

Configurable via `~/.config/knowledge-wiki/config.yaml` or environment variables.
Defaults to workspace detection (looks for AGENTS.md or HERMES_WORKSPACE env var).

```yaml
# ~/.config/knowledge-wiki/config.yaml
vault_root: "/path/to/workspace/knowledge"
inbox_root: "/path/to/workspace/inbox"
archive_root: "/path/to/workspace/archive"
```

Or via environment:
```bash
export KNOWLEDGE_VAULT_ROOT="/path/to/workspace/knowledge"
export KNOWLEDGE_INBOX_ROOT="/path/to/workspace/inbox"
export KNOWLEDGE_ARCHIVE_ROOT="/path/to/workspace/archive"
```

Priority: config file > env vars > Hermes workspace detection > `~/hermes-workspace/knowledge`

## Dependencies

- `obsidian` skill (file read/write/search patterns via Hermes tools)
- `knowledge_structure.md` (7 categories, subcategory rules) — SSOT for categories
- `knowledge_rules.md` (naming, structure, storage roles)
- `archive_rules.md` (archive protocol)
- `memory_flow.md` (memory boundary: technical knowledge → vault, preferences → external memory if present)

## Quality Gates (enforced before status: active)

- Frontmatter complete & valid per schema
- ≥2 related wikilinks for active pages
- Sources cited for non-obvious claims
- No broken wikilinks
- Category & master indexes updated
- Supersedes chain valid
- Tags from taxonomy only
- Page size ≤ 200 lines (split if exceeded)

## Handoff Interface (knowledge_workflow.md Step 5 → Step 6)

```python
# Agent calls:
result = knowledge_wiki.index_update(
    page_path="devices/entities/arduino-uno.md",
    category="devices",
    action="create"
)

# Returns for workflow Step 6:
{
  "success": true,
  "page_path": "devices/entities/arduino-uno.md",
  "master_index_updated": true,
  "category_index_updated": true,
  "category_index_path": "devices/index.md",
  "discoverable": true,
  "related_links_added": 3,
  "duplicates_found": [],
  "warnings": [],
  "errors": []
}
```

## Automatic Duplicate & Inconsistency Detection

Runs automatically on every `index_update()`:
- Duplicate check on new/updated page
- Inconsistency check on affected category
- Results included in `IndexResult` for workflow recording

## Templates

Located in `templates/`:
- `entity-page.md` — Devices, software, people, organizations
- `concept-page.md` — Programming concepts, algorithms, protocols
- `procedure-page.md` — How-to, setup guides, workflows
- `comparison-page.md` — Side-by-side analyses
- `query-page.md` — Filed research answers
- `category-index.md` — Sectioned by page type
- `master-index.md` — Top-level catalog with recent additions
- `archive-note.md` — Archive placeholder with original path
- `schema-template.md` — Frontmatter schema + tag taxonomy (references knowledge_structure.md)

## Scripts

Located in `scripts/`:
- `indexer.py` — Core indexing operations
- `validator.py` — Quality gates validation
- `duplicate_finder.py` — Multi-signal duplicate detection
- `inconsistency_checker.py` — Inconsistency detection
- `converter.py` — PDF/DOCX/XLSX → markdown extraction

## Requirements

```
pyyaml>=6.0
simhash>=2.1
python-Levenshtein>=0.25
marker-pdf>=1.0
python-docx>=1.1
openpyxl>=3.1
```