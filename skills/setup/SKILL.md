---
name: setup
description: Guided first-time setup for job-hunter. Interviews the person (role, location, salary, work model, languages, what to never accept), reads their CV, saves their private profile, optionally connects Telegram, creates the scheduled task and runs a safe dry run. Use when the user wants to start using job-hunter or change their profile.
---

# job-hunter: setup

Talk to the person in their own language (Portuguese or English, detect it from how they write). Ask **one question at a time**, in plain words, and wait for the answer. Never fill an answer in for them: when you propose a default, say it is your proposal.

This plugin's folder is the folder that contains `.claude-plugin/plugin.json` (the `CLAUDE_PLUGIN_ROOT` environment variable points to it when set). Find it first: the templates (`templates/profile.example.yaml`, `templates/answers.example.yaml`), `docs/telegram-setup.md` and `scripts/validate_profile.py` live there. If you cannot find the templates, stop and tell the person; never write `profile.yaml` from memory, because the keys must match what the `run` skill reads.

Their private data lives in `~/.job-hunter/` (Windows: `C:\Users\<name>\.job-hunter\`, or the folder in the `JOB_HUNTER_HOME` environment variable). Never write personal data anywhere else, and never inside this plugin's own folder.

## 1. Check the requirements

Tell them what job-hunter needs and check each item:
- The Claude desktop app with Claude Code (scheduled tasks only run there, and only while the app is open).
- The Claude in Chrome extension connected to their Chrome.
- Chrome signed in to their own LinkedIn account (they sign in themselves; you never handle passwords).
- Python is **not** required.

Use `mcp__claude-in-chrome__tabs_context_mcp` to confirm the extension answers, then open `https://www.linkedin.com/jobs/` in a new tab and check that it shows the person's own account (not a sign-in page); close the tab afterwards. If something is missing, explain how to fix it and stop until it is ready. If `profile.yaml` already exists, ask whether they want to change it or start over, and keep a copy named `profile.yaml.bak` before replacing it.

## 2. Read the CV and show what you understood

Ask for the path to their CV (PDF) and read it. If you cannot read it (a scanned image with no text, a password-protected or corrupt file), say so, ask for another file or a text version, and stop. Invent nothing.

Then show what you understood in a short list: current and past roles, years of experience per area, tools, certifications, languages, education. Ask them to correct anything wrong. What they confirm becomes `answers.yaml` (`facts:` entries with `source: cv`, or `source: user` for what they tell you).

## 3. Interview, one question at a time

Ask, in this order, skipping what the CV already settled:
1. Which role(s) do you want? (`target_roles`; propose `search_terms` from them and let them edit.)
2. Which neighbouring roles are also fine, and when? (`equivalent_rules`, in plain words.)
3. What should never be accepted? (`exclude`: on-site outside the city, fluent English required, industries, companies.)
4. City, search radius, and do you accept remote? (`location`)
5. Remote, hybrid, on-site: which? (`work_model`)
6. Expected monthly salary for each contract type they care about, such as CLT or PJ, and the currency. (`salary`) Make clear that an amount of 0 means "not set" and that the agent will not apply without one.
7. Your real language levels. (`languages`) The agent never claims more than this.
8. How many on-site days per week can you do, can you commute, and when could you start? (`availability`)

Save nothing yet; collect everything first.

## 4. Choose the mode (assistant is the default)

Explain plainly:
- **assistant (recommended):** the agent finds and checks jobs, prepares the answers and puts them in a queue. Nothing is sent until the person approves with `/job-hunter:approve`.
- **auto:** the agent sends applications by itself, within the per-run limit.

State the risk honestly: LinkedIn's terms prohibit automation, so using this tool can lead to limits or restrictions on their account. They use it at their own risk, and `auto` raises that risk. Keep `assistant` unless they clearly want `auto`. To enable `auto`, ask them to type exactly: **I understand the risk** (Portuguese: **Eu entendo o risco**). Anything else keeps `assistant`. Only then write `auto_mode_acknowledged: true`.

Defaults you propose: `limits.max_applications_per_run` 5 (assistant) or 10 (auto), and `schedule` three times a day (`10:00`, `15:00`, `21:00`).

## 5. Telegram (optional)

Ask whether they want alerts on Telegram when a question needs them. If yes, guide them with `docs/telegram-setup.md`: create a bot with @BotFather, send the bot a first message, and get the chat id. The safest way is that they save the file themselves: `telegram.env` in the data folder with two lines, `TOKEN=...` and `CHAT_ID=...`. If they paste the token in the chat, write the file for them, never repeat the token back, and recommend they revoke the token in BotFather afterwards and replace it. In both cases (they saved the file or you did), read the file without printing it, send a test message, and only if it arrives set `notifications.telegram.enabled: true` in the profile; if the test fails, explain what to check and keep it `false`. If they decline Telegram, set `notifications.telegram.enabled: false`.

## 6. Save, validate, schedule

1. Write `profile.yaml` and `answers.yaml` using the structure in `templates/profile.example.yaml` and `templates/answers.example.yaml`. Set `dry_run: true` for now.
2. Validate: if this plugin's folder has `scripts/validate_profile.py` and Python exists, run it; otherwise check by hand that every field in the template is present and valid. Fix problems with the person before continuing.
3. Create the scheduled task (the Claude desktop app's scheduled task tool) with the times from `schedule`, with the prompt: "Run the job-hunter `run` skill." Tell them the task only runs while the Claude app is open.

## 7. Dry run, then go live

Run the `run` skill once now with `dry_run: true`. Show them the report: every job found, what the agent would apply to or queue, and what it would skip and why. Ask whether the decisions look right; adjust `target_roles`, `equivalent_rules` or `exclude` if not. When they are happy, set `dry_run: false`.

## 8. Tell them how to stay in control

- `/job-hunter:status` shows runs, queue and pending questions, and can pause or resume the schedule.
- Asking `/job-hunter:status` to stop everything creates a `STOP` file in the data folder that halts any run (a file named `STOP.txt` also works, since Windows adds `.txt` when it is created by hand).
- `/job-hunter:approve` reviews and sends the queued applications.
- To remove everything: delete the scheduled task and the `~/.job-hunter/` folder.
