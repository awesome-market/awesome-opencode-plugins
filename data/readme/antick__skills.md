# Antick Skills

49 skills for AI coding agents: building, debugging, code review and pull
requests, refactoring, dependency upgrades, security, database and performance
audits, tests and CI, releases, documentation, workstation upkeep, and clear writing.

[Install](#install) · [All skills](SKILLS.md)

## Install

```sh
npx skills@latest add antick/skills --global
```

A menu opens. Pick the skills you want and the agents to install them in.
Restart your agents afterwards.

## Update

```sh
npx skills@latest update --global
```

`update` refreshes only the skills you already installed, and only from the
`main` branch on GitHub. Changes that are still on another branch or in an open
pull request are not picked up. It also never installs skills that were added to
the repository after your install. To get new skills, run the install command
again and pick them in the menu:

```sh
npx skills@latest add antick/skills --global
```

To try a branch before it is merged, install from it with
`npx skills@latest add antick/skills#<branch> --global`. Skills installed that
way keep following that branch on `update`, so reinstall from `antick/skills`
once it is merged.

Or ask your agent with `$update-skills`. It runs the update, lists skills added
or removed upstream and skills that follow a branch, and asks before it installs
or removes anything.

## Remove

```sh
npx skills@latest remove --global
```

A menu opens. Pick the skills to remove. Use this to clear out skills that were
renamed: `repo-disk-cleanup` (now `reclaim-dev-space`), `save-window-layout` (now
`save-omarchy-window-layout`), `update-ai-tools`, `manage-ai-tools`, or
`ai-harness-setup` (now `ai-tools-update`), and `upgrade-dependencies` (now `dependency-upgrade-minor`
and `dependency-upgrade-major`).

These commands use the [skills.sh](https://skills.sh) CLI. It sends anonymous usage
data; set `DISABLE_TELEMETRY=1` to turn that off. Avoid its `--all` flag
with `--global`: it targets every agent the CLI knows, and some of them can't
install globally, so you get dozens of errors.

## Skills

| Skill | What it does |
| --- | --- |
| [antick](skills/antick/SKILL.md) | List every Antick skill by area with installed status, or recommend one for a task |
| [skill-review](skills/skill-review/SKILL.md) | Review skills and agent instructions for conflicts and redundant confirmations. Propose edits before changes. |
| [plan-review](skills/plan-review/SKILL.md) | Review and revise plans against requirements and evidence before execution |
| [code-review](skills/code-review/SKILL.md) | Review changes or a PR against its requirements; numbered task and code health findings. Read-only. |
| [submit-review](skills/submit-review/SKILL.md) | Post review findings as inline PR comments and mark the PR draft |
| [build-review-loop](skills/build-review-loop/SKILL.md) | Build your issues in parallel, self-review each PR, and fix until clean |
| [code-build](skills/code-build/SKILL.md) | Build features and fixes in meaningful commits and finish with a draft PR |
| [electron-app](skills/electron-app/SKILL.md) | Build secure Electron apps with native behavior and deliberate text selection |
| [code-debug](skills/code-debug/SKILL.md) | Find a bug's root cause, evidence, and fix without changing code. Read-only. |
| [sync-branch](skills/sync-branch/SKILL.md) | Merge the latest `main`, or a branch you name, into a PR and resolve conflicts |
| [commit-message](skills/commit-message/SKILL.md) | Write short commit messages in the repository's convention |
| [pr-description](skills/pr-description/SKILL.md) | Write plain-language PR titles and descriptions with technical detail |
| [create-issue](skills/create-issue/SKILL.md) | File GitHub issues that match repo conventions, without duplicates |
| [branch-status](skills/branch-status/SKILL.md) | Count branches and list merged ones that are safe to delete. Read-only. |
| [spec-status](skills/spec-status/SKILL.md) | List OpenSpec changes whose implementation already reached `main`. Read-only. |
| [code-refactor](skills/code-refactor/SKILL.md) | Refactor auth, state, SDKs, routing, types, and performance with regression tests |
| [code-audit](skills/code-audit/SKILL.md) | Rank the biggest safe simplifications in a repository. Read-only. |
| [code-hardening](skills/code-hardening/SKILL.md) | Run all 20 codebase hardening checks with evidence and explicit coverage |
| [code-security](skills/code-security/SKILL.md) | Audit security; fix vulnerabilities and harden supply chains when asked |
| [app-pentest](skills/app-pentest/SKILL.md) | Penetration-test the current app and reproduce exploitable vulnerabilities |
| [database-audit](skills/database-audit/SKILL.md) | Audit schemas, migrations, queries, indexes, and access. Read-only. |
| [performance-audit](skills/performance-audit/SKILL.md) | Find queries, jobs, and polling that slow down as data grows. Read-only. |
| [github-actions-security-audit](skills/github-actions-security-audit/SKILL.md) | Audit GitHub Actions and CI security across every repo of an account. Read-only. |
| [github-actions-lock](skills/github-actions-lock/SKILL.md) | Set up and maintain GitHub Actions lockfiles with CI verification |
| [soc2-readiness](skills/soc2-readiness/SKILL.md) | Assess SOC 2 readiness and report gaps and missing evidence in chat. Read-only. |
| [dependency-upgrade-minor](skills/dependency-upgrade-minor/SKILL.md) | Apply safe patch and minor updates, pinned exactly, and verify |
| [dependency-upgrade-major](skills/dependency-upgrade-major/SKILL.md) | Upgrade major versions with planned migrations and full verification |
| [dependency-audit](skills/dependency-audit/SKILL.md) | Find outdated, end-of-life, and vulnerable dependencies in every source. Read-only. |
| [dependency-override-cleanup](skills/dependency-override-cleanup/SKILL.md) | Find and remove stale overrides, resolutions, patches, and audit waivers |
| [test-suite-hardening](skills/test-suite-hardening/SKILL.md) | Fix flaky tests, strengthen coverage, and prove changes with real regressions |
| [ci-cd-triage](skills/ci-cd-triage/SKILL.md) | Diagnose and repair failing builds and pipelines |
| [accessibility-audit](skills/accessibility-audit/SKILL.md) | Find accessibility barriers; fix them when asked |
| [documentation-generation](skills/documentation-generation/SKILL.md) | Write source-backed docs, architecture maps, and onboarding guides |
| [deep-wiki-html](skills/deep-wiki-html/SKILL.md) | Create or refresh offline HTML wikis, document explainers, and architecture maps with optional JSON |
| [public-desktop-release](skills/public-desktop-release/SKILL.md) | Ship signed Apple Silicon apps through GitHub Releases with auto-updates and a separate dev app |
| [private-desktop-release](skills/private-desktop-release/SKILL.md) | Set up signed private macOS releases, licensed updates, and device controls |
| [vercel-domain-cleanup](skills/vercel-domain-cleanup/SKILL.md) | Fix Vercel and www redirects and DNS warnings, then verify every site |
| [setup-vercel-analytics](skills/setup-vercel-analytics/SKILL.md) | Set up Vercel Web Analytics, verify integration, and remind about dashboard activation |
| [reclaim-dev-space](skills/reclaim-dev-space/SKILL.md) | Report disk used by worktrees, Docker, test databases, and agent leftovers; delete only what you confirm |
| [system-storage-audit](skills/system-storage-audit/SKILL.md) | Audit system storage or a chosen folder and compare private snapshots |
| [ai-tools-update](skills/ai-tools-update/SKILL.md) | Update installed AI tools and runtimes; install missing ones only when you ask |
| [save-omarchy-window-layout](skills/save-omarchy-window-layout/SKILL.md) | Save Omarchy/Hyprland window layout for restoring at login |
| [concise](skills/concise/SKILL.md) | Short answers that keep the important parts |
| [make-sense](skills/make-sense/SKILL.md) | Clear, plain explanations with as much detail as needed |
| [simplify](skills/simplify/SKILL.md) | Write in ASD-STE100 Simplified Technical English |
| [interview](skills/interview/SKILL.md) | Get to know you and save only what you approve to memory |
| [new-skill](skills/new-skill/SKILL.md) | Create or change skills that match the existing set and every catalogue |
| [use-chrome](skills/use-chrome/SKILL.md) | Work in your already-open Chrome in background tabs, with one Allow prompt per connection and no substitute browser |
| [update-skills](skills/update-skills/SKILL.md) | Update your installed skills, then list new skills to add and removed skills to delete |

[SKILLS.md](SKILLS.md) maps common tasks to the skill and guide that covers them.
Each skill's `SKILL.md` is the source of truth for what it does.

A few behave differently from the rest:

- **`ai-tools-update`, `save-omarchy-window-layout`, and `update-skills`** run
  only when you call them by name. `ai-tools-update` only updates by default; say
  "also install missing tools" to install. Its
  [tool list](skills/ai-tools-update/references/tools.md) covers 21 entries and
  runtimes. `save-omarchy-window-layout` needs an existing Omarchy/Hyprland setup.
  `update-skills` asks before it installs or removes any skill.
- **`reclaim-dev-space`** shows its findings in chat first and deletes nothing
  until you pick items from that report.
- **`system-storage-audit`** saves private metadata snapshots and compares each audit
  with the previous matching run. It audits accessible local system storage by
  default; naming a folder limits scanning and extra checks to that folder.
  The first run for each scope establishes a baseline. Cleanup remains separate.
- **`interview`** saves to memory only what you approve, and never to the repository.
- **`code-build`** commits in meaningful steps, pushes a branch, and opens a draft
  PR unless you ask for local-only work. **`submit-review`**, **`sync-branch`**, and
  **`build-review-loop`** post to GitHub or push branches as part of their job.
- **`code-debug`** never changes code, and asks before any browser action that
  changes data.
- **`app-pentest`** actively tests the current app and reproduces vulnerabilities
  on the established test target. Application fixes and PRs are separate requests.

## Use a skill

Call it by name. The syntax depends on your agent:

| Agent | Syntax |
| --- | --- |
| Codex | `$code-review` |
| Claude Code, OpenCode | `/code-review` |
| Pi | `/skill:code-review` (or `/code-review` with the Pi extension) |

Add your request after the name:

```text
$code-review Review my uncommitted changes.
$code-build Add search to this Astro site.
$setup-vercel-analytics Add Web Analytics to this app and remind me about Vercel dashboard activation.
$electron-app Build an Electron app with native desktop behavior.
$reclaim-dev-space Find what's eating my disk.
$code-debug Find out why login fails after a password reset.
$app-pentest Penetration-test this app and report reproducible vulnerabilities.
$build-review-loop Build issues 12 and 14, self-review each PR, and fix until clean.
$antick
$antick free up disk space taken by worktrees and node_modules
```

Not sure which skill to use? Run `antick` with your task.

A skill only gives your agent instructions. The agent's own permissions still
decide what it can do. Audits and reviews report by default; ask for changes
when you want them.

### Plugins and adapters

Installing copies skill folders only. These are set up separately:

- **Claude Code and Codex:** plugin manifests in `.claude-plugin/` and
  `.codex-plugin/`, including marketplace files. They're in the Git repo, not the
  npm package.
- **OpenCode:** [.opencode/plugins/skills.mjs](.opencode/plugins/skills.mjs) adds
  the skills folder and a slash command per skill. See [opencode.json](opencode.json).
- **Pi:** [pi-extension/index.js](pi-extension/index.js) adds `/code-review`-style
  commands that forward to `/skill:code-review`. The `pi` field in `package.json`
  loads it.

## Contribute

Edit `skills/<name>/SKILL.md`; keep supporting guides next to it. When you add,
rename, or remove a skill, update `SKILLS.md`, `packs.json`, the plugin manifests,
`pi-extension/commands.json`, `skills/antick/references/catalogue.md`, and the
website catalogue (`website/src/lib/catalog.ts` or `engineering-catalog.ts`, plus
`skill-icons.ts`). The tests fail if any of them disagree. The `new-skill` skill
walks through all of this.

```sh
npm test
node --test website/tests/*.test.mjs
npm pack --dry-run
```

With the website's dependencies installed, `npm run check --prefix website` also
catches a missing icon.

To try your local changes, install from the checkout with `node scripts/install.mjs`.
It opens the same kind of menu; `--help` lists its options.

The website lives in `website/`; see [website/README.md](website/README.md).

## License

[MIT](LICENSE)
