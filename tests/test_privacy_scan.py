import tempfile
import unittest
from pathlib import Path

from scripts.privacy_scan import scan_paths


def scan_text(text: str, name: str = "file.md") -> list:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / name).write_text(text, encoding="utf-8")
        return scan_paths(root)


class PrivacyScanTests(unittest.TestCase):
    def test_flags_telegram_token(self):
        fake = "1234567890:" + "A" * 35
        findings = scan_text(f"token = {fake}")
        self.assertEqual([f.rule for f in findings], ["token"])

    def test_flags_personal_email(self):
        findings = scan_text("write to someone@gmail.com")
        self.assertEqual([f.rule for f in findings], ["email"])

    def test_allows_example_email(self):
        self.assertEqual(scan_text("you@example.com"), [])

    def test_flags_br_phone(self):
        findings = scan_text("call +55 11 91234-5678")
        self.assertEqual([f.rule for f in findings], ["phone"])

    def test_flags_windows_user_path(self):
        findings = scan_text(r"cv at C:\Users\maria\cv.pdf")
        self.assertEqual([f.rule for f in findings], ["user_path"])

    def test_allows_placeholder_user_path(self):
        self.assertEqual(scan_text(r"C:\Users\<name>\.job-hunter"), [])

    def test_ignores_dot_git_and_pycache(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for sub in (".git", "__pycache__"):
                (root / sub).mkdir()
                (root / sub / "x.txt").write_text("someone@gmail.com", encoding="utf-8")
            self.assertEqual(scan_paths(root), [])

    def test_reports_path_and_line(self):
        findings = scan_text("ok\nsomeone@gmail.com\n", name="a.md")
        self.assertEqual((findings[0].path, findings[0].line), ("a.md", 2))


if __name__ == "__main__":
    unittest.main()
