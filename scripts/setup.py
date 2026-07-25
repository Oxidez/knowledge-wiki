#!/usr/bin/env python3
"""
Setup script for knowledge-wiki skill.
Run once after installing the skill on a new machine.
Creates ~/.config/knowledge-wiki/config.yaml with auto-detected paths.
Also copies the workspace template if workspace doesn't exist.
"""

import os
import sys
import yaml
import shutil
import argparse
from pathlib import Path


def find_hermes_workspace() -> Path:
    """Try to detect Hermes workspace."""
    # 1. Environment variable
    for env_var in ("HERMES_WORKSPACE", "HERMES_WORKSPACE_PATH", "KNOWLEDGE_VAULT_ROOT"):
        if val := os.environ.get(env_var):
            p = Path(val).expanduser().resolve()
            if p.exists():
                if p.name == "knowledge":
                    return p.parent
                return p

    # 2. Hermes config
    hermes_config = Path.home() / ".hermes" / "config.yaml"
    if hermes_config.exists():
        try:
            with open(hermes_config) as f:
                config = yaml.safe_load(f) or {}
            if isinstance(config, dict):
                terminal = config.get("terminal", {})
                cwd = terminal.get("cwd", ".")
                if cwd != ".":
                    p = Path(cwd).expanduser().resolve()
                    if p.exists():
                        return p
        except Exception:
            pass

    # 3. AGENTS.md marker (walk up from cwd)
    search_dirs = [
        Path(__file__).parent.parent.parent.parent.parent.parent,  # ~/.hermes/skills/... -> home
        Path.cwd(),
    ]
    for base in search_dirs:
        try:
            base_resolved = base.resolve()
            for parent in [base_resolved] + list(base_resolved.parents):
                if (parent / "AGENTS.md").exists():
                    if parent.name == "knowledge":
                        return parent.parent
                    return parent
        except Exception:
            pass

    # 4. Default
    return Path.home() / "hermes-workspace"


def copy_workspace_template(target_workspace: Path, template_dir: Path):
    """Copy workspace template to target location, skipping existing files."""
    print(f"\nCopying workspace template to: {target_workspace}")
    
    for src in template_dir.rglob("*"):
        if src.is_file():
            rel = src.relative_to(template_dir)
            dst = target_workspace / rel
            
            if dst.exists():
                print(f"  Exists (skipped): {rel}")
                continue
            
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  Created: {rel}")


def main():
    parser = argparse.ArgumentParser(description="knowledge-wiki skill setup")
    parser.add_argument("--auto", action="store_true", 
                       help="Non-interactive mode: accept all defaults")
    parser.add_argument("--workspace", type=str,
                       help="Override workspace path")
    parser.add_argument("--vault", type=str,
                       help="Override vault root path")
    parser.add_argument("--inbox", type=str,
                       help="Override inbox root path")
    parser.add_argument("--archive", type=str,
                       help="Override archive root path")
    args = parser.parse_args()
    
    print("=" * 60)
    print("knowledge-wiki Skill Setup")
    print("=" * 60)

    # Locate template directory (next to this script)
    template_dir = Path(__file__).parent.parent / "workspace"
    if not template_dir.exists():
        print(f"ERROR: Workspace template not found at {template_dir}")
        return 1

    # Detect workspace
    if args.workspace:
        workspace = Path(args.workspace).expanduser().resolve()
        print(f"\nUsing workspace: {workspace}")
    else:
        workspace = find_hermes_workspace()
        print(f"\nDetected workspace: {workspace}")

    # Create workspace directory
    workspace.mkdir(parents=True, exist_ok=True)
    
    # Copy workspace template
    copy_workspace_template(workspace, template_dir)
    
    # Determine paths
    if args.vault:
        vault_root = Path(args.vault).expanduser().resolve()
    else:
        vault_root = workspace / "knowledge"
    
    if args.inbox:
        inbox_root = Path(args.inbox).expanduser().resolve()
    else:
        inbox_root = workspace / "inbox"
    
    if args.archive:
        archive_root = Path(args.archive).expanduser().resolve()
    else:
        archive_root = workspace / "archive"

    print(f"\nConfigured paths:")
    print(f"  Vault root:   {vault_root}")
    print(f"  Inbox root:   {inbox_root}")
    print(f"  Archive root: {archive_root}")

    # Interactive confirmation (unless --auto)
    if not args.auto:
        choice = input("\nOptions:\n  [Enter] Accept\n  [c] Custom paths\n  [w] Change workspace only\n  [q] Quit\n\nChoice: ").strip().lower()
        
        if choice == "q":
            print("Aborted.")
            return 1
        elif choice == "c":
            vault_root = Path(input(f"Vault root [{vault_root}]: ").strip() or vault_root).expanduser().resolve()
            inbox_root = Path(input(f"Inbox root [{inbox_root}]: ").strip() or inbox_root).expanduser().resolve()
            archive_root = Path(input(f"Archive root [{archive_root}]: ").strip() or archive_root).expanduser().resolve()
        elif choice == "w":
            workspace = Path(input(f"Workspace root [{workspace}]: ").strip() or workspace).expanduser().resolve()
            vault_root = workspace / "knowledge"
            inbox_root = workspace / "inbox"
            archive_root = workspace / "archive"

    # Create directories
    for p in (vault_root, inbox_root, archive_root):
        p.mkdir(parents=True, exist_ok=True)
        print(f"Created: {p}")

    # Write config
    config_dir = Path.home() / ".config" / "knowledge-wiki"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.yaml"

    config = {
        "vault_root": str(vault_root),
        "inbox_root": str(inbox_root),
        "archive_root": str(archive_root),
    }

    with open(config_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    print(f"\n✅ Config written to: {config_file}")
    print(f"\nYou can edit it later: {config_file}")
    print("\nDone! The skill is ready to use.")
    print("\nNext steps:")
    print("  1. Restart Hermes or reload skills")
    print("  2. Skill available as 'knowledge-wiki'")
    print(f"  3. Workspace created at: {workspace}")

    return 0


if __name__ == "__main__":
    sys.exit(main())