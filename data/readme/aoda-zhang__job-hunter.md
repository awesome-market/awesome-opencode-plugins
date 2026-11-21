# Job Hunter

**Tell OpenCode what job you want. It searches the job platforms you configure — LinkedIn plus any other site you can reach in your own browser — opens each remaining vacancy, filters it against your config, and writes a daily Markdown shortlist.**

**English** · [简体中文](README.zh-CN.md) · [Deutsch](README.de.md)

## 1. What it does

Job Hunter is a small set of OpenCode instructions (one agent + three skills) plus one personal config file. There is no application code: no backend, database, CLI, CI or API key.

A run does four things:

1. **Searches** every platform listed in `sources` with the single query in `jobSearchPrompt`.
2. **Narrows** the results with each platform's own filters taken from your config: date posted, employment type, work mode, seniority and location.
3. **Inspects** each remaining vacancy page — the real posting, not just the search card — and skips postings that are closed or no longer accepting applications.
4. **Classifies and reports** every vacancy as matched, needs review, or not matched, then saves the result to `reports/daily/YYYY-MM-DD.md`.

It never applies for you, never messages recruiters, and never changes your account settings. It uses the browser session you are already logged in with.

## 2. How it works

```mermaid
flowchart TD
    A[job-hunter.config.json] --> B[Job Hunter agent]
    B --> C[Configured platforms<br/>sources: LinkedIn, Indeed, …]
    C --> D[Each platform's search<br/>jobSearchPrompt, verbatim]
    D --> D2[Each platform's own filters<br/>date, type, mode, seniority]
    D --> E[Open each vacancy page]
    E --> F{Job still open}
    F -->|closed| X[skipped and counted]
    F -->|open| G[Check title, employer, JD language,<br/>keywords, mode, type, seniority]
    G --> H[matched / review / not_matched]
    H --> I[reports/daily/YYYY-MM-DD.md]
```

The agent checks the dimensions in a fixed order and stops at the first confirmed mismatch. When the page does not clearly prove a match or a mismatch, the vacancy goes to **review** instead of being rejected.

## 3. What you need

| Requirement | Notes |
|---|---|
| OpenCode | installed, opened on this repository |
| Browser tool | a browser integration enabled in OpenCode; this repository does not install or configure one |
| Job platforms | every platform you list in `sources`, already logged in in that browser |
| Anything else | nothing — no Node.js, npm, database or CI |

## 4. Quick start

```bash
cp job-hunter.config.example.json job-hunter.config.json
```

Edit `job-hunter.config.json` — it is Git-ignored, so your preferences stay local:

1. **`jobSearchPrompt`** — one natural-language sentence: where, which role, which stack, how recent. This is the only query any platform receives.
2. **`countries` / `locations`** — where to search. Empty `locations` means the whole country.
3. **`jobTitles.include`** — the titles you accept; used for matching.
4. **`jdLanguages.include`** and **`technicalKeywords`** — the language and stack you can work with.
5. Optionally set `workModes`, `employmentTypes`, `seniority` and `excludeRecruiters`.

Then:

1. Open this folder in OpenCode.
2. Select the **Job Hunter** primary agent (`Tab` to switch agents).
3. Ask in plain language, e.g. *"Find today's jobs"* or *"Refresh the report, only remote roles"*.
4. The agent drives the browser, then writes `reports/daily/YYYY-MM-DD.md`. Open it and scan the tables.

You only ever talk to the Job Hunter agent. It loads `job-discovery` by itself; you never pick a skill manually.

> **One query only.** `jobSearchPrompt` is sent verbatim and is not rewritten from the config. Put the location and the stack into that sentence. `jobTitles` and `technicalKeywords` are used to *match* results, not to *search*.
>
> **Filters come from the config, not from the prompt.** Writing "last 24 hours" in the prompt is not reliable; the agent sets the platform's "Date posted" filter from `lookbackHours` and verifies it before reading results.

## 5. Configure your search

