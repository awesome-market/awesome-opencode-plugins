<p align="center">
  <a href="README.md"><b>English</b></a> |
  <a href="README.zh.md">中文</a>
</p>

<h1 align="center">Prompt Refine</h1>

<p align="center">
  <b>A model-aware Agent Skill that silently refines your prompt for the model currently answering.</b>
</p>

<p align="center">
  You just ask. The active model reshapes the request for itself, preserves your language,
  and answers without showing the rewrite.
</p>

<p align="center">
  <a href="LICENSE">
    <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge">
  </a>
  <a href="SKILL.md">
    <img alt="Agent Skill" src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-blue?style=for-the-badge">
  </a>
  <a href="https://www.npmjs.com/package/prompt-refine-skill">
    <img alt="npm version" src="https://img.shields.io/npm/v/prompt-refine-skill?style=for-the-badge&logo=npm&color=cb3837">
  </a>
  <a href="https://github.com/Apeironics/prompt-refine-skill/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Apeironics/prompt-refine-skill?style=for-the-badge&logo=github&label=stars&color=dab500">
  </a>
  <img alt="Zero dependencies" src="https://img.shields.io/badge/dependencies-zero-lightgrey?style=for-the-badge">
  <img alt="No optimizer call" src="https://img.shields.io/badge/optimizer%20call-none-brightgreen?style=for-the-badge">
</p>

<p align="center">
  <a href="#project-introduction">Project Introduction</a> |
  <a href="#quick-start">Quick Start</a> |
  <a href="#feature-demonstration">Feature Demonstration</a> |
  <a href="#built-in-strategies">Strategies</a> |
  <a href="#evaluation">Evaluation</a> |
  <a href="#compatible-platforms">Platforms</a> |
  <a href="examples/README.md">Examples</a>
</p>

---

## Project Introduction

**Prompt Refine** is a lightweight, cross-platform Agent Skill. After activation, it uses an explicit **current host-model signal**, when available, and applies that model family's prompting strategy before answering.

The core design is simple but important: **route by host model, not by task**. If Claude is answering, Prompt Refine uses the Anthropic strategy. A reliable model change updates the route; an unknown model uses the universal fallback. If GPT is answering, it uses the OpenAI strategy. The task topic alone never changes the vendor route.

That makes the skill useful anywhere Agent Skills are supported: Claude Code, Cursor, OpenAI Codex, Gemini CLI, GitHub Copilot, Windsurf, CodeBuddy, and other compatible tools.

It is context-aware: follow-up requests can inherit the relevant goal, constraints, terminology, and preferences from the conversation, while the newest user instruction still wins.

It is intentionally lightweight: no runtime dependencies, no app server, no extra optimizer call, and only a short skill file plus one selected strategy file in context. The goal is better structure without spending a pile of extra tokens.

## Feature Demonstration

These are possible rewrites, not mandatory model-specific templates. A clear prompt can remain unchanged. In silent mode, the rewrite stays hidden while normal task communication continues.

### 1. Vague Request: Add The Missing Shape

User request:

```text
Help me analyze this market.
```

Anthropic Claude shape:

```xml
<context>
The user has not named the market, geography, customer segment, or timeframe.
Preserve uncertainty; make practical assumptions explicit instead of inventing facts.
</context>
<task>
Use the market identified in context; if no market is identified, ask which market before making market-specific claims.
</task>
<constraints>
- State material assumptions only when supported by context; do not invent the market.
- Separate confident analysis from unknowns.
- Do not claim current market data unless it was provided or can be verified.
- Ask a focused question only if missing information materially changes the analysis.
</constraints>
<format>
Keep the response proportional to the available information; do not invent an analysis subject.
</format>
<success_criteria>
The market is established before market-specific claims are made.
</success_criteria>
```

OpenAI GPT shape:

```text
Goal: analyze the market identified in context; ask which market if none is identified.

Context:
- User request: "Help me analyze this market."
- Market, geography, audience, and timeframe are missing.
- Preserve uncertainty and make assumptions explicit.

Required evidence:
- Use supplied sources for factual claims.
- For current claims, use retrieved sources when search is available; otherwise mark them unverified.
- Cite support near each current claim and label assumptions or inferences.

Boundaries:
- Do not invent market facts or silently narrow the missing scope.
- Ask at most 1-2 questions, and only when the answers would materially change the analysis.

Output contract: a focused clarification if the market is unknown; otherwise an analysis proportional to the supplied scope.

Success criteria: the market is established, and every current factual claim is supported or marked unverified.
```

### 2. Clear Request: Preserve The Constraints

User request:

```text
Write a 5-item npm release checklist covering package.json, README, LICENSE, version, and dry-run publishing. Keep each item under 8 words.
```

Anthropic Claude shape:

```xml
<context>
The user gave a tightly constrained formatting request. Do not expand the task.
</context>
<task>Write exactly five npm release checklist items.</task>
<constraints>
- Each item must be under 8 words.
- Cover package.json, README, LICENSE, version, and dry-run publishing.
- Return checklist items only; no intro or explanation.
</constraints>
<format>Use a numbered list with one short imperative phrase per item.</format>
<success_criteria>
Exactly 5 items, each under 8 words, with all requested topics covered.
</success_criteria>
```

