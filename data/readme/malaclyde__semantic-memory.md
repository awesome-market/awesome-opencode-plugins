# Semantic Memory

A persistent memory backend for AI agents. Stores text chunks with vector embeddings for semantic search, FTS5 for keyword search, and a cross-encoder reranker for relevance fusion. Supports EAV metadata (scope, sources, memory type, etc.) and chunk-to-concept relationships.

Ships as:
- **TypeScript library** (`@malaclyde/knowledge-base`) — embed directly in Node.js agents
- **OpenCode plugins** — `coding-memory` and `assistant-memory` wrappers
- **Hermes Agent plugin** — MemoryProvider via Docker container (`plugins/memory/semantic-memory`)
- **Docker container** — REST API exposing the full memory backend

## Architecture

```
                   Hermes Agent
                  ┌─────────────────────┐
                  │  MemoryProvider     │
                  │  (Python plugin)    │
                  └──────┬──────────────┘
                         │ HTTP (localhost:3746)
                  ┌──────┴──────────────┐
                  │   Docker Container  │
                  │   Express REST API  │
                  └──────┬──────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    better-sqlite3    USearch     @huggingface/transformers
    (SQLite + FTS5)   (HNSW)      (embeddings + reranker)
```

## Quick Start

```typescript
import { Embedder, Reranker, CodingWrapper } from '@malaclyde/knowledge-base';

const embedder = new Embedder('Xenova/all-MiniLM-L6-v2', 384);
const reranker = new Reranker('Xenova/bge-reranker-base', 'Xenova/bge-reranker-base');
const memory = new CodingWrapper(embedder, reranker, { dbPath: './memory.db' });

// Store knowledge
await memory.store('Crawl4AI is an open-source LLM-friendly web crawler.', 
  [{ name: 'Crawl4AI', description: 'Web crawler framework' }],
  [], ['https://github.com/unclecode/crawl4ai']);

// Search with semantic + keyword + reranker fusion
const results = await memory.search('web crawler', 5);
// results[0] → { id, text, rerankerScore, sources }
```

## Core Concepts

### Chunks
The fundamental unit of memory. Each chunk has:
- **Text** — the stored content
- **Embedding** — vector for semantic search (auto-generated)
- **created_at** — timestamp (auto-set)
- **access_count** — retrieval counter (auto-incremented)
- **outdated** — soft-delete flag

### Concepts
Named entities that can be linked to multiple chunks. Each concept has a name and optional description. Concepts are searchable via FTS5 and vector embeddings.

### EAV Properties (Entity-Attribute-Value)
Flexible metadata attached to chunks. Properties are free-form name-value pairs stored in a separate table. Common properties used by tool wrappers:

| Property | Type | Used by | Purpose |
|----------|------|---------|---------|
| `scope` | string | CodingWrapper | Filter by project area (backend, frontend) |
| `sources` | JSON string | Both | Source URLs backing the fact |
| `memory_type` | `"working"` / `"archival"` | AssistantWrapper | Memory tier |
| `created_at` | ISO timestamp | Auto-set | Creation time |
| `access_count` | string (number) | Auto-incremented | Times retrieved |

## API Reference

### Low-Level DB (`src/kb/db.ts`)

| Method | Description |
|--------|-------------|
| `insertChunk(text, concepts?, existingConceptIds?, properties?)` | Store a chunk |
| `semanticSearch(text, limit)` | Pure vector search |
| `keywordSearch(text, limit)` | FTS5 keyword search |
| `combinedSearch(text, limit, filters?)` | Vector + FTS + reranker fusion |
| `conceptCombinedSearch(name, description?)` | Find concepts by name or description |
| `getChunksByIds(ids)` | Batch fetch chunks |
| `getChunksByProperty(name, value)` | Filter chunks by EAV property |
| `getConceptChunks(conceptId, maxLen?)` | Get linked chunks for a concept |
| `getConceptsByIds(ids)` | Batch fetch concepts |
| `setChunkProperties(id, props)` | Set EAV properties |
| `getChunkProperties(id)` | Get all EAV properties |
| `deleteChunkProperty(id, name)` | Remove a property |
| `setChunkOutdated(id)` | Soft-delete a chunk |
| `editConcept(id, name, desc)` | Update a concept |
| `mergeChunks(sourceIds, targetText)` | Consolidate chunks |