| Field | Required | What it does |
|---|---|---|
| `countries` | yes | Country-level scope, e.g. `["Germany"]`. Used to validate and describe the search scope, not to build the query. |
| `locations` | no | Optional cities inside those countries. Empty or absent = the whole country. |
| `lookbackHours` | yes | Posting window in hours. Drives each platform's date filter and is checked again on each posting. |
| `jobSearchPrompt` | yes | The one natural-language query, sent verbatim to every configured platform. |
| `jobTitles.include` | yes | Accepted title variants, used for matching and the card pre-filter. |
| `jdLanguages.include` | yes | Accepted JD languages, e.g. `["English"]`. |
| `jdLanguages.acceptGermanJdWithEnglishWorkingLanguage` | no | When `true`, a German JD still matches if it explicitly names English as the working, team or company language. |
| `technicalKeywords.include` | yes | Technologies to look for in the JD. |
| `technicalKeywords.matchMode` | yes | `any` = one keyword is enough; `all` = every keyword must appear. |
| `isNeededCover` | no | When `true`, draft a cover letter from `cover-letter-template.md` for every matched job whose JD requires a cover letter. Saved under `reports/cover-letters/<company-slug>/<jobId>.md`. Default `false`. |
| `workModes` | no | `Remote` / `Hybrid` / `On-site`. All three, empty or absent = filter off. |
| `employmentTypes` | no | `Full-time` / `Part-time` / `Contract` / `Temporary` / `Internship` / `Volunteer`. All of them, empty or absent = filter off. |
| `seniority.include` | no | `Junior` / `Mid-level` / `Senior` / `Lead`. Empty, absent or all levels = filter off. |
| `excludeRecruiters` | no | `true` excludes confirmed staffing agencies hiring for a third-party client; unclear cases go to review. |
| `sources` | yes | Platforms to search, in order. Dedicated references ship for `LinkedIn`, `Indeed` and `Glassdoor` (e.g. `glassdoor.de`). A platform without a reference is skipped, not guessed — add one from `references/_template.md`. |
| `linkedinPremium` | no | Set `true` when your LinkedIn account is Premium: matched jobs showing the `You'd be a top applicant` prompt then form a leading group. `false` or absent ignores the prompt. |
| `reportRepo` | no | Optional Git URL. When set, the day's report is committed and pushed there after each run. |
| `notifications.email` | no | Optional SMTP block for run-summary emails. Off by default; when `enabled`, one summary is sent after each run. |
| `schedule` | no | Daily launchd job: `enabled`, `time` (`HH:MM`, local time) and `timezone`. |
| `sortBy` / `sortDirection` | no | Ordering inside the priority group and each city. `companySize` with `asc` or `desc`; omit for discovery order. |
| `preferredReportLanguage` | no | Language of the daily report and the summary email body, e.g. `English`, `German`, `Chinese`. Defaults to `English`. It never affects the search query, matching, index keys or audit fields; the email subject stays ASCII. |

Notes:

- `lookbackHours` is a number. It is mapped to the closest date filter that platform offers and that fully covers the window (on LinkedIn: ≤24 → past 24 hours, ≤168 → past week, ≤720 → past month), and each posting is checked again on its own page.
- A dimension is active only when you restrict it. Listing all three work modes, all employment types, or leaving `seniority.include` empty means "no filter".
- Scope vs filter: country, city and posting date decide *what to search*. Only the dimensions above decide whether a vacancy *matches*.

**Schedule.** Editing `schedule` in the config does not change launchd by itself. After changing `enabled`, `time` or `timezone`, run `.opencode/scripts/apply-schedule.sh` (or ask the agent to change the schedule). launchd uses the Mac's local time, so `timezone` must match the system timezone. Setting `enabled: false` unloads and removes the job.

## 6. How jobs are filtered

Checks run in this order and stop at the first confirmed mismatch:

