# Task Workflow

Task root → `/media/oscar/Data/workspace/tasks`

## Purpose

Single entry point for Task mode. Orchestrates the task from evaluation to completion, with explicit handoff to Knowledge Workflow when reusable knowledge is produced.

## Task Evaluation

Before execution:

1. Confirm the request is a task and not a project.
2. Ask for clarification when required information is missing.
3. Identify required workflows, tools, or knowledge sources.
   - If the task requires **reading existing knowledge**: search knowledge vault via Obsidian skill.
   - If the task requires **external research**: use SearXNG or other search tools.
   - If the task **produces reusable knowledge**: plan for Knowledge Workflow handoff at completion.

## Task Creation

1. Create a task folder under `tasks/` when results need to be preserved.
2. Execute the requested task according to the required workflow.
3. Store task results inside the task folder.
4. Add a `<task_name>.md` file containing task information (goal, steps, results, references).

## Task Rules

- Do not create projects for tasks.
- Keep task-specific files inside the task folder.
- Do not store reusable knowledge in tasks.
- **If reusable knowledge is produced**: execute Knowledge Handoff (see below).

## Knowledge Handoff

When a task produces reusable knowledge (technical facts, procedures, references, validated research):

1. **Extract** the knowledge content from task results.
2. **Prepare payload** for Knowledge Workflow:
   - Subject: Primary topic
   - Content: Structured knowledge to store
   - Sources: References, URLs, documents used
   - Category hint: Suggested category from `knowledge_structure.md`
   - Origin: This task's ID/folder name
3. **Execute** `instructions/knowledge_workflow.md` with the payload.
4. **Record** the handoff result in the task file (link to created knowledge file).

## Completion

Completed tasks remain under `tasks/` unless the user decides otherwise.
