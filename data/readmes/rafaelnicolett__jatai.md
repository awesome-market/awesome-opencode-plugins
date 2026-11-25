<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/readme/jatai-horizontal-negativo.png">
    <img src="media/readme/jatai-horizontal.png" width="360" alt="Jataí — metodologia agêntica para construção de software">
  </picture>
</p>

<h1 align="center">Agentes para software que já existe.</h1>

<p align="center">
  <strong>Metodologia agêntica para construção de software.</strong> Uma extensão de código aberto para o VS Code.<br>
  <strong>O agente trabalha. O teste prova. O gate espera por você.</strong>
</p>

<p align="center">
  <a href="https://github.com/rafaelnicolett/jatai/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/rafaelnicolett/jatai/ci.yml?label=CI"></a>
  <img alt="versão" src="https://img.shields.io/badge/vers%C3%A3o-1.0.0-F39A1D">
  <img alt="licença" src="https://img.shields.io/badge/licen%C3%A7a-MIT-5B6B2C">
  <img alt="VS Code" src="https://img.shields.io/badge/VS%20Code-1.90%2B-007ACC">
  <img alt="Brasil" src="https://img.shields.io/badge/Brasil-F3D9A0?labelColor=2C1708">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/readme/cockpit-escuro.png">
    <img src="media/readme/cockpit-claro.png" alt="O Cockpit da Jataí: trilha de Descoberta, Planejamento, Execução e Operação, o quadro do épico e as decisões que esperam você">
  </picture>
</p>

<p align="center">
  <sub>O Cockpit mostra onde a iniciativa está, quem trabalha, o que espera você e o que está parado. Projeto fictício.</sub>
</p>

<p align="center">
  <a href="#por-que-eu-construí-isto">Por que eu construí isto</a> ·
  <a href="#o-que-é-a-jataí">O que é</a> ·
  <a href="#o-que-eu-acredito">O que eu acredito</a> ·
  <a href="#como-funciona">Como funciona</a> ·
  <a href="#o-que-você-vê">O que você vê</a> ·
  <a href="#comece-em-5-minutos">Comece em 5 minutos</a> ·
  <a href="#um-harness-para-testar-modelos">Um harness</a> ·
  <a href="#o-nome">O nome</a> ·
  <a href="#comunidade">Comunidade</a>
</p>

---

## Por que eu construí isto

Passei os últimos meses testando modelos de agentes em código que já existia: SDKs, fluxos e processo. O padrão se repetiu.

O agente entrega rápido. A revisão não acompanha. A decisão fica no chat. O teste que provaria a mudança não existe. E o sistema que já estava em produção vira o lugar onde a experiência é feita.

Eu não queria mais uma ferramenta para gerar código. Queria uma forma de **testar o modelo, o fluxo e o processo** no sistema real, e de parar antes de transformar uma boa ideia num PR que ninguém consegue revisar.

A Jataí é a minha resposta. É a que eu queria usar.

> "Eu queria uma ferramenta que me obrigasse a testar o modelo, o fluxo e o processo. Não só a resposta bonita do chat. A Jataí é isso: um método que cabe no repositório e um gate que só passa com a sua decisão."
>
> — Rafael Nicoleti, criador da Jataí

O Brasil faz boa engenharia e ainda é lido como "mais simples". A Jataí é a minha aposta para mudar essa leitura: um produto brasileiro, aberto, que trata **brownfield** com o rigor que o problema exige. Não é sobre ser a maior. É sobre ser boa, aberta e daqui.

## O que é a Jataí

A Jataí é uma extensão de VS Code com um kit de agentes, skills e regras. Ela instala um método de entrega no seu repositório e o acompanha até a operação.

- **Descoberta:** o sistema é lido, o domínio é mapeado, a dívida aparece. Nada é alterado.
- **Planejamento:** escopo, ordem, risco e ADRs. A mudança é desenhada em passos pequenos.
- **Execução:** teste de caracterização, refactor e feature em PRs que dá para revisar.
- **Operação:** CI/CD, observabilidade, incidentes e o próximo ciclo.

O produto é o que fica escrito: o estado em `.github/artifacts/`, a decisão no gate e a prova no teste.

## O que eu acredito

- **Sistema que já existe não é rascunho.** Ele paga as contas. A Jataí começa entendendo, não reescrevendo.
- **Sem teste que fixe o comportamento atual, refactor é aposta.** A Execução prova antes de trocar.
- **Gate é gente.** Nenhum agente aprova o próprio trabalho. A decisão tem nome e data.
- **Estado no chat é estado perdido.** O progresso, a decisão e a evidência ficam em arquivos no repositório.
- **Aberto sem asterisco.** MIT, local, sem telemetria, sem conta. O método não pode depender de uma empresa.

## Como funciona

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/readme/fluxo-escuro.png">
    <img src="media/readme/fluxo-claro.png" alt="O método Jataí: Descoberta, gate D1, Planejamento, gate D2, Execução, gate D3 e Operação">
  </picture>
</p>

<p align="center"><sub>Quatro etapas, três gates. O agente para em cada um; a decisão é sua.</sub></p>

