<p align="center">
  <img src="./banner.png" alt="cloudflare-d1-best-practices-skill" width="100%" />
</p>

# Cloudflare D1 Best Practices Skill (`cloudflare-d1-best-practices-skill`)

An autonomous AI agent skill (compatible with Claude Code, Cursor, Windsurf, and Agent Skills runtimes) providing production-grade engineering rules, self-explaining schema patterns, and self-verification guardrails for **Cloudflare D1** and **SQLite on Cloudflare Workers**.

Inspired by `supabase-postgres-best-practices` and tailored to D1's single-writer Durable Object architecture, global read replication (`withSession`), and `rows_read` billing physics.

## Why This Skill

Cloudflare D1 looks like SQLite, but running SQLite at the edge comes with its own rules: a single writer, a 100-parameter bind limit, Worker subrequest quotas, `SQLITE_BUSY` under load, free-tier daily row caps, and read replicas that can return stale data unless sessions are used correctly. Most AI-generated D1 code breaks on one of these details.

This skill packages those rules into a form an AI agent can apply consistently. It helps the agent understand D1 structurally — not just syntax, but why a schema, index, transaction, or replication strategy should be shaped a certain way. The result is fewer broken migrations, fewer slow queries, and less time spent debugging database behavior.

## Key Capabilities & Design Philosophy

1. **100% Stack-Neutral Core + Thin Adapters:**
   All core DDL, indexing, batching, and consistency rules are authored against standard SQLite and the native Cloudflare D1 Binding API (`env.DB`). Framework- and ORM-specific integrations (Drizzle ORM, Kysely, Prisma, Hono, Remix, Next.js OpenNext, Astro) are cleanly isolated in `references/framework-and-orm-adapters.md`.
2. **Progressive Disclosure for Low Token Overhead:**
   Instead of splitting rules across 20+ fragmented files or dumping everything into context at once, `SKILL.md` acts as a high-density routing table that directs the agent to load **only** the relevant domain reference file out of 6 cohesive modules.
3. **Pragmatic Escape Hatches:**
   Enforces strong defaults (`STRICT` tables, time-ordered IDs, `db.batch()`) while explicitly documenting when to deviate (`ANY` type for dynamic attributes, `INTEGER PRIMARY KEY` for FTS5 and high-volume logs, `WITHOUT ROWID` for junction/lookup tables, and Free-plan `ctx.waitUntil` alternatives to Cloudflare Queues).
4. **Mandatory Autonomous Verification Gate:**
   Requires agents to apply migrations against `--local` and verify every non-trivial query with `EXPLAIN QUERY PLAN` (`SCAN` detection and `PRAGMA optimize` auto-remediation) before completing a task.

## In Practice: Where This Skill Helps

I use this skill in my own client work, and these are the situations where it makes the biggest difference:

- **Starting a new app or SaaS**: schema design, `STRICT` tables, primary-key strategy, and the first Wrangler migrations are generated with D1's constraints already accounted for.
- **Adding a database to an existing website**: reviews existing SQL and catches N+1 queries, missing indexes, `SELECT *`, and offset pagination before they reach production.
- **Building APIs with your preferred stack**: works with the native `env.DB` binding, Drizzle ORM, Kysely, Prisma, Hono, Remix, Next.js (OpenNext), and Astro.
- **Handling writes under load**: chunks bulk inserts around the 100-parameter limit, replaces interactive transactions with `db.batch()`, adds retry/backoff for transient errors, and offloads heavy writes when needed.
- **Operating in production**: guides migrations, chunked data backfills, Time Travel recovery, `wrangler d1 insights` diagnostics, and 10 GB-scale sharding.
- **Reviewing AI-generated database code**: gives the model a checklist to verify its own output instead of relying on trial and error.

## Repository Structure

