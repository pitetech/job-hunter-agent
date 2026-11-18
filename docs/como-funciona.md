# Como funciona

🇬🇧 [Read in English](how-it-works.md)

## As peças

| Peça | O que faz |
|---|---|
| `/job-hunter:setup` | Entrevista você, lê o currículo, salva o perfil, cria o agendamento e termina com um teste seco |
| `/job-hunter:run` | Um ciclo: busca, lê cada vaga, decide, enfileira ou envia, gera o relatório |
| `/job-hunter:approve` | Modo assistente: revisa a fila e envia só o que você aprovar |
| `/job-hunter:status` | Mostra execuções, fila e perguntas pendentes; pausa, retoma ou para |

## Onde ficam seus dados

Tudo que é pessoal fica em `~/.job-hunter/` (no Windows, `C:\Users\<nome>\.job-hunter\`): `profile.yaml`, `answers.yaml`, `queue.md`, `applied.csv`, `skipped.csv`, `pending.md`, `relatorios/` (relatórios) e, opcionalmente, `telegram.env`. Nada disso está neste repositório.

## Uma execução, passo a passo

1. Para cedo se existir um arquivo `STOP` ou se outra execução estiver ativa (`run.lock`).
2. Lê seu perfil e currículo. Se faltar algo essencial, não se candidata a nada e avisa o que falta.
3. Busca no LinkedIn para cada termo: Candidatura simplificada, últimas 24 horas, mais recentes primeiro, sua cidade e seu modelo de trabalho.
4. Monta a lista completa de vagas, sem repetir, e marca as que você já se candidatou.
5. Abre e lê cada vaga. Decide: candidatar, pular (com motivo) ou pendente.
6. O modo assistente enfileira a candidatura preparada. O modo automático envia e espera o LinkedIn confirmar.
7. Escreve um relatório com todas as vagas encontradas e o motivo de cada decisão.
8. Avisa você (Telegram ou notificação do app) só quando algo precisar de você.

## Como ele decide

Uma vaga só recebe candidatura quando o cargo combina com seus `target_roles` (ou com uma das suas `equivalent_rules`), seu currículo atende os requisitos obrigatórios, nada bate com a sua lista `exclude` e a vaga é de Candidatura simplificada. Caso contrário ela é pulada com um motivo concreto, ou vai para pendente quando precisa de uma resposta que o agente não tem.

## A fila de aprovação

No modo assistente, cada candidatura preparada é um bloco em `queue.md`:

```
## 4400000000 | Acme | Product Designer
url: https://www.linkedin.com/jobs/view/4400000000/
status: queued
match_reason: design systems e pesquisa com usuários são sua experiência principal
answers:
- Anos de experiência com Figma? -> 6
```

O `status` vai de `queued` para `approved` e depois `sent`, ou para `rejected`.

## Por que ele pode parar

O LinkedIn mostra tela de login, CAPTCHA, verificação de segurança ou aviso de restrição; seu perfil está incompleto; o currículo não pôde ser lido; um formulário pede dados que o agente nunca deve preencher. Em todos esses casos ele para, não tenta contornar e relata o que aconteceu.
