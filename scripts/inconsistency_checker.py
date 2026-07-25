#!/usr/bin/env python3
"""
Inconsistency detection for knowledge-wiki skill.
Checks: broken wikilinks, missing frontmatter, tag violations, orphans, supersedes chains.
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict

# Import config loader
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import get_config, WikiConfig

# Load config
CONFIG = get_config()
VAULT_ROOT = CONFIG.vault_root

VALID_CATEGORIES = {"devices", "software", "programming", "electronics", "networking", "operating-systems", "ai"}
VALID_TYPES = {"entity", "concept", "procedure", "comparison", "query", "archive-note"}
VALID_STATUSES = {"active", "archived", "draft"}
VALID_CONFIDENCES = {"high", "medium", "low"}

# Tag taxonomy (from schema-template.md)
VALID_TAGS = {
    "devices": {"microcontroller", "sbc", "sensor", "actuator", "tool", "instrument"},
    "software": {"os", "library", "framework", "tool", "application", "driver"},
    "programming": {"language", "algorithm", "pattern", "architecture", "api", "protocol"},
    "electronics": {"component", "circuit", "pcb", "power", "signal", "measurement"},
    "networking": {"protocol", "topology", "security", "wireless", "wired", "monitoring"},
    "operating-systems": {"kernel", "shell", "filesystem", "process", "memory", "container"},
    "ai": {"model", "training", "inference", "dataset", "framework", "application"},
    "cross": {"tutorial", "reference", "comparison", "troubleshooting", "best-practice", "deprecated", "security", "performance", "integration", "board"}
}

FLATTENED_TAGS = set()
for cat_tags in VALID_TAGS.values():
    if isinstance(cat_tags, set):
        FLATTENED_TAGS.update(cat_tags)
FLATTENED_TAGS.update({"tutorial", "reference", "comparison", "troubleshooting", "best-practice", "deprecated", "security", "performance", "integration"})


@dataclass
class InconsistencyIssue:
    type: str  # "broken_wikilink" | "missing_frontmatter" | "tag_violation" | "orphan" | "related_insufficient" | "supersedes_broken" | "schema_violation"
    page: str
    detail: str
    severity: str  # "error" | "warning" | "info"


def parse_frontmatter(filepath: Path) -> Optional[Dict]:
    try:
        content = filepath.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        _, fm, _ = content.split("---", 2)
        return yaml.safe_load(fm)
    except Exception:
        return None


def extract_wikilinks(content: str) -> List[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def get_all_pages() -> Dict[str, Tuple[Dict, str]]:
    """Return {rel_path: (frontmatter, content)}"""
    pages = {}
    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file.name in ("index.md", "README.md"):
            continue
        rel_path = str(md_file.relative_to(VAULT_ROOT))
        fm = parse_frontmatter(md_file)
        if not fm:
            continue
        content = md_file.read_text(encoding="utf-8")
        pages[rel_path] = (fm, content)
    return pages


def check_page_inconsistencies(page_path: str) -> List[InconsistencyIssue]:
    """Check inconsistencies for a single page."""
    full_path = VAULT_ROOT / page_path
    if not full_path.exists():
        return [InconsistencyIssue("missing_page", page_path, "Page file not found", "error")]

    fm = parse_frontmatter(full_path)
    if not fm:
        return [InconsistencyIssue("missing_frontmatter", page_path, "Missing or invalid frontmatter", "error")]

    content = full_path.read_text(encoding="utf-8")
    issues = []

    # Build page title lookup
    all_pages = get_all_pages()
    page_titles = {fm.get("title", Path(p).stem): p for p, (fm, _) in all_pages.items()}

    # 1. Broken wikilinks
    for link in extract_wikilinks(content):
        if link not in page_titles:
            issues.append(InconsistencyIssue(
                "broken_wikilink", page_path,
                f"Broken wikilink: [[{link}]]",
                "error"
            ))

    # 2. Missing required frontmatter fields
    required = ["title", "created", "updated", "type", "category", "subcategory", "tags", "sources", "related", "status", "confidence", "version"]
    for field in required:
        if field not in fm:
            issues.append(InconsistencyIssue(
                "missing_frontmatter", page_path,
                f"Missing required field: {field}",
                "error"
            ))

    # 3. Tag validation
    for tag in fm.get("tags", []):
        if tag not in FLATTENED_TAGS:
            issues.append(InconsistencyIssue(
                "tag_violation", page_path,
                f"Tag not in taxonomy: {tag}",
                "error"
            ))

    # 4. Related links validation
    for link in fm.get("related", []):
        if link not in page_titles:
            issues.append(InconsistencyIssue(
                "broken_related", page_path,
                f"Related link points to non-existent page: {link}",
                "error"
            ))

    # 5. Minimum related links for active pages
    if fm.get("status") == "active" and fm.get("type") != "archive-note":
        if fm.get("type") == "entity" and fm.get("category") == "devices":
            # For devices: exactly 1 related link (board ↔ MCU bidirectional)
            if len(fm.get("related", [])) != 1:
                issues.append(InconsistencyIssue(
                    "related_count_violation", page_path,
                    f"Device entity must have exactly 1 related link (board ↔ MCU), got {len(fm.get('related', []))}",
                    "error"
                ))
        elif len(fm.get("related", [])) < 2:
            issues.append(InconsistencyIssue(
                "related_insufficient", page_path,
                f"Active page has only {len(fm.get('related', []))} related links (minimum 2)",
                "warning"
            ))

    # 6. Supersedes chain validation
    supersedes = fm.get("supersedes")
    if supersedes and supersedes not in page_titles:
        issues.append(InconsistencyIssue(
            "supersedes_broken", page_path,
            f"Supersedes link broken: {supersedes}",
            "warning"
        ))

    superseded_by = fm.get("superseded_by")
    if superseded_by and superseded_by not in page_titles:
        issues.append(InconsistencyIssue(
            "superseded_by_broken", page_path,
            f"Superseded-by link broken: {superseded_by}",
            "warning"
        ))

    # 7. Schema violations
    if fm.get("category") not in VALID_CATEGORIES:
        issues.append(InconsistencyIssue(
            "schema_violation", page_path,
            f"Invalid category: {fm.get('category')}",
            "error"
        ))

    if fm.get("type") not in VALID_TYPES:
        issues.append(InconsistencyIssue(
            "schema_violation", page_path,
            f"Invalid type: {fm.get('type')}",
            "error"
        ))

    if fm.get("status") not in VALID_STATUSES:
        issues.append(InconsistencyIssue(
            "schema_violation", page_path,
            f"Invalid status: {fm.get('status')}",
            "error"
        ))

    if fm.get("confidence") not in VALID_CONFIDENCES:
        issues.append(InconsistencyIssue(
            "schema_violation", page_path,
            f"Invalid confidence: {fm.get('confidence')}",
            "error"
        ))

    # 8. Sources validation
    sources = fm.get("sources", [])
    if not sources and fm.get("type") != "archive-note":
        issues.append(InconsistencyIssue(
            "missing_sources", page_path,
            "No sources cited for non-archive page",
            "warning"
        ))

    # 9. Page size
    line_count = len(content.splitlines())
    if line_count > 200:
        issues.append(InconsistencyIssue(
            "page_too_large", page_path,
            f"Page exceeds 200 lines ({line_count}) — consider splitting",
            "warning"
        ))

    return issues


def check_all_inconsistencies() -> List[InconsistencyIssue]:
    """Check all pages for inconsistencies."""
    all_pages = get_all_pages()
    page_titles = {fm.get("title", Path(p).stem): p for p, (fm, _) in all_pages.items()}

    # Build inbound link map
    inbound = defaultdict(list)
    for rel_path, (fm, content) in all_pages.items():
        for link in extract_wikilinks(content):
            inbound[link].append(rel_path)

    all_issues = []

    for rel_path, (fm, content) in all_pages.items():
        # Run single-page checks
        all_issues.extend(check_page_inconsistencies(rel_path))

        # 10. Orphan detection (active pages with no inbound links)
        title = fm.get("title", Path(rel_path).stem)
        if fm.get("status") == "active" and fm.get("type") != "archive-note":
            if not inbound.get(title):
                all_issues.append(InconsistencyIssue(
                    "orphan", rel_path,
                    f"No inbound wikilinks (orphan page)",
                    "info"
                ))

        # 11. Index completeness
        cat = fm.get("category")
        if cat and cat in VALID_CATEGORIES and fm.get("status") == "active":
            cat_index = VAULT_ROOT / cat / "index.md"
            if cat_index.exists():
                idx_content = cat_index.read_text(encoding="utf-8")
                if rel_path not in idx_content:
                    all_issues.append(InconsistencyIssue(
                        "missing_from_category_index", rel_path,
                        f"Active page not listed in {cat}/index.md",
                        "warning"
                    ))

        master_index = VAULT_ROOT / "index.md"
        if master_index.exists():
            master_content = master_index.read_text(encoding="utf-8")
            if fm.get("status") == "active" and rel_path not in master_content:
                all_issues.append(InconsistencyIssue(
                    "missing_from_master_index", rel_path,
                    "Active page not listed in master index.md",
                    "warning"
                ))

    return all_issues


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        issues = check_page_inconsistencies(sys.argv[1])
    else:
        issues = check_all_inconsistencies()

    for issue in issues:
        print(f"[{issue.severity.upper()}] {issue.type}: {issue.page} — {issue.detail}")