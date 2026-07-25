# Knowledge Workflow

## Purpose

Define how agents acquire, process, validate, and store reusable knowledge in the knowledge vault.

## When This Workflow Runs

**Explicit handoff** from:
- Task Workflow (when a task produces reusable knowledge)
- Project Workflow (when a project produces reusable knowledge)
- User request to create/update knowledge

**Not** automatically triggered by every task — only when reusable knowledge output is identified.

---

## Knowledge Workflow Overview

1. **Receive knowledge payload** from handoff (extracted knowledge, sources, context).
2. **Classify** the knowledge per `knowledge_structure.md` (category, subcategory).
3. **Validate** the knowledge (verify facts, check sources, ensure completeness).
4. **Create/Update** the knowledge file in `knowledge/<category>/<subcategory>/`.
5. **Index** the knowledge via knowledgeWiKi skill.
6. **Record** the handoff completion in the originating task/project.

---

## Step 1: Receive Knowledge Payload

The handoff provides:
- **Subject**: Primary topic of the knowledge.
- **Content**: Structured knowledge to store (already processed/validated by originator).
- **Sources**: References, URLs, documents used.
- **Category hint**: Suggested category from `knowledge_structure.md`.
- **Origin**: Task or project ID that produced this knowledge.

---

## Step 2: Classify per knowledge_structure.md

1. Identify the primary subject.
2. Select the appropriate category from `knowledge_structure.md`:
   - `devices/` — Hardware, boards, sensors, actuators, peripherals
   - `software/` — Applications, tools, frameworks, software systems
   - `programming/` — Languages, libraries, APIs, development techniques
   - `electronics/` — Components, circuits, interfaces, electrical concepts
   - `networking/` — Network technologies, protocols, communication systems
   - `operating-systems/` — OS administration, configuration, troubleshooting
   - `ai/` — Artificial intelligence, machine learning, LLMs, AI tools
3. Determine subcategory if multiple related files justify it.
4. If no suitable category exists → **request approval** before creating new top-level category.

---

## Step 3: Validate Knowledge

Before writing to knowledge vault:
- Verify technical details and important facts against sources.
- Ensure content is concise, structured, focused on one topic.
- Avoid: copying complete documents, unnecessary explanations, duplicate information.
- Prefer official documentation and primary sources.
- Record relevant sources in the knowledge file.

---

## Step 4: Create/Update Knowledge File

**Location**: `knowledge/<category>/<subcategory>/<topic>.md`

**File requirements**:
- Clear title describing the subject.
- Concise description when useful.
- Structured content organized by topic.
- Relevant sources cited.
- Review date when information may become outdated.
- Use links to related knowledge files when useful.

**Naming**: kebab-case, lowercase, descriptive, no spaces.

---

## Step 5: Index via knowledge-wiki Skill

After creating/updating the knowledge file, call the **knowledge-wiki skill** explicitly:

```python
# Agent executes this via the skill interface:
result = knowledge_wiki.index_update(
    page_path="<relative/path/from/knowledge/root.md>",
    category="<category from knowledge_structure.md>",
    action="create"  # or "update" or "archive"
)
```

**Parameters:**
- `page_path`: Relative path from `/media/oscar/Data/workspace/knowledge/` (e.g., `devices/entities/arduino-uno.md`)
- `category`: One of the 7 categories from `knowledge_structure.md` (devices, software, programming, electronics, networking, operating-systems, ai)
- `action`: `"create"` | `"update"` | `"archive"`

**Expected Return (for Step 6):**
```json
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

**Automatic checks performed by skill:**
- Duplicate detection (title, entity match, content similarity, naming conflicts)
- Inconsistency checks (broken wikilinks, missing frontmatter, tag violations, orphans, index completeness)
- Results included in `duplicates_found` and `warnings` fields

If `success: false`, check `errors` and re-run Step 4 before proceeding.

---

## Step 6: Record Handoff Completion

Update the originating task/project file:
- Note that knowledge was extracted and stored.
- Link to the created knowledge file.
- Close the knowledge handoff loop.

---

## Tool Roles

| Tool | Role |
|------|------|
| SearXNG | Find external information (not for knowledge storage). |
| Obsidian skill | File operations: read, write, search vault. |
| knowledgeWiKi skill | Create indexes, relationships; does not replace source files. |
| Agent | Orchestrate workflow, classify, validate, decide. |

---

## Memory Separation

Follow `memory_flow.md`:
- **Knowledge vault** = reusable information (technical facts, procedures, references).
- **External memory** (if present) = stable preferences, identity, corrections, workflow lessons.
- Do NOT store technical knowledge in external memory.

---

## Classification Reference

See `knowledge_structure.md` for full category/subcategory definitions and examples.
