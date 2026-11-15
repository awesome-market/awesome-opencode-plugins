# HireSquire

[![PyPI version](https://img.shields.io/pypi/v/hiresquire.svg)](https://pypi.org/project/hiresquire/)
[![Python versions](https://img.shields.io/pypi/pyversions/hiresquire.svg)](https://pypi.org/project/hiresquire/)
[![CI](https://github.com/bp46/hiresquire/actions/workflows/ci.yml/badge.svg)](https://github.com/bp46/hiresquire/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Unified open-source Python package for **HireSquire** — AI-powered candidate screening, local resume parsing (`PDF`, `DOCX`, `TXT`, `MD`), personalized outreach emails, compliance/bias audits, credit management, and interview scheduling.

One install gives you **three agent-ready interfaces** backed by a single Pydantic v2 schema and resilient HTTP client:

| Surface | Entry Point | Best For |
|---------|-------------|----------|
| **Python SDK** | `from hiresquire import HireSquireClient` | Python apps, LangChain, AutoGen, CrewAI, custom workflows |
| **CLI** | `hiresquire` / `uvx hiresquire` | Shell agents (Claude Code, OpenClaw, Codex), CI/CD, `--json` pipelines |
| **MCP Server** | `hiresquire-mcp` / `hiresquire mcp` | Claude Desktop, Cursor, Windsurf, VS Code, any stdio MCP host |

> **Node.js / TypeScript CLI:** Prefer npm? Install [`hiresquire-cli`](https://www.npmjs.com/package/hiresquire-cli) (`npx hiresquire-cli`).

---

## Installation

```bash
pip install hiresquire
```

Or run zero-install with [`uvx`](https://docs.astral.sh/uv/):

```bash
uvx hiresquire whoami --json
uvx --from hiresquire hiresquire-mcp
```

`pypdf` and `python-docx` are **core dependencies** — PDF and DOCX parsing work out of the box with no extra flags.

---

## Authentication & Configuration

Set your API token (`sk_...` user token or `hs_...` spend-limited Agent API key):

```bash
export HIRESQUIRE_API_TOKEN="your_token_here"
```

Or persist it locally (written with mode `0600` to `~/.hiresquire/config.json`):

```bash
hiresquire init --token YOUR_API_TOKEN
```

| Environment Variable | Precedence | Description |
|----------------------|------------|-------------|
| `HIRESQUIRE_API_TOKEN` | Highest | API token or Agent API key (`hs_...`) |
| `HIRESQUIRE_BASE_URL` | Highest | API base URL (default: `https://hiresquireai.com/api/v1`) |
| `HIRESQUIRE_WEBHOOK_URL` | Highest | Default webhook URL for job completion events |

Precedence order: **environment variables > `~/.hiresquire/config.json` > defaults**.

---

## Quick Start

### 1. MCP Server (Claude Desktop, Cursor, VS Code)

Add to `claude_desktop_config.json` or `.mcp.json` using `uvx` (zero manual install):

```json
{
  "mcpServers": {
    "hiresquire": {
      "command": "uvx",
      "args": ["--from", "hiresquire", "hiresquire-mcp"],
      "env": {
        "HIRESQUIRE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Or if installed via `pip install hiresquire`:

```json
{
  "mcpServers": {
    "hiresquire": {
      "command": "hiresquire-mcp",
      "env": {
        "HIRESQUIRE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### 2. Python SDK

```python
from hiresquire import HireSquireClient

with HireSquireClient("YOUR_API_TOKEN") as client:
    # Free health check (no credits spent)
    me = client.whoami()
    print(me["credits"]["formatted_balance"])

    # Submit resumes (local PDF/DOCX/TXT/MD paths or pre-parsed dicts)
    job = client.jobs.create(
        title="Senior Python Developer",
        description="Looking for a backend engineer with 5+ years of Python, FastAPI, and PostgreSQL experience.",
        resumes=["./resumes/john_doe.pdf", "./resumes/jane_smith.docx"],
        leniency_level=6,  # 1 (lenient) to 10 (strict), default 5
    )

    # Poll until completed and fetch ranked candidates
    results = client.jobs.wait(job["job_id"])
    for c in results["candidates"]:
        print(f"{c['id']}: {c['name']} — {c['score']}/100 | {c['summary']}")

    # Generate an interview invite for the top candidate
    top = results["candidates"][0]
    email = client.emails.generate(
        job_id=job["job_id"],
        candidate_id=top["id"],
        email_type="invite",
        tone="professional",
    )
    print(email["subject"], email["body"])
```

### 3. CLI (`--json` ready for agents)

```bash
# Free token & balance check
hiresquire whoami --json

# Estimate credit cost before screening
hiresquire estimate --candidates 25 --json

# Submit resumes, poll until completion, and output JSON
hiresquire screen \
  --title "Senior Python Developer" \
  --description "Looking for a backend engineer with 5+ years of Python, FastAPI, and PostgreSQL experience." \
  --resumes ./resumes/ \
  --leniency 6 \
  --watch \
  --json

# Filter results by score or top N
hiresquire results --job 123 --min-score 80 --only-top-n 5 --json

# Generate outreach email
hiresquire email --job 123 --candidate 456 --type invite --tone friendly --json
```

---

## MCP Tools Reference (26 Tools)

All MCP tools run locally over `stdio` via FastMCP, extract resume text locally (never uploading raw binary files), and return structured JSON dicts (including `{"error": "...", "message": "..."}` on failure rather than crashing).

| Category | Tool | Key Parameters |
|----------|------|----------------|
| **Screening** | `create_screening` | `title`, `description` (≥50 chars), `resume_paths` or `resumes`, `leniency_level` (1–10), `custom_instructions`, `webhook_url` |
| | `get_screening_status` | `job_id` |
| | `get_results` | `job_id`, `min_score`, `only_top_n` |
| | `cancel_screening_job` | `job_id` |
| | `compare_candidates` | `job_id`, `candidate_ids` (list of ints) |
| | `report_hiring_outcome` | `job_id`, `candidate_id`, `outcome` (`hired` \| `rejected` \| `withdrawn`) |
| **Outreach** | `generate_email` | `job_id`, `candidate_id`, `email_type` (`invite` \| `rejection` \| `keep-warm` \| `followup`), `tone` (`professional` \| `friendly` \| `formal`), `custom_notes` |
| | `bulk_generate_emails` | `job_id`, `candidate_ids` (max 50), `email_type`, `tone` |
| **Credits** | `get_credit_balance` | — |
| | `estimate_screening_cost` | `candidate_count` (1–100) |
| | `list_credit_packs` | — |
| | `get_credit_transactions` | `limit`, `offset` |
| | `purchase_credits` | `amount` or `pack` (`pouch` \| `satchel` \| `chest`), `payment_method_id` |
| | `create_checkout_session` | `amount` or `pack` |
| | `enable_auto_reload` | `threshold`, `amount`, `payment_method_id` |
| | `disable_auto_reload` | — |
| **Calendar** | `list_calendar_connections` | — |
| | `create_calendar_connection` | `provider` (`calendly` \| `calcom`), `api_key`, `calendar_id` |
| | `get_available_slots` | `provider`, `date`, `duration` |
| | `create_interview` | `job_id`, `candidate_id`, `scheduled_at` (ISO 8601), `duration_minutes`, `provider` |
| | `generate_meeting_link` | `provider`, `topic`, `duration` |
| **Utilities** | `whoami` | — (free token/balance check) |
| | `get_rate_limit` | — |
| | `test_webhook` | `url` |
| | `get_api_schema` | — |
| | `audit_screening_job` | `job_id`, `selection_threshold` (default 70) |

---

## Python SDK Namespaces

`HireSquireClient` organizes the API into seven typed namespaces (all validated with Pydantic v2 models in [`hiresquire.models`](src/hiresquire/models.py)):

- **`client.jobs`**: `create()`, `create_from_zip()`, `list()`, `get_status()`, `get_results()`, `wait()`, `cancel()`, `compare()`, `report_outcome()`
- **`client.candidates`**: `get()`, `update_status()`
- **`client.emails`**: `generate()`, `bulk_generate()`, `generate_questions()`, `generate_icebreaker()`
- **`client.credits`**: `get_balance()`, `estimate_cost()`, `list_packs()`, `get_transactions()`, `purchase()`, `create_checkout_session()`, `create_payment_intent()`, `enable_auto_reload()`, `disable_auto_reload()`
- **`client.calendar`**: `list()`, `connect()`, `get_slots()`, `create_interview()`, `generate_meeting_link()`
- **`client.agent_keys`**: `list()`, `create()`, `get()`, `update()`, `revoke()`, `regenerate()`, `get_usage()`
- **`client.utils`**: `whoami()`, `get_rate_limit()`, `test_webhook()`, `get_api_schema()`, `audit_screening_job()`

---

## Schemas & Contracts (for Agents)

### Create Screening Job Request (`POST /api/v1/jobs`)

```json
{
  "title": "Senior Python Developer",
  "description": "Minimum 50 characters describing role requirements and stack.",
  "resumes": [
    { "filename": "ada_lovelace.pdf", "content": "Extracted resume text..." }
  ],
  "leniency_level": 5,
  "custom_instructions": "Prioritize distributed systems experience",
  "webhook_url": "https://example.com/webhooks/hiresquire"
}
```

- `Idempotency-Key` (UUID v4) is **auto-generated and sent as an HTTP header** on `jobs.create`, `jobs.create_from_zip`, and `credits.purchase` so retries never double-charge.
- `leniency_level`: integer `1` (most lenient) to `10` (strictest), default `5`.
- Resume limits: `.txt`, `.md`, `.pdf`, `.docx`; max **20 MB** per file, max **100 resumes** per batch, minimum **50 characters** of extracted text.

### Screening Results Response (`GET /api/v1/jobs/{id}/results`)

```json
{
  "job_id": 42,
  "job_title": "Senior Python Developer",
  "status": "completed",
  "total_candidates": 1,
  "candidates": [
    {
      "id": 101,
      "name": "Ada Lovelace",
      "email": "ada@example.com",
      "score": 94,
      "summary": "Strong distributed systems and Python background.",
      "strengths": ["10+ years Python", "Event-driven architecture"],
      "weaknesses": ["Limited Kubernetes exposure"],
      "skills": ["Python", "PostgreSQL", "FastAPI"],
      "status": "new"
    }
  ],
  "agent_summary": "1 strong match identified..."
}
```

### Error Hierarchy (`hiresquire.errors`)

| HTTP Status | Exception Class | Code | Notes |
|-------------|-----------------|------|-------|
| `401` / `403` | `AuthenticationError` | `AUTHENTICATION_ERROR` | Missing/invalid token or forbidden job |
| `402` | `PaymentRequiredError` | `PAYMENT_REQUIRED` | Insufficient credits or agent spend limit reached |
| `404` | `NotFoundError` | `NOT_FOUND` | Job, candidate, or key not found |
| `400` / `422` | `ValidationError` | `VALIDATION_ERROR` | Invalid payload (e.g., description < 50 chars) |
| `429` | `RateLimitError` | `RATE_LIMIT_ERROR` | Automatically retried honoring `Retry-After` |

---

## CLI Command Reference

Pass `--json` to any command for clean machine-readable output:

```text
hiresquire init              Save token & defaults to ~/.hiresquire/config.json (0600)
hiresquire configure         Update or --clear saved configuration
hiresquire whoami            Verify token and check credit balance (free)
hiresquire estimate          Estimate cost for N candidates
hiresquire screen            Submit resumes (--resumes or --zip, --watch, --leniency)
hiresquire jobs              List screening jobs (--status, --page, --limit)
hiresquire status            Check or --watch job status
hiresquire results           Fetch ranked candidates (--min-score, --only-top-n)
hiresquire summary           Display AI summary for a completed job
hiresquire compare           Compare candidates side-by-side
hiresquire cancel            Cancel a processing job
hiresquire outcome           Report hiring outcome (hired | rejected | withdrawn)
hiresquire candidate         Get candidate details
hiresquire set-status        Update candidate status
hiresquire email             Generate outreach email (--type, --tone, --message)
hiresquire credits ...       balance | list-packs | checkout | purchase | transactions | auto-reload-enable | auto-reload-disable
hiresquire agent-keys ...    list | create | get | update | revoke | regenerate | usage
hiresquire calendar ...      connect | list (also calendar:connect, calendar:list)
hiresquire interviews ...    schedule | list (also interviews:schedule, interviews:list)
hiresquire meetings link     Generate meeting link (also meetings:link)
hiresquire rate-limit        Check API rate limit status
hiresquire webhook-test      Send a test webhook payload
hiresquire schema            Fetch API schema
hiresquire mcp               Start the stdio MCP server
```

---

## Backward Compatibility (v1 → v2)

Existing v1 code continues to work without changes:

```python
from hiresquire import HireSquire  # alias for HireSquireClient
from hiresquire import create_screening_job, get_hiresquire_tools  # deprecated v1 wrappers
```

Deprecated top-level functions emit `DeprecationWarning` and delegate to `HireSquireClient`.

---

## Links & Ecosystem

- **PyPI:** https://pypi.org/project/hiresquire/
- **GitHub:** https://github.com/bp46/hiresquire
- **Node.js CLI (npm):** https://www.npmjs.com/package/hiresquire-cli
- **MCP Registry:** `mcp-name: io.github.bp46/hiresquire`
- **API Docs:** https://hiresquireai.com/docs/api
- **Agent Docs:** https://hiresquireai.com/docs/agents
- **Support:** info@hiresquireai.com

## License

MIT License — see [LICENSE](LICENSE).