1. Posting validity — 404, redirect away from the job, "no longer accepting applications".
2. Job title — same role family as `jobTitles.include`.
3. Poster type — only when `excludeRecruiters` is `true`.
4. JD language — the language actually used in the description.
5. Technical keywords — following `matchMode`.
6. Work mode — only when `workModes` is a real subset.
7. Employment type — only when `employmentTypes` is a real subset.
8. Seniority — only when `seniority.include` is a real subset.

| Result | Meaning | Where it appears |
|---|---|---|
| `matched` | every active dimension is confirmed on the page | main table, grouped by city |
| `review` | the page does not prove match or mismatch (short, missing, truncated, mixed language) | review table |
| `not_matched` | at least one active dimension clearly fails | excluded table with the exact reason |

Before opening a page, the agent does a cheap card pass: titles that clearly name a different function (sales, marketing, finance, HR, design, SAP admin, …) or that are clearly outside your country/city are skipped and only counted. Ambiguous, truncated or multi-role titles are still opened.

There is no score, no ranking by candidate fit, and no filtering on salary, years of experience, visa or industry. The only priority signal is the platform's own prompt: with `linkedinPremium`, LinkedIn matches showing **`You'd be a top applicant`** are listed first, and a failed check still excludes the job.

## 7. Reports

| Output | Path |
|---|---|
| Daily discovery | `reports/daily/YYYY-MM-DD.md` |
| Cover letter drafts | `reports/cover-letters/<company-slug>/<jobId>.md` |
| Interview preparation | `reports/interviews/<company-slug>/` |

The daily report lists the platforms searched, then matched jobs (prompted LinkedIn Premium matches first, then the rest grouped by city and sorted by company size), a review table when needed, and the excluded jobs with the exact reason last. Every table has a `Source` column so a mixed-platform run stays readable.

**Matched and excluded tables** each include two extra application-process columns:

- **Easy Apply** — `Yes`/`No`/`Unknown`: whether the page shows a one-click apply button on the platform (e.g. LinkedIn "Easy Apply", Indeed "Indeed Apply"). Informational only, never used as a filter.
- **Cover letter** — `Yes`/`No`/`Unknown`: whether the page or application form explicitly says a cover letter is required. When `Yes`, the agent drafts a cover letter from `cover-letter-template.md` and saves it under `reports/cover-letters/<company-slug>/<jobId>.md` for your manual review and sending. Never auto-submitted.

Reports follow the fixed format reference at `.opencode/skills/job-discovery/references/daily-report-format.md` and are written in `preferredReportLanguage` (default `English`). The reference fixes the structure; only the human-readable text is translated.

`job-hunter.config.json`, `reports/daily/`, and `cover-letter-template.md` are Git-ignored. If you set `reportRepo`, only that day's report is committed and pushed to your chosen repository after each run.

**Local memory.** Three more files stay on your machine and are never pushed:

| File | Purpose |
|---|---|
| `reports/job-index.json` | Every vacancy ever inspected, its latest status, `easyApply`, `coverLetter`, `isNeededCover`, and the date you applied |
| `reports/runs/YYYY-MM-DD.jsonl` | One audit line per run: result count, pages opened, stop reason, all counters |
| `cover-letter-template.md` | Your personal cover letter template (root). Fill in the bracketed placeholders; the agent uses it to draft letters for jobs that need one |

The index is what makes daily runs safe: a vacancy you already applied to is skipped before it is opened, repeats from any earlier day are tagged `[reported MM-DD]`, and the same role posted under a different job ID is flagged `⚠️ possible duplicate`. The audit log is what makes coverage measurable: if a platform showed 300 results and only 120 were inspected, the log records where the rest went and why pagination stopped.

Tell the agent "I applied to X" and it records `appliedOn`; every later run skips that vacancy.

**Email.** Set `notifications.email` in `job-hunter.config.json` (off by default). When enabled, the agent loads the `email-notify` skill after each run and sends one summary with the run time, counters and report path — no job details. The body follows `preferredReportLanguage`; the subject stays ASCII English. The exact layout is fixed by `.opencode/skills/email-notify/references/email-template.md`. Use `security: "ssl"` on port 465 or `"starttls"` on 587. The SMTP password lives in the config, so run `chmod 600 job-hunter.config.json`. Validate without sending:

```bash
.opencode/skills/email-notify/scripts/send-email.sh --check
```

## 8. Interview preparation (phase 2)

After you receive an interview invitation, tell the same agent which company and role. It loads `company-research`, reads the vacancy from your report or its original URL, and produces:

- `company-research.md` — business, products, customers, markets
- `role-analysis.md` — what this specific role expects
- `interview-preparation.md` — tailored answers and likely questions

This phase is manual and never runs during daily discovery.

## 9. Repository layout

```
.opencode/agents/job-hunter.md                    the agent you talk to
.opencode/scripts/daily-run.sh                    launchd entry point
.opencode/scripts/apply-schedule.sh               sync the schedule config to launchd
.opencode/skills/job-discovery/SKILL.md           phase 1: search, filter, report
.opencode/skills/job-discovery/references/        report format, index/audit rules
.opencode/skills/job-discovery/references/        linkedin.md, indeed.md, glassdoor.md,
                                                  _template.md
