# opencode-tts

TTS-style Japanese text-to-speech for **OpenCode Desktop**, built on the experimental GUI plugin API. Select text, right-click, and listen — no Python, no cloud account, just the Microsoft Edge neural voices over a direct WebSocket.

日本語版: [下の「日本語」セクション](#日本語) を参照してください。

## Features

- **Right-click "選択した文字列を読み上げ"** (read selected text) on any selection in the chat view, via a floating context menu (the host has no plugin context-menu API yet, so the plugin renders its own Portal menu).
- **Read the previewed file aloud**: a header button and a command read whatever file the review panel has open (Markdown and code are cleaned up server-side before synthesis, and very long files are clipped).
- **Edge neural voices** (e.g. `ja-JP-NanamiNeural`, `ja-JP-KeitaNeural`, plus the full edge-tts voice list) streamed as MP3 through a direct `speech.platform.bing.com` WebSocket connection. **No Python and no `edge-tts` package required** — the Sec-MS-GEC token logic was ported from [msedge-tts](https://github.com/andresayac/msedge-tts) (MIT, attribution kept in `src/tts.ts`).
- **Long text is chunked** to fit one SSML frame each and stitched into a single MP3.
- **Preferences persisted server-side** (`ctx.storage`, key `tts/prefs`): voice, speaking rate (-50%..+50%), auto-play of new assistant messages.
- Player panel with play/pause/stop and progress, header button, commands (`/tts`), and English/Japanese strings.

## Install

Requires OpenCode 2.x with the Desktop GUI (the GUI half loads through the `./gui-experimental` export).

From GitHub (once published), or with a local path:

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "plugins": [
    { "package": "github:YOUR_GITHUB/opencode-tts" }
    // or: "/absolute/path/to/opencode-tts"
  ]
}
```

Then **fully restart the OpenCode background service** (quitting the window is not enough — the service is a separate process):

```sh
~/.config/ai.opencode.desktop/cli/*/opencode-cli service restart
```

A plugin's GUI half is registered only when the service boots, so without this restart you get no menu entry/button. Beyond that nothing else to install — the TTS transport is plain Node.js `WebSocket` + `crypto`.

> Network note: the plugin connects to `speech.platform.bing.com` (the same endpoint the Edge browser "Read aloud" uses). No audio ever leaves your machine other than the text being synthesized.

## Build from source

```sh
npm install
npx tsc --noEmit
npx vite build   # -> dist/gui-experimental.cjs (the GUI half)
```

The server half runs straight from `src/index.ts` (TypeScript is loaded by the host).

## How it works

```
GUI (gui.tsx)                      Server (index.ts + tts.ts)
  ctx.client.rpc(tts/*)  ->   /api/rpc/tts/<method>
  Audio(data:audio/mpeg)       <-   base64 MP3
```

- `synthesize(text, voice, rate)` opens one WebSocket per chunk, sends the `speech.config` + SSML frames exactly like Edge does (including the Sec-MS-GEC right token, time-based SHA-256), and collects binary frames into an MP3.
- Prefs live in `ctx.storage` so they survive restarts and are shared by all clients.
- The context menu: a capture-phase `contextmenu` listener finds the current selection and renders a Portal menu with 「選択した文字列を読み上げ」.
- The previewed file: each tab of the host's review panel carries `data-value="file://<workspace path>"` and the selected one is marked, so the plugin reads that path from the DOM, loads the file through `ctx.screen.current().file` and speaks it like any other text.

## 日本語

OpenCode Desktop に日本語読み上げ (TTS) を追加するプラグインです。

- チャットの文章を選択して右クリック → **「選択した文字列を読み上げ」**
- ファイルプレビューパネルで開いているファイルもそのまま読み上げられます（ヘッダーボタンまたはコマンド）。
- 音声は Microsoft Edge のオンライン音声（ニューラル音声）を直接 WebSocket で叩いて取得します。**Python 不要・edge-tts 不要**（Sec-MS-GEC トークン生成は msedge-tts (MIT) から移植、出典表記は `src/tts.ts` に保持）。
- 声の選択・話速（-50%〜+50%）・「新しいアシスタントメッセージを自動で読む」設定はサーバー側に保存されます。
- ヘッダーボタンと `/tts` コマンドからも操作できます。

注意点:

- 合成には `speech.platform.bing.com` へのアウトバウンド接続が必要です（読み上げたいテキストのみ送信されます）。
- xrdp 越しセッションではサウンド再生先が無いことがあり、再生テストは実機で行ってください。

## Security notes

- **No credentials anywhere.** The `trustedclienttoken` in `src/tts.ts` is a constant Microsoft ships inside every Edge installation (public since the EdgeTTS protocol was reverse-engineered; identical in every edge-tts implementation) — a protocol constant, not a secret. Text goes only to the public Edge TTS WebSocket, and only when you press Play. 認証情報はいかなるファイルにも含まれません。上記トークンは Edge 全インストール共通の公開定数です。
- Everything the assistant said is XML-escaped before being placed in the SSML envelope (`src/tts.ts` → `escapeXml`), so reply text can never inject tags into the request. Covered by `test/tts.test.ts`.

## Acknowledgements

- [msedge-tts](https://github.com/andresayac/msedge-tts) (MIT) — port of the Sec-MS-GEC v2 token generation.
- The `@opencode/plugin/gui` experimental API (OpenCode 2.3).

## License

MIT
