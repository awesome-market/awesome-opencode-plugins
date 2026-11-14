# Link Building Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.3.0-blue.svg)](CHANGELOG.md)
[![OpenCode](https://img.shields.io/badge/OpenCode-compatible-000000.svg)](https://opencode.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

An agent skill for **white-hat link building**: it finds relevant directories, forums, communities, and Q&A sites, handles account creation with a disposable inbox, publishes a genuinely useful contribution containing your link, and writes an auditable JSON log for every attempt.

Built for [OpenCode](https://opencode.ai) and designed to work with the companion [`temp-mail-automation`](https://github.com/devcodex2025) skill. The only required inputs are a **target URL** and a **niche**.

> **Tested in production** on a live site — see [Case study: password generator](#case-study-password-generator) for a real directory run with recorded results.

---

## Table of contents

- [Why this skill](#why-this-skill)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Persistent inbox](#persistent-inbox)
- [Search engine submission](#search-engine-submission)
- [Directory catalog](#directory-catalog)
- [Quick start](#quick-start)
- [Usage examples](#usage-examples)
- [Inputs](#inputs)
- [Output: the results log](#output-the-results-log)
- [Donor vetting and quality gates](#donor-vetting-and-quality-gates)
- [Case study: password generator](#case-study-password-generator)
- [Testing](#testing)
- [Repository structure](#repository-structure)
- [Compliance and safety](#compliance-and-safety)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Why this skill

Most "link building" automation is just form spam with a spreadsheet attached. This skill is deliberately different:

| Principle | What it means in practice |
|---|---|
| **Relevance first** | A donor must match the target's topic and audience before a single form is opened. Irrelevant listings are rejected, not queued. |
| **Real contributions** | Every post is written for the thread: 3–8 sentences that answer the question, with the link added only when it is genuinely useful. |
| **Human-in-the-loop** | Ambiguous CAPTCHAs, paid placements, and identity checks stop the run and ask the operator instead of guessing. |
| **Auditable** | Every attempt — success, rejection, or failure — produces a structured record with a screenshot and a live-URL check. |
| **Repeatable** | The JSON log doubles as a dedupe database, so the same donor is never re-submitted on a later run. |

---

## How it works

```text
┌─────────────┐   ┌──────────────┐   ┌───────────────┐   ┌──────────────┐
│ 0. Preflight│──▶│ 1. Discovery │──▶│ 2. Vetting    │──▶│ 3. Register  │
│  load skill │   │  find donors │   │  score/queue  │   │  temp inbox  │
└─────────────┘   └──────────────┘   └───────────────┘   └──────┬───────┘
                                                                │
┌─────────────┐   ┌──────────────┐   ┌───────────────┐   ┌──────▼───────┐
│ 6. Report   │◀──│ 5. Verify    │◀──│ 4. Publish    │◀──│  OTP / login │
│  JSON log   │   │  live link   │   │  contribution │   │              │
└─────────────┘   └──────────────┘   └───────────────┘   └──────────────┘
```

1. **Preflight** — load the skill, check the browser session, load `link_building_results.json` (create `[]` if missing).
2. **Discovery** — search for directories, forums, niche communities, and Q&A threads that accept submissions in the target's category.
3. **Vetting** — score each donor on topical relevance, link type, moderation risk, and effort. Only qualified donors enter the queue.
4. **Registration** — load the persistent inbox, create the account, solve email verification automatically when possible.
5. **Publishing** — write the contribution, place the link with a natural anchor, submit, capture a screenshot.
6. **Verification** — confirm the post/listing is publicly visible and the link resolves, append the result to the log, and close the tab.

Details and guardrails live in [`SKILL.md`](SKILL.md).

---

## Requirements

- An agent runtime that supports skills (tested with OpenCode).
- Browser automation tools (`browser_navigate`, `browser_click`, `browser_snapshot`, `browser_screenshot`) or equivalent MCP tools.
- The [`temp-mail-automation`](https://github.com/devcodex2025) skill for disposable inboxes and OTP retrieval. If it is unavailable, the skill uses the persistent identity file described below.
- Python 3.9+ only if you want to run the JSON validator in [`tests/`](tests).

No API keys, paid SEO tools, or captcha-solving services are required.

---

## Installation

### Global (available in every project)

```bash
git clone https://github.com/devcodex2025/link-building-skills.git \
  ~/.config/opencode/skills/link-building
```

The skill ID is derived from the directory name, so it is available as `link-building`.

### Project-local

```bash
git clone https://github.com/devcodex2025/link-building-skills.git \
  .opencode/skills/link-building
```

### Manual install

Copy `SKILL.md` into `~/.config/opencode/skills/link-building/SKILL.md`. That single file is the whole skill; the rest of the repository is documentation, fixtures, and tests. OpenCode searches `~/.config/opencode/skills` globally and `.opencode/skills` per project.

Verify the install:

```text
List the skills you have available and confirm that "link-building" is loaded.
```

### Persistent inbox

The skill uses **one** disposable inbox for every registration. It is stored outside the repository:

```text
~/.config/opencode/link-building/identity.json
```

```json
{
  "provider": "mail.tm",
  "email": "your-inbox@example.com",
  "password": "your-inbox-password",
  "api_base": "https://api.mail.tm",
  "created_at": "2026-11-10T17:08:43Z",
  "policy": "single_identity_for_all_submissions"
}
```

Rules:

- Reuse this address for directories, search engines, forums, and profiles.
- Never create a new inbox per donor or per submission.
- Keep the file outside the repository and readable only by the local user.
- Rotate it only if a site rejects the address or access is lost, and only with operator approval.
- If a donor requires a branded address, use the brand address instead.

Read the inbox with the bundled helper when `temp-mail-automation` is unavailable:

```bash
python scripts/inbox.py list
python scripts/inbox.py wait --subject "verify" --timeout 180 --otp
python scripts/inbox.py latest --otp
```

---

## Search engine submission

Search engines are not link donors. The skill includes a verified reference of own-index engines, index resellers, and crawl-only engines for the 12 supported locales:

- [`data/search-engines.md`](data/search-engines.md) — human-readable table with submission links.
- [`data/search-engines.json`](data/search-engines.json) — machine-readable list for automation.

Only these channels accept a submission that changes something:

| Channel | Locales | Method |
|---|---|---|
| Google Search Console | all | account, sitemap |
| Bing Webmaster Tools | all | account, sitemap |
| IndexNow | all | API key file, one batch |
| Yandex Webmaster | `ru`, `uk` | account, sitemap |
| Baidu / Sogou / 360 / Shenma | `zh` | account, verification |
| Coc Coc | `vi` | public form + CAPTCHA |
| LetSearch | `ru` | public form, Russian content |
| Marginalia / Wiby | `en` | public form |
| Right Dao | `en` | email |

DuckDuckGo, Ecosia, Qwant, Startpage, Yahoo, MetaGer, Rambler, Mail.ru, Meta.ua, Bigmir, Onet, Interia, WP, SAPO, UOL, Terra, Virgilio, Libero, and goo use Google or Bing indexes. Submitting to them separately has no effect; optimize for the upstream index.

Bulk account creation, automated CAPTCHA solving, and mass URL submission are out of scope.

---

## Directory catalog

[`data/directory-catalog.md`](data/directory-catalog.md) is a research catalog of **1,233 unique directories, launch platforms, marketplaces, and social channels**:

- 23 verified no-login entries;
- 890 free entries;
- 320 paid entries.

Every entry has a submission URL. The catalog is a research resource, not a submission queue: many entries are generic, dead, account-gated, paid, or irrelevant to a password-security tool. Filter it with the quality gates in `SKILL.md` before opening a single form.

Do not run a mass-submission script against the whole catalog. One relevant listing on a live directory is worth more than a thousand automated submissions, and mass registration violates the skill's guardrails.

---

## Quick start

Start a session in the directory where the results log should live, then send:

```text
Load the link-building skill.

Target URL: https://example.com/password-generator
Niche: password security and privacy tools
Max attempts: 10
Desired anchor: free password generator
```

The agent will research donors, reuse the persistent inbox for registrations, publish contributions, and write `link_building_results.json` plus screenshots as it goes.

---

## Usage examples

### 1. Minimal run

```text
Use link-building.
Target URL: https://example.com/blog/ai-writing-guide
Niche: AI writing tools
```

Defaults: up to 10 attempts, automatic anchor selection, results written to `./link_building_results.json`.

### 2. Directory-only campaign

```text
Use link-building in directory-only mode.
Target URL: https://example.com/password-generator
Niche: password generator / cybersecurity utilities
Max attempts: 15
Allowed donor types: tool directories, startup directories, free-software catalogs
Skip: forums, blog comments, paid placements
Desired anchor: strong password generator
```

Useful for a new product that has no community footprint yet. Directory listings are low-risk, permanent, and easy to verify.

### 3. Strict brand and anchor control

```text
Use link-building.
Target URL: https://example.com/pricing
Niche: B2B analytics
Max attempts: 8
Desired anchor: analytics platform for product teams
Brand name: Example Analytics
Tone: technical, no marketing superlatives
Minimum donor relevance: 7/10
Require operator approval before publishing: yes
```

The run pauses before each publication and shows you the draft. Nothing is posted until you reply `approve`.

### 4. Audit-only (dry run)

```text
Use link-building in audit mode.
Target URL: https://example.com/password-generator
Niche: password security
Produce a donor shortlist with relevance scores and submission requirements.
Do not register, submit, or publish anything.
```

Produces a scored prospect list and writes it to the log with `"status": "candidate"`. Ideal for planning a campaign without touching third-party sites.

### 5. Resume an interrupted campaign

```text
Use link-building.
Target URL: https://example.com/password-generator
Niche: password security
Resume from link_building_results.json. Skip every site that already has a success or pending record.
```

The log is the source of truth: domains with `success`, `pending`, or `rejected` records are never retried automatically.

### 6. Multi-market campaign

```text
Use link-building.
Target URL: https://example.com/password-generator
Niche: password security
Locales: en, es, de, fr
Desired anchor: free password generator
Max attempts: 10 per locale
```

Use one target URL per locale when the site has localized pages. The skill treats each locale as a separate context and rewrites the contribution for the local audience.

---

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `target_url` | Yes | — | The page that should receive the backlink. |
| `niche` | Strongly recommended | inferred from page | Topic used to find and score donors. |
| `max_attempts` | No | `10` | Upper bound on donor attempts (8–15 recommended). |
| `desired_anchor` | No | generated | Preferred anchor text; variants are generated to avoid over-optimization. |
| `brand_name` | No | from page | Name used in bios and listings. |
| `allowed_donor_types` | No | all | e.g. `directory`, `forum`, `blog_comment`, `qa`, `profile`. |
| `min_relevance` | No | `6` | Donor relevance score (0–10) required to proceed. |
| `require_approval` | No | `false` | Pause before each publication for operator sign-off. |
| `audit_only` | No | `false` | Research and score only; never submit. |
| `identity_file` | No | `~/.config/opencode/link-building/identity.json` | Persistent inbox used for every registration. |
| `close_tabs_after_submission` | No | `true` | Close every tab opened by the skill once its result is logged. |

### Browser hygiene

- Each submission gets one tab. The tab is closed as soon as the result is written to the log.
- Verification opens a temporary tab and closes it after the check.
- The skill never closes tabs the operator opened manually.
- A CAPTCHA tab stays open only until the operator resolves it, then it is closed too.
- Set `close_tabs_after_submission` to `false` only when you explicitly want to keep the final page open.

---

## Output: the results log

Every attempt appends one record to `link_building_results.json`:

```json
[
  {
    "timestamp": "2026-11-10T09:42:17Z",
    "site_url": "https://toolsdirectoryonline.com",
    "donor_type": "directory",
    "relevance_score": 8,
    "temp_email": "x7k9p2q4@mail.tm",
    "password": "Pass123!Temp",
    "action": "registration_and_listing",
    "anchor_text": "free password generator",
    "target_url": "https://example.com/password-generator",
    "posted_url": "https://toolsdirectoryonline.com/tools/password-generator",
    "status": "success",
    "http_status": 200,
    "link_rel": "dofollow",
    "screenshot": "screenshots/20261110_toolsdirectoryonline.png",
    "otp_used": "748291",
    "notes": "Free listing approved on first review; description edited to match directory tone."
  }
]
```

### Status values

| Status | Meaning |
|---|---|
| `success` | Published and the live URL returns 2xx with the target link present. |
| `pending` | Submitted, awaiting moderation or email confirmation. |
| `rejected` | Donor declined the submission or the post was removed. |
| `failed` | Technical failure (captcha, timeout, form error). Safe to retry later. |
| `skipped` | Vetted out before submission (irrelevant, paid-only, nofollow-only, duplicate). |
| `candidate` | Audit-mode record; no submission was made. |

Credentials in the log are disposable and belong to throwaway accounts. Treat the file as sensitive anyway: add it to `.gitignore` if you commit campaign folders.

---

## Donor vetting and quality gates

A donor must pass **all** gates before registration:

| Gate | Pass condition |
|---|---|
| Topical relevance | Score ≥ `min_relevance` (default 6/10). |
| Indexability | Page is crawlable, not `noindex`, not behind a login wall. |
| Link policy | Outbound links are allowed in user content or listings. |
| Cost | Free, or explicitly approved by the operator. |
| Duplicate check | Domain absent from the results log. |
| Effort | Submission path is completable in a reasonable number of steps. |

Scoring rubric (0–10): topic match (0–4), audience overlap (0–3), link quality (0–2), submission friction (0–1).

Additional publishing rules:

- One link per contribution, always inside useful text.
- Vary anchor text across donors; never repeat an exact-match anchor more than twice.
- No identical copy across sites: every post is rewritten for its thread.
- Respect `robots.txt`, rate limits, and each site's terms of service.
- Stop on CAPTCHA, phone verification, or ID checks and hand control back to the operator.

---

## Case study: password generator

A live pilot was run for a free, client-side password generator in the password-security niche. The site is intentionally anonymized in this repository.

- **Niche:** password generators, cybersecurity utilities, privacy tools
- **Donor types:** tool directories, startup directories, free-software catalogs
- **Outcome:** 2 listings live and verified (both nofollow), 5 submissions awaiting review, 11 donors vetted out, 2 unreachable endpoints. Full records: [`examples/link_building_results.json`](examples/link_building_results.json); narrative: [`examples/case-study-password-generator.md`](examples/case-study-password-generator.md)

The case study records what was submitted, what is awaiting moderation, what was skipped and why. It is intentionally honest about failures: a useful skill has to report the sites that did not work.

---

## Testing

The repository ships a schema validator and fixtures:

```bash
python tests/validate_results.py examples/link_building_results.json
```

Expected output:

```text
OK: 20 records valid
```

Run the full test suite (fixtures, edge cases, exit codes):

```bash
python -m unittest discover -s tests -v
```

Tests cover:

- required fields and ISO-8601 timestamps
- allowed `status` values
- URL validity for `target_url`, `site_url`, and `posted_url`
- duplicate-domain detection
- malformed and empty logs
- search engine reference shape, unique IDs, and locale coverage
- directory catalog size, unique URLs, and required sections
- inbox matching and OTP extraction helpers

CI runs the same suite on every push via [`.github/workflows/validate.yml`](.github/workflows/validate.yml) when Actions is enabled for the repository.

---

## Repository structure

```text
link-building-skills/
├── SKILL.md                          # the skill definition (single source of truth)
├── README.md                         # this file
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── .github/workflows/validate.yml    # CI: validate fixtures, run unit tests
├── data/
│   ├── donor-sources.md              # vetted source categories and search queries
│   ├── directory-catalog.md          # 1,233 directories and launch platforms
│   ├── search-engines.md             # engines per locale with submission links
│   └── search-engines.json           # machine-readable engine list
├── scripts/
│   └── inbox.py                      # read the persistent inbox and extract OTP codes
├── examples/
│   ├── link_building_results.json    # real sample log
│   └── case-study-password-generator.md
└── tests/
    ├── validate_results.py
    ├── test_validate_results.py
    ├── test_inbox.py
    ├── test_search_engines.py
    ├── test_directory_catalog.py
    └── fixtures/
        ├── valid.json
        └── invalid.json
```

---

## Compliance and safety

This skill is for **legitimate promotion of a real product**.

- Only submit where submissions are welcome. Read the submission guidelines first.
- Use disposable inboxes only where the site permits them. If a site requires a company or domain email, use one.
- Never create multiple accounts on the same site, vote-ring, or post the same link across dozens of low-quality pages.
- Disclose affiliation when a community requires it.
- Do not use the skill for phishing, malware, or misleading claims.
- Paid placements, link exchanges, and PBNs are out of scope.

The operator is responsible for complying with each destination site's terms and with local law (including disclosure rules for affiliate and sponsored content).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Skill not listed | Confirm `SKILL.md` is at `~/.config/opencode/skills/link-building/SKILL.md`, then restart the session. |
| `temp-mail-automation` unavailable | Install it, or pass existing account credentials for the donor and let the skill log in. |
| OTP never arrives | Wait up to 3 minutes, then ask the agent to request a resend; some sites block disposable domains and must be skipped. |
| CAPTCHA blocks the run | The skill stops by design. Solve it manually in the visible browser tab, then tell the agent to continue. |
| Results log overwritten | Restore from git or a backup; the skill only appends, so overwrites indicate a manual edit. |
| Link published but not visible | Check the record's `status`: use `pending` until moderation completes, then re-verify with the live URL. |

---

## Contributing

Contributions are welcome: new donor sources, better scoring heuristics, additional validators, and translations. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Please keep the skill's ethical constraints intact.

---

## License

[MIT](LICENSE) © 2026 devcodex2025

---

**Keywords:** link building, backlinks, SEO automation, directory submission, AI agent skill, OpenCode skill, temp mail, OTP automation, white-hat SEO, digital PR, startup directories, tool directories, password generator SEO.
