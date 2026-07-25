Agent Workspace Rules

Global rules for every agent operating in this workspace
(/media/oscar/Data/workspace). Highest priority over all other instructions.

1. Startup Sequence

Run this exact sequence at the start of every session, before any action:
  a. Read instructions/INDEX.md to map available instruction files.
  b. Read instructions/workspace_rules.md to understand workspace structure and file placement rules.
  c. Determine the session mode from the user's intent (section 2).
  d. Read the instruction file that matches the session mode.
  e. Load only the skills the work requires. If the work touches the knowledge
     vault, load the obsidian skill (filesystem interface) and the knowledgeWiKi
     skill (knowledge acquisition, indexing, maintenance). Do not load skills
     you will not use.

2. Session Modes

Route the session to exactly one primary mode. The agent must restate which mode
governs the current action. A session may shift modes; when it does, restate the mode.

  Chat
      General conversation, Q&A, brainstorming. No workspace modification is intended.
      - Instruction file: none required.
      - Do not create or modify workspace files unless the user explicitly asks.
      - May read files, search, and answer from context.
      - If the conversation surfaces a durable fact or preference, **ask the user
        if they want it stored in workspace files or the knowledge vault**.
        Session context may be used for temporary context within the chat.
    - Instruction file: instructions/task_workflow.md
    - Knowledge work is a Task. Researching, capturing, or organizing the vault
      (for example "Analyze arduino.pdf from inbox and create knowledge from it")
      is one task, executed per task_workflow.md. It does not become a project.

  Project
    Multi-step work that the user explicitly requests as a project.
    - Instruction file: instructions/project_workflow.md
    - Only create a project when the user asks for one. Do not promote a task to a
      project on your own initiative.
    - Example: "Create a project for an electronic leadscrew controller to operate
      a hobby lathe." This spans several tasks, each run per task_workflow.md,
      coordinated by project_workflow.md.
    - Active project work lives under projects/ per workspace_rules.md.

3. Within-Session Behavior

Regardless of mode:
  - State your plan before acting on non-trivial steps.
  - Use checkpoints: pause for user confirmation at milestones
    (task: acceptance criteria; project: phase boundaries).
  - Verify work against stated criteria before declaring done.
  - Prefer documented skills and workflows over ad-hoc approaches.
  - Route vault file operations through the obsidian skill.
  - Route knowledge operations through the knowledgeWiKi skill plus
    knowledge_workflow.md.
  - Do not assume. If intent, scope, or a rule is ambiguous, ask before proceeding.

4. File Placement

File creation and movement follow instructions/workspace_rules.md. Session mode
determines whether files are created at all:
  - Chat:     do not create workspace files unless the user explicitly requests it.
  - Task:     placement governed by task_workflow.md and workspace_rules.md.
  - Project:  placement governed by project_workflow.md and workspace_rules.md.
              Active work lives under projects/.
Do not create undocumented top-level directories.

5. Priority Order

  1. AGENTS.md (this file)
  2. instructions/
  3. Task or project instructions
  4. Agent profile
  5. User request

Lower-priority sources never override higher-priority ones.

6. Memory

Technical knowledge belongs in the knowledge/ vault. Workspace preferences and corrections are managed through workspace files and the knowledge vault structure.

7. Conflict Resolution

  - Higher priority always wins (section 5).
  - Never silently override a workspace rule.
  - If two instructions conflict, state the conflict and ask the user.

8. Autonomous Change Guardrails

Do not perform these without explicit user approval:
  - Create or modify skills
  - Modify profiles
  - Modify instruction files (instructions/)
  - Change workspace rules (this file)
  - Change memory workflows
  - Make permanent workspace changes as part of a temporary task

9. Session Close

Before ending a session:
  - If a knowledge artifact was produced, ensure indexes and frontmatter are updated.
  - Summarize what was done and what remains open.
