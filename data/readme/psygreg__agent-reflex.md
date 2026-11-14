# agent-reflex
Plugin for coding agent workflow optimization and safeguarding using any system one decision model, from Jev to self-hosted LM Studio, Ollama or llama.cpp.

### Goals
- Safeguard against potentially dangerous shell commands
- Improve token efficiency
- Deliver more reliable solutions to tasks

### Requirement
The plugin needs a System One decision model as its classifier, served at
`<baseURL>/systemone` — local llama.cpp (0.6 onwards), Ollama (0.35 onwards) or
LM Studio (0.4.26 onwards), or TypeSafe Jev and other System One models through
the TypeSafe API, OpenRouter, the Vercel AI Gateway or OpenCode Zen. Every
feature below is driven by this classifier.

### Features
- **Skill suggestions**: on a conversation's initial prompt the classifier scores which skills available to the agent fit the task (one `noul` question per skill, riding the same batched request as the other decisions) and injects a short suggestion naming the top matches to load via the `skill` tool (OpenCode only — it reads the agent's skill registry). Follow-up prompts in the same conversation are not re-checked: the verdict settles on the task the conversation opens with, and the nudge stays visible only through that first request's turns, dropping a skill once the model has loaded it (a first turn the classifier could not answer leaves the check pending; the next prompt completes it). The suggestion stays silent when the catalog or the classifier is unavailable: it is optional help, never a blocker
- **Project agent-docs nudge**: repositories increasingly carry agent guidance at their root — an `AGENTS.md` file (the cross-agent convention, optionally also nested per subdirectory) or a `.ai/` directory. On a conversation's initial prompt the plugin checks the project directory for both and, when one exists, injects a one-line note telling the model to read it before starting the task (the files are pointed at, never inlined). The note rides the opening turn's model calls and is never fed again on later prompts of the same conversation, so the pointer is paid for once; the check is a filesystem stat, not a classifier decision (`agentDocs` option, OpenCode only)
- **Decision-driven history compaction**: keeps the recent messages verbatim (keep-window widens with complexity), keeps a bounded set of load-bearing older messages, and folds the rest into a compact structured digest so its detail is compressed rather than discarded. Folding is incremental: each compaction only summarizes the messages that aged out of the keep window since the last fold — batched (short turns stay cheap), folded once per session — and appends their facts to a persistent per-session long-term block, so per-request compaction cost stays roughly flat as the session grows and older facts stay captured instead of being redrawn away by every fresh digest run. Tool outputs, tool-call plumbing and thinking/reasoning blocks past the keep window are not even scored: they are discarded outright, since the assistant turns that interpreted them are the load-bearing content and old file reads or command dumps would otherwise spend the preserved slots and the classifier budget
- **Dynamic thinking effort level**: qualifies each prompt as *low*, *medium* or *high* complexity, setting `maxTokens` and switching reasoning effort when the agent uses the default effort setting. A non-default model variant or explicit effort option takes precedence. The request dialect is detected per request from the model actually being requested, so multimodel setups — including one gateway proxying many models — never send a foreign field; models without a wired dialect stay untouched and can still use other features of the plugin. Wired dialects: Anthropic, llama.cpp, Ollama, OpenAI GPT reasoning models, Z.ai GLM (GLM-5.2 onwards), Xiaomi MiMo (MiMo-V2.5 onwards), Google Gemini (Gemini 3 onwards), Qwen (Qwen3.5 onwards and the qwen-plus/qwen-max aliases), Moonshot Kimi (kimi-k2.7+/kimi-k3), xAI Grok (grok-4.3 onwards) and MiniMax (MiniMax-M3 onwards)
- **Confidence level tool**: automatically suggested for *medium* and *high* complexity tasks, allows the LLM to check the confidence of its current line of thinking before finalizing a response and correct itself along the way if needed
- **Tool exposure**: for each prompt the classifier decides which tool *groups* the task actually needs (tools are judged by purpose — web, shell, edit, read, agents, other — one question per group, not per tool) and the model is given only those, so the request carries fewer tool schemas and saves input tokens; a kept group keeps its whole family of tools. In OpenCode, request complexity, tool-group relevance, and history relevance are batched and reused across tool continuations, and history verdicts persist across requests (each old prose message is judged by the classifier at most once per session; tool outputs and reasoning blocks are never judged), while folded history is summarized incrementally into a long-term block, keeping long-session compaction latency low; simultaneous safety/edit checks are batched too. Sequential safety and edit checks remain per action because their inputs arrive only then. The always-keep set is the common core (read/search/edit/shell/task, plus the `execute`/`search`/`skill`/`question` meta-tools where the harness routes everything through them) plus `reflex_run`, `systemone_check_confidence` and `systemone_reveal_tools`. If a needed tool was trimmed, the latter lists the agent's tool pool and restores all tool schemas for the current user request. Falls back to exposing everything if the classifier is unavailable
- **Decision-model tool dispatch** (`reflex_run`): an optional fallback tool for when the model cannot decide which underlying tool a task needs. It asks the decision model which tool to use (a `choice` decision), runs it, and returns its real output. The model calls tools directly whenever it already knows which one fits and reaches for `reflex_run` only when the correct tool is unclear. Tool dispatch uses the same configured classifier model as the rest of the plugin
- **Syntax checks**: up to two-step checks after `edit` and `write` tool calls using parsers and the decision model
- **Shell guardrail**: blocks commands that may damage a repository or remove files without backup; the check runs before dispatch through `reflex_run` as well

