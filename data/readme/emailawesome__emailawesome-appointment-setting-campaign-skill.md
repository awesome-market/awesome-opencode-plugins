# Appointment Setting Campaign Preparation with Email Awesome

**Official Email Awesome agent skills** · Published and maintained by [EmailAwesome](https://github.com/EmailAwesome), the official Email Awesome GitHub organization. [Visit Email Awesome](https://www.emailawesome.com/).

A client-reviewable campaign brief and rep handoff with qualified segments, verification ledger, reply-routing rules, and meeting-fit criteria. This Agent Skill helps **appointment-setting agencies preparing a campaign for a specific client and sdr team** prepare an evidence-based result using Email Awesome for email address verification before first contact.




## Release status

Public preview: the INVALID/exclusion path has a real product export and a controlled business deliverable; the live positive-contact path remains pending. Read the [dated QA report](QA-2026-09-29.md) before relying on a particular execution path.


## What you get

- Define a qualified meeting for each agency client
- Verify contact readiness before the SDR handoff
- Prepare qualification questions, reply routes and approved messaging

Start with [the worked example](skills/appointment-setting-campaign-prep/references/worked-example.md), the [deliverable template](skills/appointment-setting-campaign-prep/assets/deliverable-template.md) and the [output columns](skills/appointment-setting-campaign-prep/assets/output.csv).

## Install and start

Copy this prompt into an agent that supports skill installation:

> Review and install `appointment-setting-campaign-prep` from https://github.com/EmailAwesome/emailawesome-appointment-setting-campaign-skill. Start its included Email Awesome product onboarding and help me with: [my task]. Reuse context and any suitable installed product skill or account; ask only for decisive missing information. Confirm what you can actually install or operate, use existing capacity first and obtain approval before any paid purchase. Begin with a bounded sample and report observed results and pending work.

Or use the Skills CLI from your project folder:

```bash
npx skills add EmailAwesome/emailawesome-appointment-setting-campaign-skill --skill appointment-setting-campaign-prep
```

Select your agent when prompted. For a non-interactive installation, add the appropriate agent flag, for example `--agent codex` or `--agent claude-code`. Review installed instructions and scripts before running them. Installation does not grant browser tools, credentials or a subscription. A plain chat can read the instructions but may not install or operate the product.

The complete skill folder is the canonical package, including references and templates. A lone downloaded `SKILL.md` omits those files; use the repository installation or copy the complete folder into your agents supported skills directory. Browser operation does not require MCP. The product skill centralizes the current optional MCP guide; configuration and authorization are separate from installing this repository.

## Product setup is included

Start with this use-case skill. During onboarding, your agent recommends and prepares the official [Email Awesome product skill](https://github.com/EmailAwesome/emailawesome-email-verification-agent-skills) for the product step, reusing it if already available. You do not need to install it separately before starting. The [onboarding guide](skills/appointment-setting-campaign-prep/references/brand-onboarding.md) covers supported installation, loading instructions when installation is unavailable, and account/signup guidance.

Installing files alone does not run the product: start the skill with a task. Account access, browser tools and any paid purchase remain separate, and the agent reports what it actually completed.

## From install to first useful result

1. **Start from this use case.** Follow [the included product onboarding](skills/appointment-setting-campaign-prep/references/brand-onboarding.md). The agent reuses or prepares `emailawesome` during this conversation; the user does not need to install it beforehand. Confirm the browser/computer or authorized client capability actually available.
2. **Log in or sign up.** Open [Email Awesome](https://app.emailawesome.com/) or [create an account](https://app.emailawesome.com/signup?plan=free_trial). Reuse an existing account. Complete authentication yourself; do not share passwords in chat.
3. **Use existing credits first.** Follow the prepared product skill’s current account and capacity guidance. Inspect monthly allowance, purchased balance and the usable total or batch estimate. Exclude suppressed records before an authorized upload. A free allowance depends on the actual account; do not promise a fixed promotion.
4. **Resolve a real capacity gap.** Compare the currently offered one-time top-up with a monthly plan according to volume and frequency; a larger batch does not automatically require a subscription upgrade. Use the product skill for current terms, transaction authorization and post-payment balance/resume checks. No purchase is implied by installing this skill.
5. **Verify and reconcile.** Run the agreed batch, wait for final results and join them to source IDs. Preserve VALID, INVALID, CATCH_ALL, UNKNOWN, failed, excluded and pending independently. Verification is the product step; campaign drafts and business decisions are the skills output, and sending is a separate action.

## Try this task

> Prepare a client campaign for 80 approved HR software prospects. A meeting counts only if the buyer manages 200+ employees in the US. Verify the list and give SDRs a handoff and reply rules.

**Bring:** Client offer and proof, meeting qualification rules, approved target accounts or lead list, rep capacity, territory, and handoff owner.

**Illustrative result:** Keep company qualification and email result separate. Exclude the first from this campaign by client criteria and hold the second for address review. Deliver qualification questions and a rep handoff without booking a meeting.

Read the [complete workflow](skills/appointment-setting-campaign-prep/SKILL.md) for source access, execution and decision rules.

## Common questions

### How is this different from a cold email skill?

This workflow centers on a client-specific qualified-meeting definition, rep ownership and reply routing. The cold email skill centers on the campaign narrative and touch sequence.

### Why use Email Awesome here?

Email Awesome checks the supplied addresses before first contact. The skill connects those observed results to this business workflow, while keeping message relevance, consent and suppression separate.

### Is signup or a paid plan required?

An account is required to operate the product. Use available account capacity first. A paid plan is needed only when the requested operation requires capacity or features the account does not have; consult the current product pricing. Installing this repository does not start a paid subscription.

### Has the live workflow been verified?

Public preview: the INVALID/exclusion path has a real product export and a controlled business deliverable; the live positive-contact path remains pending. See the [latest QA evidence](QA-2026-09-29.md) for the observed sample, deliverables and remaining gates. Installation and CI do not establish live destination access.

## Access and privacy

The user must have authority to process and submit each list and to share any client deliverable. A verified address does not establish consent or permission to contact. Sender rules vary by jurisdiction; see the [FTC CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) and [ICO B2B marketing guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/). Keep contact data and credentials out of this public repository and issues.

## Related resources and support

- [Email Awesome product skill](https://github.com/EmailAwesome/emailawesome-email-verification-agent-skills) for setup and product operation.
- [Email Awesome Appointment Setters use case](https://www.emailawesome.com/use-cases/appointment-setters?utm_source=github&utm_medium=agent_skill&utm_campaign=appointment-setting-campaign-prep) for product context.
- [Report a reproducible issue](https://github.com/EmailAwesome/emailawesome-appointment-setting-campaign-skill/issues) using redacted or synthetic examples. For account, billing or service issues, use support inside the product.
- [Contribution guide](CONTRIBUTING.md) and [security guidance](SECURITY.md).

This repository documents a specific task; it does not guarantee search rankings, AI citations, delivery, platform access or commercial results. Third-party names identify the workflow and do not imply endorsement.

## License

Original instructions and code are available under the [MIT License](LICENSE). Product subscriptions, service access and third-party data remain subject to their respective terms. This license does not grant trademark rights or permission to collect third-party content.

## Latest QA review

Read the [2026-09-29 QA review](QA-2026-09-29.md) for executed checks, repaired behavior, consolidation decisions and the exact live-testing boundary.
