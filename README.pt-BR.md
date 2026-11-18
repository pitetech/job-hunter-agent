# Job Hunter Agent

🇬🇧 [Read in English](README.md)

## O que é

O Job Hunter Agent é um plugin do Claude Code que olha o LinkedIn algumas vezes por dia, lê cada vaga nova, compara com o **seu** perfil e currículo, e prepara (ou envia) as candidaturas. Você para de ficar atualizando o LinkedIn: ele avisa o que importa.

Você descreve o que quer uma vez (cargo, cidade, salário, modelo de trabalho, o que nunca aceitar) e ele faz o resto. Tudo fica no seu computador.

## Aviso de segurança

> **Leia antes de usar.** Os termos de uso do LinkedIn proíbem automação. Usar esta ferramenta pode levar a limites ou restrições na sua conta do LinkedIn. Você usa por sua conta e risco. Este projeto é **sem vínculo** com o LinkedIn, a Anthropic ou qualquer empresa contratante.
>
> Por padrão ele roda no **modo assistente**: nunca envia uma candidatura sozinho, você aprova cada uma. O **modo automático** é opcional e exige que você digite um aceite do risco durante a configuração. Mais em [SEGURANCA.md](SEGURANCA.md).

## Como funciona

```
 seu perfil + currículo
        │
        ▼
 busca no LinkedIn (vagas novas, últimas 24h, Candidatura simplificada)
        │
        ▼
 lê cada vaga ── compara com o perfil ── pular / pendente / candidatar
        │
        ▼
 modo assistente: fila para sua aprovação     modo automático: envia
        │
        ▼
 relatório + alerta opcional no Telegram para perguntas que ele não sabe responder
```

1. `/job-hunter:setup` entrevista você e salva seu perfil privado.
2. Uma tarefa agendada roda o `/job-hunter:run` (três vezes ao dia por padrão).
3. No modo assistente, você revisa a fila com `/job-hunter:approve`.
4. `/job-hunter:status` mostra o que aconteceu e deixa você pausar ou parar tudo.

O agente nunca inventa fatos sobre você. Se um formulário perguntar algo que ele não consegue responder com seu perfil e currículo, ele não envia a candidatura: guarda a pergunta e avisa você.

## Requisitos

- O **app desktop do Claude** com Claude Code (as tarefas agendadas só rodam ali, com o app aberto).
- A extensão **Claude in Chrome**, conectada ao seu Chrome.
- O Chrome logado na **sua própria** conta do LinkedIn.
- O seu currículo em PDF.
- Opcional: uma conta no Telegram para receber alertas.

## Instalação e primeira configuração

```
/plugin marketplace add pitetech/job-hunter-agent
/plugin install job-hunter@pitetech
/job-hunter:setup
```

Se esses comandos forem diferentes na sua versão do Claude Code, siga as instruções atuais de plugins na documentação do Claude Code apontando para este repositório. A configuração leva uns 15 minutos: ele lê seu currículo, faz uma pergunta por vez, salva seu perfil em `~/.job-hunter/`, cria o agendamento e termina com um **teste seco** que não envia nada, para você conferir as decisões dele.

## Exemplo de perfil e de relatório

Seu perfil é um arquivo simples (nunca vai para o Git), baseado em [templates/profile.example.yaml](templates/profile.example.yaml):

```yaml
target_roles: [Product Designer]
location: { city: Rio de Janeiro, radius_km: 40, accept_remote: true }
work_model: [remote, hybrid]
salary: { CLT: 0, PJ: 0, currency: BRL }   # você preenche seus números reais
exclude: ["presencial fora da minha cidade", "inglês fluente obrigatório"]
mode: assistant
```

Cada execução gera um relatório assim:

```
Totais: 8 encontradas / 2 na fila / 1 já candidatada / 4 puladas / 1 pendente
| Empresa | Vaga              | Local        | Decisão   | Motivo                         |
| Acme    | Product Designer  | Remoto       | Na fila   | design systems + pesquisa      |
| Globex  | Graphic Designer  | Presencial   | Pulada    | presencial fora da sua cidade  |
| Initech | UX Designer       | Híbrido      | Pendente  | pede link de portfólio         |
```

## Modo assistente vs automático

| | Assistente (padrão) | Automático |
|---|---|---|
| Envia candidaturas | Só depois da sua aprovação | Sozinho, dentro do limite por execução |
| Onde você decide | `/job-hunter:approve` | Em lugar nenhum, você revisa os relatórios depois |
| Risco para a conta | Menor | Maior |
| Como ativar | Já vem ativo | Digitar o aceite na configuração |

## Como desligar e remover tudo

- Pausar: `/job-hunter:status` e depois pausar.
- Parar na hora: peça ao `/job-hunter:status` para parar tudo (ele cria o arquivo `STOP` para você). Se criar à mão no Windows, o nome deve ser `STOP` ou `STOP.txt`; os dois funcionam.
- Remover tudo: apague a tarefa agendada e a pasta `~/.job-hunter/`.

## Perguntas frequentes e limitações

Veja [docs/faq.pt-BR.md](docs/faq.pt-BR.md) e [docs/como-funciona.md](docs/como-funciona.md). Principais limites: só LinkedIn, só Candidatura simplificada, precisa do app do Claude aberto e do computador ligado, e o LinkedIn pode mudar as páginas a qualquer momento (o agente então para e avisa em vez de adivinhar).

## Contribuir e licença

Contribuições são bem-vindas, veja [CONTRIBUTING.md](CONTRIBUTING.md). Licença MIT, veja [LICENSE](LICENSE). Feito pela Pitetech.
