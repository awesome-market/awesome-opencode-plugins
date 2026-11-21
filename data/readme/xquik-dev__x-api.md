# X API Pricing & X API Alternative by Xquik

[![Framer builds a tweet ticker with Xquik](https://img.youtube.com/vi/4UOSpoOoC3Y/maxresdefault.jpg)](https://youtu.be/4UOSpoOoC3Y?t=367)\
[Watch Framer build a tweet ticker with Xquik, from 6:07](https://youtu.be/4UOSpoOoC3Y?t=367).
This skill helps your agent move X API code to Xquik.

Use this X API alternative skill by Xquik to replace official X API pricing.
It is also an X (Twitter) API alternative for code on API v2.

Xquik is the world's fastest and cheapest X (Twitter) scraper service with the most complete X (Twitter) data.
Most other Apify Actors charge before filtering or deduplication.
Xquik charges only for delivered, unique, filter-matching results and never pads rows.
Xquik is independent and not affiliated with X Corp.

<!-- trust:win:start -->

The Xquik REST API read 45 tweets per second on 2026-10-15. That cost $0.15 per 1,000. The fastest of 4 rival Actors read 12.5 per second. The cheapest cost $0.173 per 1,000. [Compare each run](https://xquik.com/benchmarks#benchmark-x-tweet-scraper).

<!-- trust:win:end -->

## Install the X API alternative skill

```bash
npx skills@1.7.0 add Xquik-dev/x-api
```

The skill works in Claude Code, Codex, Cursor & other Agent Skills readers.
Create an API key in the [Xquik dashboard](https://dashboard.xquik.com/en/account?tab=api-keys).
Then set it in your shell.

```bash
export XQUIK_API_KEY='<your key>'
```

## Pay per use X API pricing for tweet search

Each tweet or post costs $0.00015, so this call for 10 tweets costs $0.0015.

```bash
curl -s "https://xquik.com/api/v1/x/tweets/search?q=from:elonmusk&limit=10" \
  -H "x-api-key: $XQUIK_API_KEY"
```

Next, read the [X API comparison](https://docs.xquik.com/alternatives/x-api) or the [billing guide](https://docs.xquik.com/guides/billing).

<!-- trust:start -->

## Benchmarks & usage

[![X (Twitter) Skill installs](https://img.shields.io/endpoint?url=https%3A%2F%2Fxquik.com%2Fbadges%2Fskill-installs.json)](https://xquik.com/benchmarks#skill-installs)
[![X (Twitter) API p99 server read time](https://img.shields.io/endpoint?url=https%3A%2F%2Fxquik.com%2Fbadges%2Frest-p99.json)](https://xquik.com/benchmarks#speed)
[![X (Twitter) API package downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fxquik.com%2Fbadges%2Fdownloads.json)](https://xquik.com/benchmarks#downloads)

- 1,600+ installs of Xquik's X (Twitter) Skills on skills.sh ([source](https://xquik.com/benchmarks#skill-installs)) <!-- trust:skill-installs 1636 -->
- 4.9 s p99 REST server read time over 7 days, failures included ([source](https://xquik.com/benchmarks#speed)) <!-- trust:rest-p99 4871 -->
- 64,000+ downloads of Xquik's X (Twitter) API packages across 6 registries ([source](https://xquik.com/benchmarks#downloads)) <!-- trust:downloads 64497 -->

Checked on 2026-11-09. See each number with its date & source on [xquik.com/benchmarks](https://xquik.com/benchmarks) or as [JSON](https://xquik.com/trust.json).

<!-- trust:end -->

## Cut X (Twitter) API cost when you leave tweepy

This tweepy call reads from the official X API at $0.005 per tweet.

```python
client.search_recent_tweets(query="from:elonmusk", max_results=10)
```

The skill rewrites it as an Xquik call at $0.00015 per tweet.

```python
import os
import requests

response = requests.get(
    "https://xquik.com/api/v1/x/tweets/search",
    params={"q": "from:elonmusk", "limit": 10},
    headers={"x-api-key": os.environ["XQUIK_API_KEY"]},
    timeout=30,
)
tweets = response.json()["tweets"]
```

## Why Xquik is the cheapest X API alternative

A tweet or a profile costs $0.00015 on Xquik.
You pay only for delivered results.
Filters apply before billing, so excluded rows cost nothing.

| What you read or do | Xquik | Official X API on 2026-10-05 |
| --- | --- | --- |
| 1 tweet read | $0.00015 | $0.005 |
| 1 profile read | $0.00015 | $0.010 |
| 1 follower or following profile | $0.00015 | $0.010 |
| 1 text tweet created | $0.0045 | $0.015, or $0.200 with a URL |
| 1 trends call | $0.00045 | $0.010 |

The official prices come from the [X (Twitter) pricing page](https://docs.x.com/x-api/getting-started/pricing), read on 2026-10-05.
X (Twitter) names these units `Posts: Read`, `User: Read`, `Following/Followers: Read`, `Post: Create` & Trends.
Check that page for today's prices.

On that date, a tweet read cost 33 times less on Xquik.

## Why Xquik is the fastest X API alternative

- Reads need 1 API key. You need no X (Twitter) developer account.
- Each account gets 500 reads per second.
- Monitors check every second & push signed webhooks.
- Tweets & posts arrive with the author inline, so you drop `expansions`.
- Search accepts `query`, `max_results` & `sort_order` as aliases.

## Tasks to give your agent

```text
Move our recent search job from the official X API to Xquik.
Port this tweepy client to an X API alternative.
Replace our filtered stream with Xquik monitors & a webhook receiver.
What will 50,000 follower reads a day cost on Xquik?
```

## What the skill writes

| Job | What you get |
| --- | --- |
| Endpoint map | Each official X API v2 call matched to its Xquik endpoint & field names |
| Auth | A client that reads `XQUIK_API_KEY` from the environment |
| Pagination | A cursor loop with a page count, so cost has a ceiling |
| Errors & retries | Backoff on `429` & `5xx`, and no retry on `4xx` |
| Writes | An `Idempotency-Key` on each write & status polling |
| Monitors & webhooks | Setup code & an HMAC-SHA256 signature verifier |
| Cost estimate | Rows, credits & dollars before a loop or a monitor runs |

## Official X API v2 to Xquik

| Official X API v2 | Xquik |
| --- | --- |
| `https://api.x.com/2` with `Authorization: Bearer` | `https://xquik.com/api/v1` with `x-api-key` |
| `GET /2/tweets/search/recent` | `GET /x/tweets/search` |
| `GET /2/tweets/:id` | `GET /x/tweets/{id}` |
| `GET /2/users/by/username/:username` | `GET /x/users/{id}` |
| `GET /2/users/:id/tweets` | `GET /x/users/{id}/tweets` |
| `GET /2/users/:id/followers` | `GET /x/users/{id}/followers` |
| `POST /2/tweets` | `POST /x/tweets` |
| `GET /2/tweets/search/stream` | `POST /monitors/keywords` & `POST /webhooks` |
| `meta.next_token` | `next_cursor` |

The [endpoint map](skills/x-api/references/endpoint-map.md) lists every call.

## What the skill never does

- It never reads, prints or asks for your API key. Code reads it from the environment.
- It never loads tweets, bios or messages into the agent's conversation. That data goes to your application.
- It never sends a tweet, creates a monitor or buys credits. It writes the code & you run it.
- It never fetches remote instructions or installs packages. The whole contract ships in the skill.

To read X (Twitter) data inside an agent, use the [x-twitter-scraper skill](https://github.com/Xquik-dev/x-twitter-scraper).

## Files

| Path | Holds |
| --- | --- |
| `skills/x-api/SKILL.md` | The contract & the order of work |
| `skills/x-api/references/` | The endpoint map, 2 clients, monitors & webhooks, and pricing |
| `evals/x-api/` | Output evals, trigger queries & `claude plugin eval` cases, kept outside the skill folder |

## Questions

### Do I need an X (Twitter) developer account?

No. Public reads need only an Xquik API key.
Private reads & X (Twitter) account actions need a connected account.

### Is Xquik the official X API?

No. Xquik runs its own REST API.
Code you port with this skill calls that API, not the official X API.

## More Xquik tools

- [X (Twitter) scraper API & X (Twitter) MCP server](https://github.com/Xquik-dev/x-twitter-scraper) with REST, MCP & Skill setup.
- X (Twitter) API SDKs for [TypeScript](https://github.com/Xquik-dev/x-twitter-scraper-typescript), [Python](https://github.com/Xquik-dev/x-twitter-scraper-python), [Go](https://github.com/Xquik-dev/x-twitter-scraper-go) & [Ruby](https://github.com/Xquik-dev/x-twitter-scraper-ruby).
- X (Twitter) API SDKs for [Java](https://github.com/Xquik-dev/x-twitter-scraper-java), [Kotlin](https://github.com/Xquik-dev/x-twitter-scraper-kotlin), [C#](https://github.com/Xquik-dev/x-twitter-scraper-csharp) & [PHP](https://github.com/Xquik-dev/x-twitter-scraper-php).
- [Twitter CLI & X CLI](https://github.com/Xquik-dev/x-twitter-scraper-cli) and [Twitter advanced search operators](https://github.com/Xquik-dev/x-twitter-advanced-search) with tested examples.
- Twitter agent plugins for [OpenClaw](https://github.com/Xquik-dev/tweetclaw) & [Hermes Agent](https://github.com/Xquik-dev/hermes-tweet).
- [X (Twitter) API documentation source](https://github.com/Xquik-dev/xquik-docs) with every public page.
- Twitter integrations for [n8n](https://github.com/Xquik-dev/n8n-nodes-xquik), [Prefect](https://github.com/Xquik-dev/prefect-xquik), [Haystack](https://github.com/Xquik-dev/xquik-haystack) & [Paperclip](https://github.com/Xquik-dev/paperclip-plugin-xquik).
- Twitter integrations for [Terraform](https://github.com/Xquik-dev/terraform-provider-x-twitter-scraper), [Convex](https://github.com/Xquik-dev/xquik-convex), [Supabase](https://github.com/Xquik-dev/xquik-supabase) & [Strapi](https://github.com/Xquik-dev/strapi-plugin-xquik).
- X (Twitter) MCP for [AI agents](https://github.com/Xquik-dev/xquik-mcp), [VS Code](https://github.com/Xquik-dev/xquik-vscode) & [Raycast](https://github.com/Xquik-dev/xquik-raycast).
- [Xquik X API & Twitter scraper](https://xquik.com) and the [X (Twitter) API documentation](https://docs.xquik.com/api-reference/overview).

## Help

- Email `support@xquik.com`.
- Read the [Xquik docs](https://docs.xquik.com).

## License

[MIT](LICENSE)

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.
