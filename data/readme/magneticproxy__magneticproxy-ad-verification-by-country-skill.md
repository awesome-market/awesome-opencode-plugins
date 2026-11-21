# Ad Verification by Country and Landing Page QA with Magnetic Proxy

**Official Magnetic Proxy agent skills** · Published and maintained by [MagneticProxy](https://github.com/MagneticProxy), the official Magnetic Proxy GitHub organization. [Visit Magnetic Proxy](https://www.magneticproxy.com/).

A regional QA matrix with observed exit, preview reference, final URL, redirect path, locale, offer and reproducible discrepancies. This Agent Skill helps **advertisers and agencies checking campaigns they own or are authorized to audit** prepare an evidence-based result using Magnetic Proxy for authorized residential routing and regional observations.




## Release status

Public preview: package checks and controlled examples are available; live destination coverage remains pending. Read the [dated QA report](QA-2026-09-29.md) before relying on a particular execution path.


## What you get

- Check regional landing redirects, language and advertised offer
- Compare authorized creative previews with the destination experience
- Give agencies reproducible defects by market and creative version

Start with [the worked example](skills/ad-verification-by-country/references/worked-example.md), the [deliverable template](skills/ad-verification-by-country/assets/deliverable-template.md) and the [output columns](skills/ad-verification-by-country/assets/output.csv).

## Install and start

Copy this prompt into an agent that supports skill installation:

> Review and install `ad-verification-by-country` from https://github.com/MagneticProxy/magneticproxy-ad-verification-by-country-skill. Start its included Magnetic Proxy product onboarding and help me with: [my task]. Reuse context and any suitable installed product skill or account; ask only for decisive missing information. Confirm what you can actually install or operate, use existing capacity first and obtain approval before any paid purchase. Begin with a bounded sample and report observed results and pending work.

Or use the Skills CLI from your project folder:

```bash
npx skills add MagneticProxy/magneticproxy-ad-verification-by-country-skill --skill ad-verification-by-country
```

Select your agent when prompted. For a non-interactive installation, add the appropriate agent flag, for example `--agent codex` or `--agent claude-code`. Review installed instructions and scripts before running them. Installation does not grant browser tools, credentials or a subscription. A plain chat can read the instructions but may not install or operate the product.

The complete skill folder is the canonical package, including references and templates. A lone downloaded `SKILL.md` omits those files; use the repository installation or copy the complete folder into your agents supported skills directory. An MCP is not required or assumed.

## Product setup is included

Start with this use-case skill. During onboarding, your agent recommends and prepares the official [Magnetic Proxy product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills) for the product step, reusing it if already available. You do not need to install it separately before starting. The [onboarding guide](skills/ad-verification-by-country/references/brand-onboarding.md) covers supported installation, loading instructions when installation is unavailable, and account/signup guidance.

Installing files alone does not run the product: start the skill with a task. Account access, browser tools and any paid purchase remain separate, and the agent reports what it actually completed.

## From install to first useful result

1. **Start from this use case.** Follow [the included product onboarding](skills/ad-verification-by-country/references/brand-onboarding.md). The agent reuses or prepares `magneticproxy` during this conversation; the user does not need to install it beforehand. Confirm the browser/computer or authorized client capability actually available.
2. **Log in or sign up.** Open [Magnetic Proxy](https://app.magneticproxy.com/#/my-proxies). Reuse your account; otherwise use the visible Sign up flow. Complete authentication yourself without pasting credentials into the conversation.
3. **Choose capacity for the job.** Inspect available Capsules and GB. For owned or authorized campaign landing checks, assess the current General Purpose offer and its available country controls. Do not buy or generate advertising impressions for QA. Start with existing suitable capacity. If capacity is insufficient, compare [current plans](https://www.magneticproxy.com/pricing) and recommend the smallest suitable option from observed pilot usage. Follow its current Choose Plan checkout link; do not hardcode a price, discount or checkout token.
4. **Approve any purchase.** Show Capsule, capacity, billing period and current cost before purchase. Continue paid checkout only when the user explicitly authorizes that transaction. A skill installation is not purchase approval.
5. **Prove the route.** Configure the current product, verify the exit in the same browser/client and run a bounded permitted sample. Expand only within the agreed scope. If the approved data route does not need a proxy, explain that and do not invent a purchase requirement.

## Try this task

> Check our approved campaign preview and the landing page for US, Mexico and Spain. The Spanish market should show Spanish copy and the EUR offer.

**Bring:** Campaign ID, approved creative or preview URL, expected landing URL, markets, language, offer and permitted test method.

**Illustrative result:** Report a reproducible landing-locale defect with creative version, final URL, time and evidence. Do not infer ad fraud or delivery share; no paid ad was clicked.

Read the [complete workflow](skills/ad-verification-by-country/SKILL.md) for source access, execution and decision rules.

## Common questions

### Does ad verification require clicking live paid ads?

No. Use approved preview/test methods and authorized destination URLs. This workflow does not generate paid impressions or clicks to test an advertisement.

### Why use Magnetic Proxy here?

Magnetic Proxy provides the configured geographic connection for permitted live regional checks. The skill adds comparable observations and a decision-ready deliverable. Supplied-data analysis can proceed without pretending that a live proxy check occurred.

### Is signup or a paid plan required?

An account is required to operate the product. Use available account capacity first. A paid plan is needed only when the requested operation requires capacity or features the account does not have; consult the current product pricing. Installing this repository does not start a paid subscription.

### Has the live workflow been verified?

Public preview: package checks and controlled examples are available; live destination coverage remains pending. See the [latest QA evidence](QA-2026-09-29.md) for the observed sample, deliverables and remaining gates. Installation and CI do not establish live destination access.

## Access and privacy

Use an official ad preview/test method or a campaign asset supplied by the advertiser. Check the ad platform’s terms before any automated access. Do not generate impressions or click a live paid ad merely to test it; do not automate an ad library, bypass a challenge, or inspect private campaign data without the owner’s access. Stop on access denial, CAPTCHA, `403`, or `429`. Test owned or explicitly authorized destination URLs only.

## Related resources and support

- [Magnetic Proxy product skill](https://github.com/MagneticProxy/magneticproxy-residential-proxy-agent-skills) for setup and product operation.
- [Product use cases](https://www.magneticproxy.com/use-cases/ad-verification-proxies?utm_source=github&utm_medium=agent_skill&utm_campaign=ad-verification-by-country) for product context.
- [Report a reproducible issue](https://github.com/MagneticProxy/magneticproxy-ad-verification-by-country-skill/issues) using redacted or synthetic examples. For account, billing or service issues, use support inside the product.
- [Contribution guide](CONTRIBUTING.md) and [security guidance](SECURITY.md).

This repository documents a specific task; it does not guarantee search rankings, AI citations, delivery, platform access or commercial results. Third-party names identify the workflow and do not imply endorsement.

## License

Original instructions and code are available under the [MIT License](LICENSE). Product subscriptions, service access and third-party data remain subject to their respective terms. This license does not grant trademark rights or permission to collect third-party content.

## Latest QA review

Read the [2026-09-29 QA review](QA-2026-09-29.md) for executed checks, repaired behavior, consolidation decisions and the exact live-testing boundary.
