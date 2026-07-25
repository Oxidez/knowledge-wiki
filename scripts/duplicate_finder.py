#!/usr/bin/env python3
"""
Multi-signal duplicate detection for knowledge-wiki skill.
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Set, Tuple
from collections import defaultdict

try:
    import simhash
    SIMHASH_AVAILABLE = True
except ImportError:
    SIMHASH_AVAILABLE = False

try:
    import Levenshtein
    LEVENSHTEIN_AVAILABLE = True
except ImportError:
    LEVENSHTEIN_AVAILABLE = False

# Import config loader
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import get_config

CONFIG = get_config()
VAULT_ROOT = CONFIG.vault_root

VALID_CATEGORIES = {"devices", "software", "programming", "electronics", "networking", "operating-systems", "ai"}


@dataclass
class DuplicateInfo:
    existing_page: str
    match_type: str  # "title" | "entity_match" | "content_simhash" | "naming_conflict"
    similarity: float
    detail: str


@dataclass
class DuplicateReport:
    page_path: str
    duplicates: List[DuplicateInfo]


def parse_frontmatter(filepath: Path) -> Dict:
    try:
        content = filepath.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return {}
        _, fm, _ = content.split("---", 2)
        return yaml.safe_load(fm) or {}
    except Exception:
        return {}


def extract_body(content: str) -> str:
    """Extract body text (after frontmatter)."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def compute_simhash(text: str) -> int:
    """Compute 64-bit simhash of text."""
    if not SIMHASH_AVAILABLE:
        return 0
    return simhash.Simhash(text, f=64).value


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein distance."""
    if LEVENSHTEIN_AVAILABLE:
        return Levenshtein.distance(s1, s2)
    # Fallback
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def get_all_pages() -> List[Tuple[str, Dict, str]]:
    """Get all pages as (rel_path, frontmatter, body)."""
    pages = []
    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file.name in ("index.md", "README.md"):
            continue
        rel_path = str(md_file.relative_to(VAULT_ROOT))
        fm = parse_frontmatter(md_file)
        if not fm:
            continue
        content = md_file.read_text(encoding="utf-8")
        body = extract_body(content)
        pages.append((rel_path, fm, body))
    return pages


def find_duplicates_for_page(page_path: str) -> List[DuplicateInfo]:
    """Find potential duplicates for a specific page."""
    full_path = VAULT_ROOT / page_path
    if not full_path.exists():
        return []

    fm = parse_frontmatter(full_path)
    if not fm:
        return []

    title = fm.get("title", "")
    norm_title = normalize_title(title)
    category = fm.get("category", "")
    entity_type = fm.get("type", "")

    content = full_path.read_text(encoding="utf-8")
    body = extract_body(content)
    body_hash = compute_simhash(body)

    duplicates = []

    # Scan all other pages in same category
    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file.name in ("index.md", "README.md"):
            continue
        rel_path = str(md_file.relative_to(VAULT_ROOT))
        if rel_path == page_path:
            continue

        other_fm = parse_frontmatter(md_file)
        if not other_fm:
            continue

        other_category = other_fm.get("category", "")
        other_type = other_fm.get("type", "")
        other_title = other_fm.get("title", "")
        other_norm_title = normalize_title(other_title)

        same_category = (other_category == category)

        # 1. Exact title match (normalized)
        if norm_title and norm_title == other_norm_title:
            duplicates.append(DuplicateInfo(
                existing_page=rel_path,
                match_type="title",
                similarity=1.0,
                detail=f"Exact title match: '{title}'"
            ))

        # 2. Same entity type + category + title similarity
        if same_category and other_type == entity_type and entity_type:
            dist = levenshtein_distance(norm_title, other_norm_title)
            if dist <= 3 and norm_title and other_norm_title:
                similarity = 1.0 - (dist / max(len(norm_title), len(other_norm_title)))
                duplicates.append(DuplicateInfo(
                    existing_page=rel_path,
                    match_type="entity_match",
                    similarity=similarity,
                    detail=f"Same {entity_type} in {category}, title distance={dist}: '{title}' vs '{other_title}'"
                ))

        # 3. Content similarity (simhash)
        if body_hash and SIMHASH_AVAILABLE:
            other_content = md_file.read_text(encoding="utf-8")
            other_body = extract_body(other_content)
            other_hash = compute_simhash(other_body)
            if other_hash:
                hamming = bin(body_hash ^ other_hash).count("1")
                if hamming <= 3:
                    similarity = 1.0 - (hamming / 64.0)
                    duplicates.append(DuplicateInfo(
                        existing_page=rel_path,
                        match_type="content_simhash",
                        similarity=similarity,
                        detail=f"Content similarity hamming={hamming} ({similarity:.1%})"
                    ))

        # 4. Naming conflict (same kebab-case filename in same folder)
        if same_category:
            our_name = Path(page_path).stem
            other_name = Path(rel_path).stem
            if our_name == other_name:
                duplicates.append(DuplicateInfo(
                    existing_page=rel_path,
                    match_type="naming_conflict",
                    similarity=1.0,
                    detail=f"Same filename in {category}: {our_name}.md"
                ))

    return duplicates


def find_all_duplicates() -> List[DuplicateReport]:
    """Find all duplicate pairs across the vault."""
    pages = get_all_pages()
    reports = []

    for i, (path1, fm1, body1) in enumerate(pages):
        title1 = fm1.get("title", "")
        norm1 = normalize_title(title1)
        cat1 = fm1.get("category", "")
        type1 = fm1.get("type", "")
        hash1 = compute_simhash(body1)

        for j, (path2, fm2, body2) in enumerate(pages[i+1:], i+1):
            title2 = fm2.get("title", "")
            norm2 = normalize_title(title2)
            cat2 = fm2.get("category", "")
            type2 = fm2.get("type", "")

            dupes = []

            # Exact title
            if norm1 and norm1 == norm2:
                dupes.append(DuplicateInfo(path2, "title", 1.0, f"Exact title: '{title1}'"))

            # Same entity
            if cat1 == cat2 and type1 == type2 and type1:
                dist = levenshtein_distance(norm1, norm2)
                if dist <= 3 and norm1 and norm2:
                    sim = 1.0 - (dist / max(len(norm1), len(norm2)))
                    dupes.append(DuplicateInfo(path2, "entity_match", sim, f"Same {type1} in {cat1}"))

            # Content
            if hash1 and SIMHASH_AVAILABLE:
                hash2 = compute_simhash(body2)
                if hash2:
                    hamming = bin(hash1 ^ hash2).count("1")
                    if hamming <= 3:
                        sim = 1.0 - (hamming / 64.0)
                        dupes.append(DuplicateInfo(path2, "content_simhash", sim, f"Content hamming={hamming}"))

            # Naming
            if cat1 == cat2:
                name1 = Path(path1).stem
                name2 = Path(path2).stem
                if name1 == name2:
                    dupes.append(DuplicateInfo(path2, "naming_conflict", 1.0, f"Same filename in {cat1}"))

            if dupes:
                reports.append(DuplicateReport(path1, dupes))

    return reports


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "all":
        reports = find_all_duplicates()
        for r in reports:
            print(f"Page: {r.page_path}")
            for d in r.duplicates:
                print(f"  -> {d.existing_page} [{d.match_type}] {d.similarity:.2f}: {d.detail}")
    elif len(sys.argv) > 1:
        dupes = find_duplicates_for_page(sys.argv[1])
        for d in dupes:
            print(f"{d.existing_page} [{d.match_type}] {d.similarity:.2f}: {d.detail}")
    else:
        print("Usage: python duplicate_finder.py <page_path> | all")