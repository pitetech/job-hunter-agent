# Job Hunter Agent

🇧🇷 [Leia em português](README.pt-BR.md)

## What it is

Job Hunter Agent is a plugin for Claude Code that checks LinkedIn for new jobs a few times a day, reads each posting, compares it with **your** profile and CV, and prepares (or sends) your applications. You stop refreshing LinkedIn; it tells you what matters.

You describe what you want once (role, city, salary, work model, what to never accept) and it does the rest. Everything stays on your computer.

## Safety notice

> **Read this before using.** LinkedIn's terms of service prohibit automation. Using this tool can lead to limits or restrictions on your LinkedIn account. You use it at your own risk. This project is **not affiliated** with LinkedIn, Anthropic or any employer.
>
> By default it runs in **assistant mode**: it never sends an application on its own; you approve each one. **Automatic mode** is optional and requires you to type a risk acknowledgment during setup. More in [SAFETY.md](SAFETY.md).

## How it works

```
 your profile + CV
        │
        ▼
 search LinkedIn (new jobs, last 24h, Easy Apply)
        │
        ▼
 read every posting ── compare with your profile ── skip / pending / apply
        │
        ▼
 assistant mode: queue for your approval     auto mode: send
        │
        ▼
 report + optional Telegram alert for questions it cannot answer
```

1. `/job-hunter:setup` interviews you and saves your private profile.
2. A scheduled task runs `/job-hunter:run` (three times a day by default).
3. In assistant mode, you review the queue with `/job-hunter:approve`.
4. `/job-hunter:status` shows what happened and lets you pause or stop everything.

The agent never invents facts about you. If a form asks something it cannot answer from your profile and CV, it does not send the application: it saves the question and warns you.

## Requirements

- The **Claude desktop app** with Claude Code (scheduled tasks only run there, while the app is open).
- The **Claude in Chrome** extension, connected to your Chrome.
- Chrome signed in to **your own** LinkedIn account.
- A PDF of your CV.
- Optional: a Telegram account for alerts.

## Install and first setup

```
/plugin marketplace add pitetech/job-hunter-agent
/plugin install job-hunter@pitetech
/job-hunter:setup
```

If these commands differ in your version of Claude Code, follow the current plugin instructions in the Claude Code documentation and point it at this repository. The setup takes about 15 minutes: it reads your CV, asks you one question at a time, saves your profile in `~/.job-hunter/`, creates the schedule and finishes with a **dry run** that sends nothing, so you can check its decisions.

## Example profile and report

Your profile is a plain file (never committed) based on [templates/profile.example.yaml](templates/profile.example.yaml):

```yaml
target_roles: [Product Designer]
location: { city: Rio de Janeiro, radius_km: 40, accept_remote: true }
work_model: [remote, hybrid]
salary: { CLT: 0, PJ: 0, currency: BRL }   # you fill in your real numbers
exclude: ["on-site outside my city", "fluent English required"]
mode: assistant
```

Every run writes a report like this:

```
Totals: 8 found / 2 queued / 1 already applied / 4 skipped / 1 pending
| Company | Title             | Place        | Decision | Reason                        |
| Acme    | Product Designer  | Remote       | Queued   | design systems + research     |
| Globex  | Graphic Designer  | On-site, SP  | Skipped  | on-site outside your city     |
| Initech | UX Designer       | Hybrid       | Pending  | asks for a portfolio link     |
```

## Assistant vs automatic mode

| | Assistant (default) | Automatic |
|---|---|---|
| Sends applications | Only after you approve | By itself, within the per-run limit |
| Where you decide | `/job-hunter:approve` | Nowhere, you review reports afterwards |
| Account risk | Lower | Higher |
| How to enable | Default | Type the acknowledgment in setup |

## Turn it off and remove everything

- Pause: `/job-hunter:status` then pause.
- Stop at once: ask `/job-hunter:status` to stop everything (it creates the `STOP` file for you). If you create it by hand on Windows, the name must be `STOP` or `STOP.txt`; both work.
- Remove everything: delete the scheduled task and the `~/.job-hunter/` folder.

## FAQ and limitations

See [docs/faq.md](docs/faq.md) and [docs/how-it-works.md](docs/how-it-works.md). Main limits: LinkedIn only, Easy Apply only, needs the Claude app open and your computer on, and LinkedIn can change its pages at any time (the agent then stops and warns you instead of guessing).

## Contributing and license

Contributions are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the MIT license, see [LICENSE](LICENSE). Made by Pitetech.
