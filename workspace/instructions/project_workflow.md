# Project Workflow

Project root → `/media/oscar/Data/workspace/projects`

## Purpose

Single entry point for Project mode. Orchestrates multi-step work, coordinates sub-tasks, with explicit handoff to Knowledge Workflow when reusable knowledge is produced.

## Project Evaluation

Before creation:

1. Confirm the request is a project.
2. Refine requirements with the user when needed.
3. Define the project scope before creating the project folder.

## New Project

1. Create project folder under `projects/`.
2. Create `PROJECT_STATUS.md` containing the current project state.
3. Store project files inside the project folder.

## Existing Project

1. Locate project in → `projects/`.
2. Read `PROJECT_STATUS.md`.
3. Read project context.
4. Continue from current state.

## Project Rules

- Keep all project-specific files inside the project folder.
- Do not store project files in knowledge.
- Do not store raw references in projects.
- **If the project produces reusable knowledge**: execute Knowledge Handoff (see below).
- Keep project documentation with the project.
- Update `PROJECT_STATUS.md` with project status and evolution after relevant changes.
- Do not create a project folder before requirements are sufficiently defined.
- **Sub-tasks**: Each sub-task is a Task. Follow `instructions/task_workflow.md` for each sub-task.

## Knowledge Handoff

When a project produces reusable knowledge (technical facts, procedures, references, validated research):

1. **Extract** the knowledge content from project results.
2. **Prepare payload** for Knowledge Workflow:
   - Subject: Primary topic
   - Content: Structured knowledge to store
   - Sources: References, URLs, documents used
   - Category hint: Suggested category from `knowledge_structure.md`
   - Origin: This project's ID/folder name
3. **Execute** `instructions/knowledge_workflow.md` with the payload.
4. **Record** the handoff result in the project file (link to created knowledge file).

## Completion

1. Update `PROJECT_STATUS.md` before archiving the project.
2. At user request, finished projects are moved to → `/media/oscar/Data/workspace/archive`
