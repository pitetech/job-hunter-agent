# Segurança

🇬🇧 [Read in English](SAFETY.md)

## Resumo

Os termos de uso do LinkedIn proíbem automação. O Job Hunter Agent conduz o seu próprio navegador para ler vagas e, se você permitir, se candidatar. Isso pode levar a limites ou restrições na sua conta do LinkedIn. Você usa por sua conta e risco. Este projeto é sem vínculo com o LinkedIn, a Anthropic ou qualquer empresa contratante, e vem sem garantia (veja a licença MIT).

## O que reduz o risco

- **O modo assistente é o padrão.** O agente prepara as candidaturas e espera você. O modo automático exige que você digite "Eu entendo o risco" na configuração.
- **Limites baixos.** Padrão de 5 candidaturas por execução no modo assistente, 10 no automático, nunca mais que 20. As execuções acontecem algumas vezes por dia, não em repetição contínua.
- **Ritmo humano.** Uma passada por termo de busca por execução, sem recarregar em repetição.
- **Ele para quando o LinkedIn reage.** Em tela de login, CAPTCHA, verificação de segurança ou aviso de restrição, ele para na hora, não tenta contornar e avisa você.
- **Teste seco.** A configuração termina com uma execução que não envia nada, para você conferir as decisões antes. Você pode manter `dry_run: true` pelo tempo que quiser.

## O que o agente nunca fará

- Inventar fatos sobre você. Ele responde só com seu perfil, seu arquivo de respostas e seu currículo; qualquer outra coisa vira uma pergunta pendente para você.
- Preencher ou enviar CPF ou outros documentos, senhas ou dados bancários.
- Preencher formulários de sites externos. Essas vagas são listadas para você com o link.
- Seguir empresas, mandar mensagem a recrutadores ou aceitar algo além do fluxo da candidatura.
- Criar contas ou digitar a sua senha do LinkedIn.

## Seus dados

Tudo que é pessoal fica no seu computador em `~/.job-hunter/` (perfil, respostas, caminho do currículo, fila, relatórios, token do Telegram). O repositório só contém modelos em branco. Não há telemetria. Os mantenedores rodam uma verificação de privacidade (`python scripts/privacy_scan.py`) antes de cada versão para manter dados pessoais de fora, e você mesmo pode rodá-la.

Se você usar o Telegram, o token do bot fica em `telegram.env` nessa pasta. Trate como uma senha e revogue no BotFather se vazar.

## Como desligar

1. **Pausar:** `/job-hunter:status`, depois pause o agendamento.
2. **Parar na hora:** peça ao `/job-hunter:status` para parar tudo; ele cria um arquivo `STOP` em `~/.job-hunter/`. Se criar à mão no Windows, use o nome `STOP` ou `STOP.txt` (os dois funcionam). Toda execução e toda aprovação verificam isso antes de começar e antes de cada candidatura.
3. **Remover tudo:** apague a tarefa agendada e a pasta `~/.job-hunter/`.

## Se algo der errado

Se o LinkedIn avisar sobre atividade incomum, pare de usar a ferramenta, crie o arquivo `STOP` e siga as instruções do LinkedIn. Confira o que foi enviado em `applied.csv` e os relatórios em `~/.job-hunter/relatorios/`.
