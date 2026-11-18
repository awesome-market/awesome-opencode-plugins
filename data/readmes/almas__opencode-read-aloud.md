# opencode-read-aloud

Read Aloud-style Japanese text-to-speech for **OpenCode Desktop**, built on the experimental GUI plugin API. Select text, right-click, and listen — no Python, no cloud account, just the Microsoft Edge neural voices over a direct WebSocket.

日本語版: [下の「日本語」セクション](#日本語) を参照してください。

## Features

- **Right-click "選択した文字列を読み上げ"** (read selected text) on any selection in the chat view, via a floating context menu (the host has no plugin context-menu API yet, so the plugin renders its own Portal menu).
- **Edge neural voices** (e.g. `ja-JP-NanamiNeural`, `ja-JP-KeitaNeural`, plus the full edge-tts voice list) streamed as MP3 through a direct `speech.platform.bing.com` WebSocket connection. **No Python and no `edge-tts` package required** — the Sec-MS-GEC token logic was ported from [msedge-tts](https://github.com/andresayac/msedge-tts) (MIT, attribution kept in `src/tts.ts`).
- **Long text is chunked** to fit one SSML frame each and stitched into a single MP3.
- **Preferences persisted server-side** (`ctx.storage`, key `read-aloud/prefs`): voice, speaking rate (-50%..+50%), auto-play of new assistant messages.
- Player panel with play/pause/stop and progress, header button, commands (`/read-aloud`), and English/Japanese strings.

## Install

Requires OpenCode 2.x with the Desktop GUI (the GUI half loads through the `./gui-experimental` export).

From GitHub (once published), or with a local path:

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "plugins": [
    { "package": "github:YOUR_GITHUB/opencode-read-aloud" }
    // or: "/absolute/path/to/opencode-read-aloud"
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
  ctx.client.rpc(readAloud/*)  ->   /api/rpc/read-aloud/<method>
  Audio(data:audio/mpeg)       <-   base64 MP3
```

- `synthesize(text, voice, rate)` opens one WebSocket per chunk, sends the `speech.config` + SSML frames exactly like Edge does (including the Sec-MS-GEC right token, time-based SHA-256), and collects binary frames into an MP3.
- Prefs live in `ctx.storage` so they survive restarts and are shared by all clients.
- The context menu: a capture-phase `contextmenu` listener finds the current selection and renders a Portal menu with 「選択した文字列を読み上げ」.

## 日本語

OpenCode Desktop に Read Aloud 風の日本語読み上げを追加するプラグインです。

- チャットの文章を選択して右クリック → **「選択した文字列を読み上げ」**
- 音声は Microsoft Edge のオンライン音声（ニューラル音声）を直接 WebSocket で叩いて取得します。**Python 不要・edge-tts 不要**（Sec-MS-GEC トークン生成は msedge-tts (MIT) から移植、出典表記は `src/tts.ts` に保持）。
- 声の選択・話速（-50%〜+50%）・「新しいアシスタントメッセージを自動で読む」設定はサーバー側に保存されます。
- ヘッダーボタンと `/read-aloud` コマンドからも操作できます。

注意点:

- 合成には `speech.platform.bing.com` へのアウトバウンド接続が必要です（読み上げたいテキストのみ送信されます）。
- xrdp 越しセッションではサウンド再生先が無いことがあり、再生テストは実機で行ってください。

## Acknowledgements

- [msedge-tts](https://github.com/andresayac/msedge-tts) (MIT) — port of the Sec-MS-GEC v2 token generation.
- The `@opencode/plugin/gui` experimental API (OpenCode 2.3).

## License

MIT
