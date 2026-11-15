# opencode-workspace-mailbox

A per-project handoff mailbox for [OpenCode](https://opencode.ai) sessions.

Every session gets it: a file-based inbox that other sessions write to, automatic delivery when the
session goes idle, and loop guards so an agent can never talk itself into a spin. One global config
serves a whole folder tree — **meta → account → repo** — because the tier is derived from the
directory a session opens in, not from what you remember to configure.

Built for OpenCode today; the storage layer is behind a `MailboxStore` interface, so the file
backend can be swapped for SQLite or Engram — see [Backlog](#backlog).

> Status: the code is complete (123 tests, `typecheck` and `build` green, repo at
> [mr-wolf-rsh/opencode-workspace-mailbox](https://github.com/mr-wolf-rsh/opencode-workspace-mailbox)).
> Published on npm — see [Install](#install).

## The metaphor

The mailbox is a **chain of command made of files**. Each tier owns a `handoffs/` folder holding its
own `workspace.md` plus one file per immediate child. Messages only ever move along that ladder:
escalate up, delegate down, or talk to a sibling.

| In an organisation | In opencode-workspace-mailbox |
|---|---|
| The chief of staff | **Meta** tier — `C:\work` reads `handoffs/workspace.md` |
| Account leads | **Account** tier — `acme` reads `acme/handoffs/workspace.md` |
| The team doing the work | **Repo** tier — `<account>/handoffs/<project>.md` |
| Memos, never rewrites | Append-only markdown; history is the audit trail |
| "Received" stamp | `**Status:**` flips `OPEN` → `DONE`, one line, nothing else touched |
| Handing over a task | `mailbox_send({ to: "scraper-service", ... })` |
| Standing instructions | `wake: true` — an idle session picks up new mail within one poll |
| Opening a desk for the recipient | `deliverOnSend: "auto"` — reuses or creates a session in the recipient's folder and starts it |
| A message that needs a decision | Only then does the agent reply in chat |

Tiers are **discovered from the folder tree**, not configured: a directory with `handoffs/` is a
tier root, and anything under it resolves to its nearest ancestor that has one.

## Why this exists

Multi-repo workspaces talk through asynchronous handoffs: one file per project, append-only,
addressed `from X → to Y`. The protocol works. The human relay does not.

A message sits `OPEN` until somebody opens the right session, reads it, acts on it, and flips it to
`DONE` — and "somebody remembers" is exactly the step that fails. Worse, once you have a parent
strategy session and several implementation repos, the relay has to survive closed sessions,
restarts, and a working day that never lines up.

So this plugin closes the loop **inside the session that receives the message**. No daemon, no
scheduler, no `opencode run` spawning a session per message: if a session is closed, the message
simply waits in its file. When the session is open, the message surfaces on its own.

The file format is the product, not an implementation detail: it is readable, diffable, reviewable
in a PR, greppable, and it survives every process that ever touched it.

## What it does

Delivered as tools the agent calls and two hooks the runtime calls:

- **`mailbox_read`** — list `OPEN` messages for a project (or any routed recipient).
- **`mailbox_send`** — append a message to the recipient's mailbox, optionally delivering it into the
  recipient's session.
- **`mailbox_ack`** — flip one message's `**Status:**` line to `DONE`, byte-preserving everywhere
  else.
- **`mailbox_status`** — backend, locations, and per-project counts for both backends.
- **`mailbox_migrate`** — copy every message between backends, idempotently; `dryRun` supported.
- **`mailbox_prune`** — apply `retentionDays`, moving old `DONE` messages to the archive; `dryRun`
  supported.

On `session.idle` (and, with `wake: true`, on a timer) the plugin reads the session's own mailbox,
finds `OPEN` messages it has not handled yet, and prompts the session **once** to deal with them.

### Delivery is automatic when you opt in

`wake: true` makes an already-idle session notice new mail. Without it, the plugin only reacts to an
idle *transition* — which means a session that has been sitting idle all afternoon never learns
about the message your other session just wrote.

### Delivery opens the recipient's desk

`deliverOnSend` hands the message to the recipient's session directly: it reuses one if it exists,
creates one if it does not, and prompts it — so a project with nothing open can still be reached.
Guarded so it cannot ping-pong — see [Delivery on send](#delivery-on-send).

## Install

1. Add the plugin to your `opencode.json`:

   ```jsonc
   {
     "$schema": "https://opencode.ai/config.json",
     "plugin": [
       ["opencode-workspace-mailbox", {
         "wake": true,
         "deliverOnSend": "auto"
       }]
     ]
   }
   ```

   Both flags are off by default: `wake` costs tokens while nobody is watching, and delivery starts
   (or creates) a session that runs a turn on its own. Turn them on deliberately.

   Do **not** set `mailboxDir` unless you deliberately want one pinned mailbox: it disables tier
   discovery, which is the whole point of a single global config.

2. If your config directory declares plugin dependencies (some setups keep a `package.json` next to
   `opencode.json`), add the package there too:

   ```powershell
   cd C:\Users\<you>\.config\opencode
   npm install opencode-workspace-mailbox --save
   ```

3. Restart OpenCode.

Local path variant during development (no publish needed — `prepare` builds it):

```powershell
npm install file:C:\work\acme\tools\opencode-workspace-mailbox --save
```

```jsonc
["C:\\work\\acme\\tools\\opencode-workspace-mailbox", { "wake": true }]
```

## Configuration

```jsonc
["opencode-workspace-mailbox", {
  // Master switch. false = the plugin does nothing at all.
  "enabled": true,

  // Pin ONE mailbox directory and disable tier discovery. Leave unset normally.
  "mailboxDir": null,

  // Override the derived identity ("workspace" for a tier root, else the folder name).
  "project": null,

  // Storage backend: "file" (markdown is the source) or "sqlite" (database is
  // the source, markdown is written as a mirror).
  "storage": "file",
  // Database location for storage: "sqlite". Default: <mailboxDir>/.mailbox.db
  "sqlitePath": null,
  // Mirror sqlite appends/acks back into the markdown file (default true).
  "sqliteMirror": true,

  // Auto-prompts in a row without progress, then one toast instead. 0..20.
  "maxAutoRounds": 2,

  // Minimum gap between auto-prompts (and between notices).
  "cooldownMs": 30000,

  // Poll the mailbox and wake an idle session on a new message.
  "wake": false,
  "pollMs": 10000,

  // Deliver a sent message into the recipient's session.
  //   "off"   - write only, the recipient picks it up later
  //   "reuse" - prompt an existing session, never create one
  //   "spawn" - always create a fresh session and prompt it
  //   "auto"  - reuse when one exists, otherwise create, then prompt
  "deliverOnSend": "off",
  "spawnCooldownMs": 60000,
  "maxSpawnsPerTurn": 1,

  // Explicit recipient -> directory map for delivery. Discovery covers most trees.
  "projectDirs": {},

  // Append a row for a new recipient to the tier README's `## Files` table on
  // first send. Off by default: that README is hand-authored documentation, and
  // the protocol treats it as the authoritative file list.
  "registerRecipients": false,

  // Ignore messages older than this ISO date (first-contact watermark).
  "since": null,

  // Move DONE messages older than N days into the archive (0 = never).
  "retentionDays": 0,
  "retentionArchiveDir": null,

  // Where dedupe/round/delivery state is persisted (must stay inside the project directory).
  "stateFile": null
}]
```

| Option | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master switch. |
| `mailboxDir` | discovered | Pin a mailbox directory; disables discovery. |
| `project` | resolved | Explicit identity override. |
| `storage` | `"file"` | `"file"` or `"sqlite"`. |
| `sqlitePath` | `<mailboxDir>/.mailbox.db` | Database file for the sqlite backend. |
| `sqliteMirror` | `true` | Mirror sqlite writes into the markdown file. |
| `maxAutoRounds` | `2` | Auto-prompts in a row without progress, `0..20`. |
| `cooldownMs` | `30000` | Gap between auto-prompts and notices. |
| `wake` | `false` | Poll and wake an idle session. |
| `pollMs` | `10000` | Wake poll interval, `100..600000`. |
| `deliverOnSend` | `"off"` | `off` / `reuse` / `spawn` / `auto` — see below. |
| `spawnCooldownMs` | `60000` | Gap between deliveries. |
| `maxSpawnsPerTurn` | `1` | Deliveries per human turn, `0..10`. |
| `projectDirs` | `{}` | Explicit recipient → directory map. |
| `registerRecipients` | `false` | Add a new recipient's row to the tier README's `## Files` table. |
| `since` | `null` | Ignore messages older than this ISO date. |
| `retentionDays` | `0` | Archive DONE messages older than N days (`0` = never). |
| `retentionArchiveDir` | `<mailboxDir>/_archive` | Archive destination for the file backend. |
| `stateFile` | `<dir>/.atl/mailbox-state.json` | Persisted dedupe/round/delivery state. |

## Tiers and identity

| Tier | Folder | Reads at start | Holds |
|---|---|---|---|
| **Meta** | `C:\work` | `handoffs/workspace.md` | `workspace.md` + one file per account |
| **Account** | `C:\work\acme` | `acme/handoffs/workspace.md` | `workspace.md` + one file per repo |
| **Repo** | `.../acme/tools/opencode-workspace-mailbox` | `acme/handoffs/opencode-workspace-mailbox.md` | its own file, at the account level |

Discovery rules, for a session opened in `D`:

1. `project` is set in config → use it verbatim (and `mailboxDir` if set).
2. `D` has `handoffs/` → `D` is a tier root. Parent has one too → **account**, else **meta**.
   Identity is `workspace`; its mailbox is `D/handoffs`.
3. Otherwise → walk up to the nearest ancestor with `handoffs/`; that is the **account**, `D` is a
   **repo**. Identity is `D`'s folder name, kebab-cased, and the mailbox is the account's
   `handoffs/` — so bucket layouts like `<account>/tools/<repo>` work without configuration.

For this workspace:

| Session opened at | Tier | Mailbox |
|---|---|---|
| `C:\work` | meta | `C:\work\handoffs\workspace.md` |
| `C:\work\acme` | account | `C:\work\acme\handoffs\workspace.md` |
| `C:\work\acme\tools\opencode-workspace-mailbox` | repo | `C:\work\acme\handoffs\opencode-workspace-mailbox.md` |
| `C:\work\globex\scraper-service` | repo | `C:\work\globex\handoffs\scraper-service.md` |

### Routing

- **`to: workspace`** → this tier's own `workspace.md`.
- **`to: <account>`** → the root tier's `<account>.md` — escalate up, or lateral between accounts.
- **`to: <anything else>`** — a sibling or child file in this tier: lateral, or delegate down.

The inbox for a tier is created on first run; an account session also creates its file at the root.
Unknown recipients are created on first send. Reads never create files.

## Mailbox format

Files are `<mailboxTier>/handoffs/<project>.md`. Append-only: messages are never rewritten,
reordered, or "tidied". The **only** permitted edit to history is the `**Status:**` line.

```markdown
### YYYY-MM-DD HH:MM — from <source> → to <recipient>
**Status:** OPEN | DONE
**Topic:** one-line subject
Body — what needs attention, the question, exact paths/commits/commands.
```

`mailbox_ack` replaces the status line's content with `DONE`, so an annotated
`**Status:** OPEN (confirm the wording)` becomes `**Status:** DONE`. Every other byte — spacing
elsewhere, line endings, bodies — is unchanged; the tests assert that on CRLF fixtures, and it was
verified by hand against a real 113 KB mailbox file.

## Storage

Mailboxes sit behind a `MailboxStore` interface:

```ts
interface MailboxStore {
  ensure(project: string): string
  listOpen(project: string): MailboxMessage[]
  read(project: string): MailboxMessage[]
  append(project: string, input: AppendInput): SendResult
  ack(project: string, target: { hash?: string; header?: string }): AckResult
  query(project: string, filter?: MailboxFilter): MailboxMessage[]
  close?(): void
}
```

Two backends ship:

| Backend | Source of truth | Hot path |
|---|---|---|
| `"file"` (default) | the markdown file | reads and parses one file per trigger |
| `"sqlite"` | `<mailboxDir>/.mailbox.db` | indexed `SELECT`s; no file parsing |

**SQLite details.** One database per mailbox directory, `WAL` mode, tables
`messages(project, header, sender, recipient, status, topic, body, hash, created_at)` with indexes on
`(project, status)` and `(project, hash)`, plus an `imported(project, at)` table. The driver is
`bun:sqlite` when running under Bun (OpenCode) and `node:sqlite` on Node ≥ 22.5, loaded through
`createRequire` so both work.

**Markdown stays the contract.** With `sqliteMirror: true` (default), every append is written to the
database *and* appended to `<project>.md`, and every ack flips the status line in both. Agents and
humans keep reading the file; the plugin stops parsing it on the hot path. Existing files are
imported once per project on first open, so switching backends keeps the history that started in
markdown.

The file backend and the state file write under an exclusive `.lock` sidecar (a stale lock from a crashed writer is stolen), so two sessions sharing one mailbox cannot clobber each other's append or ack.

Set `sqliteMirror: false` if you want the database to be the only artifact. Also add
`.mailbox.db*` to `.gitignore` (WAL mode creates `-wal` and `-shm` files).

A third backend (Engram, or a remote store) only has to implement the same methods — the tools,
wake path, and delivery code never change.

### Keep the mirror on

The `workspace-mailbox` skill tells agents to read `handoffs/<project>.md`. With
`sqliteMirror: false` that file stops receiving new messages, so agents following the skill read a
stale thread. Only disable the mirror if you have also changed the skill flow to use `mailbox_read`.

## Migrating between backends

`mailbox_migrate` copies messages either way, keyed by hash, so re-running it is a no-op and a
partially-completed run resumes instead of duplicating:

| Call | Effect |
|---|---|
| `mailbox_migrate({ to: "sqlite" })` | Imports every markdown mailbox into `<mailboxDir>/.mailbox.db` |
| `mailbox_migrate({ to: "file" })` | Exports every database row into its markdown mailbox |
| `mailbox_migrate({ to: "sqlite", dryRun: true })` | Reports the counts that would change, writes nothing |

Both directions also reconcile `OPEN`/`DONE`: a message marked `DONE` on the source is acked on the
target, so the two never disagree about state.

What it does **not** do:

- Change your `storage` option — set it after migrating.
- Migrate other tiers — the tool works on the tier the session belongs to. Run it once per tier
  (meta, each account) if you are switching globally.
- Deduplicate deliberately duplicated messages: duplicates are counted and preserved.

Switching backends is safe at any time; `mailbox_status` shows both sides so you can verify before
flipping `storage`.

## Loop guards

| Guard | Behaviour |
|---|---|
| Hash dedupe | One prompt per message, persisted across restarts. |
| Own writes | Messages this plugin appended never wake anybody. |
| Round cap | `maxAutoRounds` prompts in a row without progress, then a toast instead. |
| Progress reset | An `mailbox_ack`, or a drained inbox, restores the budget. |
| Cooldown | `cooldownMs` between prompts; one notice per distinct pending set. |
| Idempotent ack | Acking an already-`DONE` message is a no-op, not an error. |
| Spawn guards | Opt-in, one per message hash, cooldown, per-turn cap, never from a spawned session, never when a session already exists. |

## How delivery decides

1. **Trigger** — `session.idle`, or a `wake` poll tick for the most recently active non-busy session.
2. **Skip** — plugin is disabled, this session was just prompted by the plugin, or the session is
   mid-turn.
3. **Filter** — keep `OPEN` messages newer than `since` whose hash is not in `prompted` and not in
   `ownWrites`.
4. **Budget** — if the inbox is empty, reset the round budget; if the cap or cooldown is hit, stop
   (surfacing a one-line toast at most once per pending set).
5. **Dispatch** — record every hash *before* prompting, then send one prompt: load the
   `workspace-mailbox` skill, read the file, handle the messages, ack them, reply only if a decision
   is needed. The prompt also carries the protocol itself — use the `mailbox_*` tools, append-only,
   how to route by recipient, and never write another project's `SESSION.md` — so a session acts
   correctly even when the skill is absent or out of date.

Hashes are recorded before dispatch on purpose: a failed prompt is retried, never silently dropped.

## Delivery on send

`mailbox_send` can hand a message to a session in the recipient's directory instead of waiting for
the recipient to notice it. One option, four modes:

| `deliverOnSend` | Behaviour |
|---|---|
| `"off"` (default) | Write only. The recipient picks it up on idle or `wake`. |
| `"reuse"` | Prompt an existing session for that directory. Never create one. |
| `"spawn"` | Always create a fresh session, titled `mailbox: <recipient>`, and prompt it. |
| `"auto"` | Reuse when a session exists, otherwise create, then prompt either way. |

Delivery is a `session.prompt` (or `promptAsync`) with `query.directory`, so a session in
`tools/opencode-workspace-mailbox` can start a turn in `globex/scraper-service` without any terminal
being attached. The prompt carries the topic and the absolute mailbox path.

**How the target session is handled:**

- `reuse`/`auto` pick the most recently updated session whose `directory` matches the recipient's
  directory — that is how you keep one long-running session instead of accumulating new ones.
- `spawn` always creates a new session record. Use it only when you deliberately want a clean
  context; `auto` is the practical default.
- The delivered session runs **headless**: a server-side turn with no UI. You can open it later from
  that project's session list, but nothing pops up on screen.
- Nothing is killed afterwards. The session stays as a record (idle), and `reuse`/`auto` will pick
  it up next time; `spawn` will not.
- A headless session that hits a permission prompt has nobody to answer it, so it can stall there.

**Directory resolution**, in order:

1. `projectDirs[recipient]`, if configured.
2. `workspace` → this tier's own root directory.
3. An account name → that account's directory under the workspace root.
4. A sibling of the mailbox directory, or a bounded search for a nested bucket
   (`<account>/tools/<repo>`).

If nothing resolves, the send still succeeds and the tool reports why no delivery happened. It never
guesses a directory.

## Scale and retention

The file backend re-reads and re-parses one mailbox file per trigger — but only when the file
changed. A mtime+size fingerprint short-circuits the parse, so an idle mailbox costs one `stat`.
Measured on this workspace: a **110 KB** mailbox with 59 messages takes **0.67 ms** to parse; the
cost is linear, and append-only files never shrink on their own.

`storage: "sqlite"` removes the file from the hot path entirely: indexed lookups for
`(project, status)`, an `INSERT` per message, WAL for concurrent sessions, and no parsing per tick.
With the mirror on, markdown still grows — but only agents and humans read it, once per handled
message, never on a timer.

Growth is now bounded by two explicit mechanisms:

1. **Retention** — `retentionDays` plus `mailbox_prune` move `DONE` messages older than the window
   out of the active mailbox. The file backend writes them to `<mailboxDir>/_archive/<project>.md`;
   the sqlite backend moves the rows to the `messages_archive` table. `OPEN` messages and recent
   `DONE` history stay.
2. **`since` watermark** — set an ISO date and everything older is ignored by the wake path, so a
   fresh install does not replay a mailbox's entire history on first contact.

Both are opt-in and safe to re-run (`mailbox_prune({ dryRun: true })` previews).

## Broadcast

The protocol's `to: all` is a real fan-out: the same block is appended to every project mailbox in
the tier, addressed `to: all`. Delivery is skipped for broadcasts — one message cannot decide which
session should wake — so each recipient picks it up on its own idle or wake tick. The sender records
the hash as its own write, so it is never prompted for its own broadcast.

## Limitations

- **A spawned session is not a terminal.** Delivery creates and prompts a server-side session; it
  does not open a TUI. A headless session blocked on a permission prompt has nobody to answer it.
- **SQLite needs a driver**: `bun:sqlite` under OpenCode, or `node:sqlite` on Node ≥ 22.5. The
  plugin reports a clear error instead of silently falling back to files.
- **Retention rewrites the active file.** It is the one operation that is not append-only — the
  moved messages are preserved verbatim in `_archive/` (or the archive table) precisely so the
  audit trail survives.
- **Delivery needs a resolvable directory.** If the recipient's project folder cannot be found, the
  message is written and the tool reports why nothing was delivered.
- **One project per plugin instance.** Identity is resolved per session, never shared.
- **`wake` spends tokens with nobody watching**, at the pace messages arrive. Leave it off for
  idle-only delivery.
- **No migration of old layouts.** Pointing the plugin at a mailbox directory that still holds
  pre-hierarchy files leaves them in place; account files appear alongside.
- **Busy detection is event-driven.** If a runtime never emits `session.status`, the wake path can
  queue a prompt behind an active turn instead of waiting.
- **Message bodies are data only.** They are never executed, evaluated, or turned into commands.
- **New recipient files are only registered in the tier's `README.md` when
  `registerRecipients: true`.** Off by default, because the plugin writes mailboxes and the tier
  README is documentation. When on, it inserts one row into the existing `## Files` table, never
  creates the README, and never rewrites a row.

---

## Backlog

Ideas for the future — not implemented yet.

- **Engram backend** — reuse the persistent-memory store for teams that want mailboxes outside the
  repo. Same interface.
- **Scheduled retention** — run the prune pass on a timer instead of on demand.
- **Migration helper for legacy layouts** — move pre-hierarchy top-level files into the tier layout
  with an explicit, reviewable command instead of leaving them behind.

---

## Development

```bash
npm install
npm test          # vitest: parser, ack byte-identity, send, paths, wake, spawn, tiers, store
npm run typecheck # tsc --noEmit
npm run build     # tsc -> dist/
```

## Author

- **Renzo S.** — [mr-wolf-rsh](https://github.com/mr-wolf-rsh/)

## Contributing

All sorts of suggestions and pull requests are welcome.

## License

[MIT](./LICENSE)
