# Contributing / Contribuindo

Thanks for helping! / Obrigado por ajudar!

## Ground rules / Regras

- **No personal data, ever.** No names, e-mails, phone numbers, CV files, tokens or real salary figures in code, docs, issues or screenshots. `python scripts/privacy_scan.py` must pass.
- **Docs in two languages.** Every English doc has a Portuguese twin with the same structure (`python scripts/check_docs_parity.py`). If you only speak one language, say so in the pull request and we will help with the other.
- **Safety first.** Do not weaken the safety rules (assistant mode by default, limits, stop on CAPTCHA, never invent facts about the user). Changes that do are not accepted.
- **No hosted services or telemetry.**

## Run the checks / Rodar as verificações

```
pip install -r requirements-dev.txt
python -m unittest discover -s tests -t . -v
python scripts/privacy_scan.py
python scripts/lint_skills.py
python scripts/check_docs_parity.py
```

To check that no personal term appears in the skills, list your own terms (name, employer, e-mail, salary figures), one per line, in `~/.job-hunter/forbidden-terms.txt`; `lint_skills.py` reads it locally. That file is never committed.

## Ideas welcome / Ideias bem-vindas

Other job sources, a daily digest, tailoring the CV to each job, a weekly funnel report, ready-made profiles by field. Open an issue to discuss before a big change.
