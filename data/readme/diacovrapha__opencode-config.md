# opencode-config

> **English summary:** Global config for [opencode](https://opencode.ai) (open-source terminal coding agent). It assembles a small "team" of agents with different LLMs to balance quality and cost: Anthropic Claude models (paid per token) handle decision and review roles; MiniMax Coding Plan models (subscription, $0/token) handle volume — implementation, exploration, research. The workflow is two-stage: an `ideador` (ideation partner) refines the request into a structured BRIEF, then a `chefe` (orchestrator) executes it through the team. See [docs/AI-SETUP.md](docs/AI-SETUP.md) if you're an AI porting this config to another user.

## O que é

Esta é a **configuração global do opencode** ([opencode.ai](https://opencode.ai)), um agente de código open source para terminal. Ela monta um "time" de agentes, cada um apontando para um modelo diferente, para **equilibrar qualidade e custo**:

- Os **modelos Claude** (Anthropic, pagos por token) ficam nos papéis de **decisão e revisão**: ideação, orquestração, arquitetura e QA.
- Os **modelos MiniMax** (Coding Plan, assinatura de custo **$0 por token**) fazem o **volume**: implementação, exploração read-only e pesquisa externa.

O resultado é um time em que cada chamada cara é justificada e o trabalho repetitivo não consome orçamento.

## Fluxo em 2 etapas

```
   ┌────────────────────────┐                  ┌──────────────────────────┐
   │  ETAPA 1 — IDEAÇÃO     │                  │  ETAPA 2 — EXECUÇÃO      │
   │                        │                  │                          │
   │  Você (humano)         │                  │  chefe (orquestrador)    │
   │       ↕ conversa       │                  │       │                  │
   │  ideador               │  ─── BRIEF ───▶  │       ├─ @senior (plano) │
   │   │                    │  (aprovado)      │       │   └─ @pleno      │
   │   ├─ @pesquisador      │                  │       ├─ @qa (revisão)   │
   │   └─ @explore          │                  │       ├─ @junior        │
   │                        │                  │       └─ @pesquisador   │
   └────────────────────────┘                  └──────────────────────────┘
```

**Etapa 1 — Ideação.** O agente que abre por padrão é o `ideador`. Ele entende o pedido, aciona `@pesquisador` (e `@explore` quando precisa ler código existente), devolve alternativas com trade-offs, faz perguntas numeradas ao usuário e, **somente após aprovação explícita**, entrega um **BRIEF** com:

- **Objetivo** — em uma linha.
- **Contexto** — por que estamos fazendo isso.
- **Escopo** — o que entra.
- **Fora do escopo** — o que deliberadamente não entra.
- **Decisões tomadas** — pontos em que o usuário já escolheu.
- **Ferramentas aprovadas para instalar** — cada uma marcada como **"requer revisão de segurança do @senior antes de instalar"**.
- **Critérios de aceite** — checklist verificável.
- **Complexidade estimada** — simples / média / complexa.
- **Riscos** — principais pontos de falha.

**Etapa 2 — Execução.** Você troca para o `chefe` (pressione `Tab` no opencode) e manda executar o BRIEF. O `chefe` despacha para `@senior` (plano), `@pleno` (implementação), `@qa` (revisão), `@junior` (tarefas mecânicas), `@pesquisador` (pesquisa) e/ou `@explore` (leitura read-only no codebase). Tarefas triviais ou correções pontuais podem pular a etapa 1.

## O time

Valores lidos diretamente de `opencode.jsonc` e `agents/*.md`.

| Agente | Modo | Modelo | Papel (resumo) | Permissões principais |
|---|---|---|---|---|
| `ideador` | primary | `anthropic/claude-sonnet-5-5` | Ideação estratégica (default ao abrir). Não implementa. | `edit: deny`, `bash: deny`, `webfetch: allow`, `task: { "*": deny, pesquisador: allow, explore: allow }` |
| `chefe` | primary | `anthropic/claude-sonnet-5-5` | Orquestrador a partir do BRIEF. Não lê arquivos grandes. | `edit: deny`, `bash: { "*": deny, "git status*": allow, "git log*": allow, "git diff*": allow }`, `webfetch: deny`, `task: allow` |
| `senior` | subagent | `anthropic/claude-opus-5-5` | Arquitetura, bugs difíceis, planos, revisão de segurança de ferramentas de terceiros. | `edit: allow`, `bash: allow`, `task: { "*": deny, explore: allow }` |
| `qa` | subagent | `anthropic/claude-sonnet-5-5` | Revisão contra critérios de aceite. Não corrige produção. | `edit` apenas em `**/test_*`, `**/*_test.*`, `**/*.test.*`, `**/*.spec.*`, `**/tests/**`, `**/test/**`, `**/__tests__/**`; `bash: allow`; `task: deny` |
| `pleno` | subagent | `minimax-coding-plan/MiniMax-M3` (variant: `thinking`) | Features médias, refatorações e implementação dos planos do senior. Padrão para código. | `edit: allow`, `bash: allow`, `task: { "*": deny, explore: allow, senior: allow }` |
| `junior` | subagent | `minimax-coding-plan/MiniMax-M2.7-highspeed` | Tarefas simples e bem definidas. Sem expansão de escopo. | `edit: allow`, `bash: allow`, `task: { "*": deny, senior: allow }` |
| `pesquisador` | subagent | `minimax-coding-plan/MiniMax-M3` | Pesquisa externa (GitHub via `gh`, Reddit, HN, docs). Não instala nada. | `edit: deny`, `webfetch: allow`, `bash: { "*": deny, "gh search *": allow, "gh repo view *": allow, "gh release list *": allow, "gh release view *": allow, "gh api *": ask }`, `task: deny` |
| `explore` (built-in) | subagent | `minimax-coding-plan/MiniMax-M2.7-highspeed` | Busca/exploração read-only no codebase. | read-only (built-in do opencode) |

Cada agente também tem um limite de `steps` no frontmatter — `junior: 60`, `pleno: 100` — para travar loops longos e forçar reporte em vez de improviso.

### Protocolo de ajuda ao sênior e checkpoints

- `@junior` e `@pleno` **podem consultar o `@senior` sozinhos**, até **2 vezes por tarefa**. Na terceira dificuldade, **PARE** e reporte ao chefe. Formato do pedido: Objetivo · O que já fiz · O que tentei · Erro exato · Hipótese · Pergunta (≤ ~30 linhas).
- **Gatilhos:** mesmo erro após 2 tentativas; comando que trava/estoura timeout; ~15 passos sem progresso; dúvida de arquitetura/onde mexer; escopo maior do que o esperado.
- **Checkpoints:** para tarefas longas ou arriscadas, o chefe pede **"com checkpoints"** no prompt; o executor então envia ao `@senior` um resumo curto no fim de cada etapa e segue a direção dada. O `@senior` responde em modo mentor (~15 linhas: Diagnóstico · Próximos passos · Não faça · Critério de pronto), **sem implementar**.
- **Regras anti-trava** (junior/pleno): nunca rodar em primeiro plano comandos que não terminam (`npm run dev`, `vite`, `tauri dev`, watchers, apps GUI); usar timeouts e `Invoke-CimMethod Win32_Process Create` no Windows. Prefira comandos que terminam (`build`, `test`, `typecheck`, `lint`).

### Memória local de projetos (opcional)

`opencode.jsonc` libera acesso à pasta `C:\projetos\_memoria\` (`permission.external_directory: { "C:/projetos/_memoria/**": "allow" }`). No início de um trabalho o `ideador` ou o `chefe` lê (se existirem) `C:\projetos\_memoria\INDEX.md` e `C:\projetos\_memoria\<nome-da-pasta-do-projeto>.md`, mais o `AGENTS.md` da raiz do projeto — contexto rápido antes de propor ou delegar. O chefe pede ao `@junior` para atualizar a memória local no fim de entregas relevantes (estado, próximos passos, decisões e armadilhas, com data); se algo técnico mudou, também atualizar o `AGENTS.md` **público**. **A pasta `_memoria` nunca vai para o repositório público do projeto.** O caminho é adaptável — se você mover a pasta, ajuste a permissão no `opencode.jsonc`.

## Princípios de economia de tokens

- **Escada de escalonamento** `junior → pleno → senior`. Sobe um nível só quando o anterior não dá conta.
- **`senior` planeja, `pleno` implementa.** Modelo caro raramente escreve código — escreve um plano curto que o pleno executa.
- **`chefe` não lê arquivos grandes sozinho.** Para investigar código existente, chama `@explore`.
- **Subagentes devolvem respostas curtas.** Todo prompt termina pedindo saída concisa: "o que mudou / como testou / bloqueios" (junior/pleno) ou "conclusão / ações / riscos" (senior).
- **Pesquisa feita em modelo de custo $0.** O `@pesquisador` roda em MiniMax, então webfetch e `gh search` não custam.
- **QA focado no diff.** Recebe só os arquivos alterados e os critérios de aceite — não lê o projeto inteiro.

## Segurança

- **Nenhuma ferramenta de terceiros é instalada sem aprovação do usuário e revisão do `senior`.** Mesmo quando o `pesquisador` recomenda, quem instala de fato é o `junior` ou `pleno`, e só depois do `@senior` dar veredito claro (`APROVAR` / `REPROVAR` / `APROVAR COM RESSALVAS`).
- **Permissões restritas por agente.** Cada agente tem só as ferramentas que precisa (ver tabela acima). Por exemplo, `chefe` e `ideador` não editam arquivos; `pesquisador` não escreve nem delega; `qa` só mexe em arquivos de teste.
- **Nenhuma credencial no repositório.** O opencode guarda credenciais em `%USERPROFILE%\.local\share\opencode\auth.json` (Windows) ou `~/.local/share/opencode/auth.json` (Linux/macOS). O `.gitignore` desta config já bloqueia `auth.json`, `.env`, `*.key` e `*.pem`.
- **Plugin isolado.** `plugins/hud-launcher.js` é todo em try/catch, não-await, `detached`+`unref`, e só age no Windows quando o executável do [opencode HUD](https://github.com/diacovrapha/opencode-hud) existe. Se algo der errado, o opencode inicia normalmente.

## Estrutura de arquivos

```
.
├── README.md                      # este arquivo
├── LICENSE                        # MIT (2026, diacovrapha)
├── .gitignore                     # ignora node_modules/, auth.json, .env, *.key, *.pem…
├── opencode.jsonc                 # config global (default_agent, model, small_model, agent.*)
├── package.json                   # única dep: @opencode-ai/plugin 1.19.3
├── package-lock.json              # lockfile do npm
├── agents/
│   ├── chefe.md                   # orquestrador (primary, Sonnet)
│   ├── ideador.md                 # parceiro de ideação (primary, Sonnet)
│   ├── junior.md                  # tarefas simples (subagent, M2.7-highspeed)
│   ├── pesquisador.md             # pesquisa externa (subagent, M3)
│   ├── pleno.md                   # implementação (subagent, M3, variant: thinking)
│   ├── qa.md                      # revisão/testes (subagent, Sonnet)
│   └── senior.md                  # arquitetura/revisão (subagent, Opus)
├── plugins/
│   └── hud-launcher.js            # garante o opencode HUD aberto no Windows (opcional)
└── docs/
    └── AI-SETUP.md                # guia para uma IA portar esta config para outro usuário
```

## Pré-requisitos

- **opencode** instalado (testado com a versão **1.19.3**, a mesma fixada em `package.json`).
- **Providers autenticados via `opencode auth login`:**
  - **Anthropic** (provê os modelos `claude-sonnet-5-5` e `claude-opus-5-5`).
  - **MiniMax Coding Plan** — id do provider: `minimax-coding-plan` (provê `MiniMax-M3` e `MiniMax-M2.7-highspeed`).
- **GitHub CLI (`gh`) autenticado** — usado pelo `@pesquisador` para `gh search repos`, `gh repo view`, `gh release list/view`, `gh api`.
- **Opcional:** o [opencode HUD](https://github.com/diacovrapha/opencode-hud) instalado (app desktop de gastos/uso do opencode, Windows). O plugin `hud-launcher.js` procura o executável em `%LOCALAPPDATA%\opencode HUD\` (instalador .exe), `%ProgramFiles%\opencode HUD\` (.msi) ou na build local, e o abre com `--background` (se já estiver aberto, nada acontece). Se não encontrar, não faz nada.

## Instalação

### Linux/macOS

```bash
# 1. backup da config existente (se houver)
ts=$(date +%Y%m%d-%H%M%S)
[ -d ~/.config/opencode ] && mv ~/.config/opencode ~/.config/opencode.bak.$ts
mkdir -p ~/.config/opencode

# 2. copiar arquivos para ~/.config/opencode/
git clone https://github.com/diacovrapha/opencode-config.git ~/.config/opencode

# 3. instalar a dep do plugin (o opencode autoload exige o módulo)
cd ~/.config/opencode && npm install

# 4. (opcional) ajustar os modelos no opencode.jsonc e nos agents/*.md
#    conforme os providers que VOCÊ autenticou

# 5. validar
opencode debug config
opencode agent list

# 6. reiniciar o opencode
```

### Windows (PowerShell)

```powershell
# 1. backup
ts = Get-Date -Format "yyyyMMdd-HHmmss"
if (Test-Path "$env:USERPROFILE\.config\opencode") {
  Move-Item "$env:USERPROFILE\.config\opencode" "$env:USERPROFILE\.config\opencode.bak.$ts"
}
New-Item -ItemType Directory -Path "$env:USERPROFILE\.config\opencode" | Out-Null

# 2. clonar
git clone https://github.com/diacovrapha/opencode-config.git "$env:USERPROFILE\.config\opencode"

# 3. instalar a dep do plugin
cd "$env:USERPROFILE\.config\opencode"; npm install

# 4. (opcional) editar opencode.jsonc e agents/*.md com os modelos disponíveis
notepad "$env:USERPROFILE\.config\opencode\opencode.jsonc"

# 5. validar
opencode debug config
opencode agent list

# 6. reiniciar o opencode
```

> **Atenção:** o opencode **recusa iniciar com config inválida**. Se `opencode debug config` reclamar, confira `variant: thinking` (remova se o modelo escolhido não tiver essa variante) e o prefixo `provider/` em todos os `model:`. O schema de referência fica em https://opencode.ai/config.json.

## Como adaptar (trocar modelos/providers)

Cada "slot" da tabela abaixo tem um papel claro. Antes de trocar, confirme que o usuário autenticou o provider (`opencode auth list`) e que o modelo existe (`opencode models`).

| Slot | Requisito | Sugestão |
|---|---|---|
| Orquestração/ideação (`ideador`, `chefe`) | Modelo forte e de custo moderado | Claude Sonnet atual, GPT classe média, etc. |
| `senior` | **O modelo mais forte** disponível (pode ser caro) | Claude Opus, GPT classe alta. Uso raro, então custo importa menos. |
| `qa` | Forte em **revisão/diff** | Claude Sonnet ou similar. |
| `pleno`, `pesquisador` | Bom em código e tool calling; idealmente **barato ou de assinatura**; contexto grande | Anthropic, MiniMax Coding Plan, GPT com cache, Gemini com contexto grande, etc. |
| `junior`, `explore` (built-in) | **Rápido e barato** | Variante "highspeed" do Coding Plan, Haiku, Flash, Mini, etc. |

**Limite de `steps` (frontmatter do `agents/*.md`):** schema aceita `steps: N` (`N` inteiro > 0) — máximo de iterações agentic antes de forçar resposta só em texto. Use para impedir loops em agentes de implementação: `junior: 60`, `pleno: 100`. Não há valor padrão para o `senior` (o limite é raramente atingido com o uso esperado — plano curto).

**Onde trocar:**

- **`agents/*.md`** → campo `model:` no frontmatter de cada arquivo. Trocar o modelo aqui sobrescreve o que está no `opencode.jsonc` só para aquele agente.
- **`opencode.jsonc`** →
  - `model` → modelo principal para agentes que não definem o próprio.
  - `small_model` → modelo "leve" usado em tarefas pequenas (subagentes built-in, summarization).
  - `agent.general.model` → override do subagent `general` (caso ele seja chamado).
  - `agent.explore.model` → override do subagent `explore`.
  - `default_agent` → qual agente abre ao iniciar o opencode (precisa ser `primary` e não `hidden`).

**Formato:** sempre `provider/model-id` (ex.: `anthropic/claude-sonnet-5-5`, `minimax-coding-plan/MiniMax-M3`).

**Descobrir os disponíveis:**

```bash
opencode models   # lista provider/model-id suportados pelo seu opencode
```

> Se você é uma IA adaptando esta config para outro usuário, o guia completo está em [docs/AI-SETUP.md](docs/AI-SETUP.md).

## Uso no dia a dia

1. Abra o opencode. Por padrão cai no `ideador` (roxo).
2. Descreva o que você quer. O `ideador` vai pesquisar, propor alternativas e fazer perguntas.
3. Aprove o **BRIEF** ou itere até aprovar.
4. Pressione `Tab` para alternar para o `chefe` (vermelho). Mande executar o BRIEF.
5. O `chefe` despacha para o time. Acompanhe nos logs.
6. Para tarefas triviais, pode pular o `ideador` e ir direto ao `chefe`.

**Exemplos de prompts:**

- `ideador`: "Quero adicionar autenticação OAuth2 no meu app FastAPI de C:\projetos\meuapp. Me ajuda a desenhar a abordagem antes de implementar."
- `chefe` (após BRIEF aprovado): "Execute o brief acima: definir escopo do MVP, plano do senior, implementação do pleno, QA no final. Faça commit e push só quando eu pedir."

## Licença

MIT — veja [LICENSE](LICENSE). Copyright (c) 2026 diacovrapha.
