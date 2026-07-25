#!/usr/bin/env python3
"""
Core indexing operations for knowledge-wiki skill.
"""

import os
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set
from collections import defaultdict
from datetime import datetime

# Import config loader
import sys
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import get_config, WikiConfig

# Load config
CONFIG = get_config()
VAULT_ROOT = CONFIG.vault_root
INBOX_ROOT = CONFIG.inbox_root
ARCHIVE_ROOT = CONFIG.archive_root

VALID_CATEGORIES = [
    "devices", "software", "programming", "electronics",
    "networking", "operating-systems", "ai"
]

VALID_TYPES = ["entity", "concept", "procedure", "comparison", "query", "archive-note"]
VALID_STATUSES = ["active", "archived", "draft"]
VALID_CONFIDENCES = ["high", "medium", "low"]


@dataclass
class PageInfo:
    path: str
    title: str
    summary: str
    category: str
    type: str
    status: str
    updated: str
    tags: List[str]
    related: List[str]
    supersedes: Optional[str]
    superseded_by: Optional[str]


@dataclass
class IndexResult:
    success: bool
    page_path: str
    master_index_updated: bool
    category_index_updated: bool
    category_index_path: str
    discoverable: bool
    related_links_added: int
    duplicates_found: List[Dict]
    warnings: List[str]
    errors: List[str]


