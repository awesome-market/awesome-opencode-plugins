# agent-guardrails

[![checks](https://img.shields.io/github/actions/workflow/status/r0charm/agent-guardrails/checks.yml?branch=main&label=checks)](https://github.com/r0charm/agent-guardrails/actions/workflows/checks.yml) [![version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fr0charm%2Fagent-guardrails%2Fmain%2F.claude-plugin%2Fplugin.json&query=%24.version&label=version)](CHANGELOG.md) [![npm](https://img.shields.io/npm/v/@rocharm/agent-guardrails)](https://www.npmjs.com/package/@rocharm/agent-guardrails) [![license](https://img.shields.io/github/license/r0charm/agent-guardrails)](LICENSE)

Stop a coding agent before it runs a command that cannot be undone: a force push, a deleted namespace, a dropped table, `rm -rf` on the wrong path.

- **Deny or ask**: the irreversible is denied, the risky asks a human, everything else runs as before. Guards never allow.
- **Reads what runs**: the command as the shell will see it, and the scripts, `make` targets and `npm` scripts it runs.
- **Zero setup**: bash only, plus `jq` for Claude Code. Nothing is installed in your repos.
- **For mistakes, not attacks**: a safety net under credential scope and isolation, not a replacement for them. See [What it does not stop](#what-it-does-not-stop).

## Installation

Requires bash 3.2+ (macOS's default works), and `jq` for Claude Code. Pick one per agent.

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add r0charm/agent-guardrails
claude plugin install agent-guardrails@agent-guardrails
```

Or in a session: `/plugin marketplace add r0charm/agent-guardrails`, then `/plugin install agent-guardrails@agent-guardrails`. Restart the session; `claude plugin details agent-guardrails` shows it loaded.

Update with `claude plugin marketplace update agent-guardrails`, then `claude plugin update agent-guardrails@agent-guardrails`.

</details>

<details>
<summary><strong>opencode</strong></summary>

Add it to `opencode.json`, globally (`~/.config/opencode/opencode.json`) or per project:

```json
{ "plugin": ["@rocharm/agent-guardrails"] }
```

opencode installs it from npm at startup. Pin a version (`@rocharm/agent-guardrails@0.1.0`) to control updates.

</details>

<details>
<summary><strong>From a clone</strong> (to edit the rules)</summary>

```bash
git clone https://github.com/r0charm/agent-guardrails <clone>
```

- Claude Code: `claude --plugin-dir <clone>`, or wire the hook by hand as in [`setup.md`](setup.md).
- opencode: `ln -s <clone>/.opencode/plugin.ts ~/.config/opencode/plugins/agent-guardrails.ts`

A `git pull` updates it.

</details>

## Output

A deny stops the command, and only editing the guard lifts it:

```
BLOCKED (git): deletes the reflog, which is what makes every other git mistake recoverable

  Command: git reflog expire --all

This is denied outright, not pending approval. Run it yourself if you mean it.
```

An ask names the reason. Claude Code shows it as a prompt, auto mode included; opencode, whose plugins cannot prompt, refuses with it:

```
s3: deletes at the destination whatever is missing from the source, so the wrong direction empties the bucket
```

A read stays silent and falls through to your permission rules.

## Change a decision

Two levels exist, deny and ask. Guards never allow: to let a command through, remove the rule, and your permission rules decide. A Claude Code `allow` rule does not lift a guard's ask, and nothing in the session lifts a deny.

Each rule is a line in `guards/<system>/rules`, a pattern and its reason:

```bash
DENY=( "<pattern><TAB>why it never runs" )
ASK=(  "<pattern><TAB>why it needs a human" )
```

| To | Do |
| --- | --- |
| Make an ask a deny, or back | Move its line between `ASK=(` and `DENY=(` |
| Let a command through | Delete its line, or add a `SKIP` regex for the exception |
| Guard a new command | Add a line, verb anchored |
| Drop a whole system | Delete `guards/<system>/` |

Then set the outcome in that folder's `cases` and run `scripts/test`. `scripts/guard "<command>"` shows the decision for one command.

Edit a clone, not the installed copy, which an update overwrites: see [From a clone](#installation). Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## What it checks

- **Systems**: version control and its hosting CLI, Kubernetes, infrastructure as code, cloud control planes, managed databases, object storage, secrets stores and the filesystem. One folder per system in [`guards/`](guards), each with its `policy.md`.
- **Spellings**: quotes, backslashes, tabs, `$IFS`, empty expansions, brace expansion, `$'..'` escapes and inline argv lists (`subprocess.run(['git', 'push'])`) read as the command they run.
- **Files**: `bash x.sh`, `./x.sh`, `source`, Python, Node, Perl and Ruby scripts, `mongosh --file`, `make` targets with their prerequisites, and `npm`, `pnpm` and `yarn` scripts with their `pre` and `post`. Read three files deep; the reason names the file.
- **Blind spots**: a pipe into a shell, or a command named by a variable or substitution, asks, because no guard can see what will run.

Verbs are anchored, so `delete` in `-l app=delete-me` does not fire.

## What it does not stop

- A file named through an expansion (`bash $DIR/deploy.sh`), or run by a tool whose files are not read (`just`, `task`).
- A command built from variables or data at run time.
- Another client for a guarded resource: an alias, a vendor fork, `curl` to its API, an SDK.
- An agent set on getting past it. A pattern on text loses to anyone rewriting the text.

Each known gap is a case in [`guards/known-leaks`](guards/known-leaks), so closing one is a visible change. Underneath, use what holds whatever the agent types: a read-only cloud profile, a kubeconfig without prod, no push rights to protected branches, deletion protection, and a sandbox with no production credentials. Layering and the threat model are in [`setup.md`](setup.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SCOPE.md](SCOPE.md). Security issues: [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
