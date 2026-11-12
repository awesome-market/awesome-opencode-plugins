# good-repo

A skill for making GitHub repositories easier to evaluate, adopt, contribute to, and trust.

[![skills.sh](https://skills.sh/b/adewale/good-repo)](https://skills.sh/adewale/good-repo/good-repo)

`good-repo` audits a repository as a product surface: README, proof, examples, install path, repo structure, GitHub metadata, automation, maintenance signals, and community defaults. It is designed to pair with [`good-readme`](https://github.com/adewale/good-readme): let `good-readme` handle the README deeply; use `good-repo` for everything around it.

## Why this exists

Great code still loses users when the repo gives weak signals: no live demo, missing license, stale screenshots, vague GitHub description, no quick start, no contribution path, or no proof that the project actually works.

The first reference models are:

- [`nutlope/hallmark`](https://github.com/nutlope/hallmark) — a productized skill repo with a tight README, visible examples, live demo, install instructions, packaged skill entry point, modular references, quality gates, roadmap, license, and enough proof for a visitor to decide quickly.
- [`adewale/good-pr`](https://github.com/adewale/good-pr) — a small operational skill repo with real-pain origin, trigger-rich `SKILL.md`, PR templates, self-review checklist, readiness script, changelog, and evals.

## Install

```sh
npx skills add adewale/good-repo
```

Or copy `skills/good-repo/` into your agent skills directory.

For Pi package installs, the `package.json` includes `pi.skills`; for Claude/plugin installs, `.claude-plugin/marketplace.json` points to `./skills/good-repo`.

## Agent compatibility

The installable skill directory is `skills/good-repo`. It uses the Agent Skills `SKILL.md` format and is configured for Codex, OpenCode, Pi, Gemini CLI, and Claude Code.

| Agent/client | Install or use |
|---|---|
| Codex | `cp -R skills/good-repo ~/.codex/skills/good-repo` |
| OpenCode | `cp -R skills/good-repo ~/.config/opencode/skills/good-repo` or use `.opencode/skills/good-repo` in a project |
| Pi | `pi install https://github.com/adewale/good-repo` or `pi --skill skills/good-repo` |
| Gemini CLI | `gemini skills install https://github.com/adewale/good-repo --path skills/good-repo` or copy to `.gemini/skills/good-repo` |
| Claude Code | `npx skills add adewale/good-repo` or copy to `.claude/skills/good-repo` |

## Usage

Ask your coding agent from inside a repository:

```text
Audit this repo for GitHub effectiveness
```

```text
Configure this repo for maximum effectiveness
```

```text
Make this repo launch-ready; use good-readme for the README
```

```text
good-repo audit https://github.com/nutlope/hallmark
```

```text
good-repo explain https://github.com/adewale/good-pr
```

```text
good-repo owner-audit adewale
```

## What it checks

- **README/front door** — clarity, value proposition, install, usage, examples, honesty; delegated to `good-readme` when available.
- **Proof** — screenshots, live demos, examples, evals, tests, sample outputs, reproducible recipes.
- **Adoption path** — prerequisites, quick start, package metadata, release/download path, local dev setup.
- **Repository architecture** — docs split, examples, skill/package entry points, references, scripts, evals, generated assets, fixtures.
- **GitHub metadata** — description, homepage, topics, social preview, license, issue/discussion/wiki settings.
- **GitHub-official baseline** — README, Community Profile health/files, license, contribution guidelines, issue/PR templates, security policy, CI/workflows, and large-file hygiene.
- **Policy-check context** — Repolinter-style findings translated through repo class and maturity instead of copied blindly.
- **Trust signals** — roadmap, changelog, maintenance status, contribution guidance, security policy, code owners.
- **Automation** — CI, release workflow, dependency updates, docs/examples validation.
- **Popularity/adoption context** — stars, forks, activity, contributor network, and quality signals without confusing popularity for quality.

## Example audit output

```markdown
## Repo Effectiveness Audit

**Project:** good-repo
**Class:** agent skill / repo-effectiveness auditor
**Score:** 85 / 100
**Rating:** Strong

### Snapshot
- README/front door: clear purpose, install path, usage prompts, and relationship to good-readme.
- Proof: full behavior eval results, fixture tests, sample audits, and lessons learned are present.
- Adoption path: install command, `package.json`, `.claude-plugin`, and `pi.skills` metadata are configured.
- GitHub metadata: description and topics are set, issues are enabled, wiki is disabled, and a local MIT `LICENSE` file is present; no canonical homepage yet.
- Trust/maintenance: changelog, contributing guide, PR template, CI, and validation scripts exist; issue templates/support/security are still missing.

### Top strengths
1. Correct skill packaging — evidence: `skills/good-repo/SKILL.md`, `skills/good-repo/references/`, `.claude-plugin/marketplace.json`.
2. Behavior proof is credible — evidence: `evals/evals.json`, `evals/run_eval.py`, `docs/eval-results-2026-06-04.md`.
3. Repo-only artifacts are separated from runtime files — evidence: `docs/`, `evals/`, `.github/` live outside `skills/good-repo/`.

### Priority improvements
1. High impact — GitHub Community Profile is not complete — smallest fix: add `.github/ISSUE_TEMPLATE/bug_report.yml` and `.github/ISSUE_TEMPLATE/eval_case.yml`.
2. Medium impact — support/security expectations are implicit — smallest fix: add `SUPPORT.md` and `SECURITY.md` with honest scope.
3. Polish — README does not yet compare `good-repo` with Community Profile, Repolinter, and OpenSSF Scorecard — smallest fix: add a short positioning section.

### Scores by category
| Category | Score | Max |
| --- | ---: | ---: |
| Front door + README | 18 | 20 |
| Proof + examples | 13 | 15 |
| Adoption + DX | 13 | 15 |
| Docs + architecture | 14 | 15 |
| GitHub metadata | 8 | 10 |
| Trust + governance | 10 | 15 |
| Automation + release | 9 | 10 |
| **Total** | 85 | 100 |

### Suggested implementation plan
1. Add issue templates for bug reports and new eval cases.
2. Add `SUPPORT.md` and `SECURITY.md` after confirming maintainer contact/scope.
3. Add a README section that positions `good-repo` against GitHub Community Profile, Repolinter, OpenSSF Scorecard, and package-health tools.
4. Re-run `npm run validate`, fixture evals, and the repo readiness script.
```

## What's included

| File | Purpose |
|------|---------|
| `skills/good-repo/SKILL.md` | Skill workflow, verbs, safety rails, output format |
| `skills/good-repo/scripts/check-repo-readiness.sh` | Mechanical repo readiness check |
| `skills/good-repo/scripts/audit-github-owner.py` | Owner/profile-wide GitHub audit script |
| `evals/evals.json` | Expected skill behaviors and regression cases |
| `evals/trigger-queries.json` | Trigger and near-miss cases for skill activation |
| `evals/shared-benchmark.json` | Skill Eval Harness manifest of record (CI-gated with `skill-eval-harness==0.6.0`) |
| `evals/run_eval.py` | Schema validator for `evals.json`/`trigger-queries.json`; its grader/benchmark only reproduce the frozen 2026-06-04 run |
| `evals/run_fixture_tests.py` | Fixture-level tests for mechanical repo readiness checks |
| `evals/fixtures/` | Tiny repos for homepage, license, and skill-layout regression checks |
| `evals/README.md` | Eval strategy for improving the skill |
| `skills.sh.json` | skills.sh repository-page grouping metadata |
| `docs/eval-results-2026-06-03.md` | First with-skill vs baseline smoke eval results |
| `docs/eval-results-2026-06-04.md` | Full behavior eval suite results with with-skill vs baseline comparison |
| `skills/good-repo/references/hallmark-exemplar.md` | What makes Hallmark an exemplary productized skill repo |
| `skills/good-repo/references/good-pr-exemplar.md` | What makes good-pr an exemplary small operational skill repo |
| `skills/good-repo/references/repo-anatomy.md` | Repo structure patterns by project type |
| `skills/good-repo/references/github-official-baseline.md` | GitHub's official docs baseline for healthy/discoverable repos |
| `skills/good-repo/references/community-profile-repolinter.md` | GitHub Community Profile and Repolinter interpretation guidance |
| `skills/good-repo/references/popularity-signals.md` | Research-backed guidance on repo quality, popularity, stars, and adoption |
| `skills/good-repo/references/skill-repo-best-practices.md` | Agent Skill folder structure, packaging, eval, and marketplace guidance |
| `skills/good-repo/references/quality-checklist.md` | 100-point GitHub effectiveness rubric |
| `skills/good-repo/references/github-settings.md` | GitHub metadata, settings, and automation checklist |
| `skills/good-repo/references/anti-patterns.md` | Common repository smells and fixes |
| `docs/recipes.md` | Copy-paste prompts for audits, launch prep, and cleanup |
| `docs/sample-audits.md` | Scores and recommendations for a mixed GitHub sample |
| `docs/adewale-repos-assessment.md` | Owner-wide audit for `github.com/adewale` |
| `docs/adewale-recent-improvement-opportunities.md` | Recently modified `adewale` repos ranked by improvement opportunity |
| `docs/community-profile-repolinter-focus.md` | Focused comparison of GitHub Community Profile and Repolinter |
| `docs/multi-account-signal-assessment.md` | Cross-account audit of public repo portfolios and missed quality signals |
| `docs/lessons-learned.md` | Lessons from owner-wide and cross-account audits |
| `docs/repo-quality-popularity.md` | Research brief on whether repo quality affects popularity/adoption |
| `CONTRIBUTING.md` | Lightweight contribution guidance |
| `.claude-plugin/marketplace.json` | Claude plugin / skills CLI metadata |
| `.github/PULL_REQUEST_TEMPLATE.md` | Minimal PR checklist |
| `.github/workflows/ci.yml` | JSON, shell, link, and readiness validation |

## What gets installed vs repo-only

```text
skills/good-repo/                     Installable runtime skill
├── SKILL.md
├── references/
└── scripts/

evals/                                Repo-only behavior checks
docs/                                 Repo-only reports, recipes, and lessons
.github/                              Repo-only CI and contribution surfaces
.claude-plugin/                       Marketplace/plugin metadata
package.json                          npm/Pi package metadata
```

The runtime skill stays self-contained under `skills/good-repo/`. Reports, evals, CI, and contribution process stay outside the installable folder.

## Relationship to good-readme

`good-readme` is the README specialist. `good-repo` should not reimplement it when it is available. The intended stack is:

1. Run `good-readme` to create or improve the README.
2. Run `good-repo` to configure the rest of the repository.
3. Re-run both before launch or release.

## License

MIT — see [LICENSE](LICENSE).
