# context-guard

An OpenCode plugin that says, once per threshold, how large a session's context
has grown and what one more turn on that model now costs.

The number it watches is `input + cache.read` from each `session.step.ended`.
The whole window is re-sent on every turn, so a long session pays for its own
history over and over — and that, not the volume of output, is what quietly
empties a subscription or a credit balance. A session that reaches 200k tokens
and then runs for another two hundred turns bills those 200k tokens two hundred
more times.

In the sidebar, under the context figure OpenCode already shows:

<img src="docs/sidebar.gif" alt="A pulsing red warning in the OpenCode sidebar, reading 165k context, /compact or new session soon" width="420">

Red and pulsing, and it stays until the context is cleared. On a model that
publishes prices the first line also carries what a turn now costs, as
`▲ 174k context · ~$0.26/turn`. There is a toast at
the moment each threshold is crossed, a line in the transcript, and a desktop
notification — all of them optional.

## Install

Clone it into the `plugins` directory beside your `opencode.json`:

```sh
git clone https://github.com/pierangeloc/opencode-context-guard \
  ~/.config/opencode/plugins/context-guard
```

The server half is discovered automatically. For the sidebar, add it to
`cli.json` as well:

```jsonc
// ~/.config/opencode/cli.json
{
  "plugins": ["./plugins/context-guard"]
}
```

Put it in the global config directory rather than a project's, unless you want
it in one project only: context size is a property of how you work, not of a
repository.

## Settings

Press `/context` in a session, or find **Context thresholds** in the palette.

```
Context thresholds · this session
  Warn at 100k, 150k                        one notice each, the first time
  New session at 200k                       where compacting stops being the advice
  Notify both
  Desktop notification on
  Compact automatically off
                                            ctrl+s  Edit everywhere instead
```

`ctrl+s` switches between **this session** and **everywhere**. A session's own
setting wins; clear it and the session falls back to the global one. Thresholds
are typed the way you say them: `150k`, `1.2M`, `150000`, or `60%` for a share
of this model's window. `never` turns the last threshold off.

Settings live in the server's plugin storage and are shared by every window, so
changing a threshold in one TUI applies to the next turn in another. Changing
them re-arms the session, so a threshold you have already passed announces once.

### From the config file

The same settings can be defaults in `opencode.json`, which is the place to put
per-model rules:

```jsonc
{
  "plugins": [
    {
      "package": "./plugins/context-guard",
      "options": {
        "warn": [100000, 150000],
        "clearAt": 200000,
        "compact": false,
        "notify": "both",
        "system": true,
        "models": {
          "anthropic/claude-opus-5": { "warn": [80000], "clearAt": 150000 },
          "openrouter/some/cheap-model": { "warn": [0.5], "clearAt": 0.8 }
        }
      }
    }
  ]
}
```

Four layers, narrowest last: **session → model → config file → defaults**. Each
supplies only the fields it names.

- `warn` — thresholds that each produce one notice. A value of 1 or less is a
  share of the model's window; above 1 it is an absolute token count.
- `clearAt` — the last threshold, where the advice becomes "start a new session"
  rather than "compact". `null` for none.
- `notify` — `both`, `chat` (transcript only), `toast` (sidebar and toast only),
  or `off`. With `off`, auto-compaction still runs if it is on.
- `system` — a desktop notification. macOS only; a no-op elsewhere.
- `compact` — run `/compact` for you at the last threshold.
- `models` — keyed by `providerID/id`, or a bare `id` to catch the same model
  however it is routed.

### Choosing thresholds

The defaults — 100k, 150k, 200k — are a starting point, not a recommendation.
Pick them from how you work: the useful question is not what fraction of the
window is full, but how many more turns you expect to take at this size.

Window share is a poor unit for this. 137k tokens is 14% of a 1M window and is
still re-read in full on every turn: around $0.21 a turn on a frontier model
against $0.04 on a mid-sized one. That is why the notice prints the share last
and in brackets, where it cannot undercut the warning, and why the thresholds
are absolute token counts by default.

Cost is reported at list price from the model's published `cost`, picking the
right tier for how full the window is — a tier's `size` is the floor it applies
*above*, so a 200k tier is the price of everything past 200k. Subscription
providers publish no prices, so there the notice simply says nothing about
money.

## Scope

- Subagent sessions are ignored. They carry their own context, die with their
  task, and cannot be cleared by hand.
- Thresholds re-arm after a compaction, since compaction empties the window.
- Each location loads its own instance of the server half, and the event stream
  is shared between them, so events are filtered by location. Without that a
  session announces once per project you have open.

## Layout

```
src/guard.ts   the arithmetic: thresholds, tiers, prices, parsing. No OpenCode
               import, so `node --test` covers it and both halves share it
src/rpc.ts     the settings contract between the two halves
src/index.ts   server: decides, announces, serves and stores the settings
src/tui.tsx    terminal: the sidebar line, the toast, the /context dialog
index.ts       re-export, so a local directory install resolves
tui.tsx        the same, for the terminal half
```

```sh
node --test test/
```

Two things about loading a plugin from a local directory, neither of which
costs anything to get right but both of which fail quietly:

- The directory's **root** `index.ts` and `tui.tsx` are what a local install
  resolves; the `exports` map in `package.json` is used when it is installed as
  a package. Having both means one tree works either way.
- Relative imports need their **extension**, including `.tsx`. Without it the
  loader looks for `./src/tui.ts`, does not find it, and the terminal half is
  simply absent. The failure appears in the client log as
  `plugin operation failed ... stage=read`, not in the terminal.

To confirm the terminal half is loaded, watch the plugin count:

```sh
grep 'reconciliation completed' ~/.local/share/opencode/log/opencode.log | tail -1
```

It goes up by one when the plugin loads, and a load that does real work takes
milliseconds rather than microseconds. The TUI picks up changes without a
restart.

## License

MIT
