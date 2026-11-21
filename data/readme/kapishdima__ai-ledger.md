![](apps/web/public/hero.png)

# grossbuh

Track AI API spending across providers — right in your terminal.

After each OpenCode session, grossbuh shows what that turn cost, how much you've burned today, and how much is left in your wallet. No more switching between dashboards.

Works with Anthropic, OpenAI, Gemini, Kimi, Groq, and anything else you have configured in OpenCode.

## Install

```sh
bunx grossbuh setup
```

This detects your API providers, lets you set initial balances, and registers the plugin in OpenCode.

## Commands

```sh
grossbuh            # show current balances
grossbuh balance    # same as above
grossbuh set anthropic 20    # reset a wallet balance
grossbuh add openai 10       # top up a wallet
grossbuh history             # recent transactions
grossbuh history 20          # last N transactions
```

## How it works

grossbuh runs as an OpenCode plugin. After each session goes idle, it injects a summary into the chat:

```
─── grossbuh · turn: -$0.0032 (anthropic)
    today: -$0.12  ·  month: -$1.84
 ⚠  anthropic   $18.16  ████████░░░░░░░░░░  49.1%
```

No separate window, no extra tabs — it's just there when you need it.
