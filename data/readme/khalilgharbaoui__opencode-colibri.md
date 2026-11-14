# opencode-colibri

An [opencode](https://opencode.ai) 2 plugin that adds a local [Colibri](https://github.com/JustVugg/colibri) server (`coli serve`) as a model provider.

- Reads the served models, their context size and their input types from `GET /v1/models`, and the slot count from `GET /health`. Nothing to keep in sync by hand.
- Gives each opencode session its own Colibri cache slot (`cache_slot`), so sessions and subagents do not push each other's cached prompt out. A session keeps the same slot across opencode restarts, so a resumed conversation only reads its new tokens. Needs `coli serve --kv-slots N` with N > 1.
- Session title requests share one slot of their own and get a 64-token reply budget, so a title never evicts a session's cache or runs to the end of the context.
- Says "Colibri is not answering at ..." with the command that starts it, instead of a bare connection error.

opencode 2 only, tested on 2.2.5. opencode 1.x is not supported yet. Text and image input follow what the server reports for each model.

## Install

Start Colibri on port 8765:

```bash
cd <colibri>/c && ./coli serve --model <model-dir> --model-id qwen3.6 --kv-slots 3 --ctx 65536 --port 8765
```

Not on its usual 8000: opencode 2 polls `127.0.0.1:8000` for vLLM from every plugin host and fills Colibri's limit of 8 connections per address.

Add the plugin to `opencode.json`:

```json
{ "plugin": ["@khalilgharbaoui/opencode-colibri"] }
```

Restart opencode and pick `colibri/<model-id>`, for example `colibri/qwen3.6`.

## Settings

Set them on the plugin entry:

```json
{
  "plugin": [
    ["@khalilgharbaoui/opencode-colibri", { "baseURL": "http://127.0.0.1:8765/v1", "apiKey": "..." }]
  ]
}
```

| Option | Environment variable | Default | Use |
| --- | --- | --- | --- |
| `baseURL` | `COLIBRI_BASE_URL` | `http://127.0.0.1:8765/v1` | Where `coli serve` listens. |
| `apiKey` | `COLIBRI_API_KEY` | none | Only when the server sets `COLI_API_KEY`. Sent as `Authorization: Bearer`. |

An option on the plugin entry wins over its environment variable.

## Speed

Colibri runs the model on the CPU, so the first request of a session pays for reading the whole prompt. Measured on an M5 Pro with Qwen3.6-35B-A3B: about 3 to 5 prompt tokens a second.

- opencode's default `build` agent sends roughly 10,000 tokens on its first request, which takes 30 minutes or more here.
- A small agent with a short prompt and one tool answered its first turn in 267 s and the next turn, in a new opencode process, in 18 s, because the session kept its cache slot.

A small agent for this, in `~/.config/opencode/agents/local.md`:

```markdown
---
description: Short-prompt agent for a local Colibri model
mode: primary
model: colibri/qwen3.6
permission:
  "*": deny
  shell: allow
---
Answer briefly. Use the shell tool when you need to look at files.
```

When Colibri is down, opencode retries the request for about 85 seconds before it shows the plugin's error.

## Develop

```bash
npm install
npm run typecheck && npm test && npm run build
```

To run a checkout, point opencode at its build: `{ "plugin": ["file:///<path>/opencode-colibri/dist"] }`.

## Release

1. `npm version patch -m "v%s"` (or `minor` / `major`).
2. `git push origin master --follow-tags`. The tag runs `.github/workflows/publish.yml`, which publishes to npm through trusted publishing (no token).
3. Once the version is on npm, `gh release create vX.Y.Z --title vX.Y.Z --notes "..."`.

## License

[MIT](LICENSE)