- **Stuck-loop detection**: watches completed tool calls and breaks repetitive cycles. When the *same call keeps producing the same result* — identical arguments and identical output, several times in the last few calls — it is flagged deterministically as a stuck loop, no classifier involved, and a warning naming the repeated call and its evidence is injected into the next model call telling the model to change approach; a repeated call whose output *varies* is judged by the System One classifier instead (with a lower bar once the repetition is structurally proven, and the verdict cached per repeating pattern but re-judged as the loop grows). Detection is conservative so legitimate iteration passes through untouched: the warning is a nudge, never a stop, it is delivered once per loop and repeated only if the loop persists

### Agent support

Eight agents are supported. The classifier config is shared across all of them
(`agent-reflex.jsonc`, same option names), so the classifier questions are answered
once. Dynamic effort needs the plugin to rewrite the model request, and history
compaction needs it to rewrite the message list — both only reach agents whose hook
API allows that rewrite.

| Agent | Shell guardrail | Post-edit checks | Classify + confidence | Compaction guidance | Dynamic effort | History compaction | Tool exposure | Tool dispatch | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **OpenCode** | ✅ hard block | ✅ inline | ✅ | ✅ built-in | ✅ full (per-model dialects) | ✅ decision-driven | ✅ | ✅ (`reflex_run`) | Reference implementation and the only agent where everything works. |
| **Pi** | ✅ hard block | ✅ inline | ✅ | ✅ via `context` | ✅ full (`setThinkingLevel`) | ✅ opt-in decision-driven | ✅ (`setActiveTools`) | ✅ (`reflex_run`) | Pi translates the unified effort level per model itself, so no per-vendor dialect code is needed. |
| **MiMo Code** | ✅ hard block | ✅ inline | ✅ | ✅ compacting hook | ⚠️ token cap only | ✅ opt-in decision-driven | ❌ | ❌ | OpenCode-derived. `chat.params` sets `maxTokens` but not `reasoning_effort`, so effort cannot change how hard the model thinks. |
| **Claude Code** | ✅ hard block | ✅ inline | ✅ | ✅ fact-extraction guidance | ❌ | ⚠️ digest guidance only | ❌ | ❌ | `PreCompact` reads the transcript and extracts the fact buckets to steer the summary, but hooks cannot rewrite the message list, so it cannot choose what to keep. |
| **Qwen Code** | ✅ hard block | ✅ inline | ✅ | ✅ fact-extraction guidance | ❌ | ⚠️ digest guidance only | ❌ | ❌ | Same hook limits as Claude Code. Strongest of the shell-hook ports. |
| **Codex** | ✅ hard block | ✅ inline | ✅ | ❌ inert | ❌ | ❌ | ❌ | ❌ | No `PreCompact` `custom_instructions`; its compaction hook can only cancel compaction. Edits arrive via `apply_patch` (V4A). |
| **Antigravity** | ✅ hard block | ⚠️ one turn late | ✅ | ❌ inert | ❌ | ❌ | ❌ | ❌ | `PostToolUse` cannot inject context (open upstream antigravity-cli#808), so findings queue and surface at the next model call. |
| **Hermes** | ⚠️ wrapper tool | ✅ inline | ✅ | ❌ none | ❌ | ❌ | ❌ | ❌ | Hooks cannot block a tool call, so the guardrail is a `safe_run` wrapper over `terminal`. No compaction hook. |

Legend: ✅ works · ⚠️ works with a documented compromise · ❌ not possible (agent hook
API limitation). Dynamic effort means both the reasoning/thinking level and the
per-level `maxTokens` cap where the agent exposes one. Tool exposure means the
agent can remove tool schemas from the model's request (real input-token savings);
the shell-hook agents can only deny a tool call after the model already chose it,
which saves nothing and is therefore marked ❌.

## Usage
Install the skill using `npx skills add psygreg/agent-reflex` or `bun x skills add psygreg/agent-reflex` then ask your agent to do it: the skill briefs the agent on the plugin's capabilities and installs or updates it — updates need no answers (`bash install.sh </dev/null`), fresh installs collect the answers in chat and pipe them in.

Or run the install script provided in this repository. It will also install the skill so future updates can be performed through the agent itself.

```sh
./install.sh
```

On a fresh install it asks for the classifier provider (llama.cpp, Ollama, LM Studio, TypeSafe, OpenRouter, Vercel AI Gateway, OpenCode Zen or a custom endpoint), whether a local server runs on the same machine or a remote one (with its base URL), the classifier model, an optional API key (`{env:NAME}` supported), an optional fallback classifier model and an optional debug log path. Then it verifies the answers against the server itself before writing anything: the collected endpoint must answer a real System One question at `<baseURL>/systemone` with the configured model, and every field is checked against the mis-fills that leave the plugin broken silently (the model name in the apiKey field, a bare port as the baseURL, an api key identical to the model) — a plain chat or completion server on the same port is refused with the exact reason. `AGENT_REFLEX_SKIP_VERIFY=1` bypasses this probe for environments it cannot reach.

The OpenCode plugin installs through the OpenCode plugin CLI: `install.sh` runs `opencode plugin add github:psygreg/agent-reflex` (or `opencode plugin <spec> -g` on older CLIs), so the plugin lives in the CLI's own package install and the entry lands in the global config the standard way; the classifier options are merged into that entry (`{ "package": "github:psygreg/agent-reflex", "options": { ... } }`, keeping comments and formatting; a `.agent-reflex.bak` backup is kept next to the config and the merged file is validated before committing). Older CLIs without the standard plugin command, offline machines, or a missing JS runtime fall back to the legacy local-copy layout (`plugins/reflex` next to the config + a `./plugins/reflex` entry) — re-running the installer on such an installation migrates it to the standard package install. The skill installs through the skills CLI (`bunx`/`npx skills add`, into the CLI's own canonical path) when no copy exists yet; existing copies are detected and left untouched, so there is never a second installation path.

