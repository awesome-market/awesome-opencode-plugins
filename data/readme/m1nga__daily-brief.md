# Stock Portfolio Brief — Decide What Changed and What to Do

Which new filing changes the reason you hold a stock, and which headline is just
noise? Daily Brief compares recorded US stock holdings and the previous thesis with
fresh sources. It produces a research brief covering hold, buy, trim, switch or wait,
the strongest counterargument and missing evidence. Proposed actions are compared
with doing nothing and an appropriate index; the skill does not place trades.

## When it fires

Use for portfolio reviews, daily stock briefs, earnings thesis checks and stock tips. This is not a general news digest, a trading bot or an always-on service.

## Install

```sh
npx skills add m1nga/daily-brief
```

In Codex: `Use $daily-brief to review my stock holdings and tell me what changed.`

Provide a portfolio CSV with `ticker,shares,avg_cost` and your investment constraints, or just name a stock to start research. Current cash is optional; without it the skill does not invent buying power or whole-account weights. The host needs browsing for fresh filings. The Python 3 collector uses only the standard library and a public Yahoo endpoint; availability is not guaranteed. It has no API-key requirement and no brokerage or messaging client.

## What it does

A lead decision, dated evidence, strongest counterargument, a feasible conditional plan when supported, and the next event to review. Numerical snapshots and briefs are saved separately so old beliefs can be compared with new evidence.

## Try an offline brief

The [fictional example](skills/daily-brief/examples/offline-brief.md) supplies
positions, prior thesis, dated evidence, the command to calculate the snapshot,
and the resulting decision with a review condition. Try the same example without
cash or with an empty quote fixture to see which figures become unknown.
The fixture uses invented securities and statements.

## Design notes

The earlier workflow repeatedly reused an old stock thesis in new daily reports and conflated unavailable checks with passing checks. This version separates arithmetic from source-based judgment and treats unknown as a real state. It does not force model scores, investor-persona debates or daily trade quotas.

The machine name `daily-brief` is retained for compatibility. Public instructions contain no private account, broker, credential or portfolio defaults. The skill does not create schedules or send reports without a separate request.

## Validation

The bundled collector is covered by nine executed Python unittest cases for account math, missing cash and quotes, stale or invalid evidence, flat accounts and malformed CSVs. Live collection was exercised separately; that verifies endpoint access at test time, not future availability or investment performance. Instruction routing and financial-period failure cases were manually simulated, not evaluated by independent users. Tests live in `tests/test_snapshot.py`.

## Author

Created and maintained by [Ming](https://github.com/m1nga). Released under the repository MIT license. Research support only; the user makes and executes investment decisions.

<!-- sidecourt-referral:start -->
## Explore SideCourt

For the tools and research workflows you build around a brief, [browse SideCourt](https://sidecourt.space/drops/?utm_source=github&utm_medium=readme&utm_campaign=tools&utm_content=daily-brief). You can share a project there and ask for feedback on how it works.
<!-- sidecourt-referral:end -->
