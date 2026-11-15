# AIOX OpenCode Adapter

[English](README.en.md) | **Portugues**

Use agentes [AIOX](https://github.com/SynkraAI/aiox-core) globalmente no [OpenCode](https://opencode.ai) em qualquer projeto.

> Baseado no [AIOX Framework](https://github.com/SynkraAI/aiox-core) por [SynkraAI](https://github.com/SynkraAI) (Licenca MIT).

---

## O que esta incluso

13 agentes de IA especializados:

| Agente | Nome | Papel | Modo |
|--------|------|-------|------|
| `@aiox-master` | Orion | Orquestrador Mestre | primary |
| `@dev` | Dex | Desenvolvedor Full Stack | subagent |
| `@architect` | Aria | Arquiteta de Sistemas | subagent |
| `@sm` | River | Scrum Master | subagent |
| `@pm` | Morgan | Product Manager | subagent |
| `@po` | Pax | Product Owner | subagent |
| `@qa` | Quinn | Garantia de Qualidade | subagent |
| `@analyst` | Atlas | Analista de Negocios | subagent |
| `@devops` | Gage | Engenheiro DevOps | subagent |
| `@data-engineer` | Dara | Engenheira de Dados | subagent |
| `@ux-design-expert` | Uma | Design UX/UI | subagent |
| `@squad-creator` | Craft | Criador de Squads | subagent |
| `@cybersec` | Kira | Analista de Seguranca | subagent |

## Pre-requisitos

| Componente | Versao Minima | Obrigatorio |
|------------|---------------|-------------|
| Node.js | 18.0.0 | Sim |
| npm | 9.0.0 | Sim |
| Git | Qualquer | Sim |
| Docker | Qualquer | Apenas para Pentest MCP |
| Python | 3.8+ | Apenas para HexStrike |

## Instalacao Rapida

```bash
# 1. Instalar o pacote globalmente
npm install -g aiox-opencode-adapter

# 2. Instalar os agentes no OpenCode
aiox-global init

# 3. Gerar a configuracao
aiox-global config

# 4. Reiniciar o OpenCode
```

## Comandos Disponiveis

```bash
aiox-global init              # Instala agentes em ~/.config/opencode/agents/
aiox-global config            # Gera opencode.json com MCPs auto-detectados
aiox-global setup-hexstrike   # Instala o servidor MCP do HexStrike AI
aiox-global setup-pentest     # Instala o servidor MCP do Pentest (Docker)
aiox-global list              # Lista agentes instalados
aiox-global doctor            # Verifica saude da instalacao
aiox-global uninstall         # Remove agentes AIOX
aiox-global help              # Exibe ajuda
aiox-global --version         # Exibe a versao instalada
```

## Configuracao dos MCPs (Opcional)

Para o agente de seguranca funcionar com todas as ferramentas, instale os MCPs de seguranca:

```bash
# HexStrike AI (100+ ferramentas de pentest)
aiox-global setup-hexstrike

# Pentest MCP (baseado em Docker)
aiox-global setup-pentest
```

Veja a documentacao completa:
- [Instalacao detalhada](docs/pt/INSTALLATION.md)
- [Configuracao do Docker](docs/pt/DOCKER-SETUP.md)
- [Configuracao do HexStrike](docs/pt/HEXSTRIKE-SETUP.md)
- [Guia dos MCPs](docs/pt/MCP-GUIDE.md)
- [Descricao dos Agentes](docs/pt/AGENTS.md)
- [Guia do Cybersec (Kira)](docs/pt/CYBERSEC.md)
- [Solucao de Problemas](docs/pt/TROUBLESHOOTING.md)

## Uso

Apos a instalacao, reinicie o OpenCode. Voce tera:

- **Tab** para alternar entre `build`, `plan` e `aiox-master`
- **@nome-do-agente** para invocar qualquer subagente (ex: `@dev`, `@cybersec`)
- **aiox-master** orquestra todos os agentes automaticamente

## Exemplo de Fluxo

```
Usuario: "Crie uma API REST para gerenciamento de tarefas"

aiox-master (Orion) orquestra:
  1. @analyst (Atlas) - Analisa requisitos
  2. @architect (Aria) - Define arquitetura
  3. @pm (Morgan) - Cria historias
  4. @sm (River) - Planeja sprints
  5. @dev (Dex) - Implementa codigo
  6. @qa (Quinn) - Testa e revisa
  7. @devops (Gage) - Faz deploy
```

## Atribuicao

Este pacote e baseado no [AIOX Framework](https://github.com/SynkraAI/aiox-core) por [SynkraAI](https://github.com/SynkraAI), licenciado sob a [Licenca MIT](LICENSE).

## Licenca

MIT - Veja [LICENSE](LICENSE) para detalhes.
