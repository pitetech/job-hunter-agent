# Telegram setup (optional)

🇧🇷 [Leia em português](configurar-telegram.md)

Telegram alerts tell you when a question needs your answer or when the agent stopped. Without it, everything still works: you see the same information in the report and the app notification.

## 1. Create a bot

1. In Telegram, open a chat with **@BotFather** and send `/newbot`.
2. Choose a name and a username. BotFather replies with a **token**. Treat it like a password.

## 2. Get your chat id

1. Open a chat with your new bot and tap **Start** (or send any message).
2. The setup (`/job-hunter:setup`) can read your chat id for you, or you can find it yourself with Telegram's `getUpdates` method for your bot.

## 3. Save the file

Create `telegram.env` in `~/.job-hunter/` with two lines:

```
TOKEN=<your bot token>
CHAT_ID=<your chat id>
```

Saving it yourself is the safest option. If you paste the token in the Claude chat instead, the setup writes the file and never repeats the token, but you should then revoke it in BotFather (`/revoke`) and replace it.

## 4. Test and turn it on

The setup sends a test message. Then it sets `notifications.telegram.enabled: true` in your profile.

## Safety

- The token stays only in `telegram.env`, on your computer. It is never committed or printed.
- If it leaks, send `/revoke` to BotFather and update the file.
- The bot only sends you short alerts (company, title, the question, a link). It never receives anything from you except the first message.