### Wrappers

**BaseWrapper** — safe core API for any agent:
`search`, `store`, `getChunks`, `getPreviews`, `findConcept`, `setOutdated`, `editConcept`, `setProps`, `getProps`, `delProp`, `merge`

**CodingWrapper** — extends BaseWrapper, adds `scope` filtering and `sources` tracking. The `store()` method accepts an optional `sources` parameter.

**AssistantWrapper** — extends BaseWrapper, adds `memory_type` filtering. The `store()` method accepts optional `sources` and `memoryType` parameters. Also provides `promoteToWorking(id)` and `demoteToArchival(id)`.

### SearchOptions

All wrappers accept a `SearchOptions` object on `search()`:

```typescript
interface SearchOptions {
  filters?: { propertyName: string; value: string; required: boolean }[];
  scope?: string;       // CodingWrapper: filter by scope
  memoryType?: string;   // AssistantWrapper: filter by memory type
}
```

## Database Schema

The library uses SQLite with the following tables:

- **chunks** — text storage with native `created_at`, `access_count`, `outdated` columns
- **concepts** — named entities with name/description
- **edges** — many-to-many chunk↔concept links
- **properties** — EAV property name registry
- **chunk_properties** — EAV values linked to chunks
- **chunks_fts** — FTS5 full-text index on chunk text
- **concepts_fts** — FTS5 index on concept name + description

## OpenCode Plugins

This library is distributed with two OpenCode plugins:

- **@malaclyde/coding-memory-oc** — memory tools for coding agents (`opencode/coding-memory/`)
- **@malaclyde/assistant-memory-oc** — memory tools for personal assistant agents (`opencode/assistant-memory/`)

See their respective README files for usage and configuration.

## Hermes Agent Plugin

A Hermes Agent memory provider plugin is available at `hermes/`. It wraps the TypeScript backend in a Docker container and exposes it as a `MemoryProvider` plugin.

### Quick Start

```bash
# 1. Start the Docker container
cd docker && docker compose up -d

# 2. Symlink the plugin
ln -sf $(pwd)/hermes ~/.hermes/plugins/semantic-memory

# 3. Enable in Hermes
hermes plugins enable semantic-memory
hermes config set memory.provider semantic-memory

# 4. Verify
hermes memory status
```

### Tools

The plugin exposes 7 tools to the Hermes agent:

| Tool | Description |
|------|-------------|
| `search_memory` | Cross-session semantic search with scope and memory type filters |
| `store_memory` | Persist facts with concept tags, sources, scope, and memory tier |
| `find_concept` | Look up existing concept tags by name or description |
| `get_chunks` | Retrieve full chunk text and metadata by ID |
| `merge_memories` | Consolidate related fragments into a single entry |
| `unlink_concept` | Detach an incorrectly linked concept from a chunk |
| `set_outdated` | Mark obsolete information before storing corrections |

### Lifecycle Integration

| Hermes Hook | Semantic Memory Behavior |
|---|---|
| `system_prompt_block()` | Injects top-10 important chunks with recency/access-frequency heuristic |
| `prefetch(query)` | Splits user message into 200-char chunks, semantic search, returns `<memory-context>` block |
| `on_turn_start()` | Every N turns (default 10), background review for new facts |
| `on_memory_write()` | Captures offloaded MEMORY.md content as archival memory |
| `on_session_end()` | Extracts important facts from conversation history |

### Docker Container

The container exposes a REST API on port 3746 with endpoints for all memory operations:

```
GET  /health              → Health check
POST /store               → Store a memory chunk
POST /search              → Semantic + FTS + reranker search
POST /get-chunks          → Retrieve chunks by ID
POST /find-concept        → Search concepts
POST /set-outdated        → Soft-delete a chunk
POST /unlink-concept      → Detach concept from chunk
POST /edit-concept        → Update concept metadata
POST /important-chunks    → Top N chunks by recency + access frequency
POST /merge               → Consolidate multiple chunks
```

See `docker/API.md` for the full request/response schemas.

## Testing

```bash
npm test                # Run all 109 tests
npm run test:watch      # Watch mode
npm run seed            # Populate test DB with sample data
```

## License

MIT
