# opencode-prompt-improvement

[![Release](https://img.shields.io/github/v/release/ASTRO-CLOU/opencode-prompt-improvement)](https://github.com/ASTRO-CLOU/opencode-prompt-improvement/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Language:** [English](README.md) · [Русский](README.ru.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Italiano](README.it.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md)

Each language has its own file. Click a name to open it; the same switcher is at the top of every file.

## English

An OpenCode V2 plugin that tidies prompt text when you send it. It never adds requirements, files or steps — it only cleans what you already wrote. The default mode makes zero model calls; an optional LLM pass is enabled separately with a cheap model.

**Install**

```sh
opencode plugin add github:ASTRO-CLOU/opencode-prompt-improvement
```

Or add this to `~/.config/opencode/opencode.json(c)` or a project config:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["github:ASTRO-CLOU/opencode-prompt-improvement"]
}
```

With no tag, the latest release is picked up automatically. `opencode plugin list` shows installed plugins. Requires OpenCode V2.

**What it changes**

- CRLF becomes LF; BOM and zero-width characters are removed; exotic spaces become regular spaces
- trailing whitespace is removed and repeated inner spaces are collapsed
- three or more blank lines become one; edges are trimmed; fenced code blocks are untouched

Every path, URL, backticked fragment, number and `@mention` must survive, and the result may not be more than 20% longer. Otherwise the original prompt is sent. Prompts starting with `/` or `*`, over 2000 characters, or with three or more list items or headings are left alone.

**Turning it off**

`/refine-off` stops refinement, `/refine-on` resumes it, `/refine-status` shows the state. The same is available as `/refine <on|off|status>`. The flag survives restarts, and the status reply does not start an agent.

**Optional LLM pass**

Set `mode: "llm"` and `model: { "providerID": "...", "id": "..." }` in the plugin options. Other options: `maxGrowth` (0.2), `skipCommands` (true), `skipDetailed` (true), `detailedThreshold` (2000), `llmTimeoutMs` (4000). The main session model is never used; the pass is skipped for `@mentions`, timeouts and rejected output.


**Choosing a model**

- `/refine-models [filter]` lists the available models.
- `/refine-model provider/id` (or `provider id`, or a unique model id) saves the model, switches to the LLM pass and enables refinement.
- `/refine-model status` shows the mode and model, `/refine-model off` returns to deterministic cleanup, `/refine-model clear` restores the config settings.
- The setting is stored by the plugin and survives restarts.

Command replies are shown as interface notifications (toasts) and do not start an agent.

**License** — MIT, see [LICENSE](LICENSE).
