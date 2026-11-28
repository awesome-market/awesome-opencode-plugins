<p align="center">
  <a href="https://aerless.io"><img src=".github/assets/banner.svg" alt="Aerless Code: code in your terminal, pictures built in" width="100%"></a>
</p>

<p align="center"><a href="https://aerless.io"><b>AERLESS.IO</b></a></p>

<p align="center">
Aerless Code is the coding assistant for your terminal, with pictures built in.<br>
Ask for a hero image, an icon or a banner and it makes it, crops it and puts it in your project.<br>
Open source, one install, lighter than the opencode it is built on.
</p>

<p align="center">
  <a href="https://github.com/aerless-ai/aerless-code/releases/latest"><img alt="release" src="https://img.shields.io/github/v/release/aerless-ai/aerless-code?label=release&color=d41f26&labelColor=1a1a1a"></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-MIT-d41f26?labelColor=1a1a1a&style=flat"></a>
  <img alt="platforms" src="https://img.shields.io/badge/macOS%20%7C%20Linux%20%7C%20Windows-supported-f2f2f2?labelColor=1a1a1a">
  <a href="https://github.com/anomalyco/opencode"><img alt="fork of opencode" src="https://img.shields.io/badge/fork%20of-opencode-f2f2f2?labelColor=1a1a1a"></a>
</p>

---

## Install

macOS, Linux and WSL:

```bash
curl -fsSL https://github.com/aerless-ai/aerless-code/releases/latest/download/install.sh | sh
```

Windows (PowerShell):

```powershell
irm https://github.com/aerless-ai/aerless-code/releases/latest/download/install.ps1 | iex
```

Open a new terminal and type `aerless` in any project folder. The first run signs you in.

## Use it

| Command | What it does |
| --- | --- |
| `aerless` | Start the coding assistant in this folder |
| `/imgengine` | Inside the assistant: open the picture studio |
| `aerless img "prompt"` | Make a picture from the shell (`-o file.png`, `--size 1920x1080`, `--ref photo.jpg`) |
| `aerless icon logo.png` | Make favicons and app icons from one picture |
| `aerless studio` | Open the picture studio in your browser |
| `aerless-code webui` | Open the full web interface ([guide](docs/webui.md)) |
| `aerless login` | Sign in with Aerless, or use your own OpenRouter or Venice key |
| `aerless doctor` | Check that everything works |

## Why Aerless Code

- **Pictures built in.** The assistant makes, edits, crops and places images while it codes. No second tool, no copy and paste.
- **Lighter.** The interface and its server run in one process, and the 100+ provider catalog loads only when needed: about 300 MB idle instead of about 450-560 MB.
- **Signed in from the start.** `aerless login` sets up Aerless, OpenRouter or Venice keys.
- **Nothing left running.** No background service. Quitting stops the commands the assistant started.
- **Lives next to opencode.** Its own command and folders (`~/.config/aerless-code`, `~/.local/share/aerless-code`), so it never touches opencode's settings or sessions.

## Build from source

Needs the Bun version in [`package.json`](package.json) (`packageManager`).

```bash
bun install
cd packages/cli && bun run script/build.ts --single
```

The build lands in `packages/cli/dist/cli-<os>-<arch>/bin/aerless-code`. For every platform, run `bun run script/build.ts` with `OPENCODE_VERSION` set.

## Repository layout

| Folder | What is in it |
| --- | --- |
| [`packages/`](packages) | The app: `cli` (entry point), `tui` (terminal interface), `core`, `server`, `app` (web interface), `desktop`, `ai`, `plugin` and the rest |
| [`script/`](script) | Build, lint, release and install scripts |
| [`patches/`](patches) | Patches applied to dependencies on `bun install` |
| [`docs/`](docs) | Guides and design specs |
| [`.github/`](.github) | Release workflows, issue templates, contributing guide and security policy |

Contributing: [CONTRIBUTING.md](.github/CONTRIBUTING.md). Security reports: [SECURITY.md](.github/SECURITY.md).

## License

MIT, like opencode. Aerless Code is a fork of [opencode](https://github.com/anomalyco/opencode) 2.0.26, and opencode's copyright notice is kept in [LICENSE](LICENSE) as the license requires.