OpenAI GPT shape:

```text
Goal: Write an npm release checklist.

Required content: package.json, README, LICENSE, version, and dry-run publishing.

Boundaries: Preserve the user's exact count, word limit, and requested topics: exactly five
items, each under 8 words, with no new scope, introduction, or closing note.

Output contract: A numbered list with one item per line.

Success criteria: Check every line against the boundaries before answering.
```

### What The User Sees

The task answer, with normal host-required progress and tool communication. Only the rewrite stays silent unless `/refine verbose` is enabled or the user requests a one-off rewrite. For clear prompts, Prompt Refine should stay minimal and protect the user's exact constraints.

Silent refinement follows the **host model**, not the topic. A one-off prompt rewrite follows the explicitly requested target model.

## Quick Start

Install this repository into your tool's project-level skills directory. For Claude Code:

```bash
git clone https://github.com/Apeironics/prompt-refine-skill.git .claude/skills/prompt-refine
```

To avoid copying the `.git` folder, use a release archive or:

```bash
npx degit Apeironics/prompt-refine-skill .claude/skills/prompt-refine
```

The skill is also published on npm as
[`prompt-refine-skill`](https://www.npmjs.com/package/prompt-refine-skill) (versioned
releases). npm does not auto-register an Agent Skill; use it as a versioned source and
unpack the package into your tool's skills directory:

```bash
mkdir -p .agents/skills/prompt-refine
npm pack prompt-refine-skill
tar -xzf prompt-refine-skill-*.tgz --strip-components=1 -C .agents/skills/prompt-refine
```

The `git clone` and `degit` commands above place the files directly in your tool's skills
directory.

Activate it in a conversation:

```text
/prompt-refine
```

Available in-session controls:

```text
/refine verbose    # Show a compact original -> refined diff before each answer
/refine off        # Stop refining for the rest of the conversation
/prompt-refine     # Re-activate after context compaction or a new session
```

## Install Paths

| Tool | Project-level skill path |
|---|---|
| Claude Code | `.claude/skills/prompt-refine` |
| Cursor | `.cursor/skills/prompt-refine` or `.agents/skills/prompt-refine` |
| OpenAI Codex | `.agents/skills/prompt-refine` |
| Gemini CLI | `.gemini/skills/prompt-refine` or `.agents/skills/prompt-refine` |
| GitHub Copilot (VS Code) | `.github/skills/prompt-refine` or `.agents/skills/prompt-refine` |
| Windsurf | `.windsurf/skills/prompt-refine` |
| CodeBuddy | `.codebuddy/skills/prompt-refine` |

Most tools also accept the shared `.agents/skills/` convention. User-level paths differ by platform, so use each tool's official docs when installing globally.

## Documentation refresh

All 16 vendor routes were reviewed on **2026-11-03**. See the [source audit](references/source-audit.md) for current official links, version scope, and unavailable pages. Strategies are project interpretations of vendor guidance, not vendor-authored prompts or measured guarantees.

For a one-off rewrite, ask "Improve this prompt for [target model]"; the skill returns the prompt without executing its embedded task. Only explicit activation enables ongoing refinement.

