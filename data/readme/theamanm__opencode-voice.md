<p align="center">
  <img src="assets/banner.png" alt="OpenCode Voice: speech-to-text input for the OpenCode terminal UI" width="100%" />
</p>

# OpenCode Voice

Use your microphone to dictate into the [OpenCode](https://opencode.ai/) terminal UI. OpenCode Voice transcribes the recording and inserts the text into the active prompt. You review and submit the prompt yourself.

> [!IMPORTANT]
> OpenCode Voice 0.0.x is prerelease software. It supports Linux x64, requires Node.js 22.22.2, and declares compatibility with OpenCode `>=1.18.3 <2`. Microphone capture is experimental.

## Quick start

Install the plugin globally:

```sh
opencode plugin @moozie/opencode-voice --global
```

Open OpenCode, then:

1. Run `OpenCode Voice: Config` from the command palette.
2. Select a transcription provider and microphone.
3. Press `Ctrl+X V` to start recording.
4. Press `Enter` to stop and transcribe.
5. Edit the transcript in the prompt, then submit it normally.

Pressing `Ctrl+X V` before setup opens the configuration screen.

## Requirements

| Requirement      | Version or platform |
| ---------------- | ------------------- |
| Operating system | Linux x64           |
| Node.js          | 22.22.2             |
| OpenCode         | `>=1.18.3 <2`       |

Microphone capture also requires one of these commands on your `PATH`:

- `ffmpeg` for PulseAudio or PipeWire-Pulse
- `pw-record` for native PipeWire
- `arecord` from `alsa-utils` for ALSA

For the default system microphone, OpenCode Voice tries the available backends in the order shown above.

A specifically selected microphone uses its detected backend without fallback. If that device disconnects, select another device or switch to `Default system microphone`.

## Controls

| Action              | Control                            |
| ------------------- | ---------------------------------- |
| Start recording     | `Ctrl+X V`                         |
| Stop and transcribe | `Enter` or `Ctrl+X V`              |
| Cancel and discard  | Press `Esc` twice within 3 seconds |
| Open settings       | `OpenCode Voice: Config`           |

While recording, the prompt footer shows the recording state and elapsed time. It can also display a live microphone-level waveform.

Voice controls override normal OpenCode shortcuts until recording stops.

The default recording limit is five minutes. You can set it anywhere from 10 seconds to 30 minutes. Recording stops automatically at the configured limit.

## Transcription providers

| Provider      | Audio leaves your machine | Credential                                          | Models                                           |
| ------------- | ------------------------- | --------------------------------------------------- | ------------------------------------------------ |
| Local Whisper | No                        | None                                                | Managed Whisper models or a custom `whisper-cli` |
| OpenAI        | Yes                       | `OPENAI_API_KEY` or an exposed OpenCode-managed key | `gpt-4o-mini-transcribe`, `gpt-4o-transcribe`    |
| ElevenLabs    | Yes                       | `ELEVENLABS_API_KEY`                                | `scribe_v2`, `scribe_v1`                         |
| Handy         | No                        | None                                                | Models installed in Handy                         |

### Local Whisper

Local Whisper runs on your CPU and does not send audio to a cloud provider. OpenCode Voice downloads and verifies a pinned build of [`whisper.cpp`](https://github.com/ggml-org/whisper.cpp) and the selected model.

The managed models are English-only:

| Model                 | Download | Notes                                       |
| --------------------- | -------: | ------------------------------------------- |
| `tiny.en`             |    78 MB | Fastest; lowest accuracy                    |
| `base.en`             |   148 MB | Lightweight general use                     |
| `small.en`            |   488 MB | Better accuracy; higher CPU use             |
| `large-v3-turbo-q5_0` |   574 MB | Best managed local quality; highest CPU use |

The configuration screen manages model downloads, deletion, retries, and runtime reinstallation.

To use an existing compatible binary, select its path in the configuration screen or set:

```sh
export OPENCODE_VOICE_WHISPER_BINARY="/path/to/whisper-cli"
```

### OpenAI

Set the API key before launching OpenCode:

```sh
export OPENAI_API_KEY="..."
```

OpenCode Voice can also use an OpenCode-managed OpenAI key when OpenCode exposes that key through its provider API.

OAuth-only OpenAI connections cannot be used unless OpenCode also exposes a corresponding API key.

### ElevenLabs

Set the API key before launching OpenCode:

```sh
export ELEVENLABS_API_KEY="..."
```

ElevenLabs credentials are currently environment-variable only.

> [!NOTE]
> OpenAI and ElevenLabs receive the recorded WAV file for transcription.

### Handy

Handy uses its installed local models. Open `OpenCode Voice: Config` and select
an installed Handy model. If Handy is not on `PATH`, set **Handy executable** to
an absolute AppImage or GUI executable path; OpenCode Voice never downloads or
installs Handy.

Resolution order is `OPENCODE_VOICE_HANDY_BINARY`, the saved Handy executable,
`handy` on `PATH`, then standard platform locations. On Linux, either add Handy
to `PATH` or select an AppImage such as `~/.local/bin/Handy.AppImage` or
`~/Applications/Handy.AppImage` in the configuration screen.

## Audio and privacy

OpenCode Voice records mono 16 kHz WAV audio. It sends the complete recording to the selected transcription provider after recording stops; it does not insert interim text.

After transcription, the plugin trims the result and appends it to the active prompt. Existing prompt text and the transcript are separated by a blank line. Empty or silent transcriptions append nothing.

The WAV file is deleted after successful transcription or cancellation.

The plugin retries eligible transcription failures once. If the second attempt fails, it keeps the WAV file in:

```text
~/.cache/opencode-voice/failed-recordings
```

Failed recordings do not expire automatically. Review or clear this directory periodically, or remove failed recordings from the configuration screen.

OpenCode Voice does not collect telemetry. Audio and transcript content are excluded from diagnostics.

Keep provider API keys in environment variables rather than repository or project configuration files.

## Settings

Run `OpenCode Voice: Config` to change global user settings, including:

- Provider and transcription model
- Default or named microphone
- Maximum recording duration
- Microphone-level waveform
- Local Whisper models and runtime
- Custom `whisper-cli` path
- Handy executable path or auto-detection
- Failed-recording cleanup

Settings are global rather than project-specific.

Linux microphone discovery supports PulseAudio, PipeWire, and ALSA. A saved device that is no longer connected remains listed as unavailable until you select another device.

## Troubleshooting

### No recorder found

Install `ffmpeg`, `pw-record`, or `arecord` and make sure the command is available on your `PATH`.

On many Linux desktops, `ffmpeg` with PulseAudio support is the simplest option.

### Selected microphone unavailable

Reconnect the device or choose another microphone from `OpenCode Voice: Config`.

`Default system microphone` allows fallback between available recording backends. A named microphone does not.

### Cloud provider key missing

Export the provider key before starting OpenCode:

```sh
export OPENAI_API_KEY="..."
# or
export ELEVENLABS_API_KEY="..."
```

Do not place provider keys in the repository or project-level configuration.

### Local Whisper cannot start

Open `OpenCode Voice: Config` and reinstall the selected model or local runtime.

For a self-managed installation, set the path to a compatible `whisper-cli`:

```sh
export OPENCODE_VOICE_WHISPER_BINARY="/path/to/whisper-cli"
```

### Transcription failed twice

The error message includes the retained WAV path. The recording remains available for recovery or manual transcription until you delete it.

## Known limitations

- Release support is limited to Linux x64.
- Managed local transcription is CPU-only.
- Managed local models are English-only.
- The full microphone hardware matrix has not yet been tested.
- ElevenLabs requires `ELEVENLABS_API_KEY`.
- OAuth-only OpenAI credentials cannot be used without an exposed API key.
- Another plugin that replaces the same OpenCode prompt-footer slots may conflict with the recording UI.
- Failed recordings have no automatic age or size limit.

## Advanced overrides

Most users do not need these variables:

| Variable                               | Purpose                                                  |
| -------------------------------------- | -------------------------------------------------------- |
| `OPENCODE_VOICE_WHISPER_BINARY`        | Use a custom `whisper-cli` binary                        |
| `OPENCODE_VOICE_HANDY_BINARY`          | Use Handy before saved or auto-detected executable paths  |
| `OPENCODE_VOICE_FAILED_RECORDINGS_DIR` | Change the failed-recording directory                    |
| `OPENCODE_VOICE_CAPTURE_COMMAND`       | Override WAV capture; use `{output}` for the destination |

See [`docs/linux-smoke.md`](docs/linux-smoke.md) for the Linux capture matrix.

### Testing overrides

| Variable                        | Purpose                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------ |
| `OPENCODE_VOICE_RECORD_COMMAND` | Replace recording and transcription with a command that prints transcript text |
| `OPENCODE_VOICE_TRANSCRIPT`     | Supply a fixed transcript                                                      |

## Development

```sh
npm ci
npm run build
npm run typecheck
npm test
```

Maintainer documentation:

- [`docs/public-api.md`](docs/public-api.md): package API compatibility
- [`docs/linux-smoke.md`](docs/linux-smoke.md): Linux capture validation
- [`RELEASE-PLAN.md`](RELEASE-PLAN.md): release procedure
- [`SECURITY.md`](SECURITY.md): private vulnerability reporting
- [`CHANGELOG.md`](CHANGELOG.md): release history

## License

[MIT](LICENSE)