Re-running the installer only updates the plugin: an existing installation (standard package, legacy copy or config entry) is detected and the configured options are left untouched — except that a legacy local-copy install migrates to the standard package install, with its options carried over. Each part installs only for the software actually present: the OpenCode plugin and its `opencode.json(c)` entry are written only when the `opencode` CLI is on `PATH`, and each agent port (Claude Code, Codex, Hermes, Qwen Code, Antigravity, Pi, MiMo Code) only when that agent's CLI is present — anything you do not have installed is skipped entirely, with no files or config written for it. If none of the supported agents is installed, a fresh install stops before the classifier prompts and reports that there is nothing to install. After installing or updating, restart OpenCode (`opencode service restart`) to load the plugin.

For development, add a `"debugLog":` key to the plugin's options pointing to a file to write the logs into. Configuration reference examples live in `opencode.example.jsonc`.

## TO-DO
- Add automatic effort changing capabilities for local models running through LM Studio (blocked upstream: its OpenAI-compatible endpoint documents no reasoning field yet)
- Add automatic effort changing capabilities for other providers beyond the wired dialects (Anthropic, GPT, GLM, MiMo, Gemini, Qwen, Kimi, Grok, MiniMax)
- Port to further agents (Claude Code, Codex, Hermes, Qwen Code, Antigravity, Pi and MiMo Code are done)