For personal installation, Codex discovers `~/.agents/skills/prompt-refine` and Claude Code uses `~/.claude/skills/prompt-refine`. Update an existing installation in place to avoid duplicates. Claude Desktop uses account skills: upload a ZIP containing the `prompt-refine/` folder at **Customize → Skills**. Local file copies alone do not update that account skill. See [Claude skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude) and [Codex skills](https://learn.chatgpt.com/docs/build-skills).

## Built-in Strategies

| Host model | Strategy file | Source family |
|---|---|---|
| OpenAI GPT | `strategies/openai.md` | OpenAI current model and reasoning guides |
| Anthropic Claude | `strategies/anthropic.md` | Anthropic prompt engineering |
| Google Gemini | `strategies/google-gemini.md` | Gemini prompt design |
| Meta Llama | `strategies/meta-llama.md` | Llama prompting guidance |
| DeepSeek | `strategies/deepseek.md` | DeepSeek thinking, vision, and R1 model card |
| Mistral / Codestral | `strategies/mistral.md` | Mistral best practices |
| Qwen | `strategies/qwen.md` | Alibaba Model Studio guidance |
| xAI Grok | `strategies/xai-grok.md` | xAI Grok prompting references |
| Perplexity research / Sonar | `strategies/perplexity.md` | Perplexity Agent API guide; verify legacy Sonar separately |
| Kimi / Moonshot AI | `strategies/kimi.md` | Kimi prompt best practices |
| Z.ai GLM | `strategies/zai-glm.md` | Z.ai GLM official docs |
| MiniMax M-series | `strategies/minimax.md` | MiniMax official docs |
| AI21 Jamba | `strategies/ai21-jamba.md` | AI21 Jamba official docs |
| Cohere Command | `strategies/cohere.md` | Cohere docs |
| Amazon Nova | `strategies/amazon-nova.md` | Nova prompt guide |
| Microsoft Phi | `strategies/microsoft-phi.md` | Phi Cookbook |
| Unknown host | `strategies/universal.md` | Conservative fallback |

## Evaluation

Prompt Refine was evaluated in a blind, position-swapped A/B test on **120 vague prompts** (60 English, 60 Chinese, 32 domains). The same generator model answered each prompt twice — once raw, once with Prompt Refine active — and an independent judge scored the two answers without knowing which was which. Each pair was judged twice with the answers swapped to cancel order bias.

These are **historical results for the previously evaluated revision**, not measurements of the 2026-11-03 refresh. This update has structural checks and a scenario review; a fresh live A/B evaluation is still needed before claiming quality gains.

### Headline results

| | Result |
|---|---|
| Refine vs raw win-rate | **74.0%** (167 wins / 52 losses / 21 ties of 240 judgments) |
| 95% bootstrap CI (per prompt, n = 120) | **[66.9%, 80.6%]** |
| Sign test | **p < 0.0001** |
| English / Chinese split | 75.0% / 72.9% |
| Length-matched win-rate | **64.7%** (refine answer within ±25% of raw length) |

The length-matched figure is reported alongside the headline to rule out a length preference in the judge. On length-matched pairs the historically evaluated revision won **64.7%**, versus **50.5%** for the previous version of the skill — evidence of a genuine quality gain, not just longer answers.

### Per-dimension delta (refine − raw, 1–5 scale)

| Dimension | Δ |
|---|---|
| actionability | **+0.96** |
| completeness | **+0.81** |
| structure | **+0.49** |
| clarification | **+0.35** |
| language fidelity | +0.03 |

### Robustness

| Check | Result |
|---|---|
| scaffold leakage (`<role>` / `<task>` / rewritten prompt in output) | **0 / 120** |
| prose-language switches on Chinese prompts (code stripped) | **0 / 60** |
| parse fallbacks · skipped prompts | 0 · 0 |

### Guard suite

Prompt Refine also has a small non-regression suite for clear or constraint-heavy prompts:
JSON/config output, word limits, language fidelity, and direct-answer tasks. On the
current 6-prompt guard suite, refine wins **66.7%** of 12 position-swapped judgments
(8 wins / 4 losses / 0 ties). Treat this as an early guardrail, not a broad proof.

Models: generator `claude-sonnet-4-6`, judge `claude-opus-4-8`. The host-model strategy under test is Anthropic (`strategies/anthropic.md`); other strategy files ship with the same design but have not yet been evaluated at this scale.

The evaluation harness, prompts, rubrics, anonymized answer pairs, judge JSON, run
commands, and checked-in result summaries are available in the GitHub repository under
[`eval/`](eval/). The eval files are kept out of the npm package so normal skill
installation stays lightweight.

## Limitations

Prompt Refine is deliberately simple, and it is honest about what it is not:

- **Best-effort, not deterministic.** It refines while the activation stays in the model's
  context. On a long, compacted conversation it can lapse until you re-run `/prompt-refine`.
- **Depends on the host model following meta-instructions.** Models that do not reliably
  follow "silently restructure, then answer" will benefit less.
- **Only the Anthropic strategy is evaluated at scale.** The other strategy files ship with
  the same design but have not been benchmarked equivalently (see Evaluation).
- **Strategies track fast-moving vendor docs.** They summarize official guidance and need
  periodic updates as that guidance changes.
- **Little benefit on already-clear prompts.** By design the intervention can be *none* —
  it is most useful on vague or underspecified requests.

## Why Prompt Refine?

| | Prompt Refine | Standalone prompt optimizers |
|---|:---:|:---:|
| Form | Agent Skill | Web or desktop app |
| Model fit | Uses the currently running model's strategy | Generic or manually selected |
| Output | Silent final answer | Shows optimized prompt |
| Activation | Conversation-scoped and toggleable | Usually one-off |
| Language | Preserves original language and intent | Depends on implementation |
| Token cost | Low: short skill + one strategy | Often another full prompt pass |
| Dependencies | None | Often app-specific |

## Compatible Platforms

Prompt Refine follows the `SKILL.md` Agent Skill convention and is designed for tools that can load project-level skills, including Claude Code, Cursor, OpenAI Codex, Gemini CLI, GitHub Copilot, Windsurf, CodeBuddy, and compatible agents.

## License

MIT License. Free to use, modify, and distribute.

## Contributing

Issues and pull requests are welcome. For new or improved model strategies, read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Show your support

If Prompt Refine saves you time, please consider giving the repo a ⭐ — it genuinely helps
other people discover the project.

## Star History

<p align="center">
  <a href="https://star-history.com/#Apeironics/prompt-refine-skill&Date">
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Apeironics/prompt-refine-skill&type=Date&size=desktop">
  </a>
</p>