def parse_frontmatter(filepath: Path) -> Optional[Dict]:
    """Extract and parse YAML frontmatter from markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        _, fm, _ = content.split("---", 2)
        return yaml.safe_load(fm)
    except Exception:
        return None


def extract_summary(content: str) -> str:
    """Extract first non-header paragraph as summary."""
    lines = content.split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            # Remove markdown formatting
            line = re.sub(r"\[\[(.*?)\]\]", r"\1", line)  # wikilinks
            line = re.sub(r"[#*_`]", "", line)  # markdown
            return line[:160] + ("..." if len(line) > 160 else "")
    return "No summary available"


def scan_vault() -> List[PageInfo]:
    """Walk vault and parse all knowledge pages."""
    pages = []
    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file.name in ("index.md", "master-index.md", "README.md"):
            continue
        rel_path = md_file.relative_to(VAULT_ROOT)
        fm = parse_frontmatter(md_file)
        if not fm:
            continue

        content = md_file.read_text(encoding="utf-8")
        summary = extract_summary(content)

        pages.append(PageInfo(
            path=str(rel_path),
            title=fm.get("title", md_file.stem),
            summary=summary,
            category=fm.get("category", "unknown"),
            type=fm.get("type", "unknown"),
            status=fm.get("status", "unknown"),
            updated=fm.get("updated", ""),
            tags=fm.get("tags", []),
            related=fm.get("related", []),
            supersedes=fm.get("supersedes"),
            superseded_by=fm.get("superseded_by"),
        ))
    return pages


def build_category_index(category: str, pages: List[PageInfo]) -> str:
    """Build category index markdown with path-based wikilinks."""
    cat_pages = [p for p in pages if p.category == category and p.status == "active"]
    entities = [p for p in cat_pages if p.type == "entity"]
    concepts = [p for p in cat_pages if p.type == "concept"]
    procedures = [p for p in cat_pages if p.type == "procedure"]
    comparisons = [p for p in cat_pages if p.type == "comparison"]
    queries = [p for p in cat_pages if p.type == "query"]

    lines = [
        f"# {category.title()} Index",
        f"",
        f"> Content catalog for **{category}** category. Every page in this category listed under its type with a one-line summary.",
        f"> Read this first to find relevant pages for any query in this category.",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d')} | Total pages: {len(cat_pages)}",
        f"",
    ]

    def section(title: str, items: List[PageInfo]):
        if not items:
            return []
        out = [f"## {title}", ""]
        for p in sorted(items, key=lambda x: x.title.lower()):
            # Use path-based wikilink for discoverability
            out.append(f"- [[{p.path}|{p.title}]] — {p.summary}")
        out.append("")
        return out

    lines.extend(section("Entities", entities))
    lines.extend(section("Concepts", concepts))
    lines.extend(section("Procedures", procedures))
    lines.extend(section("Comparisons", comparisons))
    lines.extend(section("Queries", queries))
    lines.append("---")
    lines.append("")
    lines.append("**Scaling rule:** When any section exceeds 50 entries, split into sub-sections by first letter or sub-domain.")

    return "\n".join(lines)


def build_master_index(pages: List[PageInfo]) -> str:
    """Build master index markdown."""
    active_pages = [p for p in pages if p.status == "active"]
    by_category = defaultdict(list)
    for p in active_pages:
        by_category[p.category].append(p)

    recent = sorted(active_pages, key=lambda x: x.updated, reverse=True)[:10]

    lines = [
        f"# Knowledge Vault Index",
        f"",
        f"> Master content catalog. Every knowledge page listed under its category with a one-line summary.",
        f"> Read this first to find relevant pages for any query.",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d')} | Total pages: {len(active_pages)} | Categories: {len(by_category)}",
        f"",
    ]

    for cat in VALID_CATEGORIES:
        cat_pages = by_category.get(cat, [])
        if not cat_pages:
            continue

        lines.append(f"## {cat.title()} ({len(cat_pages)} pages)")
        lines.append("")

        for ptype, label in [("entity", "Entities"), ("concept", "Concepts"),
                             ("procedure", "Procedures"), ("comparison", "Comparisons"),
                             ("query", "Queries")]:
            items = [p for p in cat_pages if p.type == ptype]
            if not items:
                continue
            lines.append(f"### {label}")
            for p in sorted(items, key=lambda x: x.title.lower()):
                lines.append(f"- [[{p.path}|{p.title}]] — {p.summary}")
            lines.append("")

    lines.append("## Recent Additions (last 10)")
    lines.append("")
    for p in recent:
        lines.append(f"- [[{p.path}|{p.title}]] ({p.category}/{p.type}) — {p.updated}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("**Scaling rule:** When total entries exceed 200, create `_meta/topic-map.md` grouping pages by theme for faster navigation.")

    return "\n".join(lines)


def update_indexes_for_page(page_path: str, category: str, action: str) -> IndexResult:
    """Update indexes for a single page change."""
    result = IndexResult(
        success=True,
        page_path=page_path,
        master_index_updated=False,
        category_index_updated=False,
        category_index_path=f"{category}/index.md",
        discoverable=False,
        related_links_added=0,
        duplicates_found=[],
        warnings=[],
        errors=[],
    )

    # Scan vault
    pages = scan_vault()

    # Build category index
    try:
        cat_index_content = build_category_index(category, pages)
        cat_index_path = VAULT_ROOT / category / "index.md"
        cat_index_path.parent.mkdir(parents=True, exist_ok=True)
        cat_index_path.write_text(cat_index_content, encoding="utf-8")
        result.category_index_updated = True
    except Exception as e:
        result.errors.append(f"Category index update failed: {e}")
        result.success = False

    # Build master index
    try:
        master_content = build_master_index(pages)
        master_path = VAULT_ROOT / "index.md"
        master_path.write_text(master_content, encoding="utf-8")
        result.master_index_updated = True
    except Exception as e:
        result.errors.append(f"Master index update failed: {e}")
        result.success = False

    # Verify discoverability
    result.discoverable = verify_discoverable(page_path)

    return result


def verify_discoverable(page_path: str) -> bool:
    """Check if page is reachable from master index → category index → page."""
    master_path = VAULT_ROOT / "index.md"
    if not master_path.exists():
        return False

    master_content = master_path.read_text(encoding="utf-8")
    # Check if page path appears in master index (path-based wikilink)
    if page_path not in master_content:
        return False

    # Check category index
    try:
        rel_path = Path(page_path)
        category = rel_path.parts[0]
        cat_index = VAULT_ROOT / category / "index.md"
        if not cat_index.exists():
            return False
        cat_content = cat_index.read_text(encoding="utf-8")
        # Category index now uses path-based wikilinks
        if page_path not in cat_content:
            return False
    except Exception:
        return False

    return True


def index_update(page_path: str, category: str, action: str) -> IndexResult:
    """
    Main entry point called by knowledge_workflow.md Step 5.
    """
    if category not in VALID_CATEGORIES:
        return IndexResult(
            success=False,
            page_path=page_path,
            master_index_updated=False,
            category_index_updated=False,
            category_index_path="",
            discoverable=False,
            related_links_added=0,
            duplicates_found=[],
            warnings=[],
            errors=[f"Invalid category: {category}"],
        )

    if action not in ("create", "update", "archive"):
        return IndexResult(
            success=False,
            page_path=page_path,
            master_index_updated=False,
            category_index_updated=False,
            category_index_path="",
            discoverable=False,
            related_links_added=0,
            duplicates_found=[],
            warnings=[],
            errors=[f"Invalid action: {action}"],
        )

    result = update_indexes_for_page(page_path, category, action)

    # Run duplicate detection
    try:
        from duplicate_finder import find_duplicates_for_page
        dupes = find_duplicates_for_page(page_path)
        result.duplicates_found = [d.__dict__ for d in dupes]
    except Exception as e:
        result.warnings.append(f"Duplicate check failed: {e}")

    # Run inconsistency check
    try:
        from inconsistency_checker import check_page_inconsistencies
        issues = check_page_inconsistencies(page_path)
        if issues:
            result.warnings.extend([f"Inconsistency: {i.type} - {i.detail}" for i in issues])
    except Exception as e:
        result.warnings.append(f"Inconsistency check failed: {e}")

    return result


def full_rebuild() -> IndexResult:
    """Complete rebuild of all indexes."""
    pages = scan_vault()

    # Build all category indexes
    cat_updated = 0
    for cat in VALID_CATEGORIES:
        try:
            cat_index_content = build_category_index(cat, pages)
            cat_index_path = VAULT_ROOT / cat / "index.md"
            cat_index_path.parent.mkdir(parents=True, exist_ok=True)
            cat_index_path.write_text(cat_index_content, encoding="utf-8")
            cat_updated += 1
        except Exception:
            pass

    # Build master index
    try:
        master_content = build_master_index(pages)
        master_path = VAULT_ROOT / "index.md"
        master_path.write_text(master_content, encoding="utf-8")
        master_updated = True
    except Exception:
        master_updated = False

    return IndexResult(
        success=True,
        page_path="all",
        master_index_updated=master_updated,
        category_index_updated=cat_updated > 0,
        category_index_path="all",
        discoverable=True,
        related_links_added=0,
        duplicates_found=[],
        warnings=[],
        errors=[],
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python indexer.py <command> [args...]")
        print("Commands: index_update <page_path> <category> <action> | full_rebuild")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "index_update":
        result = index_update(sys.argv[2], sys.argv[3], sys.argv[4])
        print(yaml.dump(asdict(result)))
    elif cmd == "full_rebuild":
        result = full_rebuild()
        print(yaml.dump(asdict(result)))