# utt for OpenCode

[![npm](https://img.shields.io/npm/v/utt-opencode)](https://www.npmjs.com/package/utt-opencode)
[![CI](https://github.com/doublej/utt-opencode/actions/workflows/ci.yml/badge.svg)](https://github.com/doublej/utt-opencode/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**Talk to your coding agent. Press `ctrl+s` in OpenCode and speak; your words
appear in the prompt as you say them.**

This plugin adds voice dictation to [OpenCode](https://opencode.ai), the coding
agent for the terminal. The listening is done by
[utt](https://utt.jurrejan.com), a free speech-to-text app for the Mac that runs
entirely on your machine. OpenCode draws the whole dictation itself: a level
meter in the footer, the live words in the prompt, and then the finished
transcript in their place, with punctuation and without the filler. Nothing you
say leaves your Mac.

![OpenCode with a dictation open: live words in italics in the prompt, and a footer that reads "listening", a level meter, "Parakeet Standard" and the keys ctrl+s stop, ctrl+y redo, esc drop](https://raw.githubusercontent.com/doublej/utt-opencode/main/assets/dictating.png)

## Part of utt: one app, many tools

utt is one on-device speech-to-text app for the Mac. It runs Parakeet TDT v3 or
Whisper locally, and it keeps your settings in one place: the model you chose,
your vocabulary, your replacements and your cleanup rules. Extensions bring that
same engine into other tools, so you install utt once and add an extension for
each tool you use. utt asks you to approve every extension before it gets
anything.

| Extension | What it does |
| --- | --- |
| **OpenCode** (this repo) | Dictate into the prompt of the OpenCode terminal coding agent. |
| [Deckhand](https://github.com/doublej/deckhand) | Talk to Claude Code from your iPhone. |
| [Reel](https://github.com/doublej/reel) | An MCP server that transcribes any video on your Mac. |
| [Raycast](https://github.com/doublej/utt/tree/main/raycast) | Toggle dictation, pick a microphone and browse recent transcriptions from Raycast. |

More about utt and its extensions: [utt.jurrejan.com](https://utt.jurrejan.com).

## Requirements

- macOS 26 or later, on Apple silicon.
- [utt](https://utt.jurrejan.com/download) 2.4 or later, installed.
- OpenCode with plugin support (`opencode plugin add`).

## Install

```sh
opencode plugin add utt-opencode
```

This adds `utt-opencode` to `plugins` in `~/.config/opencode/cli.json`.

1. Restart OpenCode to load the plugin.
2. On its first start the plugin registers itself with utt as the **OpenCode**
   extension, and utt waits for you to approve it. The first time you press
   `ctrl+s` before you have, utt opens on that page in place of recording.
3. Approve it there, then press `ctrl+s` again.

Words appear while you speak only if **Show words while you speak** is on in
utt. Those live words come from utt's smaller streaming model and are English
only. The transcript that replaces them comes from your chosen model, after your
replacements, cleanup and formatting.

## Keys

| Key | What it does |
| --- | --- |
| `ctrl+s` | Start talking. Press it again to stop. Pressed while a transcript is still on its way, it starts the next take. |
| `ctrl+y` | Clear the prompt and start a new take. Works at any point. |
| `esc` | Throw the dictation away, also while it is still being transcribed. It only does this while a dictation is open; otherwise Esc does what it always does. |
| `enter` | Held while a dictation is open, so the prompt cannot go out before the transcript has replaced the live words. A toast says what it is waiting for. |

No key ever waits on utt, apart from Enter, which waits on purpose. The same
commands are in the palette (`utt: dictate`, `utt: clear and dictate again`) and
as `/dictate` and `/redictate`.

While a dictation is open, it takes over the whole prompt footer: `● listening`
with utt's level meter in its own green, yellow and red, or `◌ transcribing`,
then the speech model writing the transcript (`Parakeet Standard`), and the keys
that end it. The token count, cost and command hints come back when the
dictation closes. The live words are drawn italic in the theme's info colour.
The transcript lands in ordinary text, so you can tell when the words are final.

Words you already typed stay. The dictation goes in at the cursor, with a space
added where it would otherwise run into the text around it.

## Options

Other keys go in the object form of the plugin entry:

```json
{
  "plugins": [{ "package": "utt-opencode", "options": { "key": "ctrl+s", "redoKey": "ctrl+y" } }]
}
```

| Option | Default | What it sets |
| --- | --- | --- |
| `key` | `ctrl+s` | Start and stop a dictation. |
| `redoKey` | `ctrl+y` | Clear the prompt and dictate again. |

To run the plugin from a checkout instead, put the folder's path where the
package name is, for example `"/Users/you/dev/utt-opencode"`.

## Without utt

The plugin stays quiet until you press the key. Then it shows a toast that says
dictation needs utt and where to download it. Nothing else changes in OpenCode.

Until you approve the extension in utt, or with a utt that is too old to hand a
dictation over, a dictation is an ordinary one: utt shows its own indicator and
panel and pastes the text at the cursor. The plugin then stays out of the prompt.

## Privacy

- Speech is turned into text by utt, on your Mac. No audio and no text is sent
  to any server by utt or by this plugin.
- The plugin talks only to utt, through files in utt's Application Support
  folder and `utt://` links. It makes no network requests.
- The plugin keeps a log at `~/Library/Logs/utt-opencode.log` with one line per
  event. It records lengths, never the words.

Your prompt still goes to whichever model provider you use in OpenCode once you
press Enter, the same as text you typed.

## How it works

It uses the same two channels as every utt extension. Commands go through utt's
URL scheme, always opened with `open -g` so the terminal stays frontmost:

- `utt://start?for=opencode` starts a dictation of the plugin's own.
- `utt://stop` and `utt://cancel` end it.

Everything the plugin reads is an extension file in
`~/Library/Application Support/dev.jurrejan.utt/extensions/`:

| File | Direction | What for |
| --- | --- | --- |
| `opencode.json` | write | The manifest, rewritten at every start. Declares `ownsDictation`, `wantsTranscripts` and `wantsPartials` |
| `opencode.level.json` | read | The microphone level, about 20 times a second, for the meter, and the name of the speech model writing the transcript |
| `opencode.partial.json` | read | Words heard so far, while you speak |
| `opencode.transcript.json` | read | The finished transcript, or `""` when nothing came of it |
| `opencode.consent.json` | read | Whether you approved it, for the first-press detour |

The first write to `opencode.level.json` after the plugin starts a dictation is
how it knows utt handed that dictation over. Without one, utt is showing and
pasting the dictation itself, and the plugin stays out of the prompt. Every
dictation utt hands over ends in exactly one transcript write, so the plugin
never has to guess when to stop waiting. The full contract is the
`ownsDictation` section of utt's extension guide, which you can copy from the
Extensions page in utt.

`wantsTranscripts` hands the plugin every transcript you dictate anywhere. It
only reads the file while a dictation it started is open, and it never sends
anything anywhere.

## Development

```sh
bun install
bun run check   # typecheck
bun test
bun run build   # dist/tui.js
just check      # all three
```

The npm package ships `dist/tui.js`, built by `bun build.ts` when it is packed.
OpenCode compiles a plugin's JSX only outside `node_modules`, so the package
cannot ship the `.tsx` source. A local checkout still loads `tui.ts` directly.

Changes load on the next OpenCode start. To try it without utt listening, start
OpenCode with `UTT_APPLICATION_SUPPORT` pointed at a scratch folder and a fake
`open` first on `PATH`. Then write `opencode.consent.json`, `opencode.level.json`,
`opencode.partial.json` and `opencode.transcript.json` by hand.

The utt side of the contract lives in [doublej/utt](https://github.com/doublej/utt).
Issues and ideas: [github.com/doublej/utt-opencode/issues](https://github.com/doublej/utt-opencode/issues).

## License

[MIT](LICENSE)
