# Lark

Lark is a tap-to-talk companion for a child's room. A Linux host runs the speech,
conversation, and household state; ESP32 terminals provide the microphone,
speaker, touchscreen, and animated pixel face. Companions tell stories, keep
memories, exchange messages, and can be controlled from a phone.

![Lark system map: terminals connect to the Go edge, which connects to the Node brain and external services](docs/diagrams/system.svg)

## Hardware

| Board | Display | Power | Notes |
| --- | --- | --- | --- |
| ESP-VoCat v1.2 | 360 × 360 round touch | Battery | `BOARD=vocat` (default) |
| ESP32-S3-BOX-3 | 320 × 240 rectangular touch | USB | `BOARD=box3`, no battery gauge |

Both boards are ESP32-S3 with a 16 kHz mono microphone and speaker. The edge
renders frames at the panel's physical size; layouts use a 120 × 120 logical
canvas on VoCat and 160 × 120 on BOX-3. An unlinked board draws a local fallback
face and dims after 120 seconds; touch wakes it.

Lark needs one Vulkan GPU on the host. Models run without an X display.

## Quick start

### 1. Host

Install Go 1.26, Node 26 with npm, GCC, a C++ compiler, CMake, Ninja, Vulkan
drivers with development headers and the loader, `glslc`, the SPIR-V Headers
CMake package, Python 3, Podman or Docker, `ffmpeg`, `curl`, and `uvx` (USB
flashing only). Use a systemd user session.

```sh
./scripts/setup-host.sh
```

Setup builds `lark-edge`, `lark-library`, and `lark-ops` into
`~/.local/share/lark/`, runs `npm ci` for the TypeScript brain, verifies and
installs Parakeet Q8_0, Silero v5, Smart Turn v3.2, and the Kokoro
`kokoro-multi-lang-v1_0` pack, downloads `deltachat-rpc-server`, and installs and
starts `lark-edge.service` and `lark-brain.service`.

On a multi-GPU host, use `vulkaninfo --summary` and pass `--gpu-index INDEX`.
`TTS_MODEL_DIR` in `~/.config/lark/lark.env` loads Kokoro from another
directory. `LARK_REPO_DIR` locates the agent prompt and remote assets when the
checkout moves; the units set it.

Rebuild and restart from the checkout with:

```sh
~/.local/share/lark/lark deploy
```

It reuses the cached Parakeet build, reinstalls the binaries atomically,
refreshes the units, and restarts both services. Setup remains the first-install
path.

### 2. Firmware config

```sh
cp firmware/sdkconfig.local.example firmware/sdkconfig.local
chmod 600 firmware/sdkconfig.local
```

Set `CONFIG_LARK_WIFI_SSID`, `CONFIG_LARK_WIFI_PASSWORD`, `CONFIG_LARK_URL`
(`lark://<host>:8766`, `http://<host>:8765`, or bare `<host>[:port]`), and
`CONFIG_LARK_TOKEN` (copy `LARK_TOKEN` from `~/.config/lark/lark.env`). Both
board builds read the same file. Never commit it or share the resulting
binaries.

### 3. Build and flash

```sh
./scripts/build.sh vocat
./scripts/flash-usb.sh /dev/ttyACM0
./scripts/monitor.sh /dev/ttyACM0
```

BOX-3:

```sh
./scripts/build.sh box3
BOARD=box3 ./scripts/flash-usb.sh /dev/ttyACM0
```

Builds run the ESP-IDF 5.5 container through Podman or Docker, keep `ccache` in
`~/.cache/lark-ccache`, and write `firmware/build/` or `firmware/build-box3/`.
An unchanged board prints `up to date`; `--force` rebuilds.

The board sets its DHCP hostname to its terminal id (`vocat-…` or `box3-…`).
Check your router's lease table for the address.

### 4. Update over the network

```sh
~/.local/share/lark/lark ota <ip|host>
BOARD=box3 ~/.local/share/lark/lark ota <ip|host>
```

`--no-build` reuses the current image and `--board box3` selects the board.
The command refuses a board mismatch, uploads the image, and waits for the
device to boot the new version on the other OTA partition and reconnect. OTA is
push-only; boards never pull.

### 5. Pair a contact

On the companion: **Menu → More → Pair**. Scan the QR code with Delta Chat on
the phone. The QR is the only pairing path; there is no host-side pairing form.
`/help` lists every command.

### 6. Check the install

```sh
./scripts/check.sh
```

The gate covers shell checks, TypeScript typecheck and the brain suite, Python
setup tests, Go vet and race tests, host C tests for both boards, diagram
hygiene, and tracked-file hygiene. `--remote-ui` adds the headless-Chromium
remote-page tests. `--fast` runs only areas touched by the current diff. See
[docs/testing.md](docs/testing.md).

## Operator commands

Use `~/.local/share/lark/lark`, or put that directory on `PATH`.

