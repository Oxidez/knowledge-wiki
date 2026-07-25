#!/usr/bin/env python3
"""
Configuration loader for knowledge-wiki skill.
Resolves paths from config file, environment variables, or Hermes workspace.
"""

import os
import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class WikiConfig:
    vault_root: Path
    inbox_root: Path
    archive_root: Path

    @property
    def workspace_root(self) -> Path:
        return self.vault_root.parent


def find_config_file() -> Optional[Path]:
    """Find the knowledge-wiki config file in standard locations."""
    candidates = [
        Path.home() / ".config" / "knowledge-wiki" / "config.yaml",
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "knowledge-wiki" / "config.yaml",
        Path.home() / ".hermes" / "skills" / "knowledge-management" / "knowledge-wiki" / "config.yaml",
        Path.cwd() / "knowledge-wiki.yaml",  # Local override
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def get_hermes_workspace() -> Optional[Path]:
    """Try to detect Hermes workspace from various sources."""
    # 1. Environment variable (set by Hermes or user)
    for env_var in ("HERMES_WORKSPACE", "HERMES_WORKSPACE_PATH", "KNOWLEDGE_VAULT_ROOT"):
        if val := os.environ.get(env_var):
            return Path(val).expanduser().resolve()

    # 2. Hermes config file (~/.hermes/config.yaml)
    hermes_config = Path.home() / ".hermes" / "config.yaml"
    if hermes_config.exists():
        try:
            with open(hermes_config) as f:
                config = yaml.safe_load(f)
            # Check for workspace path in various possible locations
            if isinstance(config, dict):
                # Terminal cwd might be workspace
                if "terminal" in config and "cwd" in config["terminal"]:
                    cwd = config["terminal"]["cwd"]
                    if cwd and cwd != ".":
                        return Path(cwd).expanduser().resolve()
        except Exception:
            pass

    # 3. Check if we're running from a known workspace (has AGENTS.md)
    cwd = Path.cwd()
    if (cwd / "AGENTS.md").exists():
        return cwd.resolve()

    # 4. Walk up from cwd to find AGENTS.md
    for parent in cwd.parents:
        if (parent / "AGENTS.md").exists():
            return parent.resolve()

    return None


def load_config() -> WikiConfig:
    """
    Load configuration with priority:
    1. Config file (~/.config/knowledge-wiki/config.yaml)
    2. Environment variables (KNOWLEDGE_VAULT_ROOT, KNOWLEDGE_INBOX_ROOT, KNOWLEDGE_ARCHIVE_ROOT)
    3. Hermes workspace detection + standard subfolder structure
    4. Default fallback (~/.hermes-workspace/knowledge)
    """
    # Default relative to workspace
    default_workspace = Path.home() / "hermes-workspace"

    # Start with defaults
    vault_root = default_workspace / "knowledge"
    inbox_root = default_workspace / "inbox"
    archive_root = default_workspace / "archive"

    # 1. Try config file
    config_file = find_config_file()
    if config_file:
        try:
            with open(config_file) as f:
                cfg = yaml.safe_load(f) or {}
            if "vault_root" in cfg:
                vault_root = Path(cfg["vault_root"]).expanduser().resolve()
            if "inbox_root" in cfg:
                inbox_root = Path(cfg["inbox_root"]).expanduser().resolve()
            if "archive_root" in cfg:
                archive_root = Path(cfg["archive_root"]).expanduser().resolve()
        except Exception:
            pass

    # 2. Environment variables override config file
    if env_vault := os.environ.get("KNOWLEDGE_VAULT_ROOT"):
        vault_root = Path(env_vault).expanduser().resolve()
    if env_inbox := os.environ.get("KNOWLEDGE_INBOX_ROOT"):
        inbox_root = Path(env_inbox).expanduser().resolve()
    if env_archive := os.environ.get("KNOWLEDGE_ARCHIVE_ROOT"):
        archive_root = Path(env_archive).expanduser().resolve()

    # 3. Hermes workspace detection (if vault_root still default)
    if vault_root == default_workspace / "knowledge":
        hermes_ws = get_hermes_workspace()
        if hermes_ws:
            vault_root = hermes_ws / "knowledge"
            inbox_root = hermes_ws / "inbox"
            archive_root = hermes_ws / "archive"

    # Ensure paths exist
    for p in (vault_root, inbox_root, archive_root):
        p.mkdir(parents=True, exist_ok=True)

    return WikiConfig(
        vault_root=vault_root,
        inbox_root=inbox_root,
        archive_root=archive_root,
    )


# Global config instance (loaded once)
_CONFIG: Optional[WikiConfig] = None


def get_config() -> WikiConfig:
    """Get global config instance (lazy load)."""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = load_config()
    return _CONFIG


def reload_config() -> WikiConfig:
    """Force reload config (e.g., after env change)."""
    global _CONFIG
    _CONFIG = load_config()
    return _CONFIG


if __name__ == "__main__":
    cfg = get_config()
    print(f"Vault root: {cfg.vault_root}")
    print(f"Inbox root: {cfg.inbox_root}")
    print(f"Archive root: {cfg.archive_root}")
    print(f"Workspace root: {cfg.workspace_root}")