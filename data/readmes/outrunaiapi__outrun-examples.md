<p align="center">
  <a href="https://outrun.to/?utm_source=github&utm_medium=repo&utm_campaign=examples">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/outrun-logo-cream.png">
      <img src="assets/outrun-logo-dark.png" alt="Outrun AI API" width="320">
    </picture>
  </a>
</p>

# Outrun API examples

**One OpenAI-compatible API key for 81 AI models: GPT, Claude, Gemini, Grok, DeepSeek, GLM,
Kimi, Qwen, MiniMax, uncensored and abliterated LLMs, plus image, video and speech models.**

Outrun is a prepaid AI API. You top up one USD balance, and every request is billed per use at
a published per-token (or per-image, per-second) rate. This repo has copy-paste examples and
ready config files for the tools developers already use.

```text
Base URL:  https://api.outrun.to/v1
Auth:      Authorization: Bearer $OUTRUN_API_KEY
```

- Works with the official OpenAI SDKs (Chat Completions and Responses), the Anthropic Messages
  API for Claude model IDs, and the Gemini native format.
- The model ID you send is the model that answers.
- Prices: [outrun.to/model/](https://outrun.to/model/?utm_source=github&utm_medium=repo&utm_campaign=examples)
  (every model, its billed price, context and setup values).
- Docs: [outrun.to/docs/](https://outrun.to/docs/?utm_source=github&utm_medium=repo&utm_campaign=examples)

## Quick start

1. Get a key: sign in at [outrun.to](https://outrun.to/overview?utm_source=github&utm_medium=repo&utm_campaign=examples)
   or open the Telegram bot [@outrunAPI_Bot](https://t.me/outrunAPI_Bot?start=gh_examples).
2. Put it in an environment variable (never in code or a commit):

   ```bash
   export OUTRUN_API_KEY="your-key"
   ```

3. Send a request:

   ```bash
   curl https://api.outrun.to/v1/chat/completions \
     -H "Authorization: Bearer $OUTRUN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-5.6-sol", "messages": [{"role": "user", "content": "Say hello in five words."}]}'
   ```

### Python (OpenAI SDK)

```python
import os
from openai import OpenAI

client = OpenAI(base_url="https://api.outrun.to/v1", api_key=os.environ["OUTRUN_API_KEY"], max_retries=0)

resp = client.chat.completions.create(
    model="claude-sonnet-5",  # or gpt-5.6-sol, gemini-3.8-flash, grok-4.7, deepseek-v4-pro, glm-5.3-abliterated ...
    messages=[{"role": "user", "content": "Say hello in five words."}],
)
print(resp.choices[0].message.content)
```

### Node (OpenAI SDK)

```js
import OpenAI from "openai";

const client = new OpenAI({ baseURL: "https://api.outrun.to/v1", apiKey: process.env.OUTRUN_API_KEY, maxRetries: 0 });

const resp = await client.chat.completions.create({
  model: "gemini-3.8-flash",
  messages: [{ role: "user", content: "Say hello in five words." }],
});
console.log(resp.choices[0].message.content);
```

Change only `model` to switch between GPT, Claude, Gemini, Grok, DeepSeek, GLM, Kimi, Qwen,
MiniMax and the uncensored models. All IDs are in [CATALOG.md](CATALOG.md).

> The examples set `max_retries=0`: every request is billed, so if a request is interrupted,
> check Activity in your dashboard before you send it again.

## Examples

| Task | curl | Python | Node |
| --- | --- | --- | --- |
| Chat Completions | [chat.sh](examples/curl/chat.sh) | [chat.py](examples/python/chat.py) | [chat.mjs](examples/node/chat.mjs) |
| Streaming | [stream.sh](examples/curl/stream.sh) | [stream.py](examples/python/stream.py) | [stream.mjs](examples/node/stream.mjs) |
| Responses API (GPT) | [responses.sh](examples/curl/responses.sh) | | |
| Anthropic Messages (Claude) | [anthropic-messages.sh](examples/curl/anthropic-messages.sh) | [anthropic_messages.py](examples/python/anthropic_messages.py) | |
| Image generation | [image.sh](examples/curl/image.sh) | [image.py](examples/python/image.py) | [image.mjs](examples/node/image.mjs) |
| List models | [models.sh](examples/curl/models.sh) | | |
| LiteLLM SDK + proxy | | [sdk_example.py](examples/litellm/sdk_example.py), [config.yaml](examples/litellm/config.yaml) | |

Video, text-to-speech, speech-to-text and Gemini native examples are in the
[API reference](https://outrun.to/docs/api?utm_source=github&utm_medium=repo&utm_campaign=examples).

## Coding agents and IDE tools

Ready config files, copied from the setup guides in the Outrun docs:

| Tool | Config | Protocol | Guide |
| --- | --- | --- | --- |
| Claude Code | [configs/claude-code](configs/claude-code) | Anthropic Messages | [setup/claude](https://outrun.to/docs/setup/claude?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Codex CLI | [configs/codex](configs/codex) | OpenAI Responses | [setup/codex](https://outrun.to/docs/setup/codex?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| OpenCode | [configs/opencode](configs/opencode) | OpenAI Chat Completions | [setup/opencode](https://outrun.to/docs/setup/opencode?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Cline | [configs/cline](configs/cline) | OpenAI Chat Completions | [setup/cline](https://outrun.to/docs/setup/cline?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Roo Code | [configs/roo-code](configs/roo-code) | OpenAI Chat Completions | [setup/uncensored](https://outrun.to/docs/setup/uncensored?utm_source=github&utm_medium=repo&utm_campaign=examples) |

The docs also cover Gemini CLI, Grok Build CLI, the Codex desktop app and Zo Computer.

## Models by family

| Family | Example model IDs | Page |
| --- | --- | --- |
| OpenAI GPT | `gpt-6.1-sol`, `gpt-6-astra`, `gpt-5.6-sol` | [GPT API](https://outrun.to/gpt-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Anthropic Claude | `claude-opus-5-5`, `claude-sonnet-5`, `claude-haiku-5-5` | [Claude API](https://outrun.to/claude-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Google Gemini | `gemini-3.8-flash`, `gemini-3.1-pro-preview` | [Gemini API](https://outrun.to/gemini-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| xAI Grok | `grok-4.7` | [Grok API](https://outrun.to/grok-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| DeepSeek | `deepseek-v4-pro`, `deepseek-v4.1-flash` | [DeepSeek API](https://outrun.to/deepseek-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Zhipu GLM | `glm-5.3`, `glm-5.3-flash` | [GLM API](https://outrun.to/glm-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Moonshot Kimi | `kimi-k3.1-pro`, `kimi-k3` | [Kimi API](https://outrun.to/kimi-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Alibaba Qwen | `qwen3.8-max`, `qwen3.8-flash`, `qwen3.7-plus` | [Qwen API](https://outrun.to/qwen-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| MiniMax | `MiniMax-M3` | [MiniMax API](https://outrun.to/minimax-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Uncensored and abliterated | `glm-5.3-abliterated`, `glm-5.3-uncensored`, `deepseek-v4-pro-uncensored` | [Uncensored AI API](https://outrun.to/uncensored-ai-api?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Image | `gemini-3-pro-image`, `gpt-image-2`, `grok-imagine-image` | [Image setup](https://outrun.to/docs/setup/images?utm_source=github&utm_medium=repo&utm_campaign=examples) |
| Video and speech | `veo-3.1`, `seedance-2.5-720p`, `gemini-3.1-tts` | [All models](https://outrun.to/model/?utm_source=github&utm_medium=repo&utm_campaign=examples) |

Model IDs are case-sensitive. The full, current list is in [CATALOG.md](CATALOG.md),
regenerated from the public feed `https://api.outrun.to/pricing` by
[`scripts/update_catalog.py`](scripts/update_catalog.py). Prices are kept out of this repo
so they can't go stale; the model pages always show the billed rate.

## FAQ

**Is Outrun OpenAI-compatible?**
Yes. Set the base URL to `https://api.outrun.to/v1` in any OpenAI SDK or tool and use an
Outrun key. `/v1/chat/completions`, `/v1/responses`, `/v1/models`, `/v1/images/generations`,
`/v1/audio/speech` and `/v1/videos` are supported.

**Can I use Claude models with the Anthropic SDK or Claude Code?**
Yes. Claude model IDs work on `/v1/messages` with the `x-api-key` header. In the Anthropic
SDK and Claude Code, the base URL is the bare host `https://api.outrun.to`.

**How does billing work?**
Prepaid. You add credit to one USD balance, and each request is charged at the model's
published rate. Eligible new accounts get $0.10 in free API credit to try it. See
[billing](https://outrun.to/docs/billing?utm_source=github&utm_medium=repo&utm_campaign=examples).

**Does Outrun store my prompts?**
Outrun does not store your prompts, images or outputs unless you choose to save them.

**Where is a machine-readable model list?**
[`https://outrun.to/llms.txt`](https://outrun.to/llms.txt?utm_source=github&utm_medium=repo&utm_campaign=examples)
for LLMs and agents, and `https://api.outrun.to/pricing` as JSON.

## Links

- Website: [outrun.to](https://outrun.to/?utm_source=github&utm_medium=repo&utm_campaign=examples)
- All models and prices: [outrun.to/model/](https://outrun.to/model/?utm_source=github&utm_medium=repo&utm_campaign=examples)
- Docs: [outrun.to/docs/](https://outrun.to/docs/?utm_source=github&utm_medium=repo&utm_campaign=examples)
- llms.txt: [outrun.to/llms.txt](https://outrun.to/llms.txt?utm_source=github&utm_medium=repo&utm_campaign=examples)
- Telegram bot: [@outrunAPI_Bot](https://t.me/outrunAPI_Bot?start=gh_examples)

Found a broken example? Open an issue. Please never paste your API key into an issue.

## License

[MIT](LICENSE)
