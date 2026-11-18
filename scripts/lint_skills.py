"""Lint the plugin skills: frontmatter present, no personal terms, required clauses.

Usage: python scripts/lint_skills.py   (exit code 1 when a skill has problems)

Personal terms (your name, employers, e-mail, salary figures) are NOT stored in the
repo. List them one per line in ~/.job-hunter/forbidden-terms.txt (or in the folder
given by the JOB_HUNTER_HOME environment variable) and they are checked locally.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

GENERIC_FORBIDDEN = ["telegram.env contents"]

REQUIRED_CLAUSES: dict[str, list[str]] = {
    "run": [
        "STOP file exists",
        "run.lock",
        "CAPTCHA",
        "logged out",
        "does not crash",
        "incomplete profile",
        "never invent",
        "queue.md",
        "dry_run",
    ],
    "setup": [
        "the requirements",
        "show what you understood",
        "one question at a time",
        "cannot read",
        "assistant (recommended)",
        "I understand the risk",
        "dry run",
        "scheduled task",
        "BotFather",
    ],
    "approve": [
        "only approved",
        "confirm the page shows",
        "CAPTCHA",
        "never invent",
        "STOP file",
    ],
    "status": [
        "STOP file",
        "disable the scheduled task",
        "enable it again",
        "status: open",
        "queue.md",
    ],
}


def _home() -> Path:
    return Path(os.environ.get("JOB_HUNTER_HOME") or Path.home() / ".job-hunter")


def forbidden_terms() -> list[str]:
    terms = list(GENERIC_FORBIDDEN)
    local = _home() / "forbidden-terms.txt"
    if local.is_file():
        terms += [line.strip() for line in local.read_text(encoding="utf-8").splitlines() if line.strip()]
    return terms


def lint_skill(path: Path) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    problems: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---" or "---" not in [l.strip() for l in lines[1:]]:
        problems.append(f"{path}: missing frontmatter")
    else:
        end = [l.strip() for l in lines[1:]].index("---") + 1
        head = "\n".join(lines[1:end])
        for key in ("name:", "description:"):
            if key not in head:
                problems.append(f"{path}: frontmatter needs {key}")
    lowered = text.lower()
    for term in forbidden_terms():
        if term.lower() in lowered:
            problems.append(f"{path}: contains forbidden term '{term}'")
    return problems


def main() -> int:
    root = Path(__file__).resolve().parent.parent / "skills"
    problems: list[str] = []
    for skill in sorted(root.glob("*/SKILL.md")):
        problems += lint_skill(skill)
        text = skill.read_text(encoding="utf-8").lower()
        for clause in REQUIRED_CLAUSES.get(skill.parent.name, []):
            if clause.lower() not in text:
                problems.append(f"{skill}: must mention '{clause}'")
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
