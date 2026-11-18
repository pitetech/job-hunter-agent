# FAQ

🇧🇷 [Leia em português](faq.pt-BR.md)

## Is this allowed by LinkedIn?

No. LinkedIn's terms prohibit automation. That is why assistant mode is the default, limits are low and the agent stops when LinkedIn pushes back. You use it at your own risk. See [SAFETY.md](../SAFETY.md).

## Do I need to know how to code?

No. You install it, answer the setup questions in plain language, and that is all. Python is not required.

## What does it cost?

The project is free (MIT). You need a Claude subscription that includes Claude Code and the Chrome extension, since that is what runs it.

## Does my computer have to be on?

Yes. Scheduled tasks run in the Claude desktop app, and only while it is open. If the app was closed at the scheduled time, the run happens when you open it again.

## Does it work with sites other than LinkedIn?

Not yet. Version 1 is LinkedIn only, Easy Apply only. Jobs that send you to another website are listed for you with a link.

## What if it asks something it does not know?

It does not guess. It saves the question in `pending.md`, does not send that application, and alerts you. You can answer it with `/job-hunter:status`, and the answer is used next time.

## Can it lie about my experience?

It is built not to. It answers only from your profile, your answers file and your CV. You review the answers in assistant mode before anything is sent.

## Why did it skip a job I like?

Every skipped job has a reason in the report and in `skipped.csv`. If the rule is too strict, loosen `exclude` or add an `equivalent_rules` entry.

## How do I stop it?

Ask `/job-hunter:status` to stop everything (it creates a `STOP` file in `~/.job-hunter/`; a file named `STOP.txt` works too), or use it to pause the schedule. To remove everything, delete the scheduled task and the `~/.job-hunter/` folder.

## Something broke after LinkedIn changed its pages

The agent stops and reports instead of guessing. Please open an issue on GitHub with the report text (remove personal data first).
