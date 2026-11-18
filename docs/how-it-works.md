# How it works

🇧🇷 [Leia em português](como-funciona.md)

## The pieces

| Piece | What it does |
|---|---|
| `/job-hunter:setup` | Interviews you, reads your CV, saves your profile, creates the schedule, ends with a dry run |
| `/job-hunter:run` | One cycle: search, read every posting, decide, queue or send, report |
| `/job-hunter:approve` | Assistant mode: review the queue and send only what you approve |
| `/job-hunter:status` | See runs, queue and pending questions; pause, resume or stop |

## Where your data lives

Everything personal is in `~/.job-hunter/` (on Windows, `C:\Users\<name>\.job-hunter\`): `profile.yaml`, `answers.yaml`, `queue.md`, `applied.csv`, `skipped.csv`, `pending.md`, `relatorios/` (reports) and optionally `telegram.env`. None of it is in this repository.

## One run, step by step

1. Stop early if a `STOP` file exists or another run is active (`run.lock`).
2. Read your profile and CV. If something essential is missing, apply to nothing and tell you what.
3. Search LinkedIn for each search term: Easy Apply, last 24 hours, newest first, your city and work model.
4. Build the full list of jobs, without duplicates, and mark the ones you already applied to.
5. Open and read every job. Decide: apply, skip (with a reason) or pending.
6. Assistant mode queues the prepared application. Automatic mode sends it and waits for LinkedIn to confirm.
7. Write a report with every job found and the reason for each decision.
8. Alert you (Telegram or app notification) only when something needs you.

## How it decides

A job is applied to only when the role fits your `target_roles` (or one of your `equivalent_rules`), your CV meets the mandatory requirements, nothing matches your `exclude` list, and it is an Easy Apply job. Otherwise it is skipped with a concrete reason, or goes to pending when it needs an answer the agent does not have.

## The approval queue

In assistant mode each prepared application is a block in `queue.md`:

```
## 4400000000 | Acme | Product Designer
url: https://www.linkedin.com/jobs/view/4400000000/
status: queued
match_reason: design systems and user research are your core experience
answers:
- Years of experience with Figma? -> 6
```

`status` goes from `queued` to `approved` to `sent`, or to `rejected`.

## Why it may stop

LinkedIn shows a sign-in page, a CAPTCHA, a security check or a restriction notice; your profile is incomplete; the CV cannot be read; a form needs data the agent must never fill in. In all these cases it stops, does not try to get around it and reports what happened.
