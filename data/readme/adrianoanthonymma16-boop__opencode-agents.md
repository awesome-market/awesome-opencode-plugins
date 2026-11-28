# opencode-agents

Configuração de engenharia que roda comigo em **todo** projeto, dentro do
[OpenCode](https://opencode.ai). Não é um boilerplate: é o conjunto de regras,
skills e agentes que decide o que acontece antes de eu escrever uma linha de código.

[![Skills](https://img.shields.io/badge/skills-119-F1EFF6?style=flat-square)](skills)
[![Agentes](https://img.shields.io/badge/agentes-35-F1EFF6?style=flat-square)](agents)
[![Comandos](https://img.shields.io/badge/comandos-71-F1EFF6?style=flat-square)](commands)

---

## O problema que resolve

Agente de IA sem instrução erra de formas previsíveis: escreve código sem teste,
ignora a biblioteca que já existe no projeto, refaz o que o repositório vizinho
já resolveu, chama API sem validação. Não por falta de capacidade — por falta
de contexto.

A resposta é um `AGENTS.md` que não é documentação, é **gatilho**. Cada regra tem
uma condição de disparo, uma ação e um limite do que não fazer.

## Como está organizado

```
AGENTS.md            24 regras de invocação automática, indexadas por fase de projeto
opencode.jsonc       configuração do agente
settings.json        permissões e ajustes
agents/              35 agentes especializados (mapers, reviewers, depuradores)
commands/            71 comandos de fluxo (plan, execute, verify, ship)
skills/              117 skills, cada uma com SKILL.md próprio
gsd-core/            núcleo do fluxo de trabalho em fases
hooks/               gatilhos de shell
scripts/             automações de instalação e verificação
```

## As 24 regras, por área

| Área | O que é acionado automaticamente |
| --- | --- |
| **Detecção de estado** | Se o projeto tem `.planning/` ou `ROADMAP.md`, o agente descobre em que fase está antes de agir |
| **Início de projeto** | Setup de repositório novo: contexto, hooks de pre-commit, modelagem de domínio |
| **Planejamento** | Escopo vira plano executável; decisões técnicas passam por pesquisa antes de virar código |
| **Escopo indefinido** | Ideia solta vira exploração, não implementação adivinhada |
| **Código novo** | TDD por padrão, classificado por tamanho (trivial / pequeno / grande) |
| **Testes** | Cobertura gerada sem eu pedir; bug não óbvio passa por diagnóstico antes de correção |
| **Python** | Detecta projeto Python e carrega os padrões de cada framework (FastAPI, Django, Flask) |
| **SQL** | Detecta banco relacional e carrega design de tabela, revisão de query e migração |
| **Node/TypeScript** | Detecta stack Node e carrega o skill do framework, ORM e autenticação em uso |
| **Docker** | Dockerfile e compose com lint e healthcheck obrigatório |
| **Code review** | Antes de qualquer PR, sete reviews em ordem fixa, com sobreposição resolvida |
| **Frontend** | Especificação de UI antes de codar, e auditoria visual na entrega |
| **Reuso** | Antes de escrever, pesquisa o que já existe — biblioteca, repositório ou código interno |
| **Antes de sair** | Verificação conversacional e revisão por outra IA antes de fechar a fase |

## Princípio de design: pedir antes só quando é destrutivo

A regra que atravessa o arquivo inteiro: o agente age sozinho no trabalho
reversível e **sempre pergunta** em operação destrutiva — force push, delete,
revert, migration que derruba coluna. Isso é o que torna a automação aceitável.

## Uso

```bash
git clone https://github.com/adrianoanthonymma16-boop/opencode-agents
cp -r opencode-agents/* ~/.config/opencode/
```

O `AGENTS.md` vai para a raiz do repositório em que você está trabalhando; o restante
é configuração do OpenCode. Regras de um `AGENTS.md` não portada não se aplicam — a
portabilidade é por repositório, não global.

## Licença

MIT
