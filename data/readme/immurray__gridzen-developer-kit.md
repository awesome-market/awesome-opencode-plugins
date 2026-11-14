# Gridzen Developer Kit 0.7.3

The hosted developer interface supports Vietnamese alongside English, Spanish and Simplified Chinese: https://gridzen.ai/developers/?lang=vi . UI language does not enable live checks or country coverage. See [UI language maintenance](docs/multilingual-ui.md).

[Choose direct integration or GridZen for your task](docs/verification-evaluation.md#english) · [Production and cost checklist](https://gridzen.ai/console/learn?lang=en&source=developer_kit#decision-fit)


Single-task entry points: [tool catalog](https://gridzen.ai/tools/) · [setup and boundaries](docs/atomic-tools.md).

```bash
python3 -m venv .venv
.venv/bin/python -m pip install gridzen-developer-kit
.venv/bin/gridzen tools
.venv/bin/gridzen setup --client codex --product clabe-format --project .
# Review the preview, then add --apply. No key is needed for local tools.
```

## Start immediately without signup

Open [GridZen instant trial](https://gridzen.ai/console/start?lang=en) to run synthetic signup-phone and identity-onboarding responses without an account, API key or approval. Success, rejection and unavailable scenarios make no upstream calls and verify no real person. Agents can use the separate [key-free trial MCP](https://gridzen.ai/console/downloads/quickstart_mcp.py), installed with `mcp==2.3.0` and `httpx==0.28.1` in a virtual environment.

For persistent test records and supplier sandbox callbacks, connect a verified merchant sandbox account. Production access is capability-specific: eligible routes may offer bounded real trials, while others remain unavailable. Read the authenticated capability conditions; published prices do not enable paid purchases. Package releases and the hosted MCP Registry entry have independent versions; installing this package grants no merchant permissions.

Fourteen Skills: the original six research/workflow Skills plus eight single-task profiles. Three new tools run offline; five merchant profiles call the existing authenticated GridZen API only with separate authorization, current availability and permitted use. The anonymous remote MCP retains five research/synthetic tools and never performs live verification. Research covers 198 countries/territories as a dated 2026-10-07 snapshot, not live service coverage.

[中文指南](README.zh-CN.md) · [Guía en español](README.es.md)

## Runnable task guides and distribution

| Customer task | Guide | Runnable code |
| --- | --- | --- |
| First identity onboarding | [Guide](https://gridzen.ai/console/learn/identity-first-run?lang=en) | [Delivery fixture](examples/verification_delivery/) |
| Registration phone boundaries | [Guide](https://gridzen.ai/console/learn/phone-check-boundaries?lang=en) | [Four-branch example](https://gridzen.ai/guides/signup-phone-check/) |
| Missing or delayed callback | [Guide](https://gridzen.ai/console/learn/callback-recovery?lang=en) | [Recovery fixture](examples/verification_delivery/) |
| Verification to business permission | [Guide](https://gridzen.ai/console/learn/business-permission-boundary?lang=en) | [Self-hosted n8n fixture](examples/n8n/) |

[Chinese and Spanish article files](https://github.com/immurray/gridzen-developer-kit/tree/main/distribution/market-expansion-2026-10-13/articles/) · [Demo video](https://github.com/immurray/gridzen-developer-kit/blob/main/distribution/market-expansion-2026-10-13/media/identity-three-outcomes.mp4).

Public examples are synthetic. Published per-product prices and availability are subject to the authenticated merchant console; paid activation remains unavailable. [Request an approved pilot](https://gridzen.ai/console/pilot), without sending identity documents or credentials to public MCP tools.

[Per-check plan and activation requirements](https://gridzen.ai/console/quote?lang=en) · [JSON](https://gridzen.ai/console/api/commercial/options)

## Try it

Public playground: https://gridzen.ai/developers/

Download `gridzen-developer-kit.zip`, extract it, then:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install './gridzen-developer-kit[mcp]'
gridzen coverage --country ID --capability bank_account_match
gridzen plan --country ID --event onboarding
gridzen simulate --country ID --capability bank_account_match --scenario timeout
python gridzen-developer-kit/examples/customer_tasks.py
```

Python 3.11+. CLI and MCP use the bundled offline catalog and fixtures; the Python HTTP client/example calls the public sandbox. Dependencies are downloaded only during installation. API reference: https://gridzen.ai/developers/api/openapi.json .

## MCP

Register a local stdio server in your MCP client. Use the absolute path to the installed executable; configuration syntax varies by client. A conventional `mcpServers` configuration is:

```json
{"mcpServers":{"gridzen":{"command":"/absolute/path/to/.venv/bin/gridzen-mcp","args":[]}}}
```

Tools: get_coverage, plan_verification, create_sandbox_verification, get_sandbox_verification, explain_result. All operate on local research or synthetic fixtures, with read-only/idempotent annotations. Public research/sandbox MCP endpoint: `https://gridzen.ai/developers/mcp` (Streamable HTTP, no account or API key). It has the same five tools and zero live providers. Remote usage sends the documented arguments to Gridzen; local stdio is offline by default. Limits: 120 requests/minute per client address and 600/minute overall, returning HTTP 429 with Retry-After.

## Skills

Copy the individual directories from `skills/` into your compatible agent's project or user skill directory. Each entrypoint is `SKILL.md`; preserve its `references/` directory. No marketplace listing or automatic registration is implied.

## HTTP SDK

```python
from gridzen_developer.client import Gridzen
client = Gridzen()
plan = client.plan('ID', 'onboarding')
result = client.simulate('ID', 'bank_account_match', 'not_found')
assert result['status'] == 'inconclusive'
assert result['verified'] is False
```

Only documented country/event/capability/scenario fields are accepted. Never send identity numbers, bank accounts, documents or credentials to the sandbox. Simulation IDs encode fixtures and are not unique transaction identifiers. A synthetic match cannot authorize real users or production actions. Research evidence is distinct from Gridzen availability or commercial permission.

## Repository source: local service and checks

```sh
python -m pip install '.[test,server]'
python -m pytest -q
python scripts/check_mcp.py
uvicorn gridzen_developer.server:app --host 127.0.0.1 --port 8030
```

Production uses an independent container at localhost:8030 proxied only under `/developers/`. See deploy/compose.yml and deploy/developers.conf. Removing that proxy file and stopping this container rolls back the preview; the existing API and Agent Company stacks are separate.

## Repository source: build distributions

`python scripts/build_downloads.py` creates allowlisted developer-kit and Skills ZIPs; it excludes tests, deployment files, private credentials and itself from recursive download packaging. `python scripts/build_catalog.py <repo>/docs/research/identity-verification/2026-10-07` refreshes the public research projection. Main repository report files remain the provenance source.

## Public distribution

<!-- mcp-name: ai.gridzen/verification -->

Source: https://github.com/immurray/gridzen-developer-kit . Install the Skills:

```sh
npx skills add immurray/gridzen-developer-kit
```

Install the tagged Python/MCP release from GitHub (Python 3.11+ and Git):

```sh
python -m pip install "gridzen-developer-kit[mcp] @ git+https://github.com/immurray/gridzen-developer-kit.git@v0.7.3"
```

Install the latest PyPI release with `python -m pip install --upgrade
gridzen-developer-kit`. See [the release tracker](https://github.com/immurray/gridzen-developer-kit/blob/main/distribution/STATUS.md) for
publication and installation evidence.

Remote client configuration (conventional JSON; client syntax may vary):

```json
{"mcpServers":{"gridzen":{"type":"http","url":"https://gridzen.ai/developers/mcp"}}}
```

For Claude Code: `claude mcp add --transport http gridzen https://gridzen.ai/developers/mcp`.
For Cursor: add the remote URL in its MCP settings. For portable Agent Plugins,
use the packaged `plugin.json` and `mcp.json`; the portable transport identifier
is `streamable-http`. Marketplace admission is separate from compatibility.

Original code and Skills: MIT. Research provenance and third-party rights:
[NOTICE.md](NOTICE.md). Support: open@gridzen.ai .

## Marketplace availability

Source and previous release downloads are public. Existing Registry and Skills.sh listings cover the research service; new product profiles are not separate approved listings. Docker catalog submission is awaiting review. See [the publication ledger](https://github.com/immurray/gridzen-developer-kit/blob/main/distribution/STATUS.md) for exact status and remaining platform steps.


## 14 bundled Skills (0.7.3)

`python -m pip install gridzen-developer-kit` installs the CLI, stdio MCP dependencies
and all 14 Skill directories.

The 14 Skills comprise 6 research/workflow Skills and 8 single-task profiles. Of the 8 profiles, 3 run offline and 5 merchant profiles require separate authorization. Five public MCP tools provide research/synthetic operations. No live identity verification. No extra MCP
dependency installation is required. Check available versions on
[PyPI](https://pypi.org/project/gridzen-developer-kit/).

```sh
gridzen coverage --country MX
gridzen skills
gridzen-mcp
```

Connect `gridzen-mcp` as your client's stdio server, or use the remote endpoint
`https://gridzen.ai/developers/mcp`. `gridzen skills` prints the installed directories;
copy a complete directory into your assistant's configured Skills directory to
activate it. Installing a wheel does not automatically activate a client's Skills.

The existing select/integrate/explain Skills remain available. Added offline
workflows, version 1.0.0, cover evaluation scope, evidence-review policies and
provider-rights readiness. Each includes MIT, README, complete response fixtures
and agent acceptance prompts. They make no third-party calls and grant no real
verification, legal approval or regulatory conclusion.

## Configure your assistant (v0.7.3)

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gridzen-developer-kit
gridzen setup --client all --project .
gridzen setup --client all --project . --apply
```

Use `--client` for Codex, Claude Code/Desktop, Cursor, VS Code/Copilot, Copilot CLI, Gemini CLI, Cline, Roo Code or OpenCode. Setup previews by default, merges existing unrelated settings, backs up changed configurations and refuses differing Gridzen entries or Skill files. No global client settings are modified. Native clients require workspace trust; Desktop and Cline require manual MCP import. Desktop produces separately uploadable Skill ZIPs. See [client-specific instructions](docs/harness/README.md) and [actual compatibility evidence](clients/compatibility.json). Configuration preparation is not model acceptance or real verification.

## Hosted MCP aggregate attribution

Hosted calls count successful tool invocations, not customers. Existing totals
remain unchanged. The hosted service records UTC day, tool name, one source
category and a count; it never persists request arguments or client addresses.
Historical and unlabelled calls remain `unknown`. Local stdio is offline by default.

Explicit acceptance requests to the loopback-published service may set
`X-Gridzen-Purpose: internal_test`. Only configured local peers with no forwarded
client headers are classified as `internal_test`. The public reverse proxy must
overwrite `X-Real-IP`; publicly supplied labels are only `self_reported_test`.
An unlabelled public request is not an authenticated external customer. The
`GRIDZEN_MCP_LOCAL_TEST_PEERS` deployment setting must match the container gateway
and must never contain public client addresses. Source counts use the existing
90-day retention and fail-open behavior. This hosted change does not publish a
new PyPI version or enable any live provider.


## Customer tasks and voluntary feedback (0.6.0)

```sh
gridzen plan --country US --event onboarding --task signup_phone
gridzen plan --country US --event onboarding --task identity_onboarding
gridzen plan --country US --event onboarding --task identity_onboarding --stage production
python examples/customer_tasks.py
gridzen feedback --task signup_phone --country US --outcome blocked --blocker missing_workflow_step --output task-summary.json
# Only after choosing to share:
gridzen feedback --input task-summary.json --share
```

Phone intelligence is not OTP or ownership verification. Identity fixtures are not hosted document/liveness sessions. Provider intake Skills are for provider operations/BYO, not a universal customer gate.

Remote APIs count fixed task/capability/country/stage/error categories for 90 days, including technical failures. They store no arguments, identity data, credentials, raw chats or per-user tracking. Local feedback is off by default. After explicit opt-in, CLI and stdio MCP automatically upload category-only events. Reading static Skills remains unobservable. Optional feedback requires explicit consent, contains only fixed categories, and is unverified self-reported evidence. A SHA-256 hash of its random receipt ID is retained 30 days for 30-day retry deduplication; the ID itself is not stored. Counters are capped at 10,000 requests/day and 500 summaries/day per database; missing history or offline usage is unknown. Requests are not unique customers.

## Optional automatic local feedback (0.6.0)

```sh
gridzen telemetry status
# Run only after reading and agreeing to category-only automatic sharing:
gridzen telemetry enable --consent
gridzen plan --country US --event onboarding --task signup_phone
# Send one queued event per invocation after reconnecting:
gridzen telemetry flush
# Disable future uploads and clear the pending queue:
gridzen telemetry disable
```

No network calls occur from local CLI/MCP when disabled. Consent is saved per OS user, not silently added to a project. Events contain only documented categories, ISO country, and a random per-event receipt, with no conversation, identity fields, credentials, user or project IDs. Feedback failures do not fail tool execution. The local queue is capped at 1,000 events/30 days; reconnect or `flush` retries one queued event, with a one-second HTTP timeout. Uploads are self-reported usage, not authenticated customers or completed verification. No background daemon is installed. Merely reading a Skill is unobservable; after consent, an Agent can explicitly record a fixed-category task summary.

Local queued events expire after 30 days and are removed on the next enqueue/flush. Daily aggregates use server receipt date; delayed uploads are not proof that work occurred on that date.

## Separate owner-approved customer pilot

The package and its five public tools retain their research/synthetic boundaries. A separate hosted pilot accepts customer applications for basic signup-phone validity and hosted personal identity onboarding: [apply](https://gridzen.ai/console/pilot?lang=en), [integration guide](https://gridzen.ai/console/pilot-guide?lang=en), [public scope](https://gridzen.ai/guides/customer-pilot/).

Submitting an application never activates production. The owner must approve supplier rights, downstream agreements, capabilities, request limits and expiry; only confirmed free allowances are used. The production pilot has its own downloaded MCP client and merchant API key. Do not send documents, faces or provider keys to the public research MCP. Basic phone validity does not provide OTP or ownership.

Real basic phone checks and retrieval of a historical Approved operator identity session were validated through the live customer API/MCP. New-session human completion and its final real webhook remain unvalidated. Operator tests, downloads and self-reported interest are not customer demand. This documentation update does not change the PyPI package or Registry version.


Use `gridzen start --task identity_onboarding --lang en` to find the anonymous trial, free sandbox account and integration assistant. `gridzen start` makes no network calls. Account progress measurement is a separate, optional console consent; completing a sandbox does not verify a real person. Paid activation remains unavailable.

## Complete a customer task

- [Identity onboarding: three outcomes and application decisions](https://gridzen.ai/console/learn/identity-first-run?lang=en)
- [Phone checks: validity, ownership and unavailable outcomes](https://gridzen.ai/console/learn/phone-check-boundaries?lang=en)
- [Recover delayed callbacks](https://gridzen.ai/console/learn/callback-recovery?lang=en)
- [Bind verification to seller permissions](https://gridzen.ai/console/learn/business-permission-boundary?lang=en)
- [Runnable SQLite delivery example](examples/verification_delivery/README.md)
- [Importable n8n fixture workflow](examples/n8n/README.md)

These are synthetic integration examples. They do not prove real identity,
production webhook delivery or customer adoption. No account is needed
for the anonymous response trial or local examples.

Install all fourteen skills into your project:

```bash
npx skills add immurray/gridzen-developer-kit --skill '*' --agent codex --copy -y
```

Choose your supported agent instead of `codex`. Installation compatibility does
not prove all agents have executed or recommended the skills.

## Existing Mexico SPEI payment evidence

In the installed package or developer source ZIP, use `gridzen tools --product mx-cep` to discover the separate authenticated CEP workflow. Public tools remain research/synthetic only. [Live capability conditions](https://gridzen.ai/console/api/payment-evidence/mx/cep/capabilities) require a merchant key; do not send transaction details or keys to public tools. [Runnable offline example](examples/cep_reconciliation/) makes no network calls. CEP preserves original XML, independent signature and exact expected-transaction binding; historical names do not establish current identity or account control. This workflow verifies existing SPEI evidence; it does not initiate a transfer.

## Mexico identity and beneficiary-name comparison

[Task, pricing boundaries and zero-cost integration examples](docs/mexico-identity-account.md) cover first account binding, account changes and exception review. Published per-product prices and availability are subject to the authenticated merchant console; read the authenticated capability response. Public MCP and Skills remain research/synthetic only.

[Run the identity/account result example offline, without signup](examples/mx_identity_account/).

## Documents included with pip installation

The wheel and source distribution include the same 14 canonical Skill directories
and public integration guides as the website source download. English, Chinese and
Spanish READMEs, task guides, ten-client instructions, examples and client templates
are installed under `share/gridzen-developer-kit/` in your Python environment.

```sh
python -c "import sysconfig; from pathlib import Path; print(Path(sysconfig.get_path('data')) / 'share/gridzen-developer-kit/README.md')"
```

Open that README or `docs/harness/README.md` locally. Research snapshots and old
offline identifiers remain compatible; they do not grant live verification or
business authorization. CEP/SPEI guides describe evidence for existing transactions.
