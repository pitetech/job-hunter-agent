import re
import tempfile
import unittest
from pathlib import Path

from scripts.check_docs_parity import PAIRS, parity

ROOT = Path(__file__).resolve().parent.parent

README_SECTIONS = [
    "what it is",
    "safety notice",
    "how it works",
    "requirements",
    "install and first setup",
    "example profile and report",
    "assistant vs automatic mode",
    "turn it off and remove everything",
    "faq and limitations",
    "contributing and license",
]


def make_pair(d: Path, en: str, pt: str) -> list[tuple[str, str]]:
    (d / "a.md").write_text(en, encoding="utf-8")
    (d / "a.pt-BR.md").write_text(pt, encoding="utf-8")
    return [("a.md", "a.pt-BR.md")]


class DocsParityTests(unittest.TestCase):
    def test_all_pairs_exist(self):
        for en, pt in PAIRS:
            self.assertTrue((ROOT / en).is_file(), en)
            self.assertTrue((ROOT / pt).is_file(), pt)

    def test_heading_structure_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            pairs = make_pair(Path(d), "# A\n## B\n[pt](a.pt-BR.md)\n", "# A\n[en](a.md)\n")
            problems = parity(Path(d), pairs)
        self.assertTrue(any("heading" in p.lower() for p in problems))

    def test_code_block_count_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            pairs = make_pair(
                Path(d), "# A\n```\nx\n```\n[pt](a.pt-BR.md)\n", "# A\n[en](a.md)\n"
            )
            problems = parity(Path(d), pairs)
        self.assertTrue(any("code block" in p.lower() for p in problems))

    def test_missing_cross_link_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            pairs = make_pair(Path(d), "# A\n", "# A\n")
            problems = parity(Path(d), pairs)
        self.assertEqual(sum("link" in p.lower() for p in problems), 2)

    def test_missing_file_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            problems = parity(Path(d), [("nope.md", "nope.pt-BR.md")])
        self.assertTrue(any("missing" in p.lower() for p in problems))

    def test_matching_pair_has_no_problems(self):
        with tempfile.TemporaryDirectory() as d:
            pairs = make_pair(
                Path(d), "# A\n## B\n[pt](a.pt-BR.md)\n", "# A\n## B\n[en](a.md)\n"
            )
            self.assertEqual(parity(Path(d), pairs), [])

    def test_repo_docs_are_in_parity(self):
        self.assertEqual(parity(ROOT), [])

    def test_readme_has_required_sections_in_order(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        titles = [t.strip().lower() for t in re.findall(r"^## (.+)$", text, re.M)]
        positions = []
        for wanted in README_SECTIONS:
            matches = [i for i, t in enumerate(titles) if wanted in t]
            self.assertTrue(matches, f"README.md is missing a section about: {wanted}")
            positions.append(matches[0])
        self.assertEqual(positions, sorted(positions))

    def test_docs_say_linkedin_prohibits_automation(self):
        for name in ("README.md", "README.pt-BR.md", "SAFETY.md", "SEGURANCA.md"):
            text = (ROOT / name).read_text(encoding="utf-8").lower()
            self.assertIn("linkedin", text)
            self.assertTrue("not affiliated" in text or "sem vínculo" in text, name)


if __name__ == "__main__":
    unittest.main()