| Gate | Fecha | A pergunta |
|---|---|---|
| **D1** | Descoberta | O que existe foi entendido o bastante para planejar? |
| **D2** | Planejamento | O que vai mudar está decidido, com risco e ordem? |
| **D3** | Execução | O que foi entregue está provado e pode ir para operação? |

| Etapa | O que acontece | O que fica registrado |
|---|---|---|
| **Descoberta** | agentes leem o código, o domínio e os riscos; nada é alterado | assessment, mapa de domínio, dívida técnica |
| **Planejamento** | roadmap, ADRs e matriz de risco; o escopo é decidido | plano, decisões, ordem das mudanças |
| **Execução** | teste de caracterização, refactor e feature em PRs pequenos | relatórios, testes, commits |
| **Operação** | CI/CD, observabilidade, incidentes e sustentação | runbooks, métricas, histórico |

Cada gate tem uma pergunta simples: **o que está em jogo, e você aprova?** O Cockpit mostra a resposta em texto, com o motivo e o nome de quem decidiu.

## O que você vê

### O Cockpit

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/readme/cockpit-escuro.png">
    <img src="media/readme/cockpit-claro.png" alt="Cockpit da Jataí com a trilha da fase, o épico em andamento e as decisões pendentes">
  </picture>
</p>

A tela **Agora** foi desenhada para responder em três segundos: onde a iniciativa está, quem está trabalhando, o que espera você e o que travou. O motivo aparece em texto, nunca só numa cor.

### O mapa da colmeia

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/readme/mapa-escuro.png">
    <img src="media/readme/mapa-claro.png" alt="Mapa da colmeia: ilhas de Descoberta, Planejamento, Execução e Operação ligadas pelos gates; abelhas são agentes e potes são entregas">
  </picture>
</p>

Cada etapa é uma ilha, cada gate é uma ponte, cada agente trabalhando é uma abelha. A guarda acesa é uma decisão que espera você. O mapa **só acompanha**: nada nele aprova ou grava.

### O Wizard

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="media/readme/wizard-escuro.png">
    <img src="media/readme/wizard-claro.png" alt="Primeira tela do Wizard da Jataí, com o que a extensão vai fazer e o que não vai fazer antes de escrever">
  </picture>
</p>

O Wizard prepara a pasta, mostra o que será escrito e **não altera seus repositórios** antes da revisão. Ele existe para o primeiro dia não ser uma surpresa.

## Comece em 5 minutos

