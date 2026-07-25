# Workspace Rules

Workspace root:
`/media/oscar/Data/workspace`

## Folder Rules

`projects/` → Active and new projects only.
`archive/` → Retired content: archived projects, superseded knowledge, processed inbox material.
`knowledge/` → Curated reusable knowledge (managed by the knowledgeWiKi skill).
`documentation/` → Raw external references and source documents.
`instructions/` → Workspace operating rules and workflows.
`inbox/` → Temporary incoming material waiting for classification.
`tasks/` → Task work folders (managed by task_workflow.md).

## Knowledge Pipeline

Raw material flows through three stages; do not skip a stage:
`inbox/` (unclassified) → `documentation/` (classified raw source) → `knowledge/` (curated page).

## General Rules

- Always read instructions before modifying workspace content.
- Never create new top-level folders without approval.
- Store information in the correct folder per the Folder Rules above.
- Before creating new content, search existing folders to avoid duplication.
- Keep markdown files focused on one topic, structured with headers and concise.
- Use kebab-case for markdown filenames (lowercase, descriptive, no spaces).
- Whether files are created depends on session mode — see AGENTS.md §4.
- Route vault file operations through the obsidian skill.
- Route knowledge operations through the knowledgeWiKi skill plus knowledge_workflow.md.
