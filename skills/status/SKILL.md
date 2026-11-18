---
name: status
description: Show the state of job-hunter (last runs, approval queue, pending questions) and control it: pause or resume the schedule, create or remove the STOP file. Use when the user asks what job-hunter did, wants to pause it, resume it or stop everything.
---

# job-hunter: status and controls

Data folder: `~/.job-hunter/` (or the folder in `JOB_HUNTER_HOME`). Speak the language of `profile.language`. This skill only reads and toggles things; it never applies to a job.

## 1. Show the state

Read the files and give a short summary:
- **Schedule:** the job-hunter scheduled task, its times, whether it is enabled, last and next run (use the scheduled task tools of the Claude app).
- **Recent runs:** the three newest files in `relatorios/` with their totals (found, queued or applied, skipped, pending).
- **Queue:** how many blocks in `queue.md` (the approval queue) have `status: queued` and how many are `approved`, and remind them to run `/job-hunter:approve`.
- **Pending:** every block in `pending.md` with `status: open` and its exact `question:`, so the person can answer it. When they answer, save the answer to `answers.yaml` (`source: user`) and set that block to `status: answered`, so the next run evaluates the job again. Tell them that a job whose form needs an outside site is not retried automatically and must be applied to by hand.
- **Mode and safety:** the profile `mode`, `dry_run`, and whether a STOP file exists.

## 2. Controls

Do only what the person asks:
- **Pause:** disable the scheduled task. **Resume:** enable it again.
- **Stop everything now:** create an empty file named `STOP` in the data folder (you do it, so the name is exact). Any run or approval checks for a STOP file before it starts and before each application, and does nothing while it exists. A file named `STOP.txt` counts too, because Windows adds the `.txt` when someone creates the file by hand. **Allow runs again:** delete the STOP file (`STOP` or `STOP.txt`).
- **Change mode or limits:** edit `profile.yaml`. Switching to `auto` requires the person to type exactly "I understand the risk" ("Eu entendo o risco") and sets `auto_mode_acknowledged: true`; otherwise stay in `assistant`. Remind them LinkedIn's terms prohibit automation and that they use it at their own risk.
- **Remove everything:** with the person's explicit confirmation, delete the scheduled task and then the data folder. Say that this is permanent.
