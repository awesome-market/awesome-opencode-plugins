# Amazon Product Research and Price Comparison with Magnetic Proxy

**Official Magnetic Proxy agent skills** · Published and maintained by [MagneticProxy](https://github.com/MagneticProxy), the official Magnetic Proxy GitHub organization. [Visit Magnetic Proxy](https://www.magneticproxy.com/).

A sourced comparison matrix that shows which listings and variants are genuinely comparable across regions. This Agent Skill helps **marketplace analysts, ecommerce operators, and product teams comparing authorized Amazon product records** prepare an evidence-based result using Magnetic Proxy for authorized residential routing and regional observations.




## Release status

Public preview: package checks and controlled examples are available; live destination coverage remains pending. Read the [dated QA report](QA-2026-09-29.md) before relying on a particular execution path.


## What you get

- Compare Amazon models, features, exact variants and sellers
- Separate marketplace price from shipping and destination eligibility
- Build a sourced shortlist from authorized product records

Start with [the worked example](skills/amazon-product-research/references/worked-example.md), the [deliverable template](skills/amazon-product-research/assets/deliverable-template.md) and the [output columns](skills/amazon-product-research/assets/output.csv).

## Install and start

Copy this prompt into an agent that supports skill installation:

> Review and install `amazon-product-research` from https://github.com/MagneticProxy/magneticproxy-amazon-product-research-skill. Start its included Magnetic Proxy product onboarding and help me with: [my task]. Reuse context and any suitable installed product skill or account; ask only for decisive missing information. Confirm what you can actually install or operate, use existing capacity first and obtain approval before any paid purchase. Begin with a bounded sample and report observed results and pending work.

Or use the Skills CLI from your project folder:

```bash
npx skills add MagneticProxy/magneticproxy-amazon-product-research-skill --skill amazon-product-research
```

Select your agent when prompted. For a non-interactive installation, add the appropriate agent flag, for example `--agent codex` or `--agent claude-code`. Review installed instructions and scripts before running them. Installation does not grant browser tools, credentials or a subscription. A plain chat can read the instructions but may not install or operate the product.

The complete skill folder is the canonical package, including references and templates. A lone downloaded `SKILL.md` omits those files; use the repository installation or copy the complete folder into your agents supported skills directory. An MCP is not required or assumed.

## Product setup is included

Start with this use-case skill. During onboarding, your agent recommends and prepares the official [Magnetic Proxy product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills) for the product step, reusing it if already available. You do not need to install it separately before starting. The [onboarding guide](skills/amazon-product-research/references/brand-onboarding.md) covers supported installation, loading instructions when installation is unavailable, and account/signup guidance.

Installing files alone does not run the product: start the skill with a task. Account access, browser tools and any paid purchase remain separate, and the agent reports what it actually completed.

## From install to first useful result

1. **Start from this use case.** Follow [the included product onboarding](skills/amazon-product-research/references/brand-onboarding.md). The agent reuses or prepares `magneticproxy` during this conversation; the user does not need to install it beforehand. Confirm the browser/computer or authorized client capability actually available.
2. **Log in or sign up.** Open [Magnetic Proxy](https://app.magneticproxy.com/#/my-proxies). Reuse your account; otherwise use the visible Sign up flow. Complete authentication yourself without pasting credentials into the conversation.
3. **Choose capacity for the job.** Inspect available Capsules and GB. For permitted catalog, product and offer research, assess Web Scraping first; use Price Monitoring for recurring checks of a defined comparable watchlist. Check current target restrictions. A supplied or licensed export can be compared without consuming proxy traffic. Start with existing suitable capacity. If capacity is insufficient, compare [current plans](https://www.magneticproxy.com/pricing) and recommend the smallest suitable option from observed pilot usage. Follow its current Choose Plan checkout link; do not hardcode a price, discount or checkout token.
4. **Approve any purchase.** Show Capsule, capacity, billing period and current cost before purchase. Continue paid checkout only when the user explicitly authorizes that transaction. A skill installation is not purchase approval.
5. **Prove the route.** Configure the current product, verify the exit in the same browser/client and run a bounded permitted sample. Expand only within the agreed scope. If the approved data route does not need a proxy, explain that and do not invent a purchase requirement.

## Try this task

> Compare the public Amazon US and UK listings for these two blender models, including the 1.5 L variant, seller, displayed price, shipping, and availability.

**Bring:** User-approved Amazon product URLs or ASINs, product attributes to compare, target marketplaces/countries, and a small collection scope.

**Illustrative result:** Keep the 1.5 L models in the attribute matrix, exclude 1.2 L from exact-variant comparison, and declare no landed-price winner. Regional live checks remain pending unless the approved route and proxy exit are observed.

Read the [complete workflow](skills/amazon-product-research/SKILL.md) for source access, execution and decision rules.

## Common questions

### Does this Amazon scraping skill download the full catalog?

No. It supports bounded Amazon product research using approved access or authorized records. Magnetic Proxy supplies a permitted geographic route; it does not grant Amazon scraping permission or estimate sales.

### Why use Magnetic Proxy here?

Magnetic Proxy provides the configured geographic connection for permitted live regional checks. The skill adds comparable observations and a decision-ready deliverable. Supplied-data analysis can proceed without pretending that a live proxy check occurred.

### Is signup or a paid plan required?

An account is required to operate the product. Use available account capacity first. A paid plan is needed only when the requested operation requires capacity or features the account does not have; consult the current product pricing. Installing this repository does not start a paid subscription.

### Has the live workflow been verified?

Public preview: package checks and controlled examples are available; live destination coverage remains pending. See the [latest QA evidence](QA-2026-09-29.md) for the observed sample, deliverables and remaining gates. Installation and CI do not establish live destination access.

## Access and privacy

Amazon collection requires an approved Amazon access route or express permission for the requested scope. When unavailable, work from licensed or user-provided product records and leave live regional collection pending.

Check the destination’s terms, access permission, and rate limits before collection. A public URL and a successful proxy connection are not authorization to scrape. Stop on access denials or challenges; do not rotate to evade them. [Magnetic Proxy documentation](https://www.magneticproxy.com/documentation) explains routing and restricted targets.

Magnetic Proxy is not affiliated with, endorsed by, or sponsored by Amazon. References to Amazon describe the third-party use case.

## Related resources and support

- [Magnetic Proxy product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills) for setup and product operation.
- [Magnetic Proxy Amazon use case](https://www.magneticproxy.com/use-cases/amazon-proxies?utm_source=github&utm_medium=agent_skill&utm_campaign=amazon-product-research) for product context.
- [Report a reproducible issue](https://github.com/MagneticProxy/magneticproxy-amazon-product-research-skill/issues) using redacted or synthetic examples. For account, billing or service issues, use support inside the product.
- [Contribution guide](CONTRIBUTING.md) and [security guidance](SECURITY.md).

This repository documents a specific task; it does not guarantee search rankings, AI citations, delivery, platform access or commercial results. Third-party names identify the workflow and do not imply endorsement.

## License

Original instructions and code are available under the [MIT License](LICENSE). Product subscriptions, service access and third-party data remain subject to their respective terms. This license does not grant trademark rights or permission to collect third-party content.

## Latest QA review

Read the [2026-09-29 QA review](QA-2026-09-29.md) for executed checks, repaired behavior, consolidation decisions and the exact live-testing boundary.
