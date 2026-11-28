# SpecDD Starter Pack

<p align="center">
  <img src="SpecDD_Starter_Pack.png" alt="SpecDD mascot" width="160" />
</p>

Um conjunto mínimo de documentos para **desenvolvimento orientado a especificação (Spec Driven Development)** com IA, sem perder o controle do projeto. Um canivete suíço que serve para qualquer tipo de sistema (web, SaaS, CLI, biblioteca, pipeline de dados, o que for) e foi pensado para alguns dos principais harness de codificação agêntica que eu (e provavelmente você também kkkkk) tenho utilizado: **Claude, Codex e OpenCode**.

## Instalação

Na raiz do seu repositório, rode:

```bash
npx specdd-starter-pack
```

<p align="center">
  <img src="how-to-install.gif" alt="Demonstração da instalação via npx" width="700" />
</p>

[![npm](https://img.shields.io/npm/v/specdd-starter-pack.svg)](https://www.npmjs.com/package/specdd-starter-pack)


## Por que este projeto?

Minha ideia é inspirada em ferramentas como o [GitHub Spec Kit](https://github.com/github/spec-kit), [OpenSpec](https://github.com/Fission-AI/OpenSpec) e [AI Coders Context](https://github.com/vinilana/dotcontext), mas **extremamente enxuto e dando máxima liberdade para quem está construindo**.

Eu particularmente acho Spec Kit e OpenSpec ótimos, mas caem em alguns pontos: o Spec Kit traz muito overhead com vários documentos e isso é peso demais para alguns projetos; o OpenSpec é leve, porém enxergo ele um pouco engessado em determinados usos. Este starter pack fica no meio-termo pragmático: **4 documentos, rails fortes de processo onde importa (governança), liberdade no resto**.

A ideia central: programar de forma agêntica: **planejar, implementar e revisar** com IA mantendo `docs/` como fonte única da verdade, para que a IA não invente nem fuja do escopo.

---

## O que está incluído

Quatro documentos em `docs/`, duas pastas de apoio e roteadores curtos por ferramenta.

| Arquivo / Pasta | Para quê |
|---|---|
| `docs/RULES.md` | **Como a IA deve trabalhar**: processo/governança. Fonte oficial das regras. Neutro a stack. |
| `docs/SPEC.md` | Fonte de verdade: **produto** (visão/escopo/fora-de-escopo) + **contrato técnico** (regras, restrições, anti-alucinação). |
| `docs/ARCH.md` | Decisões arquiteturais, ADRs, contratos entre partes. |
| `docs/NOW.md` | Task atual (uma por vez) + **Backlog** (fila ordenada do que vem depois) + seção "Feito" (marcos recentes; histórico completo no git). |
| `docs/knowledge/` | Conhecimento durável: guias internos, FAQs, integrações, problemas conhecidos e decisões operacionais. Consulta sob demanda, com índice próprio. |
| `docs/plans/` | Planos e rascunhos que ainda não viraram task. Não é fonte de verdade e não autoriza execução. |
| `CLAUDE.md` / `AGENTS.md` | Roteadores curtos que apontam para `docs/RULES.md`. Não duplicam regra. |
| `.claude/agents/` · `.codex/agents/` · `.opencode/agents/` | Definições de subagentes por ferramenta (`planner` → `implementer` → `reviewer`). |

> **O toolkit é adaptativo.** Estes são apenas os arquivos iniciais, um ponto de partida, não uma camisa de força. Crie, edite ou renomeie o que fizer sentido para o seu projeto: ajuste as regras em `docs/RULES.md`, molde os docs, altere os subagents ou adicione novos. Mantenha só o espírito: `docs/` como fonte da verdade e a IA no trilho.

---

## Como funciona

A fonte oficial das regras é **`docs/RULES.md`**. `CLAUDE.md` e `AGENTS.md` são só roteadores, não duplicam regra.

**Ordem de leitura canônica:** `docs/RULES.md` → `docs/SPEC.md` → `docs/ARCH.md` → `docs/NOW.md`. Em conflito, `docs/SPEC.md` vence. `docs/knowledge/` e `docs/plans/` ficam **fora** da leitura obrigatória: são consulta sob demanda, para não inflar contexto em toda task.

Princípios:
- **Disciplina de processo é lei** por aqui: plano pequeno → partes reversíveis → uma task por vez → SPEC vence → atualizar doc no mesmo PR.
- **A IA nunca adivinha o próximo passo**: o **Backlog** do `docs/NOW.md` é a fila. Ao fechar uma task, o topo do backlog vira a próxima. Backlog vazio = a IA para e pergunta.
- **Estilo de código é neutro**: o pack não impõe qualquer regra de estilo. Se o seu projeto quiser defaults de estilo e princípios como KISS, YAGNI ou DRY, escreva-os na SPEC (seção **Convenções de código**).
- **`docs/` é a ponte**: qualquer modelo lê de lá. Por isso você pode misturar ferramentas livremente.

---

## Como usar

Ao rodar `npx specdd-starter-pack`, a CLI é interativa e pergunta:

1. **Tipo de projeto**: novo ou existente (auto-detecta pelo conteúdo da pasta).
2. **Harness**: Claude Code · Codex · OpenCode (um ou vários; copia só o que cada um usa).
3. **Bootstrap**: gera um `BOOTSTRAP.md` com o prompt pronto para o agente preencher os docs.

Divisão de trabalho: a **CLI copia os arquivos**; o **seu agente (LLM) preenche** `SPEC.md`/`ARCH.md`/`NOW.md`. Por isso ela gera o `BOOTSTRAP.md`: você cola no Claude/Codex/OpenCode (ou pede "Execute BOOTSTRAP.md") e o agente preenche. O prompt se adapta:

- **Projeto novo** (sem código): o agente **entrevista você** (pergunta produto, objetivos, escopo e stack) e só então preenche os docs.
- **Projeto existente**: o agente **lê a codebase** e infere os docs a partir do que já existe.

Depois é só apagar o `BOOTSTRAP.md`.

---

## Exemplos de uso

Não há "modos" nem comando especial. Você combina ferramentas como quiser, sempre ancorado na documentação mestra. Quatro receitas comuns:

### 1. Um agente só (o mais simples)
Sem subagents, sem trocar de ferramenta: o mesmo agente planeja e executa na mesma thread.

1. Peça o plano (o agente lê `docs/` e escreve a próxima task em `docs/NOW.md`):
   > Leia `docs/RULES.md`, `docs/SPEC.md`, `docs/ARCH.md` e `docs/NOW.md`. Planeje a próxima entrega em passos pequenos e escreva apenas a primeira task em `docs/NOW.md`.
2. Revise a task no `docs/NOW.md` e aprove.
3. Peça para implementar só o que está no NOW:
   > Implemente apenas a task de `docs/NOW.md`. Ao terminar, atualize os docs conforme `docs/RULES.md`.

Tudo em uma janela. O rigor vem dos docs, não da separação de ferramentas.

### 2. Claude planeja → Codex executa
Bom para misturar modelos da Anthropic e da OpenAI na criação de planos/tarefas e na execução dos mesmos. Há duas formas de fazer isso:

**Opção A — Build prompt (copiar e colar):**
1. No Claude, peça o plano (ele lê `docs/` e escreve a próxima task em `docs/NOW.md`):
   > Leia `docs/RULES.md`, `docs/SPEC.md`, `docs/ARCH.md` e `docs/NOW.md`. Planeje a próxima entrega em passos pequenos e escreva apenas a primeira task em `docs/NOW.md`. Depois, gere um **build prompt** pronto para colar em outra ferramenta, pedindo para implementar só o que está em `docs/NOW.md`.
2. Cole o build prompt no Codex para implementar.
3. Volte ao Claude para revisar o diff contra SPEC/ARCH/NOW.

**Opção B — Plugin oficial do Codex no Claude Code (sem copiar e colar):**
1. Instale o plugin oficial do Codex no Claude Code (requer o Codex CLI instalado e autenticado):
   ```
   /plugin install codex@codex-plugins
   ```
2. Peça o plano normalmente no Claude e, na hora de executar, delegue direto:
   > Use o Codex para implementar apenas a task de `docs/NOW.md`, seguindo `docs/RULES.md`.
3. O Codex roda dentro da mesma sessão e o Claude revisa o resultado na sequência — tudo em uma janela, sem troca manual de prompts.

### 3. Vice-versa (ou qualquer par)
Mesma mecânica, invertendo papéis: qualquer modelo (de preferência um forte) planeja/revisa, qualquer modelo executa.

### 4. Subagents (uma ferramenta só)
Tanto Claude, quanto Codex e OpenCode suportam subagents, portanto:
`planner` → `implementer` → `reviewer` (em `.claude/agents/`, `.codex/agents/`, `.opencode/agents/`).
O `planner` lê os docs e escreve a task no `docs/NOW.md`; o `implementer` implementa só o NOW; o `reviewer` revisa o diff. Todos seguem `docs/RULES.md`.

> **Nota do autor:** Eu costumo usar Claude Opus 5 para planejar e revisar, e delego o desenvolvimento para o GPT 5.6 Luna com effort **high**, pelo plugin oficial do Codex no Claude Code. Assim tenho os dois na mesma sessão: o Claude planeja/revisa e o Codex executa, sem copiar e colar build prompts entre janelas.

---

## Skills (Separei algumas que acho interessantes):

O pack é neutro; skills são um extra que você liga se quiser. Três recomendadas:

Skills usam o formato aberto [`SKILL.md`](https://agentskills.io), portável entre ferramentas. Mas o **path de descoberta muda por ferramenta**, então não vêm pré-instaladas: instale na gaveta da sua.

| Ferramenta | Instale em |
|---|---|
| Claude Code | `.claude/skills/<nome>/` |
| Codex | `.agents/skills/<nome>/` |
| OpenCode | `.opencode/skills/<nome>/` (também lê `.claude/skills/` e `.agents/skills/`) |

**find-skills: descoberta de skills (recomendada)**
Acha e instala skills para tarefas específicas, direto do ecossistema aberto.
- Buscar: `npx skills find <tarefa>`
- Instalar: `npx skills add <pacote>` (na pasta de skills da sua ferramenta)

Fonte: [vercel-labs/skills](https://www.skills.sh/vercel-labs/skills/find-skills).
> Espírito: busque/instale à vontade, mas **capacidade nova continua passando por `docs/NOW.md` / `docs/SPEC.md`**: a skill amplia o que você pode fazer, não autoriza a IA a sair do escopo sozinha.

**Test-Driven Development: disciplina de teste (opt-in por projeto)**
Força o ciclo red-green-refactor (teste primeiro → vê falhar → código mínimo). Regra estrita.
O pack é **neutro em estilo**, então TDD **não vem ligado**. Se o seu projeto quer TDD:
1. Ache e instale: `npx skills find test-driven-development` → `npx skills add <pacote>`.
2. Declare na `docs/SPEC.md` que este projeto usa TDD (é um default de estilo, pertence à SPEC, não ao pack).

Fonte: [obra/superpowers](https://www.skills.sh/obra/superpowers/test-driven-development).

**frontend-design: qualidade de UI (opt-in)**
Skill oficial da Anthropic para elevar o design de frontend. Ajuda o agente a produzir interfaces mais consistentes e bem-acabadas, em vez do visual genérico padrão.
1. Ache e instale: `npx skills find frontend-design` → `npx skills add <pacote>`.
2. Use quando a task envolver UI; combine com o que a `docs/SPEC.md` define de produto.

Fonte: [anthropics/skills](https://www.skills.sh/anthropics/skills/frontend-design).

---

## Contribuindo

PRs bem-vindos. Só mantenha a ideia: **organização que mantém a IA no trilho com o mínimo possível**.

## Licença

MIT
