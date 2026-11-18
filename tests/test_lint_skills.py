import os
import tempfile
import unittest
from pathlib import Path

from scripts.lint_skills import REQUIRED_CLAUSES, forbidden_terms, lint_skill

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"


def skill_path(name: str) -> Path:
    return SKILLS / name / "SKILL.md"


class LintMachineryTests(unittest.TestCase):
    def test_forbidden_terms_reads_local_file_via_env(self):
        with tempfile.TemporaryDirectory() as home:
            Path(home, "forbidden-terms.txt").write_text("Acme Corp\n\nJane Roe\n", encoding="utf-8")
            os.environ["JOB_HUNTER_HOME"] = home
            try:
                terms = forbidden_terms()
            finally:
                del os.environ["JOB_HUNTER_HOME"]
        self.assertIn("Acme Corp", terms)
        self.assertIn("Jane Roe", terms)
        self.assertNotIn("", terms)

    def test_lint_reports_missing_frontmatter_and_forbidden_term(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as d:
            Path(home, "forbidden-terms.txt").write_text("Acme Corp\n", encoding="utf-8")
            skill = Path(d) / "SKILL.md"
            skill.write_text("Works at Acme Corp\n", encoding="utf-8")
            os.environ["JOB_HUNTER_HOME"] = home
            try:
                problems = lint_skill(skill)
            finally:
                del os.environ["JOB_HUNTER_HOME"]
        text = " | ".join(problems).lower()
        self.assertIn("frontmatter", text)
        self.assertIn("acme corp", text)


class RunSkillTests(unittest.TestCase):
    def test_run_skill_has_frontmatter_and_no_personal_terms(self):
        self.assertEqual(lint_skill(skill_path("run")), [])

    def test_run_skill_covers_review_focus(self):
        text = skill_path("run").read_text(encoding="utf-8").lower()
        for clause in REQUIRED_CLAUSES["run"]:
            self.assertIn(clause.lower(), text, f"run skill must mention: {clause}")

    def test_run_documents_queue_format(self):
        text = skill_path("run").read_text(encoding="utf-8")
        self.assertIn("match_reason", text)
        self.assertIn("status: queued", text)


class SetupSkillTests(unittest.TestCase):
    def test_setup_skill_has_frontmatter_and_no_personal_terms(self):
        self.assertEqual(lint_skill(skill_path("setup")), [])

    def test_setup_skill_covers_flow(self):
        text = skill_path("setup").read_text(encoding="utf-8").lower()
        for clause in REQUIRED_CLAUSES["setup"]:
            self.assertIn(clause.lower(), text, f"setup skill must mention: {clause}")


class ApproveAndStatusSkillTests(unittest.TestCase):
    def test_approve_skill_is_clean(self):
        self.assertEqual(lint_skill(skill_path("approve")), [])

    def test_approve_skill_covers_rules(self):
        text = skill_path("approve").read_text(encoding="utf-8").lower()
        for clause in REQUIRED_CLAUSES["approve"]:
            self.assertIn(clause.lower(), text, f"approve skill must mention: {clause}")

    def test_status_skill_is_clean(self):
        self.assertEqual(lint_skill(skill_path("status")), [])

    def test_status_skill_covers_controls(self):
        text = skill_path("status").read_text(encoding="utf-8").lower()
        for clause in REQUIRED_CLAUSES["status"]:
            self.assertIn(clause.lower(), text, f"status skill must mention: {clause}")

    def test_approve_reads_the_queue_format_run_writes(self):
        approve = skill_path("approve").read_text(encoding="utf-8")
        for key in ("status: queued", "status: approved", "status: sent", "status: rejected", "match_reason"):
            self.assertIn(key, approve)


def read(name: str) -> str:
    return skill_path(name).read_text(encoding="utf-8")


class ReviewFixesTests(unittest.TestCase):
    """Behaviors the final review found missing from the skill text."""

    def test_pending_jobs_have_a_format_and_are_reevaluated_once_answered(self):
        run, status = read("run"), read("status")
        for key in ("status: open", "status: answered", "question:"):
            self.assertIn(key, run)
        self.assertIn("status: answered", status)

    def test_dry_run_writes_no_state_files(self):
        self.assertIn("writes no state files", read("run"))

    def test_zero_salary_for_the_jobs_regime_blocks_that_application(self):
        self.assertIn("amount for the job's regime is 0", read("run"))

    def test_telegram_token_never_appears_in_the_command_line(self):
        run = read("run")
        self.assertNotIn("<TOKEN>", run)
        self.assertIn("source", run)
        self.assertIn("text@", run)

    def test_job_posting_text_is_untrusted_data(self):
        for name in ("run", "approve"):
            self.assertIn("untrusted data", read(name).lower(), name)

    def test_stop_is_checked_before_every_application(self):
        for name in ("run", "approve"):
            self.assertIn("before each application", read(name).lower(), name)

    def test_stop_file_with_windows_extension_is_honored(self):
        for name in ("run", "approve", "status"):
            self.assertIn("STOP.txt", read(name), name)

    def test_approve_respects_the_run_lock(self):
        self.assertIn("run.lock", read("approve"))

    def test_approve_checks_every_visible_field(self):
        text = read("approve").lower()
        self.assertIn("every visible field", text)
        self.assertIn("pre-filled", text)

    def test_assistant_mode_never_clicks_submit_and_exits_with_discard(self):
        run = read("run")
        self.assertIn("Submit application", run)
        self.assertIn("Discard", run)

    def test_auto_without_acknowledgment_falls_back_to_assistant(self):
        self.assertIn("falls back to assistant", read("run").lower())

    def test_assistant_mode_notifies_when_jobs_were_queued(self):
        self.assertIn("jobs were queued", read("run").lower())

    def test_setup_tests_telegram_in_both_cases(self):
        self.assertIn("in both cases", read("setup").lower())

    def test_setup_finds_the_plugin_folder_and_never_writes_from_memory(self):
        text = read("setup").lower()
        self.assertIn("plugin's folder", text)
        self.assertIn("from memory", text)

    def test_unparsable_profile_is_treated_as_incomplete(self):
        self.assertIn("cannot be parsed", read("run").lower())

    def test_template_cv_path_uses_single_quotes_for_windows_paths(self):
        template = (ROOT / "templates" / "profile.example.yaml").read_text(encoding="utf-8")
        self.assertIn("cv_path: '", template)

    def test_stop_file_instructions_do_not_tell_windows_users_to_make_a_bare_file(self):
        for name in ("README.md", "README.pt-BR.md", "SAFETY.md", "SEGURANCA.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("/job-hunter:status", text, name)
            self.assertIn("STOP.txt", text, name)

    def test_required_clauses_are_specific_not_generic_words(self):
        for generic in ("STOP", "lock", "assistant", "telegram", "confirm", "queue"):
            for clauses in REQUIRED_CLAUSES.values():
                self.assertNotIn(generic, clauses)


if __name__ == "__main__":
    unittest.main()
