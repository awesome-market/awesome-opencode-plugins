# opencode-invalid-request-fix

**One-command fix for OpenCode sessions that die forever with `Error: Invalid request parameters`.**

Two different causes are covered:

| # | Cause | Symptom | Fix in this repo |
|---|---|---|---|
| 1 | **NUL bytes (`\x00`) in conversation history** | `400` + `"String must not contain null bytes"` — every later message in that session fails | `nul-sanitizer` plugin strips them before every model call |
| 2 | **Removed / deprecated model** | `410` + `"Model X has been deprecated."` | plugin auto-switches the session to your configured default model and retries |

Both of these are *sticky*: once they happen, the session is unusable and "continue" does not help,
because the bad state is stored in the session history.

---

## Install

### One-liner (recommended)

```sh
curl -fsSL https://raw.githubusercontent.com/CanArslanDev/opencode-invalid-request-fix/main/install.sh | bash
```

### From a clone

```sh
git clone https://github.com/CanArslanDev/opencode-invalid-request-fix.git
cd opencode-invalid-request-fix
./install.sh
```

Installing is idempotent. Existing files are backed up first (`*.bak.<timestamp>`).

### Optional flags

```sh
./install.sh --model venice/deepseek-v4-1-flash-uncensored   # also set a default model
./install.sh --no-agents                                     # skip the AGENTS.md guidance block
./install.sh --dry-run                                       # show what would happen
./install.sh --prefix ~/.config/opencode                     # custom config dir
```

---

## What gets installed

| Path | Purpose |
|---|---|
| `<config>/plugins/nul-sanitizer.ts` | The fix. Hooks `prompt`, `context`, `compaction`, `generate`, `title` and `retry`. |
| `<config>/scripts/fix-nul-bytes.py` | Permanent DB cleanup for sessions that already contain NULs. |
| `<config>/AGENTS.md` | A managed block telling the agent to filter binary output at the source. |
| `<config>/nul-sanitizer.log` | Runtime diagnostics (created on first use; silence with `OPENCODE_NUL_QUIET=1`). |

`<config>` is `${XDG_CONFIG_HOME:-$HOME/.config}/opencode`.

### `/fix-nuls` command

The plugin also registers a TUI command:

```
/fix-nuls         # permanently clean NULs from the session database (takes a backup first)
/fix-nuls dry     # report only, change nothing
```

You do **not** need it for the fix to work — the plugin sanitizes on the fly. It is only for
housekeeping so stored history stays small and clean.

---

## How it works

The plugin runs inside the OpenCode **server** and hooks the moment right before a request is
dispatched. It walks `event.messages` and `event.system` and replaces any `\u0000` with a space.
Persisted history is not rewritten, so **old broken sessions become usable again** too.

```ts
await ctx.session.hook("context", onRequest)  // agent loop
await ctx.session.hook("compaction", onRequest)
await ctx.session.hook("generate", onRequest)
await ctx.session.hook("title", onRequest)
await ctx.session.hook("retry", onRetry)      // 400 → retry, 410 → switch model + retry
```

See [`docs/how-it-works.md`](docs/how-it-works.md) for the full mechanism, including the root
cause analysis and a reproducible controlled experiment.

---

## Verify

```sh
ocf-doctor                                     # or ./doctor.sh
# / or:
opencode plugin list                           # "nul-sanitizer" must be listed
python3 ~/.config/opencode/scripts/fix-nul-bytes.py --dry-run
tail ~/.config/opencode/nul-sanitizer.log      # what the plugin actually did
```

Expected: the plugin is listed and no NUL bytes are reported.

### Proof it actually works

Controlled experiment on a real install — one session, one injected NUL, the plugin as the only
variable, against a provider that rejects NUL bytes:

```
plugin OFF + NUL in history ->  finish=error  provider.invalid-request   (the bug)
plugin ON  + same NUL       ->  finish=stop   + log: "scrubbed NUL bytes from 1 string(s)"
```

For the removed-model path: a session pinned to a delisted model
(`opencode/exo-free`) is switched to the configured fallback and completes normally.

---

## Uninstall

```sh
./uninstall.sh
# or, from anywhere:
curl -fsSL https://raw.githubusercontent.com/CanArslanDev/opencode-invalid-request-fix/main/uninstall.sh | bash
```

Removes the plugin, the script and the managed `AGENTS.md` block. Your own `AGENTS.md` content and
all session data are left untouched.

---

## Requirements

- macOS or Linux, `bash`, `curl`, `python3`
- OpenCode **v2** (plugin API `@opencode/plugin`)
- No network at run time; everything is local

## Limitations / notes

- The plugin only fixes the **outgoing** request. Your database may still contain NULs — harmless,
  and `/fix-nuls` cleans them if you care.
- If OpenCode ships a breaking plugin-API change, re-check with `opencode plugin list` after
  upgrading. See [`docs/troubleshooting.md`](docs/troubleshooting.md).
- The deprecated-model recovery needs a usable default model. Keep `model` in `opencode.json`
  pointing at something that exists, or set `OPENCODE_NUL_FALLBACK_MODEL=provider/model`.
- It does not help with unrelated 400s (oversized payloads, provider outages).

## Credits

Root cause found while debugging a real Ableton Live cracking session that kept dying on
`grep -a` over binary files. Reverse-engineered from that incident.

## License

[MIT](LICENSE)
