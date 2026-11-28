# OpenCode TTS

[![Works with OpenCode](https://opencode.ai/brand/badges/opencode-works-with-a-light-20.svg)](https://opencode.ai)

Text-to-speech for [OpenCode](https://opencode.ai) replies on Windows.

A small C++ helper uses Windows SAPI voices, and a local OpenCode plugin speaks
the final assistant reply after each turn. It listens for
`session.execution.succeeded`, cleans Markdown from the reply, and speaks the
most recent assistant message that contains text.

## Install as an OpenCode plugin

The repo includes a local plugin at `release/plugin/index.ts` and a portable
config template at `release/config.snippet.jsonc`. After copying `release` into
your project, the config should contain:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "-opencode.tts",
    {
      "package": "./.opencode/plugins/tts",
      "options": {
        "enabled": true,
        "exe": "release\\tts.exe",
        "voice": "Zira",
        "rate": 1,
        "volume": 100,
        "maxChars": 1200,
        "mode": "interrupt",
        "debug": false
      }
    }
  ]
}
```

Run `.\release\install.ps1` from the project root to install the plugin and write
this config for you, then reload OpenCode with
`opencode api post /api/location/reload`.

## Quick start

1. Copy the `release` folder into your OpenCode project, or clone this repo and
   run OpenCode from the repo root.
2. Run the installer from the project root:

   ```powershell
   .\release\install.ps1
   ```

3. Ask OpenCode something:

   ```powershell
   opencode run "Reply with exactly: OpenCode TTS is working"
   ```

You should hear the reply in the default voice (**Zira**). See
[`release/README.md`](release/README.md) for the full option list and
troubleshooting.

## Natural voices (optional)

The built-in SAPI voices (David, Zira) work offline but sound dated. For a more
natural voice on Windows 11:

1. Install a Narrator natural voice under
   **Settings → Accessibility → Narrator → Narrator's voice → Add natural
   voices** (Aria, Jenny, or Guy).
2. Install [NaturalVoiceSAPIAdapter](https://github.com/gexgd0419/NaturalVoiceSAPIAdapter)
   to expose those voices to SAPI applications. It is a separate MIT-licensed
   project and is not bundled here.
3. Set `"voice": "Aria"` in `opencode.jsonc`, then reload:

   ```powershell
   opencode api post /api/location/reload
   ```

Check available voices with:

```powershell
.\release\tts.exe --list-voices
```

## Contents

- `release/tts.exe` — release speaker (MSVC `/O2 /MT`, statically linked runtime)
- `release/plugin/index.ts` — OpenCode plugin source
- `release/install.ps1` — installs the plugin and writes `opencode.jsonc`
- `release/config.snippet.jsonc` — portable starter config
- `OpenCodeTTS/` — C++ source and Visual Studio project

## Building from source

Open `OpenCodeTTS\OpenCodeTTS.sln` in Visual Studio and build `Release|x64`, or
run:

```powershell
cmd /c OpenCodeTTS\build-release.bat
```

The build scripts locate Visual Studio with `vswhere.exe`.

## Requirements

- Windows 10/11 with SAPI voices
- OpenCode with local plugin support
- No cloud service or API key is required

## License

MIT — see [LICENSE](LICENSE).
