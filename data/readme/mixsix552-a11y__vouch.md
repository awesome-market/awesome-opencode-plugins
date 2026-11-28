# vouch

Evidence packets and remembered refusals for OpenCode agents.

An agent's closing sentence is a claim, not evidence. `vouch` records every
`write`, `edit`, `patch`, `read` and `shell` call the runtime actually performs,
then refuses to let the agent call the work done until the claims it makes are
carried by that record. It also remembers what you said no to, as a target and a
rule rather than a sentence, so the same request cannot come back in different
words.

No network calls, no telemetry, no model in the loop. Everything is local files
you can read with `cat`.

## Install

Drop it in the plugins directory and OpenCode picks it up:

```bash
git clone https://github.com/<you>/vouch ~/.config/opencode/plugins/vouch
```

Or point at it from your config, which also lets you turn enforcement off:

```jsonc
// ~/.config/opencode/opencode.json
{
  "plugins": [
    { "package": "~/.config/opencode/plugins/vouch", "options": { "block": true } }
  ]
}
```

`block: false` still records refusals but stops blocking them. `ledger` moves the
refusal file.

Requires OpenCode 2.1.4 or something whose plugin API still has `tool.transform`
and `ctx.location.directory` — if it does not, the plugin logs to
`~/.local/share/opencode/vouch/errors.log` and installs nothing rather than
breaking your session.

## What it does

**The runtime observes, the agent does not.** While a packet is open, every tool
call lands in it because the runtime put it there. A write is recorded with no
output and no hash on purpose: a file being written is a claim about a file until
something reads it back or runs after it.

**The packet is hash-chained.** A witness file sits beside it, one line per
action, claim, retraction and seal, each link carrying the hash of the one before.
Edit a number in the packet by hand and `vouch_check` says `TAMPERED` instead of
quietly agreeing with you.

**Tests that pass prove nothing on their own.** `vouch_inert` takes a recorded
change back out — in a throwaway copy of the tree, never yours — and re-runs the
command. If it still passes, the suite never depended on the change. A claim
carrying `proves: "tests"` stays `UNPROVEN` until one of those runs fails without
the change.

**A refusal is a resource and a rule.** `vouch_refuse` stores the target plus the
constraint that killed it, never the sentence that carried the no. From then on the
tool layer blocks writes, edits and shell commands touching that target, including
paths inside a denied directory, so a rephrase matches the ledger instead of
escaping it.

## Tools

| tool | what it does |
| --- | --- |
| `vouch_start` | open a packet before the work |
| `vouch_claim` | say something is true, name the actions behind it |
| `vouch_retract` | drop a claim you cannot support |
| `vouch_check` | would this survive a reviewer? |
| `vouch_seal` | close the packet |
| `vouch_inert` | revert a change in a copy of the tree and re-run the command |
| `vouch_refuse` | remember a refusal as (resource, constraint) |
| `vouch_review` | was this already refused? |
| `vouch_release` | lift a refusal, keeping the record |
| `vouch_list` | what is currently refused |

Every description is one line and `vouch_check` answers in one line when the
packet is clean — both are paid for on every request, not once.

## Failure modes `vouch_check` reports

- **UNSUPPORTED** — the claim points at no recorded action.
- **BLIND** — every action behind it carries no output and no hash.
- **WEAK** — every action behind it is recorded as failed. The run contradicts you.
- **UNVERIFIED_WRITE** — a file was written and nothing read it back and nothing ran.
- **NO_PROGRESS** — three identical actions. The approach is dead, not tired.
- **UNPROVEN** — a claim about tests with no revert check after it.
- **BROKEN_CHAIN** — the witness does not recompute. Something was edited in place.
- **TAMPERED** — the chain is intact but the packet no longer matches it.

## Where things live

- packets: `.vouch/<task>.json`, and `.vouch/current` points at the open one.
- witnesses: `.vouch/<task>.chain.jsonl`, append-only, one line per action.
- pre-write copies: `.vouch/snapshots/<sha256>.txt`, what a file held before a
  write touched it. This is what `vouch_inert` restores.
- refusals: `~/.local/share/opencode/refusals.jsonl`, append-only.
- observer failures: `~/.local/share/opencode/vouch/errors.log`. A silent observer
  would be worse than no observer.

## What it cannot do

- **The chain is not signed.** Anyone who edits the packet *and* rebuilds every
  link produces a chain that verifies. It catches the ordinary edit — a hand fix, a
  `sed`, a scripted patch — not a determined forger. Signing is a later version.
- **The shell blocker is a substring check.** Deterministic path blocking is exact;
  a command string is not parseable, so a deliberately obfuscated command gets
  past. It is a deterrent, not a sandbox.
- **`vouch_inert` reads the exit code, nothing else.** A test script that prints
  "passed" and exits 0 without running anything reads as `INERT` — the right
  verdict about a script that cannot fail, but it means your suite has to actually
  report failure. Use `set -e`.

## Development

```bash
node --test test/          # 77 tests
```

`test/interop.test.ts` cross-checks the packet format against a second
implementation of the same verifier. It skips unless one is present; point it at
yours with `VOUCH_EVIDENCE_CLI=/path/to/evidence`.

The tests need a POSIX shell, `cp`, `du` and `python3` present — `python3` only as
a fixture for the revert-check tests.

## License

MIT.
