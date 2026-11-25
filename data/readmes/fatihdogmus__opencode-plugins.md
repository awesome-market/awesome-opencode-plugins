# opencode-plugins

[OpenCode](https://opencode.ai) plugins, each published to npm under the `@fatihdogmus` scope.

| Package | Description |
| --- | --- |
| [`@fatihdogmus/opencode-codex-guardian`](packages/codex-guardian) | Codex Guardian permission reviews for OpenCode V2 |
| [`@fatihdogmus/opencode-message-timestamps`](packages/message-timestamps) | Adds each reply's completion time, in your computer's time zone, to the TUI's assistant footer |
| [`@fatihdogmus/opencode-project-tab-groups`](packages/project-tab-groups) | Groups OpenCode Desktop's tabs by project, with colors, labels and a grouped switcher |
| [`@fatihdogmus/opencode-voice-input`](packages/voice-input) | Voice prompts for OpenCode Desktop and the TUI, transcribed with your OpenAI account |
| [`@fatihdogmus/opencode-agentic-review`](packages/agentic-review) | Turn snapshots for the Agentic Review IntelliJ plugin |

Install a plugin with `opencode plugin add <package>`, or add its package name to `plugins` in your `opencode.json(c)`;
OpenCode installs it itself. Each package's README covers its requirements and options.

**For agents:** to install one of these plugins, follow the **For agents** section of that package's README. It lists
what to check first, the install command, how to verify it, and what not to change.

## Layout

```
packages/<id>/          one plugin, published as @fatihdogmus/opencode-<id>
  package.json          build, typecheck, test and check scripts
  scripts/smoke.mjs     optional checks run against the installed tarball
scripts/release/        shared bump, validate, pack and smoke-test tooling
test/                   tests for the release tooling and workflows
.github/workflows/      Build (every push and PR) and Release (manual)
```

The repository is a [pnpm workspace](https://pnpm.io/workspaces). Each package declares its own dependencies; pnpm keeps
them isolated, so packages can pin different `@opencode/plugin` and TypeScript versions.

## Develop

Requires Node.js 26 and pnpm (the version in `packageManager` is picked up automatically).

```sh
pnpm install
pnpm check                      # release-tooling tests, then every package's check
pnpm --filter ./packages/voice-input check
pnpm package                    # pack every package into artifacts/ and smoke-test each tarball
pnpm package codex-guardian     # just one
```

To try a package locally in OpenCode, point a `plugins` entry at its directory, for example
`/path/to/opencode-plugins/packages/voice-input`.

Dependency install scripts are off unless listed in `allowBuilds` in `pnpm-workspace.yaml`. When `pnpm install` stops on a
new dependency's build script, allow it there only if the package actually needs it.

## Add a plugin

1. Create `packages/<id>` with a `package.json` named `@fatihdogmus/opencode-<id>`, version `0.1.0`, `"license": "MIT"`,
   `publishConfig` (`access: public`, `registry: https://registry.npmjs.org/`), `repository` with
   `url: git+https://github.com/fatihdogmus/opencode-plugins.git` and `directory: packages/<id>`, `exports`, and `files`.
2. Add `build`/`typecheck`/`test` scripts as needed and a `check` script that runs them.
3. Add a `README.md` with a `## For agents` section: the prerequisites to check, `opencode plugin add <package>`, how to
   verify with `opencode plugin list`, what an agent must not change, and `opencode plugin remove <package>`.
4. Copy the root `LICENSE` into the package.
5. Add `<id>` to the `package` options in `.github/workflows/release.yml`.

`pnpm check` fails until the manifest passes release validation, the README has its agent section, and the workflow
lists the package.

## Releasing

Run the **Release** workflow on `main` and choose the package and a `patch`, `minor` or `major` bump. It:

1. bumps the package's `version`, and requires a new `<id>-vX.Y.Z` tag and a version that isn't on npm yet;
2. runs the release-tooling tests and the package's `check`, packs it, and smoke-tests the tarball;
3. commits only that package's `package.json` as `github-actions[bot]` and tags it, locally;
4. checks that `main` hasn't moved, then publishes the tested tarball to npm with provenance;
5. only after publishing succeeds, pushes the commit and tag atomically and creates a GitHub release with notes since
   the package's previous tag.

Publishing uses npm [trusted publishing](https://docs.npmjs.com/trusted-publishers): npm accepts the Release
workflow's GitHub OIDC identity, so no npm token is stored anywhere. Each package needs it set up once on npmjs.com
(the package → **Settings** → **Trusted Publisher** → **GitHub Actions**):

| Field | Value |
| --- | --- |
| Organization or user | `fatihdogmus` |
| Repository | `opencode-plugins` |
| Workflow filename | `release.yml` |
| Environment | `npm` |
| Allowed actions | `npm publish` |

A new trusted publisher must be used for a successful publish within 2 days, or it expires. Once it works, set the
package's publishing access to disallow tokens.

A package must already exist on npm before it can have a trusted publisher. For a new package, publish its first
version (`0.1.0`) from your machine with your own 2FA:

```sh
pnpm package <id>
npm publish ./artifacts/fatihdogmus-opencode-<id>-0.1.0.tgz --access public
```

Keep the `./`: without it, npm reads `artifacts/<file>` as a GitHub `user/repo` shorthand.

Then push a `<id>-v0.1.0` tag on the commit you published, add the trusted publisher, and use the Release workflow from
then on.

The GitHub repository needs an `npm` environment, and branch and tag rules that let the workflow's `GITHUB_TOKEN` push to
`main` and create tags. The workflow never force-pushes.

Nothing is pushed unless npm publishing succeeds, so a failed check or publish leaves `main` untouched; fix the cause and
release again. npm and GitHub are still not atomic: if the push fails after publishing (for example, because `main`
moved), npm has the version but `main` doesn't. The next release then stops at **Require an unpublished npm version**
and explains how to record the version: set the package's `version` to it and push a matching `<id>-vX.Y.Z` tag. An npm
version cannot be overwritten.

## License

[MIT](LICENSE) © Muhammed Fatih Doğmuş.
