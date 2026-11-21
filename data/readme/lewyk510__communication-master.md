# communication-master

A trilingual — **中文 / English / Bahasa Malaysia** — communication and reply knowledge base,
packaged as an agent skill. Load it whenever you need to **decode what someone really means**
(subtext / 弦外之音 / hint), read a social or workplace situation, or draft a reply, letter, or AI
prompt. Malaysia-first, with global and Chinese material.

Three language lanes are **authored natively** — they are lanes, not translations.

## Install

**One command (recommended)** — via the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add lewyk510/communication-master
```

```bash
npx skills add lewyk510/communication-master -a claude-code -a opencode   # pick agents
npx skills add lewyk510/communication-master -g                           # install globally
npx skills add lewyk510/communication-master --list                       # list, don't install
```

**Manual** — clone it in:

```bash
git clone https://github.com/lewyk510/communication-master ~/.agents/skills/communication-master
```

Then **restart your agent** (skills load at startup).

## What it covers

- **Concepts** (18): subtext & implicature, persuasion, NVC & conflict repair, emotional
  intelligence, personality typology, nonverbal signals, manipulation defense, rhetoric, …
- **Scenarios** (19): workplace power, romance, family, hard conversations, job interviews,
  negotiation, mediation, condolence & grief, landlord–tenant, medical, live streaming, …
- **Cultures** (5): Malaysia Malay / Chinese / Indian, cross-cultural, code-switching.
- **Playbooks** (4): reply engine (S2), subtext decoder (S1), formal writing (S3), AI prompting (S4).

## Usage

Ask in any of the three languages; the router picks the topic and the matching lane:

- "Ta 在暗示什么 / 他这话什么意思？" → decode subtext
- "我该怎么回这句话？" → draft options
- "写一封投诉/申诉/申请信" → formal letter
- "怎么让 AI / 客服机器人做我要的事" → prompt patterns

Offline one-command resolver (no network, no API):

```bash
python3 tools/ask.py "<question>"                 # cache → route → digest card
python3 tools/ask.py "<question>" --full          # + core.md and the language lane
python3 tools/ask.py "<question>" --json          # structured output
```

## How it works

- `router-index.json` — compact matching index (the resolver loads this to route).
- `sidecars/cards.json` — one ~400-token digest card per topic (light-load path).
- `cache/` — local exact-match answer cache, auto-invalidated when content changes.
- `tools/router_match.py` — the single implementation of the documented matcher; the recall
  gate and `ask.py` share it.

Per query: the **light** path (compact index + one card) is ~3× cheaper than loading a full topic.

## Layout

```
SKILL.md                 agent entry point
AGENTS.md                schema, conventions, anti-fabrication rules
wiki/                    the knowledge body (concepts/scenarios/cultures/playbooks/synthesis)
router.json              full trigger → file map (source of truth)
router-index.json        compact matching index (generated)
sidecars/cards.json      per-topic digest cards (generated)
tools/                   resolver, matcher, lint, index/card builders, cache, backup, publish
commands/                /decode /reply /draft /prompt
qa/                      frozen scenarios + recall smoke test + proof transcripts
```

## Verify

```bash
bash tools/check.sh      # lint + recall smoke + resolver + freshness (must pass)
```

## Note on sources

This public repository intentionally ships **without** `raw/` — that directory holds third-party
web captures (articles, search snapshots) whose redistribution is not licensed. The original
source URLs remain cited in every wiki page's `## Sources` section. The private working copy
keeps `raw/` for maintenance.

## Contributing

Issues and pull requests are welcome — see `CONTRIBUTING.md`. The project is built to evolve:
add a topic, sharpen a trigger, improve a lane.

## License

MIT — see `LICENSE`.