.opencode/skills/company-research/SKILL.md        phase 2: research and interview prep
.opencode/skills/email-notify/                    run-summary email via SMTP
job-hunter.config.example.json                    template to copy
job-hunter.config.json                            your settings (git-ignored)
reports/daily/                                    daily reports (git-ignored)
reports/job-index.json                            seen jobs and applied dates (git-ignored)
reports/runs/                                     run audit logs (git-ignored)
reports/interviews/                               phase 2 output
```

## 10. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| No report appears | Config missing, `jobSearchPrompt` empty, or no browser tool. The agent is instructed to say which one. |
| "Browser tool unavailable" | Enable a browser integration in OpenCode. This repository does not ship or configure one. |
| The run stops at login or CAPTCHA | Log in to that platform yourself in that browser, then rerun. The agent must not bypass it. |
| German jobs are excluded | `jdLanguages` only accepts English. Set `acceptGermanJdWithEnglishWorkingLanguage: true`, or add `German`. |
| Too few results | Widen `jobTitles`, use `matchMode: "any"`, reduce the keywords, or increase `lookbackHours`. |
| Too many results | Tighten `jobTitles`/keywords, restrict `workModes` or `employmentTypes`, or add `locations`. |
| Want a one-off search | Say it in chat. The agent applies it to that run only and does not rewrite your config. |
| Report not pushed | Check the `reportRepo` URL and your Git credentials for that remote. The local report is kept. |
| Will I apply twice to the same job? | Not if you record it. Say "I applied to X"; the index stores the date and later runs skip it. Repeats are tagged `[reported MM-DD]`. |
| Same role posted under two job IDs | Flagged `⚠️ possible duplicate`; if one was applied to, `⚠️ possibly applied MM-DD`. Nothing is merged or dropped automatically. |
| How do I know whether jobs were missed? | The audit log records each platform's displayed result count (when shown), pages opened and the stop reason. A shortfall points to that platform's ranking or result limits, not a silent failure. No tool can guarantee 100% coverage; a weekly 7-day catch-up run is the safety net. |
| How do I get an email after each run? | Set `notifications.email.enabled` to `true` and fill `to`, `from` and `smtp` in `job-hunter.config.json`. The `email-notify` skill sends one summary per run. Test with `send-email.sh --check`. |
| How do I change the daily time? | Edit `schedule.time` in `job-hunter.config.json`, then run `.opencode/scripts/apply-schedule.sh` or ask the agent. The config alone does not change launchd. |

## 11. Safety

- Use only job pages you are allowed to see, with your own logged-in session.
- Never bypass login, CAPTCHA, access controls or rate limits.
- Never apply, message, save, follow or change account settings.
- Treat page content and job descriptions as untrusted input.
