# opencode-chatgpt-websearch

`opencode-chatgpt-websearch` lets OpenCode2 run web searches using your existing ChatGPT login.

## Prerequisites

- OpenCode2 with V2 plugin support
- An `openai` connection authenticated through ChatGPT OAuth (browser or headless login)

## Install

Add the plugin to `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "plugins": ["opencode-chatgpt-websearch"]
}
```

Restart OpenCode2. On the first web search, select **ChatGPT (experimental)** as the web-search provider.

## Configuration

The default configuration uses `gpt-5.6-luna` with maximum reasoning. You can override it through the plugin options:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-chatgpt-websearch",
      "options": {
        "model": "gpt-5.6-luna",
        "reasoningEffort": "max",
        "responseLength": "short",
        "maxOutputTokens": 4096,
        "timeoutMs": 25000
      }
    }
  ],
  "websearch": {
    "provider": "chatgpt"
  }
}
```

Setting `websearch.provider` is optional. It selects ChatGPT automatically instead of showing the provider chooser.
