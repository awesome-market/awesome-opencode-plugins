# opencode-memsearch

Persistent cross-session memory for [OpenCode](https://opencode.ai), powered by [memsearch](https://github.com/nicobako/memsearch).

This plugin gives your OpenCode agent long-term memory. It automatically summarizes each conversation turn and stores it in a local vector database. On session start, recent context is injected into the system prompt, and the agent can search all past memories with semantic search.

## Features

- **Automatic memory capture** — each conversation turn is summarized by an LLM and appended to daily Markdown files in a [memory store](#storage) that you can [sync across machines](#syncing-across-machines)
- **Cold-start context** — the last 30 lines of the 2 most recent memory files are injected into the system prompt when a new session starts
- **Semantic search** — two custom tools (`memsearch_search` and `memsearch_expand`) let the agent search and drill into past memories
- **Per-project isolation** — memory collections are scoped by project directory
- **Local embeddings** — works with memsearch's ONNX or local embedding providers, so no API keys are needed for vector search
- **Fast search** — a shared background [daemon](#daemon) keeps the embedding model loaded
- **Memory protocol** — a system prompt directive instructs the agent to check memory at session start and whenever it encounters a topic that might have prior context

## Prerequisites

You need the `memsearch` CLI installed with ONNX embeddings. The easiest way is via [uv](https://docs.astral.sh/uv/):

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install memsearch with ONNX embeddings (recommended)
uv tool install 'memsearch[onnx]'

# Configure the ONNX embedding provider
memsearch config set embedding.provider onnx
```

Or install directly with pip:

```bash
pip install 'memsearch[onnx]'
memsearch config set embedding.provider onnx
```

The ONNX provider uses the `bge-m3` embedding model locally on your machine — no API keys or network requests needed for vector search. If you prefer a different embedding provider (e.g., OpenAI, a local `all-MiniLM-L6-v2` via `memsearch[local]`, or Ollama), see the [memsearch documentation](https://github.com/nicobako/memsearch) for configuration options.

If `memsearch` is not installed, the plugin's tools will return a clear error message asking the agent to tell you to install it.

## Install

Requires OpenCode 2.0.29 or later. Add `opencode-memsearch` to `plugins` in your OpenCode 2 config:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["opencode-memsearch"]
}
```

This can go in either:
- `opencode.json` in your project root (project-level)
- `~/.config/opencode/opencode.json` (global)

OpenCode will install the npm package automatically on startup.

### Using OpenCode 1.x

`opencode-memsearch@0.6.0` is the last V1-compatible release, also available at the `v1` git tag. Use the V1 config key when pinning it:

```json
{
  "plugin": ["opencode-memsearch@0.6.0"]
}
```

## How it works

### Memory capture

After a successful top-level session execution (`session.execution.succeeded`), the plugin:

1. Reads the completed turn through the V2 service, including user messages, assistant text, tool inputs, results, and errors. Idle markers bound each turn, including prompts added while the agent was working.
2. Summarizes it into 2-6 bullet points using a stateless in-process model call (Claude Haiku by default, [configurable](#summarization-model)). This creates no throwaway sessions and runs no session hooks.
3. Appends the summary to `YYYY-MM-DD.md` in this machine's folder for the project (see [Storage](#storage))
4. Re-indexes the project's memory into the vector database

Summaries are written in third person (e.g. "User asked about...", "Agent edited file X...") and include specific file names, function names, and outcomes.

Child/subagent sessions, failed or interrupted executions, and prompts shorter than 10 characters are skipped. Capture is best-effort; if generation fails or returns no usable notes, the plugin stores a concise transcript extract. Each directory's plugin instance handles only sessions in that directory.

Live capture requires the shared OpenCode service, which normal V2 clients use by default. Standalone servers are not supported for transcript capture.

### Memory recall

On session start, the plugin:

1. Reads the tail of the 2 most recent memory files, from any machine, and injects them into the system prompt as `<memsearch-context>`
2. Adds a MEMORY PROTOCOL to the system prompt instructing the agent to use `memsearch_search` at session start and whenever relevant

The agent can also search memories on demand:

- **`memsearch_search`** — semantic search across all past memory chunks. Returns ranked results with content previews and chunk hashes.
- **`memsearch_expand`** — expand a specific chunk to see full context, source file location, and session IDs for deeper investigation.

Both tools are exposed through V2 Code Mode. Use the catalog (or search discovery) to find their exact paths, then call them inside `execute`:

```js
const memory = await tools.memsearch_search({ query: "previous deployment decision" })
if (memory.error) return memory.content
return memory.results
```

The catalog paths are `tools.memsearch_search` and `tools.memsearch_expand`. They are not direct model tools. Search returns `{results, content, error?}`; expand returns `{result?, sessionIDs, machine?, local?, content, error?}`. `local` is false when the memory came from another machine, whose sessions don't exist locally. The `content` field preserves the text notes and expansion guidance, while the structured fields let code select results and pass a `chunk_hash` into expand.

### Storage

Memory lives in a store outside your projects, by default `$XDG_DATA_HOME/opencode-memsearch` (`~/.local/share/opencode-memsearch`):

```
opencode-memsearch/
  projects/
    opencode-memsearch-f58003ab60be/   # one folder per project
      laptop-3f9a2c/                   # one folder per machine
        2026-11-12.md                  # daily memory summaries
        2026-11-11.md
      desktop-81be07/
        2026-11-10.md
```

The project folder name is the same on every machine and in every clone:

1. `project_id` from `.memsearch/config.json` in the opened folder or the repo root, if set. Commit that file, or copy it to every machine, for it to apply everywhere.
2. Otherwise, for a git repo, the `origin` remote, ignoring protocol and a `.git` suffix. The hash is the start of OpenCode's project ID. Worktrees and subfolders of a repo share its memory.
3. Otherwise, for a git repo with no `origin`, its root commit
4. Otherwise the folder's path, which only matches on the same machine

The machine folder name is generated once from the hostname and saved in `$XDG_STATE_HOME/opencode-memsearch/machine.json` (`~/.local/state/...`). Each machine only writes to its own folder.

Older versions kept memory in each project's `.memsearch/memory/`. The plugin, `seed` and `reindex` move those files into this machine's folder for the project the first time they see the project. When two folders have files for the same day, the second is renamed to `YYYY-MM-DD.legacy-<hash>.md`.

### Syncing across machines

To share memory between machines, set `store_dir` in the global config to a folder that a file sync tool such as Syncthing, Dropbox or iCloud Drive keeps in sync:

```json
{
  "store_dir": "~/Dropbox/opencode-memsearch"
}
```

Each machine only writes its own files and only appends to them, so syncing never causes conflicts. Each machine builds its own search index from the synced files. Before each search, the plugin checks whether any memory file has changed and re-indexes if so.

Memories recorded on another machine refer to sessions that only exist there. `memsearch_expand` says so, and the notes themselves are all that's available.

Memory notes can contain anything discussed in a session, including code, file contents and secrets. Syncing sends them to wherever your sync tool stores data.

## CLI

The package includes a CLI for utility tasks. It requires [Bun](https://bun.sh/) and OpenCode 2 on PATH. The CLI discovers the shared service and runs `opencode service start` if needed, so service configuration and its environment apply.

```bash
bunx opencode-memsearch --help
```

### Seed

Backfill memory from existing OpenCode sessions. This is useful when first installing the plugin on a project you've already been working on.

```bash
# Seed from the last 14 days of sessions (default)
bunx opencode-memsearch seed

# Seed from the last 30 days
bunx opencode-memsearch seed --days 30
```

The command lists sessions and reads paginated message history through `@opencode/client`, across all projects. It summarizes successful completed turns through the service's stateless generate endpoint and writes results to each project's folder in the [memory store](#storage), moving any memory left in `.memsearch/memory/` first. It can be run from anywhere. It skips existing turn anchors and respects the same [configuration](#configuration) as the plugin. It does not read OpenCode's database directly.

### Reindex

```bash
bunx opencode-memsearch reindex --dry-run
bunx opencode-memsearch reindex
```

Reindex first moves memory left in the `.memsearch/memory/` folders of known session directories into the store. It then resets the memory collection of every project in the [memory store](#storage) and indexes existing Markdown files using the current embedding configuration. It restarts the shared Python daemon so embedding changes take effect. It does not regenerate summaries.

## Configuration

The plugin can be configured via a JSON config file and/or environment variables. Environment variables take precedence over config file values, and project-level config takes precedence over global config.

### Config file

The plugin looks for config in two locations (highest precedence first):

1. **Project config**: `.memsearch/config.json` in your project root
2. **Global config**: `$XDG_CONFIG_HOME/opencode/memsearch.config.json` (defaults to `~/.config/opencode/memsearch.config.json`)

Both files use the same schema. Values from the project config override the global config, except as noted below.

**Example:**

```json
{
  "summarization_model": "anthropic/claude-sonnet-4-5"
}
```

All fields are optional. The full schema:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `summarization_model` | `string` | `"anthropic/claude-haiku-4-5"` | The OpenCode model ID used to summarize conversation turns |
| `store_dir` | `string` | `~/.local/share/opencode-memsearch` | Where memory is stored. Global config only. See [Syncing across machines](#syncing-across-machines). |
| `project_id` | `string` | derived from git | Names the project's folder in the store. Project config only. Set it to share memory between projects that don't share a git remote. |

### Summarization model

Each conversation turn is summarized by an LLM before being stored. By default, the plugin uses `anthropic/claude-haiku-4-5` — a fast, cheap model that produces good summaries.

To use a different model, set it in your config file:

```json
{
  "summarization_model": "anthropic/claude-sonnet-4-5"
}
```

Or override it with an environment variable:

```bash
export MEMSEARCH_SUMMARIZATION_MODEL="openai/gpt-4.1-mini"
```

The model must be configured and authenticated in OpenCode. Use `provider/model` or `provider/model#variant`. Live capture uses the directory's model configuration; the seed command's service generate endpoint uses the global configuration, so seed models must be available globally. Neither path creates a session or launches `opencode run`.

### Milvus storage

The plugin uses [Milvus](https://milvus.io/) (via memsearch) as its vector database. There are two modes:

#### Local mode (default)

By default, memsearch uses **Milvus Lite**, which stores data in a local `.db` file (typically `~/.memsearch/milvus.db`). This requires no server setup.

#### Remote mode

You can point memsearch at a Milvus server:

```bash
memsearch config set milvus.uri http://localhost:19530
```

To switch back to local mode:

```bash
memsearch config set milvus.uri "~/.memsearch/milvus.db"
```

Don't share one Milvus server between machines. Each project's collection has the same name on every machine, and each machine's index drops chunks from files it can't see. To share memory, [sync the store](#syncing-across-machines) instead.

### Daemon

All database access goes through one background daemon shared by every OpenCode session and project on the machine. Milvus Lite allows only one process to open its database, and the daemon also keeps the embedding model loaded, so searches take milliseconds instead of several seconds.

The plugin starts the daemon on first use and replaces it if it is from an incompatible plugin version. It keeps running after OpenCode exits. Its files live in `~/.memsearch/daemon/`:

- `daemon.sock` — the Unix socket the plugin connects to
- `daemon.pid` — the daemon's PID, locked while it runs so only one daemon can start
- `daemon.log` — startup errors and indexing failures

The daemon reads memsearch's global config (`~/.memsearch/config.toml`). Project-level `.memsearch.toml` files are not used.

The `seed` and `reindex` commands also index through the daemon. `reindex` restarts it first so it picks up changes to the embedding config.

In local mode, the `memsearch` CLI can't open the database while the daemon is running. To use the CLI directly, stop the daemon first:

```bash
pkill -f memsearch-daemon.py
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `MEMSEARCH_SUMMARIZATION_MODEL` | Override the model used for summarization (takes precedence over config file) |
| `MEMSEARCH_STORE_DIR` | Override `store_dir` |

Set `MEMSEARCH_SUMMARIZATION_MODEL` in the service's environment (`service.json` → `env`) when running the shared background service. The CLI also reads it from its own environment. `MEMSEARCH_DISABLE` is no longer needed: stateless generation cannot trigger memory capture.

### Precedence

Configuration values are resolved in this order (highest precedence first):

1. Environment variables
2. Project config (`.memsearch/config.json`)
3. Global config (`~/.config/opencode/memsearch.config.json`)
4. Built-in defaults

## License

MIT
