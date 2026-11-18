import copy
import unittest
from pathlib import Path

import yaml

from scripts.validate_profile import load_and_validate, validate_profile

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "templates" / "profile.example.yaml"


def example() -> dict:
    return copy.deepcopy(yaml.safe_load(EXAMPLE.read_text(encoding="utf-8")))


def problems_with(word: str, data: dict) -> list[str]:
    return [p for p in validate_profile(data) if word in p.lower()]


class ValidateProfileTests(unittest.TestCase):
    def test_example_profile_is_valid(self):
        self.assertEqual(load_and_validate(EXAMPLE), [])

    def test_missing_salary_is_reported(self):
        data = example()
        del data["salary"]
        self.assertEqual(len(problems_with("salary", data)), 1)

    def test_invalid_mode(self):
        data = example()
        data["mode"] = "robot"
        self.assertTrue(problems_with("mode", data))

    def test_empty_target_roles(self):
        data = example()
        data["target_roles"] = []
        self.assertTrue(problems_with("target_roles", data))

    def test_limit_out_of_range(self):
        data = example()
        data["limits"]["max_applications_per_run"] = 50
        self.assertTrue(problems_with("max_applications_per_run", data))

    def test_bad_schedule_time(self):
        data = example()
        data["schedule"] = ["25:99"]
        self.assertTrue(problems_with("schedule", data))

    def test_auto_mode_requires_acknowledgment(self):
        data = example()
        data["mode"] = "auto"
        data["auto_mode_acknowledged"] = False
        self.assertTrue(problems_with("acknowledg", data))

    def test_auto_mode_with_acknowledgment_is_valid(self):
        data = example()
        data["mode"] = "auto"
        data["auto_mode_acknowledged"] = True
        self.assertEqual(validate_profile(data), [])

    def test_missing_cv_path(self):
        data = example()
        data["cv_path"] = ""
        self.assertTrue(problems_with("cv_path", data))

    def test_invalid_work_model(self):
        data = example()
        data["work_model"] = ["moon"]
        self.assertTrue(problems_with("work_model", data))

    def test_answers_example_has_facts_with_source(self):
        facts = yaml.safe_load(
            (ROOT / "templates" / "answers.example.yaml").read_text(encoding="utf-8")
        )["facts"]
        self.assertTrue(facts)
        for fact in facts:
            self.assertIn(fact["source"], {"cv", "user"})
            self.assertTrue(fact["question_topic"])


if __name__ == "__main__":
    unittest.main()
