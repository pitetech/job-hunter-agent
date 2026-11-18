"""Check that every English doc has a Portuguese twin with the same structure.

Usage: python scripts/check_docs_parity.py   (exit code 1 when a pair is out of sync)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PAIRS: list[tuple[str, str]] = [
    ("README.md", "README.pt-BR.md"),
    ("SAFETY.md", "SEGURANCA.md"),
    ("docs/how-it-works.md", "docs/como-funciona.md"),
    ("docs/telegram-setup.md", "docs/configurar-telegram.md"),
    ("docs/faq.md", "docs/faq.pt-BR.md"),
]

HEADING = re.compile(r"^(#{1,6})\s+\S")


def _structure(text: str) -> tuple[list[int], int]:
    """Return (sequence of heading levels outside code fences, number of code blocks)."""
    levels: list[int] = []
    fences = 0
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fences += 1
            in_fence = not in_fence
            continue
        if not in_fence:
            match = HEADING.match(line)
            if match:
                levels.append(len(match.group(1)))
    return levels, fences // 2


def parity(root: Path, pairs: list[tuple[str, str]] = PAIRS) -> list[str]:
    root = Path(root)
    problems: list[str] = []
    for en_name, pt_name in pairs:
        en_path, pt_path = root / en_name, root / pt_name
        missing = [n for n, p in ((en_name, en_path), (pt_name, pt_path)) if not p.is_file()]
        if missing:
            problems += [f"{n}: missing" for n in missing]
            continue
        en_text = en_path.read_text(encoding="utf-8")
        pt_text = pt_path.read_text(encoding="utf-8")
        en_levels, en_blocks = _structure(en_text)
        pt_levels, pt_blocks = _structure(pt_text)
        if en_levels != pt_levels:
            problems.append(f"{en_name} / {pt_name}: heading structure differs")
        if en_blocks != pt_blocks:
            problems.append(f"{en_name} / {pt_name}: code block count differs ({en_blocks} vs {pt_blocks})")
        if Path(pt_name).name not in en_text:
            problems.append(f"{en_name}: missing link to {Path(pt_name).name}")
        if Path(en_name).name not in pt_text:
            problems.append(f"{pt_name}: missing link to {Path(en_name).name}")
    return problems


def main() -> int:
    problems = parity(Path(__file__).resolve().parent.parent)
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
