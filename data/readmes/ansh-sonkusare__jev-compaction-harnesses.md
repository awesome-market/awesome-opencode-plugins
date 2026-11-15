# jev-compaction-harnesses

Context compaction for [pi](https://github.com/earendil-works/pi) and [opencode](https://opencode.ai) that deletes stale tool calls instead of summarizing your conversation.

This is a port of [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction), which does the same thing for Claude Code. The pruning logic is theirs, vendored unchanged. This repo adds the glue that lets pi and opencode use it.

## Why

When a coding agent runs out of context, the usual fix is to ask an LLM to summarize the old turns. Summaries lose things: the exact error message, the file path you mentioned once, the "never touch src/generated" rule from the first prompt.

fast-jev-compaction takes a different route. It shows TypeSafe's Jev model the whole conversation (with tool outputs replaced by one-line notes) and asks two yes/no questions about every old tool call: does the call still matter, and does its full output still need to stay? Whatever Jev lets go is deleted or cut down to its first 300 characters. Your messages and the assistant's replies are never rewritten. A Jev round trip usually takes under a second.

## How it plugs in

### pi (and senpi / omo)

pi's compaction hook returns a summary string plus the point where the recent, untouched history starts. It can't delete individual old entries. So the extension runs the old part of the history through Jev and puts what Jev kept, verbatim, where the summary would go. It also stores those kept messages on the compaction entry, so the next compaction can prune them again instead of treating them as frozen text.

If anything goes wrong (no key, Jev error, less than 25% saved, or the kept history would take more than a quarter of the context window), it steps aside and pi's normal summary runs.

senpi ships its own builtin `compaction` extension, which writes an LLM summary on every compaction. If both run, you pay for a summary that gets thrown away. Add this to your senpi agent `settings.json` and the extension will host the builtin itself, calling it only as the fallback:

```json
{ "disabledBuiltinExtensions": ["compaction"] }
```

Plain pi doesn't have that builtin and needs no setting.

### opencode

opencode doesn't let plugins replace its compaction summary, but it does let them rewrite the message list before every model call (`experimental.chat.messages.transform`). The plugin uses that:

1. Before each request it estimates the size of the conversation.
2. Once that passes a threshold (60k tokens by default) and there are enough new tool calls, it asks Jev about them.
3. Jev's decisions are remembered per session and applied to every later request: dropped tool calls are left out, truncated outputs are shortened.

Nothing in opencode's stored session changes. Only what gets sent to the model does, so opencode's own compaction still works as a backstop. Decisions live in memory, so after a restart the plugin asks Jev again the next time the threshold is crossed. If Jev fails, the request goes out unpruned and the plugin waits five minutes before trying again.

## When it runs, and running it yourself

It runs on its own when context gets big, like any compaction, and you can also run it by hand.

| | Automatic | By hand | What you see |
|---|---|---|---|
| pi / senpi | When pi auto-compacts (context close to the window limit) | `/compact` | A `[fast-jev] kept 33/214 messages verbatim, ...` card under the compaction entry. It stays in the transcript and is never sent to the model. |
| opencode | Once the conversation passes `FAST_JEV_TRIGGER_TOKENS` (60k) with enough new tool calls | `/jev-compact` | The report shows up in the chat (for example `Jev reviewed 5 old tool call(s) ... dropped 5 ... ~83% smaller`) plus a toast. The model replies with a one-line acknowledgement. The context counter in the sidebar drops on the next request. |

On opencode, `/jev-compact` ignores the size threshold and asks Jev about every old tool call right away. The newest few messages (`FAST_JEV_PRESERVE_RECENT`) are never touched.

## Install

You need a TypeSafe API key. Set `TYPESAFE_API_KEY` in your environment. If it isn't set, the adapters read it from the `env` block of `~/.claude/settings.json`, which is where the Claude Code plugin keeps it.

Heads up: this sends your conversation (minus tool outputs) to `api.typesafe.ai` every time it prunes. That is how Jev works, so only use it where that's acceptable.

### pi

```sh
pi install git:github.com/Ansh-Sonkusare/jev-compaction-harnesses
```

Or try it for one session from a checkout:

```sh
git clone https://github.com/Ansh-Sonkusare/jev-compaction-harnesses
pi -e ./jev-compaction-harnesses/pi/index.ts
```

For senpi, the same `-e` flag works, or copy the repo into your agent `extensions/` folder. Remember the `disabledBuiltinExtensions` setting above.

### opencode

Clone the repo and point your `opencode.json` at the plugin file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["/absolute/path/to/jev-compaction-harnesses/opencode/plugin.ts"]
}
```

These environment variables tune it:

| Variable | Default | Meaning |
|---|---|---|
| `FAST_JEV_TRIGGER_TOKENS` | `60000` | Estimated conversation size before Jev is asked |
| `FAST_JEV_MIN_NEW_CALLS` | `8` | New tool calls needed since the last Jev run |
| `FAST_JEV_PRESERVE_RECENT` | `6` | Newest messages Jev never touches |
| `FAST_JEV_KEEP_THRESHOLD` | `0.5` | Probability a call or output needs to stay |
| `FAST_JEV_LOG_FILE` | unset | Append one JSON line per Jev run, handy for seeing what it decided |

`opencode run` doesn't surface plugin logs, so `FAST_JEV_LOG_FILE` is the easiest way to watch it work.

## Tuning notes

With the default threshold of 0.5, Jev prunes hard. In our tests on real coding sessions it dropped around 90% of old tool calls. That's usually fine, because the agent can re-read a file or re-run a command. If you notice it re-running tools a lot, raise `keepThreshold` (`FAST_JEV_KEEP_THRESHOLD` on opencode).

## Development

```sh
bun install
bun test
bun run typecheck
```

The tests use a fake Jev and never hit the network. To pull a newer upstream:

```sh
sh scripts/sync-upstream.sh <commit>
```

Then update the pinned commit in `NOTICE`, this README, and `UPSTREAM_COMMIT` in `pi/index.ts`, and rerun the tests.

## Credits and references

- [tamaratran/fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) by Tamara Tran. The pruning algorithm, the Jev request format, the state fitting and the token estimates all come from there. Vendored unmodified at commit [`e3f262a`](https://github.com/tamaratran/fast-jev-compaction/tree/e3f262a7f4d42bd8dd32ced30d26176f7cb545b0) in `vendor/fast-jev-compaction/`, under its MIT license.
- Its [Claude Code hook adapter](https://github.com/tamaratran/fast-jev-compaction/blob/main/hooks/fast-jev.ts) was the model for the pi and opencode adapters here.
- [Jev](https://typesafe.ai) by TypeSafe answers the keep-or-drop questions.
- [pi](https://github.com/earendil-works/pi) extension API and [opencode](https://opencode.ai/docs/plugins/) plugin API.

A note on npm: the `fast-jev-compaction` package on npm is published by a different account and bundles extra hooks that aren't in the GitHub repo. This project uses the GitHub source only.

## License

MIT for the adapters, see [LICENSE](LICENSE). The vendored library keeps its own MIT license in [vendor/fast-jev-compaction/LICENSE](vendor/fast-jev-compaction/LICENSE). See [NOTICE](NOTICE).
