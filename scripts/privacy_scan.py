"""Scan the repository for personal data that must never be committed.

Usage: python scripts/privacy_scan.py   (exit code 1 when something is found)
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", ".superpowers", "node_modules"}
SKIP_PREFIXES = ("docs/superpowers/", "tests/test_privacy_scan.py")
ALLOWED_EMAIL_DOMAINS = {"example.com", "example.org", "users.noreply.github.com"}

TOKEN = re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")
EMAIL = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
PHONE = re.compile(r"\+?55\s?\(?\d{2}\)?\s?9?\d{4}-?\d{4}")
USER_PATH = re.compile(r"[A-Za-z]:\\Users\\(?!<)[^\\\s<]+")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str


def _scan_line(line: str) -> list[str]:
    rules = []
    if TOKEN.search(line):
        rules.append("token")
    if any(m.group(1).lower() not in ALLOWED_EMAIL_DOMAINS for m in EMAIL.finditer(line)):
        rules.append("email")
    if PHONE.search(line):
        rules.append("phone")
    if USER_PATH.search(line):
        rules.append("user_path")
    return rules


def scan_paths(root: Path) -> list[Finding]:
    root = Path(root)
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if not path.is_file() or any(part in SKIP_DIRS for part in rel.parts):
            continue
        rel_posix = rel.as_posix()
        if rel_posix.startswith(SKIP_PREFIXES):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for rule in _scan_line(line):
                findings.append(Finding(rel_posix, number, rule))
    return findings


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    findings = scan_paths(root)
    for f in findings:
        print(f"{f.path}:{f.line}: {f.rule}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
