# opencode-copilot-1m

OpenCode plugin that adds long-context variants for Claude and GPT-5 models on GitHub Copilot.

Without this plugin, Copilot can expose smaller client-side limits than you want for long sessions. This plugin creates separate `(1M)` model entries with higher client-side limits while keeping the original models available.

## Supported models

- Claude Opus 4.6
- Claude Opus 4.7
- Claude Opus 4.8
- Claude Sonnet 4.6
- GPT-5.4
- GPT-5.5

## Install

Add to your `opencode.json`:

```json
{
  "plugin": ["opencode-copilot-1m"]
}
```

Restart OpenCode. You'll see new model entries like "Claude Opus 4.8 (1M)", "GPT-5.4 (1M)" and "GPT-5.5 (1M)" alongside the originals.

## Recommended: set reasoning effort

The plugin can't control reasoning effort (that's a per-user config setting). Recommended settings for the 1M variants:

```json
{
  "plugin": ["opencode-copilot-1m"],
  "provider": {
    "github-copilot": {
      "models": {
        "claude-opus-4.6-1m": {
          "reasoningEffort": "high"
        },
        "claude-opus-4.7-1m": {
          "reasoningEffort": "medium"
        }
      }
    }
  }
}
```

> `high` is the max for Opus 4.6. `medium` is currently the highest available for Opus 4.7.

## How it works

The plugin hooks into the `github-copilot` provider's model list and clones each supported model into a `-1m` variant with model-specific long-context limits. It keeps the original API model ID but overrides the client-side limit metadata OpenCode uses for budgeting and compaction.

It also sets the `Copilot-Integration-Id: copilot-developer-cli` header on all Copilot requests.

## Related

- [opencode-anthropic-context-1m](https://github.com/DusKing1/opencode-anthropic-context-1m) -- same thing for Anthropic direct API and Amazon Bedrock
- [OpenCode issue #12338](https://github.com/anomalyco/opencode/issues/12338) -- background on the problem
- [OpenCode issue #16298](https://github.com/anomalyco/opencode/issues/16298) -- GPT-5.4 input/context limit background

## License

MIT