```text
cloudflare-d1-best-practices-skill/
├── SKILL.md                                           # Trigger metadata, core invariants & progressive disclosure router
├── README.md                                          # Repository overview & installation guide
├── banner.png                                         # Repository banner
└── references/
    ├── schema-design-and-types.md                     # Zero-peek DDL, STRICT + ANY, PK selection, WITHOUT ROWID, JSON virtual columns
    ├── query-performance-and-indexing.md              # ESR composite/covering/partial indexes, keyset pagination, FTS5, KV/Cache API
    ├── transactions-batching-and-retries.md           # Atomic db.batch(), 100-param chunking, idempotent write retries, tiered write scaling
    ├── read-replication-and-sessions.md               # Global read replication, withSession() routing hints, x-d1-bookmark propagation
    ├── migrations-verification-and-scale.md           # EXPLAIN QUERY PLAN gate, 1,000-row chunked migrations, wrangler d1 insights, 10GB sharding
    └── framework-and-orm-adapters.md                  # Adapters for Drizzle, Kysely, Prisma, Hono, Remix, Next.js (OpenNext), and Astro
```

## Installation

### Agent Skills CLI / Claude Code
```bash
npx skills add nozomicreative/cloudflare-d1-best-practices-skill
```

### Cursor / Windsurf / Manual Setup
Copy `SKILL.md` and the `references/` directory into `.claude/skills/cloudflare-d1-best-practices-skill/` or `.cursor/rules/cloudflare-d1-best-practices-skill/`.

---

<a id="japanese"></a>
## 🇯🇵 日本語

### このスキルについて

Cloudflare D1 は手軽に始められますが、エッジ環境ならではのクセがあります。シングルライターの SQLite、1クエリ100個までのバインドパラメータ、Worker のサブリクエスト上限、Free プランの日次 row 上限、読み取りレプリカの整合性、`SQLITE_BUSY` への対応など、通常の PostgreSQL と同じ感覚で設計すると本番でつまずきやすいポイントです。

このスキルは、**AI が Cloudflare D1 をより構造的に理解し、あなたの開発がもっと便利になる**ように作られています。スキーマ、クエリ、トランザクション、レプリケーション、マイグレーション、フレームワーク連携のルールを6つの凝集したリファレンスに整理し、AI エージェントが必要なファイルだけを読み込める構成にしています。

### 実際の開発で役に立つ場面

私自身、Web サイトやアプリの開発で D1 が必要なときにこのスキルを活用しています。特に次のような場面で役立ちます。

- **新規アプリ・SaaS の立ち上げ**: D1 の制約を踏まえたスキーマ設計、STRICT テーブル、主キー戦略、Wrangler マイグレーションを最初から整えられます。
- **既存サイトへのデータベース追加**: N+1 クエリ、インデックス不足、`SELECT *`、OFFSET ページネーションなど、本番前にパフォーマンス上の問題を潰せます。
- **API 開発**: Hono、Remix、Next.js (OpenNext)、Astro に加え、Drizzle ORM、Kysely、Prisma など、採用しているスタックに合わせて D1 を組み込めます。
- **書き込みが多いサービスの運用**: 100パラメータ制限を考慮したバルクインサート、`db.batch()` によるトランザクション、`SQLITE_BUSY` のリトライ、Free プラン向けの `ctx.waitUntil()` 退避を適切に設計できます。
- **本番運用・保守**: マイグレーション、大量データの分割更新、Time Travel による復旧、`wrangler d1 insights` によるボトルネック特定、10GB 上限を見据えたシャーディングまでカバーします。
- **AI が生成した DB コードのレビュー**: `EXPLAIN QUERY PLAN` の合否基準と自動修復ループにより、モデル自身が出力を検証できます。

---

## 👤 About the Creator

This skill is maintained by **[Nozomi Creative](https://nozomicreative.com)**, a creative engineering studio specializing in bespoke web production, high-conversion landing pages, brand identity systems, and AI-integrated digital workflows.

I built this skill from the database patterns I use in client projects. When a website or application needs Cloudflare D1, this is the workflow I reach for — and I hope it makes your D1 development smoother too.

🌐 **Website**: [https://nozomicreative.com](https://nozomicreative.com)

### 企画・開発について

このスキルは、Web 制作・UI/UX デザイン・デジタルクリエイティブを手がける **[Nozomi Creative（のぞみクリエイティブ）](https://nozomicreative.com)** が、実際の開発で培った知見をもとに公開しています。

Web サイトやアプリの制作で Cloudflare D1 が必要なとき、私はいつもこのスキルを活用しています。同じように D1 を使う開発者の手助けになれば嬉しいです。

🌐 **Web サイト**: [https://nozomicreative.com](https://nozomicreative.com)  
✉️ **お問い合わせ**: [https://nozomicreative.com#contact](https://nozomicreative.com#contact)
