#!/usr/bin/env python3
"""
Quality gates validation for knowledge-wiki skill.
"""

import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

# Import config loader
sys.path.insert(0, str(Path(__file__).parent))
from config_loader import get_config

CONFIG = get_config()
VAULT_ROOT = CONFIG.vault_root

# Load config
CONFIG = get_config()
VAULT_ROOT = CONFIG.vault_root
VALID_CATEGORIES = {"devices", "software", "programming", "electronics", "networking", "operating-systems", "ai"}
VALID_TYPES = {"entity", "concept", "procedure", "comparison", "query", "archive-note"}
VALID_STATUSES = {"active", "archived", "draft"}
VALID_CONFIDENCES = {"high", "medium", "low"}


@dataclass
class ValidationResult:
    page: str
    passed: bool
    errors: List[str]
    warnings: List[str]


def parse_frontmatter(filepath: Path) -> Optional[Dict]:
    try:
        content = filepath.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        _, fm, _ = content.split("---", 2)
        return yaml.safe_load(fm) or {}
    except Exception:
        return None


def extract_wikilinks(content: str) -> List[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def validate_page(filepath: Path) -> ValidationResult:
    rel_path = str(filepath.relative_to(VAULT_ROOT))
    fm = parse_frontmatter(filepath)
    content = filepath.read_text(encoding="utf-8")

    errors = []
    warnings = []

    if not fm:
        return ValidationResult(rel_path, False, ["No valid frontmatter"], [])

    # 1. Required fields
    required = ["title", "created", "updated", "type", "category", "subcategory",
                "tags", "sources", "related", "status", "confidence", "version"]
    for field in required:
        if field not in fm:
            errors.append(f"Missing required field: {field}")

    # 2. Field value validation
    if "type" in fm and fm["type"] not in VALID_TYPES:
        errors.append(f"Invalid type: {fm['type']} (valid: {VALID_TYPES})")

    if "category" in fm and fm["category"] not in VALID_CATEGORIES:
        errors.append(f"Invalid category: {fm['category']} (valid: {VALID_CATEGORIES})")

    if "status" in fm and fm["status"] not in VALID_STATUSES:
        errors.append(f"Invalid status: {fm['status']} (valid: {VALID_STATUSES})")

    if "confidence" in fm and fm["confidence"] not in VALID_CONFIDENCES:
        errors.append(f"Invalid confidence: {fm['confidence']} (valid: {VALID_CONFIDENCES})")

    # 3. Date format
    for date_field in ["created", "updated"]:
        if date_field in fm:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fm[date_field])):
                errors.append(f"Invalid date format for {date_field}: {fm[date_field]} (expected YYYY-MM-DD)")

    # 4. Sources validation
    if "sources" in fm:
        if not isinstance(fm["sources"], list):
            errors.append("Sources must be a list")
        else:
            for i, src in enumerate(fm["sources"]):
                if not isinstance(src, dict):
                    errors.append(f"Source {i} must be a dict")
                elif "title" not in src:
                    warnings.append(f"Source {i} missing title")

    # 5. Related links - count check
    related = fm.get("related", [])
    if not isinstance(related, list):
        errors.append("Related must be a list")
    elif fm.get("type") == "entity" and fm.get("category") == "devices":
        # For devices: exactly 1 related link (board ↔ MCU bidirectional)
        if len(related) != 1:
            errors.append(f"Device entity must have exactly 1 related link (board ↔ MCU), got {len(related)}")
    elif len(related) < 2 and fm.get("status") == "active" and fm.get("type") != "archive-note":
        warnings.append(f"Active page has only {len(related)} related links (minimum 2)")

    # 6. Wikilinks in content vs related field consistency
    wikilinks = extract_wikilinks(content)
    for link in wikilinks:
        if link not in related:
            warnings.append(f"Wikilink in content not in related field: {link}")

    # 7. Tags validation (basic structure)
    tags = fm.get("tags", [])
    if not isinstance(tags, list):
        errors.append("Tags must be a list")
    elif len(tags) == 0:
        warnings.append("Page has no tags")

    # 8. Content size check
    line_count = len(content.splitlines())
    if line_count > 200:
        warnings.append(f"Page exceeds 200 lines ({line_count}) — consider splitting")

    # 9. Category folder match
    category = fm.get("category", "")
    if category and not rel_path.startswith(f"{category}/"):
        warnings.append(f"Page category '{category}' but located in '{rel_path.split('/')[0]}/'")

    # 10. Version format
    if "version" in fm:
        if not isinstance(fm["version"], str) or not re.match(r"^\d+\.\d+", str(fm["version"])):
            warnings.append(f"Version should be semantic (e.g., '1.0'), got: {fm['version']}")

    return ValidationResult(rel_path, len(errors) == 0, errors, warnings)


def validate_all() -> Dict:
    results = []
    total_errors = 0
    total_warnings = 0

    for md_file in VAULT_ROOT.rglob("*.md"):
        if md_file.name in ("index.md", "README.md"):
            continue
        result = validate_page(md_file)
        results.append({
            "page": result.page,
            "passed": result.passed,
            "errors": result.errors,
            "warnings": result.warnings
        })
        total_errors += len(result.errors)
        total_warnings += len(result.warnings)

    return {
        "summary": {
            "total_pages": len(results),
            "passed": len([r for r in results if r["passed"]]),
            "failed": len([r for r in results if not r["passed"]]),
            "total_errors": total_errors,
            "total_warnings": total_warnings
        },
        "results": results
    }


if __name__ == "__main__":
    import sys
    import yaml

    if len(sys.argv) > 1:
        result = validate_page(VAULT_ROOT / sys.argv[1])
        print(yaml.dump({
            "page": result.page,
            "passed": result.passed,
            "errors": result.errors,
            "warnings": result.warnings
        }))
    else:
        report = validate_all()
        print(yaml.dump(report))