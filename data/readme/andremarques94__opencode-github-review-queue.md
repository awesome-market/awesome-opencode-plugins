<div align="center">

# OpenCode GitHub Review Queue

**Every pull request waiting on your review, inside OpenCode.**

A review queue for the TUI and the Desktop app, so checking GitHub never
breaks your flow.

[![CI](https://github.com/andremarques94/opencode-github-review-queue/actions/workflows/ci.yml/badge.svg)](https://github.com/andremarques94/opencode-github-review-queue/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenCode 2.3](https://img.shields.io/badge/OpenCode-2.3-000000.svg)](https://opencode.ai)
[![npm](https://img.shields.io/npm/v/opencode-github-review-queue.svg)](https://www.npmjs.com/package/opencode-github-review-queue)


</div>

## Why

Review requests arrive when you are in the middle of something. The usual answer is another tab, another search,
another context switch. This plugin puts them where you already are: one queue, grouped by repository, kept current
in the background, with a notification only when something actually needs you.

## Features

- **One queue, both surfaces.** The TUI panel and the Desktop side panel read the same server-side poller, and only
  one OpenCode location polls GitHub however many review sessions are open.
- **Readiness at a glance.** Each row shows its checks (✓ passing, ✗ failing, ● running), merge conflicts, and
  unresolved review threads.
- **Re-reviews that focus on what changed.** A pull request you reviewed comes back to the queue when the author
  pushes, even without a re-request, and the next review can cover only the commits since.
- **Your own pull requests too.** **Mine** lists them with how their reviews stand, and you are notified when one
  gets changes requested, becomes ready to merge, or starts failing its checks.
- **Snooze** a pull request until its checks finish, until the author pushes, or until a time you pick.
- **Summaries on demand:** a pull request's intent, main changes, and what to inspect, without starting a review.
- **Grouped by repository**, with a **Current** scope for the repository in the session.
- **Size and wait at a glance.** Rows show lines added and removed, and how long the pull request has waited on you;
  sort by the longest wait, the smallest change, or ready to merge first, and highlight what waited too long.
- **Only what you want to see.** Hide drafts, bots, repositories, or requests made to a team rather than to you;
  team requests are marked _via @team_.
- **Notifications that respect you.** New requests are batched into one notification; a request that briefly drops
  out of GitHub's search index does not notify twice.
- **Keyboard and mouse.** Move, open, copy, filter and refresh, or click and right-click.
- **Review with a human in the loop.** Start a review from the queue: the plugin checks the pull request out into
  its own worktree and opens an agent session that drafts findings. You decide on each one, and only you can post.
- **Stays useful offline.** The last successful queue is shown, marked stale, while GitHub is unreachable.
- **Polite to the API.** Paginated search, request timeouts, bounded backoff, and GitHub's rate-limit reset time.
- **No tokens touched.** The GitHub CLI is spawned directly; the plugin reads and stores no credentials.

## Requirements

- **OpenCode 2.3.0** (the version this plugin is built and tested against).
- **[GitHub CLI](https://cli.github.com/)** installed and authenticated.

```sh
gh auth status   # if this fails:
gh auth login
```

## Install

Add the plugin to the `plugins` array in your **global** `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "opencode-github-review-queue"
    }
  ]
}
```

OpenCode downloads the package and loads its server, TUI and Desktop parts. The global config is required for the
Desktop part. Run `/reload` if an already-open client does not pick it up.

Then open the queue with `/reviews`, or **Show GitHub review requests** from the command palette.

## Usage

### TUI

| Key       | Action                                                        |
| --------- | ------------------------------------------------------------- |
| `j` / `k` | Move the selection (or `↓` / `↑`)                              |
| `Enter`   | Start a review of the selected pull request, or resume it     |
| `o`       | Open the pull request on GitHub                               |
| `p`       | Post the selected review, after a preview                     |
| `i`       | Summarize the selected pull request                           |
| `a`       | Address the review of your selected pull request              |
| `s`       | Snooze the selected pull request, or wake it                  |
| `z`       | Show or hide snoozed pull requests                            |
| `m`       | Actions menu, listing every action with its key               |
| `y`       | Copy `owner/repo#123`                                         |
| `u`       | Copy the URL                                                  |
| `f`       | Switch between **All**, **Current**, and **Mine** (or `←` / `→`) |
| `r`       | Refresh                                                       |
| `Shift+F` | Toggle full screen                                            |
| `Esc`     | Close the panel                                               |

The footer only shows `enter` and `m`, so it fits a narrow panel; the actions menu lists the rest. With mouse support
enabled in your terminal, click a request to select it, click it again to start or resume its review, and right-click
for the actions menu. **All** / **Current**, the footer hints, and **N snoozed** in the header are clickable, and the
wheel scrolls the list. The actions menu's **Open on GitHub** entry spells out the row's readiness.
Copying uses OSC 52, so it needs a terminal that supports it.

### Desktop

Open the pinned **Review requests** tab in the side panel, or **Show GitHub review requests** from the command palette.
Click a row to start or resume its review. Its menu (or a right-click) opens it on GitHub, copies its reference or
link, summarizes it, snoozes or wakes it, and posts or resets its review. Hover a readiness mark for its meaning, and
click **N snoozed** under the title to show snoozed requests. New requests also raise a toast with a **Show reviews**
button.

### Readiness

Rows show what GitHub reports about the pull request's last commit and mergeability: ✓, ✗, or ● for checks that
pass, fail, or are still running, _conflicts_ when it cannot merge cleanly, and _N threads_ for unresolved review
threads. Anything GitHub does not know yet, such as a pull request without checks or mergeability still being
computed, shows nothing. On a pull request with more than 100 review threads only the first 100 are counted, so the
mark reads _N+ threads_.

Next come the lines added and removed (_+120 −30_), the author, and how long the pull request has waited on you:
since you, or a team you are in, were last asked to review, or for a follow-up since its last commit. Hover it on the
Desktop for the exact time.

### Your pull requests

**Mine** lists your own open pull requests, grouped by repository like the queue, with their readiness and where
their reviews stand: _changes requested by @alice_, _blocked_ (conflicts or failing checks), _ready to merge_,
_approved_ (but not mergeable yet, such as while checks run), or _waiting on @bob, @acme/web_. The scope shows how
many need you, which means changes requested or ready to merge. Selecting one opens it on GitHub; its menu copies,
summarizes, and snoozes it as in the queue.

**Address review** (`a` in the TUI, or the row's menu) appears when changes were requested or threads are still
unresolved. It opens a session in your own clone, with every open review comment as a checklist, and the agent works
through them with you: what each asks for, the fix it proposes, and a drafted reply where no change is needed. It can
edit files there, but pushing, resolving threads, and posting on GitHub stay with you: those commands are denied in
the session. If your clone is on another branch, the plugin asks before adding a worktree on the pull request's
branch under the cache directory, and never switches your branch; that worktree is kept afterwards, since it may hold
your commits. **Address review** returns to the same session until the pull request is closed or merged.

You are notified when one of them gets changes requested, becomes ready to merge, or its checks go from passing or
running to failing. A pull request seen for the first time, such as one you just opened, never notifies. Set
`"notifyOnMyPullRequests": false` to keep the list without the notifications, or `"myPullRequests": false` to turn
both off.

### Snooze

**Snooze** hides a pull request until a condition is met: **Until checks finish** (offered while checks are running),
**Until the author pushes**, **For 1 hour**, **Until tomorrow** (9:00), or **Until…** a duration (`45m`, `3h`, `2d`),
a time (`14:30`), or a date (`2026-11-20 09:00`). A snoozed request comes back on its own when its condition is met.
The header counts the snoozed requests; show them to see what each waits for, or to wake one early. A snooze is
dropped when its pull request leaves the queue.

### Summaries

**Summarize** asks which model to use (your last review model is selected), reads the pull request's title,
description, and diff with `gh`, and asks that model for its intent, main changes, and the areas worth inspecting. The
Desktop shows it as Markdown, the TUI in a dialog. Diffs beyond about 80,000 characters are cut, and the dialog says
so; for a pull request of more than about 1,500 changed lines, the model picker warns you first.

### Reviews

**Start review** asks which model should review, listing the enabled chat models of your connected providers with
your last pick selected, then prepares a local review and opens its session:

1. It finds a local clone of the repository. That is the session's own checkout when it is a clone of the pull
   request's repository, or a clone the plugin made earlier. Otherwise it asks before making a bare, blobless clone
   in the cache directory, which later reviews reuse.
2. It fetches the pull request head into a detached worktree under the cache directory. Your checkout and branch are
   never touched.
3. It opens a session in that worktree with the review instructions. The agent investigates, records findings with
   the `review_*` tools, and walks you through them one at a time. Lines outside the diff are rejected, and file
   edits are denied in the session.

The row shows where the review stands: _reviewing_, _N to decide_, _ready to post_, or _posted_. **Resume review**
returns to the same session.

The agent's comments are checked against the exact commits under review, so a push during the review does not move
the lines it may comment on.

After you post, the plugin remembers the commit you reviewed and your verdict until the pull request is closed or
merged. When the author pushes, the pull request comes back to the queue even if nobody re-requests your review, and
you are notified once. The row shows _new commits since your review_, and starting a review offers **Review changes since last review** (the default) or **Full review**. A follow-up review
fetches both commits, looks only at the changes between them, reads your earlier comments on GitHub, and its summary
says which of them the changes address and which they leave unresolved. Once you post the follow-up, the pull request
leaves the queue until the next push. **Snooze › Until the author pushes** sets one aside, and `"followUps": false`
turns this off. Only reviews posted from the plugin are followed up.

Each finding ends with a question: **Keep**, **Edit wording**, **Drop**, **Explain**, or **Investigate**, with the
agent's recommendation first. Click one or type a reply. Explain and Investigate answer about that finding and ask
again.

Inside a review session you can also triage without the chat:

- **Desktop:** the **Review** pill above the composer shows _N of M decided_ and the verdict, with **Post review…** and
  **Show findings**, which opens a **Findings** side tab (close it like any other tab). It lists every finding in
  walkthrough order with its comment and decision, and buttons to keep, drop, edit the comment, ask the agent about
  it, or read its evidence in a dialog.
- **TUI:** the line above the composer shows the same progress; click **findings** or run `/findings` to open the list,
  and **post review…** to post. The list shows one line per finding and opens the selected one with its comment
  rendered as Markdown. `j`/`k` move, `y` keeps, `d` drops, `e` edits the comment (`ctrl+s` saves), `a` asks the
  agent, `enter` shows the evidence, `p` posts, and `shift+f` toggles full screen.

On the Desktop you can also point at code yourself: leave line comments on the review session's files or diff, then
click **Add as findings** in the Findings tab. The agent investigates each marked line and records a finding there,
or says why it found nothing; the comments are removed from the composer once sent.

A decision made there is yours: the agent skips it and moves on instead of asking again. Saving an edited comment keeps
the finding. The `review_*` tools only appear in review sessions.

When a fix is concrete, the agent attaches it as a GitHub **suggestion**, which the author can apply with one click.
It is posted under the comment as a `suggestion` block, and only on new lines within one hunk, which is where GitHub can
apply it. Editing a comment shows the block as it will be posted: change it, or delete it to post the comment alone.

**Post review** shows the verdict, summary, and every retained comment, and posts only after you confirm. It refuses
while findings are undecided, and asks again if new commits were pushed since the draft. The agent cannot post.
After posting, the worktree is removed, and so is a clone the plugin made once no other review uses it (set
`keepClones` to keep clones for faster re-reviews). If cleanup fails, the review still counts as posted and a warning
names the folder left behind.

**Reset review** deletes the draft and its worktree. The session's chat history and anything already on GitHub
stay.

When a reviewed pull request leaves the queue, its draft is forgotten once the review was posted or the pull request
was closed or merged, and any worktree left is cleaned up. A pull request that is still open keeps its draft, so you
can still post it.

The default review guidelines cover readability, naming, dead code, duplication, error handling, tests, and types,
in a direct tone. Point `reviewGuidelines` at a Markdown file to replace them with your own quality bar and tone.

### Notifications

Desktop notifications follow **Settings › Notifications**; TUI notifications follow the TUI's attention settings.
Set `"notifications": false` to keep the in-app toasts but silence native ones.

Each poll runs up to three GitHub searches (requests, follow-ups once you have posted a review, and your own pull
requests), about 13 points of GitHub's 5,000-an-hour GraphQL budget together. Raise `intervalMs` if you share that
budget with other tools.

## Configuration

```jsonc
{
  "plugins": [
    {
      "package": "opencode-github-review-queue",
      "options": {
        "intervalMs": 60000,
        "timeoutMs": 20000,
        "maxBackoffMs": 900000,
        "notifications": true,
        "cacheDirectory": "~/.cache/opencode-github-review-queue",
        "reviewGuidelines": "/path/to/review-guidelines.md",
        "keepClones": false,
        "followUps": true,
        "myPullRequests": true,
        "notifyOnMyPullRequests": true,
        "sort": "oldest",
        "staleAfter": "2d",
        "includeDrafts": true,
        "excludeAuthors": ["dependabot", "renovate"],
        "excludeRepositories": ["acme/legacy", "archive-org/*"],
        "teamRequests": "show"
      }
    }
  ]
}
```

| Option          | Default   | Description                                                       |
| --------------- | --------- | ----------------------------------------------------------------- |
| `intervalMs`    | `60000`   | Poll interval; minimum 10 seconds                                 |
| `timeoutMs`     | `20000`   | Timeout for each GitHub CLI request                               |
| `maxBackoffMs`  | `900000`  | Longest delay after transient failures                            |
| `notifications` | `true`    | Native and terminal-attention notifications                       |
| `cacheDirectory` | `$XDG_CACHE_HOME/opencode-github-review-queue` | Plugin-made clones, review worktrees, and worktrees for addressing a review; falls back to `~/.cache` |
| `reviewGuidelines` | built-in | Path to a Markdown file that replaces the review quality bar and tone |
| `keepClones` | `false` | Keep the plugin's clones after their last review instead of deleting them |
| `followUps` | `true` | Queue pull requests you reviewed when new commits arrive, without waiting for a re-request |
| `myPullRequests` | `true` | List your own open pull requests under **Mine** |
| `notifyOnMyPullRequests` | `true` | Notify when one of them gets changes requested, becomes ready to merge, or starts failing its checks |
| `sort` | `"oldest"` | `"oldest"` (longest wait first), `"smallest"` (fewest changed lines), or `"ready"` (checks passing and no conflicts first, then smallest) |
| `staleAfter` | none | Highlight the wait once it passes this, such as `"4h"` or `"2d"` |
| `includeDrafts` | `true` | Show draft pull requests |
| `excludeAuthors` | `[]` | Hide pull requests by these logins; bots match with or without `[bot]` |
| `excludeRepositories` | `[]` | Hide these repositories: `owner/repo`, or `owner/*` for every repository of an owner |
| `teamRequests` | `"show"` | `"hide"` drops requests made only to a team you are in, keeping the ones made to you |


## Development

```sh
git clone https://github.com/andremarques94/opencode-github-review-queue.git
cd opencode-github-review-queue
pnpm install     # also installs the Husky hooks
pnpm check       # typecheck, lint, test, build
pnpm fallow      # full repository audit
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the hook and commit conventions.

Releases use Conventional Commits and Release Please: merging the release PR tags the version and publishes it to
npm.

## Contributing

Issues and pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) covers setup, hooks and commit style.

## License

[MIT](LICENSE) © André Marques

---

<sub>An independent plugin. Not built by, or affiliated with, the OpenCode team.</sub>
