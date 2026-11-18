# Safety

🇧🇷 [Leia em português](SEGURANCA.md)

## The short version

LinkedIn's terms of service prohibit automation. Job Hunter Agent drives your own browser to read jobs and, if you allow it, to apply. That can lead to limits or restrictions on your LinkedIn account. You use it at your own risk. This project is not affiliated with LinkedIn, Anthropic or any employer, and it comes with no warranty (see the MIT license).

## What reduces the risk

- **Assistant mode is the default.** The agent prepares applications and waits for you. Automatic mode needs you to type "I understand the risk" in setup.
- **Low limits.** Default of 5 applications per run in assistant mode, 10 in automatic mode, never more than 20. Runs happen a few times a day, not in a loop.
- **Human pace.** One pass per search term per run, no reloading in loops.
- **It stops when LinkedIn pushes back.** On a sign-in page, CAPTCHA, security check or restriction notice it stops at once, does not try to get around it, and tells you.
- **Dry run.** Setup ends with a run that sends nothing, so you can check the decisions first. You can keep `dry_run: true` for as long as you like.

## What the agent will never do

- Invent facts about you. It answers only from your profile, your answers file and your CV; anything else becomes a pending question for you.
- Fill in or send CPF or other ID numbers, passwords or bank data.
- Fill in forms on outside websites. Those jobs are listed for you with a link.
- Follow companies, message recruiters or accept anything beyond the application flow.
- Create accounts or enter your LinkedIn password.

## Your data

Everything personal stays on your computer in `~/.job-hunter/` (your profile, answers, CV path, queue, reports, Telegram token). The repository contains only blank templates. There is no telemetry. The maintainers run a privacy check (`python scripts/privacy_scan.py`) before every release to keep personal data out, and you can run it yourself.

If you use Telegram, the bot token lives in `telegram.env` in that folder. Treat it like a password and revoke it in BotFather if it ever leaks.

## How to turn it off

1. **Pause:** `/job-hunter:status`, then pause the schedule.
2. **Stop at once:** ask `/job-hunter:status` to stop everything; it creates a `STOP` file in `~/.job-hunter/`. If you create it by hand on Windows, name it `STOP` or `STOP.txt` (both work). Every run and approval checks for it before it starts and before each application.
3. **Remove everything:** delete the scheduled task and the `~/.job-hunter/` folder.

## If something goes wrong

If LinkedIn warns you about unusual activity, stop using the tool, create the `STOP` file, and follow LinkedIn's instructions. Review what was sent in `applied.csv` and the reports in `~/.job-hunter/relatorios/`.