| Command | Purpose |
| --- | --- |
| `lark status` | Health, model states, library plan, companions, and terminals. |
| `lark doctor` | Edge socket, HTTP API, model states, song recognizer, Delta Chat readiness, and orphaned accounts. Exits non-zero on failure. |
| `lark deploy` | Rebuild and reinstall the edge and host tools, refresh units, restart both services. |
| `lark ota <ip\|host>` | Build and push firmware; `--no-build`, `--board box3`. |
| `lark tunnels [stop <companion>]` | List or stop saved `/remote` tunnels. |
| `lark capture <companion> [seconds]` | Record the voice-owner mic to a local 16 kHz WAV. |
| `lark library [--plan\|--status]` | Show the disk-aware library plan. |
| `lark library --download --build` | Provision library packs. |
| `lark companions [add <name> <form>\|rm <id>]` | List or edit companions. |
| `lark terminals [attach\|detach\|rm]` | List or edit terminals. |

Captures live under `~/.local/share/lark/debug/` (directory `0700`, files
`0600`) and are pruned after 14 days or 1 GiB. They are never uploaded, never
used as fixtures, and only the host or a scoped `/remote` link holder can
play, transcribe, or delete them.

## Using Lark

### Voice and touch

Tap the face, wait for the tone, and speak. Pause to send automatically, or tap
**Send** to finish early, **Cancel** to discard, and **Stop** to interrupt a
reply. The edge owns endpointing: it keeps the mic open through thinking pauses
and commits on gated silence. See [docs/endpointing.md](docs/endpointing.md).

Tap **Menu**:

- **Stories** opens the Twee reader.
- **Memories** lists saved memories.
- **Voice** pages through eight voices and previews each on the device.
- **More** holds **Volume**, **Pair**, **Unpair**, and **Stats**.

**Stats** shows the companion, voice, board, firmware, volume, timers, stories,
battery, and Wi-Fi signal. `GET /api/diagnostics` returns live router state, and
firmware reports CPU, heap, PSRAM, RSSI, battery, and uptime every 5 seconds
(15 seconds while the panel sleeps).

### Delta Chat

Each companion has its own Chatmail account and talks to verified contacts. All
off-device traffic is text: incoming voice notes are decoded with `ffmpeg` and
transcribed, and replies are sent as text. Lark never sends an audio attachment.

| Command | Effect |
| --- | --- |
| `/say <words>` | Speak the words aloud exactly. |
| `/private <words>` | Reply just to the sender; do not speak in the room. |
| `/story <name>` | Open a story on the device. |
| `/stories` | List stories and progress. |
| `/remote` | Reply with a scoped phone control link. |
| `/remote off` | Stop the link and revoke its tokens. |
| `/help` | Show the command list. |

Sending a `.twee` file imports a story.

### Phone controls

`/remote` returns one tappable link. It opens a phone-first page over an
OpenTunnel HTTPS subdomain with live state, **Say**, a listening toggle,
per-terminal volume, story progress with **Continue** and **Start over**,
history, voice preview, and a Diagnostics tab for opt-in 15/30/60-second room
captures with playback and transcription. It installs to a home screen with the
companion's name and portrait.

A link is scoped to one companion and one Delta Chat contact. Each `/remote`
mints a new token and retires the previous one; `/remote off` revokes it and
stops the tunnel. See [ARCHITECTURE.md](ARCHITECTURE.md#security-and-privacy).

### Agent and models

The brain embeds `@opencode/sdk` in its own process with its own config, session
data, cache, and state. It loads only Lark's `lark.context`,
`lark.model-fallback`, and `lark.tools` plugins and never reads personal
OpenCode sessions or coding configuration. The default companion model is
`opencode/claude-haiku-5-5#none`, with one fallback retry on
`opencode/gpt-6-luna#low` and a `deep` subagent on
`opencode/claude-sonnet-5-5#high`. Model choices and tool contracts live in
[ARCHITECTURE.md](ARCHITECTURE.md#agent-and-tools).

## Where next

- [ARCHITECTURE.md](ARCHITECTURE.md) — process map, voice pipeline, wire
  protocol, data model, invariants, and security boundaries.
- [docs/README.md](docs/README.md) — documentation index.
- [docs/protocol.md](docs/protocol.md) — generated terminal wire catalogue.
- [docs/endpointing.md](docs/endpointing.md) — endpoint policy and measurements.
- [docs/stt-speed.md](docs/stt-speed.md) — local speech recognition numbers and
  artifact pins.
- [docs/testing.md](docs/testing.md) — gate phases, `--fast`, and timings.
- [lark-upgrade changelog](.opencode/skills/lark-upgrade/references/changelog.md)
  — breaking changes and upgrade steps.

Run Lark on a trusted LAN. Device transport and the admin HTTP API are
unencrypted; keep configs and firmware images private.

## License

Lark's source code is [Apache-2.0](LICENSE). See [NOTICE](NOTICE) for
third-party software and model licenses.
