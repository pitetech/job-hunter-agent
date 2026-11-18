# Configurar o Telegram (opcional)

🇬🇧 [Read in English](telegram-setup.md)

Os alertas do Telegram avisam quando uma pergunta precisa da sua resposta ou quando o agente parou. Sem ele, tudo continua funcionando: você vê as mesmas informações no relatório e na notificação do app.

## 1. Criar um bot

1. No Telegram, abra uma conversa com o **@BotFather** e envie `/newbot`.
2. Escolha um nome e um usuário. O BotFather responde com um **token**. Trate como uma senha.

## 2. Descobrir seu chat id

1. Abra uma conversa com o seu novo bot e toque em **Iniciar** (ou mande qualquer mensagem).
2. A configuração (`/job-hunter:setup`) pode ler o seu chat id por você, ou você pode achar sozinho com o método `getUpdates` do Telegram para o seu bot.

## 3. Salvar o arquivo

Crie o `telegram.env` em `~/.job-hunter/` com duas linhas:

```
TOKEN=<token do seu bot>
CHAT_ID=<seu chat id>
```

Salvar você mesmo é a opção mais segura. Se você colar o token no chat do Claude, a configuração grava o arquivo e nunca repete o token, mas depois você deve revogá-lo no BotFather (`/revoke`) e trocar.

## 4. Testar e ligar

A configuração envia uma mensagem de teste. Depois ela define `notifications.telegram.enabled: true` no seu perfil.

## Segurança

- O token fica só no `telegram.env`, no seu computador. Nunca é commitado nem impresso.
- Se vazar, envie `/revoke` ao BotFather e atualize o arquivo.
- O bot só manda alertas curtos para você (empresa, vaga, a pergunta, um link). Ele nunca recebe nada de você além da primeira mensagem.
