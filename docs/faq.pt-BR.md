# Perguntas frequentes

🇬🇧 [Read in English](faq.md)

## O LinkedIn permite isso?

Não. Os termos do LinkedIn proíbem automação. Por isso o modo assistente é o padrão, os limites são baixos e o agente para quando o LinkedIn reage. Você usa por sua conta e risco. Veja [SEGURANCA.md](../SEGURANCA.md).

## Preciso saber programar?

Não. Você instala, responde as perguntas da configuração em linguagem normal e pronto. Python não é necessário.

## Quanto custa?

O projeto é gratuito (MIT). Você precisa de uma assinatura do Claude que inclua o Claude Code e a extensão do Chrome, porque é isso que o executa.

## O computador precisa ficar ligado?

Sim. As tarefas agendadas rodam no app desktop do Claude, e só enquanto ele está aberto. Se o app estava fechado na hora agendada, a execução acontece quando você abrir de novo.

## Funciona em outros sites além do LinkedIn?

Ainda não. A versão 1 é só LinkedIn, só Candidatura simplificada. Vagas que levam para outro site são listadas para você com o link.

## E se ele perguntar algo que não sabe?

Ele não chuta. Guarda a pergunta em `pending.md`, não envia aquela candidatura e avisa você. Você responde com `/job-hunter:status` e a resposta é usada na próxima vez.

## Ele pode mentir sobre a minha experiência?

Foi feito para não mentir. Responde só com seu perfil, seu arquivo de respostas e seu currículo. No modo assistente você revisa as respostas antes de qualquer envio.

## Por que ele pulou uma vaga que eu gostei?

Toda vaga pulada tem um motivo no relatório e no `skipped.csv`. Se a regra estiver rígida demais, afrouxe o `exclude` ou adicione uma entrada em `equivalent_rules`.

## Como paro tudo?

Peça ao `/job-hunter:status` para parar tudo (ele cria um arquivo `STOP` em `~/.job-hunter/`; um arquivo `STOP.txt` também funciona), ou use-o para pausar o agendamento. Para remover tudo, apague a tarefa agendada e a pasta `~/.job-hunter/`.

## Algo quebrou depois que o LinkedIn mudou as páginas

O agente para e relata em vez de adivinhar. Abra uma issue no GitHub com o texto do relatório (remova dados pessoais antes).