1. **Instale a extensão.** No VS Code, procure **Jataí** no Marketplace ou rode:
   ```sh
   code --install-extension jatai.jatai
   ```
   Se a loja ainda não listar a 1.0.0, baixe o `.vsix` na página de [releases](https://github.com/rafaelnicolett/jatai/releases).

2. **Abra a pasta do projeto.** Pode ser um sistema que já existe ou uma pasta vazia para começar do zero.

3. **Rode o Wizard.** Abra a paleta (`Cmd/Ctrl+Shift+P`) e escolha **Jataí: Initialize Delivery Kit**. Selecione **Projeto existente** para analisar o que já existe, ou **Projeto novo** para gerar a estrutura.

4. **Comece pelo agente `jatai`.** No chat do seu harness:
   - **Claude Code:** chame `@jatai`;
   - **GitHub Copilot:** selecione o agente **jatai** no seletor e escreva a intenção;
   - **OpenCode:** selecione o agente **jatai** (primary) ou rode `/jatai`.

   Diga o que quer fazer — por exemplo, *"mapear o projeto"*. O `jatai` valida os pré-requisitos e chama o agente da etapa certa.

5. **Aprove o D1, o gate que fecha a Descoberta.** O agente para e mostra o que encontrou. Você decide se a Descoberta está concluída. Depois, **Planejamento (D2)** e **Execução (D3)** seguem o mesmo contrato.

> O primeiro comando é sempre o mesmo. O que muda é o ponto de partida; o método não muda.

## O que fica no seu repositório

```
.github/artifacts/          # estado, decisões e evidências — a fonte da verdade
  assessment/               # Descoberta
  planning/                 # Planejamento, ADRs e risco
  execution/                # relatórios de execução e testes
.claude/agents/             # agentes (Claude Code)
.github/agents/             # agentes (GitHub Copilot)
.opencode/agents/           # agentes (OpenCode)
.claude/skills/             # skills reutilizáveis
AGENTS.md                   # o ponto de entrada, lido pelo harness
jatai.config.yaml           # o workspace, os repositórios e o kit instalado
```

Tudo é texto, versionado com o código. O chat pode fechar; o estado não fecha com ele.

## CLI headless

Quem vive no terminal pode instalar e manter o kit sem abrir o VS Code:

```sh
npx @rafael_nicoleti/jatai init --harness opencode
npx @rafael_nicoleti/jatai doctor
npx @rafael_nicoleti/jatai update
```

A CLI usa o mesmo `KitInstaller` e o mesmo kit da extensão; o Wizard, o
Cockpit e o mapa continuam no VS Code. O guia completo está em
[docs/cli.md](docs/cli.md).

## Um harness para testar modelos, não só prompts

A Jataí nasceu dessa necessidade: trocar o modelo sem trocar o método. O mesmo repositório, o mesmo teste, o mesmo gate, o mesmo artefato. A diferença aparece no diff, não no texto de apresentação.

| Muda | Não muda |
|---|---|
| modelo e provedor | as quatro etapas e os três gates |
| Claude Code, GitHub Copilot ou OpenCode | o estado em `.github/artifacts/` |
| prompt e contexto | os testes que provam a mudança |

Se você publica um modelo, um agente ou um harness, a Jataí é um lugar para medir o que ele faz num sistema real. A comparação é bem-vinda; o método é o mesmo.

## O nome

A jataí é uma abelha nativa sem ferrão (*Tetragonisca angustula*). Ela vive em quase todo o Brasil, do oco de árvore ao muro de cidade. Na entrada do ninho, a guarda inspeciona quem entra e quem sai.

No produto, a guarda é o gate: **ela não decide sozinha. Ela espera você.** As quatro faixas de mel do abdômen são as quatro etapas do método; a ponta redonda, sem ferrão, é a mudança segura e reversível.

Nenhum agente passa da guarda sem você.

## Para quem

- **Times com sistema existente:** a Descoberta entende antes de mexer; a Execução troca em passos que você aprova, com um teste que fixa o comportamento atual.
- **Times começando um projeto:** o contrato vem antes do código, cada decisão de arquitetura vira ADR e cada agente cuida da sua stack.
- **Consultorias e tech leads:** o trabalho fica auditável no repositório, não na memória de uma sessão de chat.

## Status e limites

- **1.0.0.** O método funciona de ponta a ponta; as arestas estão documentadas.
- **O Cockpit e o Wizard vivem no VS Code.** O método, os agentes e os artefatos não dependem do editor; a interface depende.
- **Três harnesses hoje:** Claude Code, GitHub Copilot e OpenCode. O mesmo kit é instalado por adaptador, com testes de paridade; o OpenCode usa `.opencode/`, agente `jatai` primary e o comando `/jatai`.
- **Sem serviço hospedado.** A Jataí é local; não há conta, nuvem ou painel web na 1.0.0.
- **Windows no CI:** a suíte roda em Linux e macOS na 1.0.0; o job do Windows está em portabilidade experimental. A extensão funciona no Windows; o que falta é a suíte no runner, não o produto.

## Comunidade

A Jataí é mantida por uma pessoa, [Rafael Nicoleti](https://github.com/rafaelnicolett), e aberta a quem quiser usar, criticar e contribuir.

- **Dúvida ou ideia:** abra uma [issue](https://github.com/rafaelnicolett/jatai/issues) com o template de pergunta.
- **Bug:** issue com o template de bug e o passo a passo.
- **Vulnerabilidade:** siga o [SECURITY.md](https://github.com/rafaelnicolett/jatai/blob/main/SECURITY.md); nunca em issue pública.
- **PR:** leia o [CONTRIBUTING.md](https://github.com/rafaelnicolett/jatai/blob/main/CONTRIBUTING.md). Um PR por assunto, com o teste que prova a mudança.

Se você publica um modelo, um agente ou um harness, a seção [Um harness para testar modelos](#um-harness-para-testar-modelos) é o lugar de comparar. A Jataí é o meu harness; quero que ela seja útil para os seus também.

## Documentação

- [A metodologia](https://github.com/rafaelnicolett/jatai/tree/main/docs/metodologia) — as quatro etapas, os gates e o estado em arquivos.
- [Catálogo de agentes](https://github.com/rafaelnicolett/jatai/tree/main/docs/agentes) — o que cada agente faz e quando entra.
- [Arquitetura](https://github.com/rafaelnicolett/jatai/blob/main/docs/arquitetura.md) — o núcleo, a casca e as fronteiras.
- [Decisões](https://github.com/rafaelnicolett/jatai/tree/main/docs/decisoes) — as ADRs que moldaram o projeto.
- [API de extensão](https://github.com/rafaelnicolett/jatai/blob/main/docs/api-de-extensao.md) — como um serviço próprio se conecta, com consentimento.
- [Como contribuir](https://github.com/rafaelnicolett/jatai/blob/main/CONTRIBUTING.md) — ambiente, testes e o caminho de um PR.
- [Código de conduta](https://github.com/rafaelnicolett/jatai/blob/main/CODE_OF_CONDUCT.md) e [segurança](https://github.com/rafaelnicolett/jatai/blob/main/SECURITY.md).

## Desenvolvimento

Requisitos: Node 20 e VS Code 1.90+.

```sh
npm ci
npm --prefix webview-ui ci

npm run ci:local        # typecheck, lint, testes, build e .vsix
npm run test            # testes do host
npm run test:webview    # testes do webview
npm run package         # gera o .vsix
```

As telas deste README são capturadas do mock visual com o Chrome, pelo script
`webview-ui/scripts/capture-readme.mjs`; as imagens ficam em `media/readme/`.

## Licença

[MIT](LICENSE). A Jataí é aberta para uso, estudo, mudança e distribuição.
