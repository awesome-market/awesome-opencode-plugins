# Competitor Price Monitoring by Country with Magnetic Proxy

**Official Magnetic Proxy agent skills** · Published and maintained by [MagneticProxy](https://github.com/MagneticProxy), the official Magnetic Proxy GitHub organization. [Visit Magnetic Proxy](https://www.magneticproxy.com/).

A country-by-country price watchlist with confirmed changes, source URLs, timestamps, and reasons when a comparison is unsafe. This Agent Skill helps **retail, ecommerce, and pricing teams tracking the same sku or variant across stores and countries** prepare an evidence-based result using Magnetic Proxy for authorized residential routing and regional observations.




## Release status

Public preview: package checks and controlled examples are available; live destination coverage remains pending. Read the [dated QA report](QA-2026-09-29.md) before relying on a particular execution path.


## What you get

- Find comparable price changes across stores and markets
- Separate genuine changes from different packs, sellers and promotions
- Deliver a dated watchlist with evidence and a proposed next check

Start with [the worked example](skills/competitor-price-monitoring/references/worked-example.md), the [deliverable template](skills/competitor-price-monitoring/assets/deliverable-template.md) and the [output columns](skills/competitor-price-monitoring/assets/output.csv).

## Install and start

Copy this prompt into an agent that supports skill installation:

> Review and install `competitor-price-monitoring` from https://github.com/MagneticProxy/magneticproxy-competitor-price-monitoring-skill. Start its included Magnetic Proxy product onboarding and help me with: [my task]. Reuse context and any suitable installed product skill or account; ask only for decisive missing information. Confirm what you can actually install or operate, use existing capacity first and obtain approval before any paid purchase. Begin with a bounded sample and report observed results and pending work.

Or use the Skills CLI from your project folder:

```bash
npx skills add MagneticProxy/magneticproxy-competitor-price-monitoring-skill --skill competitor-price-monitoring
```

Select your agent when prompted. For a non-interactive installation, add the appropriate agent flag, for example `--agent codex` or `--agent claude-code`. Review installed instructions and scripts before running them. Installation does not grant browser tools, credentials or a subscription. A plain chat can read the instructions but may not install or operate the product.

The complete skill folder is the canonical package, including references and templates. A lone downloaded `SKILL.md` omits those files; use the repository installation or copy the complete folder into your agents supported skills directory. An MCP is not required or assumed.

## Product setup is included

Start with this use-case skill. During onboarding, your agent recommends and prepares the official [Magnetic Proxy product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills) for the product step, reusing it if already available. You do not need to install it separately before starting. The [onboarding guide](skills/competitor-price-monitoring/references/brand-onboarding.md) covers supported installation, loading instructions when installation is unavailable, and account/signup guidance.

Installing files alone does not run the product: start the skill with a task. Account access, browser tools and any paid purchase remain separate, and the agent reports what it actually completed.

## From install to first useful result

1. **Start from this use case.** Follow [the included product onboarding](skills/competitor-price-monitoring/references/brand-onboarding.md). The agent reuses or prepares `magneticproxy` during this conversation; the user does not need to install it beforehand. Confirm the browser/computer or authorized client capability actually available.
2. **Log in or sign up.** Open [Magnetic Proxy](https://app.magneticproxy.com/#/my-proxies). Reuse your account; otherwise use the visible Sign up flow. Complete authentication yourself without pasting credentials into the conversation.
3. **Choose capacity for the job.** Inspect available Capsules and GB. For repeated authorized offer observations, assess Price Monitoring and the current target restrictions. Estimate traffic from a small pilot before suggesting a larger allocation. Start with existing suitable capacity. If capacity is insufficient, compare [current plans](https://www.magneticproxy.com/pricing) and recommend the smallest suitable option from observed pilot usage. Follow its current Choose Plan checkout link; do not hardcode a price, discount or checkout token.
4. **Approve any purchase.** Show Capsule, capacity, billing period and current cost before purchase. Continue paid checkout only when the user explicitly authorizes that transaction. A skill installation is not purchase approval.
5. **Prove the route.** Configure the current product, verify the exit in the same browser/client and run a bounded permitted sample. Expand only within the agreed scope. If the approved data route does not need a proxy, explain that and do not invent a purchase requirement.

## Try this task

> Monitor the same 500 ml product on three public stores in the US and Colombia. Alert me when the comparable displayed total changes by at least 5%.

**Bring:** A user-approved watchlist of product URLs, canonical product/variant IDs, countries, comparison cadence, and alert threshold.

**Illustrative result:** Report +8.33% on the displayed item price; do not call it a landed total when shipping is unknown. A 2-pack offer and a blocked observation stay outside the price comparison.

Read the [complete workflow](skills/competitor-price-monitoring/SKILL.md) for source access, execution and decision rules.

## Common questions

### Can I compare prices in different currencies?

Keep original currencies. A converted comparison needs an agreed FX source, rate timestamp and matching tax/shipping context. The lowest displayed number alone does not identify the cheapest offer.

### Why use Magnetic Proxy here?

Magnetic Proxy provides the configured geographic connection for permitted live regional checks. The skill adds comparable observations and a decision-ready deliverable. Supplied-data analysis can proceed without pretending that a live proxy check occurred.

### Is signup or a paid plan required?

An account is required to operate the product. Use available account capacity first. A paid plan is needed only when the requested operation requires capacity or features the account does not have; consult the current product pricing. Installing this repository does not start a paid subscription.

### Has the live workflow been verified?

Public preview: package checks and controlled examples are available; live destination coverage remains pending. See the [latest QA evidence](QA-2026-09-29.md) for the observed sample, deliverables and remaining gates. Installation and CI do not establish live destination access.

## Access and privacy

Check the destination’s terms, access permission, and rate limits before collection. A public URL and a successful proxy connection are not authorization to scrape. Stop on access denials or challenges; do not rotate to evade them. [Magnetic Proxy documentation](https://www.magneticproxy.com/documentation) explains routing and restricted targets.

## Related resources and support

- [Magnetic Proxy product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills) for setup and product operation.
- [Magnetic Proxy Price Monitoring Capsule](https://www.magneticproxy.com/capsules/price-monitoring?utm_source=github&utm_medium=agent_skill&utm_campaign=competitor-price-monitoring) for product context.
- [Report a reproducible issue](https://github.com/MagneticProxy/magneticproxy-competitor-price-monitoring-skill/issues) using redacted or synthetic examples. For account, billing or service issues, use support inside the product.
- [Contribution guide](CONTRIBUTING.md) and [security guidance](SECURITY.md).

This repository documents a specific task; it does not guarantee search rankings, AI citations, delivery, platform access or commercial results. Third-party names identify the workflow and do not imply endorsement.

## License

Original instructions and code are available under the [MIT License](LICENSE). Product subscriptions, service access and third-party data remain subject to their respective terms. This license does not grant trademark rights or permission to collect third-party content.

## Latest QA review

Read the [2026-09-29 QA review](QA-2026-09-29.md) for executed checks, repaired behavior, consolidation decisions and the exact live-testing boundary.
