"""Validate a job-hunter profile.yaml.

Usage: python scripts/validate_profile.py path/to/profile.yaml
Prints one problem per line; exit code 1 when there is any.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

LANGUAGES = {"pt-BR", "en"}
MODES = {"assistant", "auto"}
WORK_MODELS = {"remote", "hybrid", "onsite"}
TIME = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def _nonempty_str_list(data: dict, key: str, problems: list[str], required: bool = True) -> None:
    value = data.get(key)
    if value is None:
        if required:
            problems.append(f"{key}: required")
        return
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        problems.append(f"{key}: must be a list of non-empty text")
    elif required and not value:
        problems.append(f"{key}: must have at least one item")


def validate_profile(data: dict) -> list[str]:
    problems: list[str] = []
    if not isinstance(data, dict):
        return ["profile: must be a mapping"]

    if data.get("language") not in LANGUAGES:
        problems.append(f"language: must be one of {sorted(LANGUAGES)}")

    _nonempty_str_list(data, "target_roles", problems)
    _nonempty_str_list(data, "equivalent_rules", problems, required=False)
    _nonempty_str_list(data, "exclude", problems, required=False)
    _nonempty_str_list(data, "search_terms", problems)

    location = data.get("location")
    if not isinstance(location, dict) or not str(location.get("city", "")).strip():
        problems.append("location: needs a city")

    work_model = data.get("work_model")
    if (
        not isinstance(work_model, list)
        or not work_model
        or not set(work_model) <= WORK_MODELS
    ):
        problems.append(f"work_model: list with values from {sorted(WORK_MODELS)}")

    salary = data.get("salary")
    if not isinstance(salary, dict) or not salary:
        problems.append("salary: required, a mapping such as {CLT: 0, currency: BRL}")
    else:
        amounts = {k: v for k, v in salary.items() if k != "currency"}
        if not amounts or not all(isinstance(v, (int, float)) and v >= 0 for v in amounts.values()):
            problems.append("salary: needs at least one regime with a number >= 0")
        if not str(salary.get("currency", "")).strip():
            problems.append("salary: needs a currency")

    if not str(data.get("cv_path", "")).strip():
        problems.append("cv_path: required")

    mode = data.get("mode")
    if mode not in MODES:
        problems.append(f"mode: must be one of {sorted(MODES)}")
    elif mode == "auto" and data.get("auto_mode_acknowledged") is not True:
        problems.append("auto_mode_acknowledged: must be true to use mode auto (risk acknowledgment)")

    limit = (data.get("limits") or {}).get("max_applications_per_run")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
        problems.append("limits.max_applications_per_run: integer from 1 to 20")

    schedule = data.get("schedule")
    if not isinstance(schedule, list) or not schedule or not all(
        isinstance(t, str) and TIME.match(t) for t in schedule
    ):
        problems.append("schedule: list of HH:MM times (00:00 to 23:59)")

    return problems


def load_and_validate(path: Path) -> list[str]:
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return [f"profile: cannot read {path}: {error}"]
    return validate_profile(data)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_profile.py path/to/profile.yaml")
        return 2
    problems = load_and_validate(Path(argv[1]))
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
