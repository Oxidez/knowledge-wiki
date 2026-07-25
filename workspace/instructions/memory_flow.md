# Memory Flow

## Purpose

Define how agents use persistent memory in this workspace.

## Memory Systems

| System | Purpose | Scope | Access |
|--------|---------|-------|--------|
| Knowledge vault (`knowledge/`) | Technical facts, procedures, references, documentation | Workspace-shared, versioned, structured | Explicit via knowledge-wiki skill, obsidian skill |
| Workspace files (`instructions/`, `AGENTS.md`, task/project files) | Rules, workflows, project state, preferences | Workspace-shared, explicit | Read/write via file tools |
| External memory (Mnemosyne, Mem0, Hindsight, etc.) | Preferences, identity, corrections, personal facts, workflow lessons | Agent-profile-private, associative, semantic | Automatic (injected by Hermes) or via memory tools |

## Rules

- **Technical knowledge → knowledge vault** (never external memory or workspace instruction files).
- **Workspace preferences/corrections → workspace files** (e.g., `instructions/`, `AGENTS.md`, task files).
- **Agent-profile preferences/identity/corrections → external memory** (if installed and configured).
- Do not store temporary tasks, troubleshooting steps, or conversation details in external memory.
- Do not infer permanent preferences from conversations without explicit user confirmation.

## Before Creating Memory

Verify:
- Is this information useful beyond the current session?
- Should it be stored in knowledge vault, workspace files, or external memory?
- Did the user explicitly request storage in external memory?
- Is this a fact or stable preference?

## External Memory (If Present)

If an external memory system is installed (e.g., Mnemosyne, Mem0, Hindsight):
- It handles agent-profile-private preferences, identity, corrections, workflow lessons automatically.
- Agents do not need to explicitly manage it — Hermes injects relevant memories into prompts.
- Use memory tools (`mnemosyne_remember`, `mnemosyne_recall`, etc.) only when the user explicitly asks to store/recall something specific.

## Memory Management

- Verify destructive memory operations after completion.
- Do not use consolidation as a deletion method.
- The knowledge vault is the source of truth for technical information.