# knowledge-wiki Skill — Portable Install Package

This package contains everything needed to install the **knowledge-wiki** skill on any computer with Hermes Agent installed.

---

## Why This Skill Exists

The original **LLM Wiki** (by Andrej Karpathy) and **LLM Wiki V2** (by Rohit G) are excellent methodologies for *personal* knowledge bases:
- [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 3 page types, wikilink-based linking
- [LLM Wiki V2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) — adds confidence scores, supersession chains, memory lifecycle

**But they lack:**
- Governance (no workspace rules, no agent workflow integration)
- Quality enforcement (no validation, duplicate detection, inconsistency checking)
- Agent operability (standalone tools, not callable via skill interface)
- Portability (hardcoded paths, no installer)
- Structured taxonomy (free-form categories)

**knowledge-wiki** was built to fill these gaps for a **team/agent workspace** where:
- Agents must *reliably* find, create, and maintain knowledge
- Quality gates are non-negotiable (validator, duplicates, inconsistencies)
- Installation is "run once, works everywhere" (config.yaml + workspace template)
- Workflows are formal (AGENTS.md → task_workflow → knowledge_workflow → skill handoff)

---

## Comparison: knowledge-wiki vs LLM Wiki / LLM Wiki V2

### Core Philosophy

| Aspect | LLM Wiki (Karpathy) | LLM Wiki V2 (rohitg00) | **knowledge-wiki (ours)** |
|--------|---------------------|------------------------|---------------------------|
| **Purpose** | Personal knowledge base for LLMs | Evolved methodology with memory lifecycle | **Workspace-integrated, agent-usable vault** |
| **Architecture** | 3 page types (Entity, Concept, Procedure) | 3 types + confidence + supersession | **7 categories × 6 page types = 42 combinations** |
| **Governance** | None (personal) | None (personal) | **AGENTS.md → instructions/ → skill (enforced)** |
| **Agent Integration** | Manual | Manual | **Hermes skill interface + knowledge_workflow.md handoff** |

### Page Types

| Type | LLM Wiki | LLM Wiki V2 | **knowledge-wiki** |
|------|----------|-------------|-------------------|
| Entity | ✅ | ✅ | ✅ (devices, software, people, orgs) |
| Concept | ✅ | ✅ | ✅ (algorithms, protocols, theories) |
| Procedure | ✅ | ✅ | ✅ (how-to, setup, workflows) |
| Comparison | ❌ | ❌ | ✅ (side-by-side analyses) |
| Query | ❌ | ❌ | ✅ (filed research answers) |
| Archive Note | ❌ | ❌ | ✅ (superseded placeholders) |

### Structural Innovations (Ours)

| Feature | LLM Wiki | LLM Wiki V2 | **knowledge-wiki** |
|---------|----------|-------------|-------------------|
| **Fixed Categories (7)** | ❌ Free-form | ❌ Free-form | ✅ SSOT in `knowledge_structure.md` |
| **Subcategory Rules** | ❌ | ❌ | ✅ Entity constraint: exactly 1 `related` link |
| **Cross-reference Enforcement** | Wikilinks only | Wikilinks + typed edges | **Validator: broken links, orphans, schema** |
| **Duplicate Detection** | ❌ | ❌ | ✅ Multi-signal (title, content, wikilinks, tags) |
| **Inconsistency Detection** | ❌ | ❌ | ✅ 8 check types (broken links, tags, frontmatter, index sync) |
| **Auto-index Rebuild** | Manual | Manual | ✅ `full_rebuild()` with discoverability check |
| **Portable Config** | ❌ | ❌ | ✅ `config.yaml` via env/auto-detect/defaults |
| **Workspace Template** | ❌ | ❌ | ✅ Bundled AGENTS.md + instructions/ + knowledge/ |

### Agent Workflow Integration (Ours Only)

```
User Task
    ↓
AGENTS.md §2 (Task mode)
    ↓
task_workflow.md → Knowledge Handoff (Step 5)
    ↓
knowledge_workflow.md (6 steps)
    ↓
Step 5: knowledge-wiki skill via Hermes interface
    ↓
IndexResult payload (category, pages, discoverable, validation_status)
    ↓
Agent continues with verified knowledge map
```

**Key differentiator:** The skill is **callable via Hermes skill interface** from a formal workflow handoff, not a standalone tool.

### Quality Gates (Ours Only)

| Gate | Trigger | Blocks |
|------|---------|--------|
| **Validator** | `index_update` / `full_rebuild` | Invalid frontmatter, broken wikilinks, missing `related`, tag violations, page too large |
| **Inconsistency Checker** | On demand / CI | Broken links, orphans, schema drift, index staleness, circular refs |
| **Duplicate Finder** | On demand / per-page | Near-duplicate titles, content similarity, wikilink overlap |
| **Discoverability Check** | `full_rebuild` | Master index reachable, category indexes consistent |

### What We Borrowed

| From LLM Wiki | From LLM Wiki V2 |
|---------------|------------------|
| Wikilink-based linking (`[[page]]`) | Confidence scores in frontmatter |
| Entity → Concept → Procedure flow | Supersession chains (`supersedes:`) |
| Category indexes | Typed knowledge graph (our `related` + templates) |

### What We Added (Workspace-Native)

1. **Governance layer** — AGENTS.md + 8 instruction files
2. **Handoff protocol** — Explicit payload between workflows
3. **Skill interface** — Hermes-callable with typed results
4. **Template system** — 9 page templates with enforced frontmatter
5. **Document conversion** — PDF/DOCX/XLSX → markdown
6. **Portable installation** — Auto-detect, workspace template, cross-platform
7. **Category taxonomy** — 7 fixed, subcategories extensible (SSOT)

---

## Contents

```
knowledge-wiki/
├── install.sh              # Linux/macOS installer
├── install.bat             # Windows installer
├── SKILL.md                # Skill manifest
├── config.yaml.example     # Config template
├── scripts/
│   ├── config_loader.py    # Portable path resolution
│   ├── indexer.py          # Core indexing
│   ├── validator.py        # Quality gates
│   ├── duplicate_finder.py # Duplicate detection
│   ├── inconsistency_checker.py # Inconsistency detection
│   ├── converter.py        # Document conversion (PDF/DOCX/XLSX)
│   ├── setup.py            # Post-install configuration
│   └── requirements.txt    # Python dependencies
├── templates/
│   ├── entity-page.md      # Devices, software, people, orgs
│   ├── concept-page.md     # Concepts, algorithms, protocols
│   ├── procedure-page.md   # How-to, setup guides, workflows
│   ├── comparison-page.md  # Side-by-side analyses
│   ├── query-page.md       # Filed research answers
│   ├── category-index.md   # Category indexes
│   ├── master-index.md     # Top-level catalog
│   ├── archive-note.md     # Archive placeholders
│   └── schema-template.md  # Frontmatter schema + tag taxonomy
└── workspace/              # Complete workspace template (copied on install)
    ├── AGENTS.md           # Workspace constitution
    ├── instructions/       # All 8 instruction files
    ├── knowledge/          # 7-category vault with indexes + 4 device pages
    │   ├── devices/
    │   ├── software/
    │   ├── programming/
    │   ├── electronics/
    │   ├── networking/
    │   ├── operating-systems/
    │   └── ai/
    ├── inbox/              # Raw input processing
    ├── archive/            # Archived pages
    ├── tasks/              # Task-mode work
    ├── projects/           # Project-mode work
    └── documentation/notes/
```

## Quick Install

### Linux / macOS
```bash
cd knowledge-wiki
chmod +x install.sh
./install.sh
```

### Windows (Command Prompt)
```cmd
cd knowledge-wiki
install.bat
```

### Windows (PowerShell)
```powershell
cd knowledge-wiki
.\install.bat
```

## What the Installer Does

1. **Checks prerequisites** — Hermes config (`~/.hermes/config.yaml`), Python 3.8+
2. **Copies skill** → `~/.hermes/skills/knowledge-management/knowledge-wiki/`
3. **Installs Python deps** — Core: `pyyaml`, `simhash`, `python-Levenshtein`
4. **Runs setup** — Auto-detects workspace, creates `~/.config/knowledge-wiki/config.yaml`
5. **Copies workspace template** — Creates full workspace structure in detected location

## Post-Install

1. Restart Hermes or reload skills
2. Skill appears as `knowledge-wiki`
3. Config file: `~/.config/knowledge-wiki/config.yaml` (edit anytime)
4. Workspace created at detected location with:
   - AGENTS.md (constitution)
   - instructions/ (8 workflow files)
   - knowledge/ (7 categories, indexes, 4 device pages)
   - inbox/, archive/, tasks/, projects/

## Config Priority

1. `~/.config/knowledge-wiki/config.yaml`
2. Env vars: `KNOWLEDGE_VAULT_ROOT`, `KNOWLEDGE_INBOX_ROOT`, `KNOWLEDGE_ARCHIVE_ROOT`
3. Hermes workspace detection (AGENTS.md, `~/.hermes/config.yaml`, `HERMES_WORKSPACE`)
4. Default: `~/hermes-workspace/`

## Requirements

- Hermes Agent installed and configured
- Python 3.8+
- pip

Optional (for document conversion):
- `pymupdf` (PDF)
- `python-docx` (DOCX)
- `openpyxl` (XLSX)

## Skill Operations (via Hermes)

```python
# Index a new/updated page
result = knowledge_wiki.index_update(
    page_path="devices/boards/arduino-uno.md",
    category="devices",
    action="create"
)

# Full rebuild
result = knowledge_wiki.full_rebuild()

# Validate all pages
report = knowledge_wiki.validate_all()

# Find duplicates
report = knowledge_wiki.find_duplicates()

# Find inconsistencies
report = knowledge_wiki.find_inconsistencies()
```

## Workspace Structure

Follows `workspace_rules.md` and `knowledge_structure.md`:

| Folder | Purpose |
|--------|---------|
| `knowledge/<category>/<subcategory>/` | Knowledge pages (7 fixed categories) |
| `inbox/` | Raw inputs (PDFs, docs, web saves) |
| `documentation/` | Processed references |
| `archive/` | Superseded pages |
| `tasks/` | Task-mode work files |
| `projects/` | Project-mode work |

## Categories (Fixed — from knowledge_structure.md)

1. `devices` — boards, microcontrollers, sensors, actuators, tools, instruments
2. `software` — os, library, framework, tool, application, driver
3. `programming` — language, algorithm, pattern, architecture, api, protocol
4. `electronics` — component, circuit, pcb, power, signal, measurement
5. `networking` — protocol, topology, security, wireless, wired, monitoring
6. `operating-systems` — kernel, shell, filesystem, process, memory, container
7. `ai` — model, training, inference, dataset, framework, application

> **Note:** The 7 top-level categories are fixed (SSOT in `knowledge_structure.md`). Subcategories can be extended per-category. When creating new pages, the agent **must ask the user for category/subcategory** if not specified in the task request.

### Adding New Subcategories

**Method:** Create a new folder under the category directory, then run `full_rebuild()`.

**Example — Adding `sensors/` under `devices/`:**

```bash
# 1. Create subcategory folder
mkdir -p ~/hermes-workspace/knowledge/devices/sensors

# 2. Create first sensor page (e.g., from template)
cp templates/entity-page.md ~/hermes-workspace/knowledge/devices/sensors/bme280.md
# Edit frontmatter: category: devices, subcategory: sensors, related: []

# 3. Rebuild indexes (agent does this, or run manually)
python3 -m knowledge_wiki full_rebuild
```

**What happens on rebuild:**
- Master index (`knowledge/index.md`) updated with new category entry
- Category index (`knowledge/devices/index.md`) updated with `sensors/` section
- All cross-references validated
- Discoverability check passes

> **Note:** Index rebuild is **not automatic** on folder creation. It runs:
> - At user/agent request via `full_rebuild()`
> - After `index_update()` for new/updated pages
> - In CI/CD if configured

## License

MIT — Use freely in your Hermes workspace.