# opencode-github

Browse GitHub pull requests without leaving the OpenCode v2 TUI.

`opencode-github` adds a `/prs` command that opens a searchable, read-only dialog for the current Git repository. It uses the authenticated GitHub CLI for repository detection and pull request data.

Pull requests are prefetched when the TUI starts and refreshed in the background every minute, so opening `/prs` normally uses cached data.

> OpenCode v2 and its TUI plugin API are beta. This release targets OpenCode `0.0.0-next-16741` exactly.

## Requirements

- OpenCode `0.0.0-next-16741`, available as `opencode2`
- Node.js 22.12 or newer
- [GitHub CLI](https://cli.github.com/) authenticated with access to the current repository

Verify GitHub CLI access with:

```sh
gh api user --jq .login
```

## Install

Add the package to `~/.config/opencode/cli.json`:

```json
{
  "plugins": [
    {
      "package": "opencode-github"
    }
  ]
}
```

Restart OpenCode after adding or updating a package plugin.

## Use

Start OpenCode in a GitHub repository and run:

```text
/prs
```

The pull request dialog supports keyboard navigation. Press Enter to view a pull request's title and description inside the dialog, then press `d` for the full pull request diff or `c` to browse its commits and Enter to view a commit diff. Press `b` from the pull request list or details view to copy its branch name, or press `o` from either view to open it in the default browser.

## Develop

Install dependencies and create the initial build:

```sh
npm install
npm run build
```

Run the compiler in watch mode:

```sh
npm run dev
```

Register the absolute local build path in `~/.config/opencode/cli.json`:

```json
{
  "plugins": [
    {
      "package": "/absolute/path/to/opencode-github/dist/tui.js"
    }
  ]
}
```

Restart OpenCode after adding the plugin. You can then launch it normally from any repository:

```sh
cd /path/to/repository
opencode2
```

Local plugin builds are hot-reloaded by OpenCode. Restart the development TUI after changing dependencies or package configuration.

To test interactive changes, open a repository with open pull requests, run `/prs`, and verify searching, Up/Down navigation, Enter for details, `d` for the full pull request diff, `c` for commits, Enter for a commit diff, `/` to return to search, `b` to copy the branch in both pull request views, `o` to open the PR, and Escape/back behavior. After testing, replace the local path in `cli.json` with the published package entry.

## Verify

```sh
npm run check
npm pack --dry-run
```

For OpenCode diagnostics:

```sh
OPENCODE_LOG_LEVEL=DEBUG opencode2
```

Installed OpenCode logs are written to `~/.local/share/opencode/log/opencode.log`.

## Releases

Every non-bot push to `main` creates the next patch release, publishes it to npm, tags the release, and creates a GitHub Release. Publishing uses npm trusted publishing with GitHub Actions OIDC, so no npm token is stored in GitHub.

Configure the `opencode-github` package's trusted publisher in npm before pushing the workflow: select GitHub Actions, enter organization `vestia-dev`, repository `opencode-github`, workflow filename `release.yml`, and allow `npm publish`.

The workflow updates both `package.json` and `package-lock.json` in its release commit. Its bot-authored push is excluded from triggering another release.

## License

MIT
