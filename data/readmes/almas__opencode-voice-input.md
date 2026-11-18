# opencode-voice-input

Local speech-to-text for **OpenCode Desktop**: click the microphone (composer pill, header button, command palette, or `Ctrl+Shift+M` / `Cmd+Shift+M`), speak, and the transcript is inserted into the composer. Recording uses PipeWire, transcription runs entirely on your machine with **whisper.cpp** — no cloud STT, no API keys.

日本語版: [下の「日本語」セクション](#日本語) を参照してください。

## Features

- **Four ways to trigger**: composer pill (always visible, shows state + elapsed time), session header button, command palette, and the `mod+shift+m` keybind.
- **Floating recording overlay**: animated level meter from your live mic (WebAudio RMS), elapsed timer, Stop / Cancel buttons, `Esc` to cancel.
- **Silence auto-stop**: after the first words, ~2.5 s of silence ends the take for you. If the meter never moves at all, the take auto-cancels with a clear warning (dead/blocked mic).
- **Audible cues**: short tones on start/stop (opt-out in settings), so you never stare at a mic that isn't recording.
- **PipeWire capture** via `pw-record --rate 16000 --channels 1 --format s16`, stopped with SIGINT/SIGTERM.
- **Local whisper.cpp** transcription (`whisper-cli`, e.g. `large-v3-turbo`), tuned flags: `-l ja -t 24 -np -otxt`. Whisper's classic silence hallucinations (「ご視聴ありがとうございました」, 【音楽】 …) are filtered out instead of inserted.
- **Inserts into the composer** through `ctx.screen.current()?.composer.insert(text)` — you review before sending. With no open session the text goes to the clipboard instead of being lost, and **"Voice Input: copy last transcription"** re-copies the latest take.
- **Preferences** persisted server-side (`ctx.storage`, key `voice-input/prefs`): language (ja/en/auto), thread count, whisper binary path, model path, start/stop tones.
- 300 s safety cap on a single recording; `Esc` or Cancel aborts without transcribing; failed attempts leave a visible warning pill with the error.
- **Failures never lose your audio**: if whisper fails (bad model path, out of memory…), the WAV take is kept, the overlay shows a red *failed* state with the error and a **Retry** button (`Esc`/Discard drops it), and the pill turns into a retry shortcut — re-transcribe the exact same take without recording again.

## Requirements (Ubuntu)

1. **PipeWire** with a microphone input source (`pw-record` must exist; not tested on PulseAudio-only).
2. **whisper.cpp** ≥ 1.7 with `whisper-cli`, plus a GGML model.

Run the bundled scripts instead of doing it by hand (they are idempotent and need no root):

```sh
./script/check-prereqs.sh    # what's missing? prints OK/NG with hints
./script/setup-whisper.sh    # apt-download + unpack whisper.cpp into ~/.local, then fetch large-v3-turbo (~1.6 GB)
./script/check-prereqs.sh    # verify
```

<details>
<summary>Manual equivalent (no root)</summary>

```sh
# the deb package is literally named "whisper.cpp" on Ubuntu
cd /tmp && apt-get download whisper.cpp libwhisper1 libggml0
for p in whisper.cpp libwhisper1 libggml0; do dpkg-deb -x $p*.deb ~/.local; done
mkdir -p ~/.local/bin && ln -sf ~/.local/usr/bin/whisper-cli ~/.local/bin/whisper-cli

# model (~1.6 GB)
mkdir -p ~/.local/share/whisper-models
curl -L -o ~/.local/share/whisper-models/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
```

</details>

The plugin resolves `~/.local/bin/whisper-cli` and `~/.local/share/whisper-models/ggml-large-v3-turbo.bin` by default, and exports `LD_LIBRARY_PATH` for the `~/.local/usr/lib` libs. Override both paths in the plugin settings panel.

> xrdp note: with xrdp **audio redirection enabled** the mic works end-to-end — PipeWire shows an `xrdp-sink`/`xrdp-source` pair; set them as the default source/sink (`wpctl status`, `wpctl set-default`). Without audio redirection there is no input source and recording will auto-cancel.

## Install

```jsonc
// ~/.config/opencode/opencode.jsonc
{
  "plugins": [
    { "package": "github:YOUR_GITHUB/opencode-voice-input" }
    // or: "/absolute/path/to/opencode-voice-input"
  ]
}
```

Then **fully restart the OpenCode background service** (quitting the window is not enough — the service is a separate process):

```sh
~/.config/ai.opencode.desktop/cli/*/opencode-cli service restart
```

The server half hot-reloads on config changes, but a plugin's GUI half is registered only when the service boots. Without the restart you get the RPC side and no button.

## Build from source

```sh
npm install
npx tsc --noEmit
npx vite build   # -> dist/gui-experimental.cjs (the GUI half)
```

GUI-only changes are served from disk on every renderer load, so after `npx vite build` a plain window reload (Ctrl+R) is enough. Adding the plugin itself requires the service restart above.

## How it works

```
GUI (gui.tsx)                        Server (index.ts)
  ctx.client.rpc(voiceInput/*)  ->    /api/rpc/voice-input/<method>
  start / stop / cancel / status      pw-record -> SIGINT -> whisper-cli -> txt
  retry / discardTake                 failed take kept on disk -> re-transcribe
  live meter (getUserMedia+RMS)       silence-hallucination filter
  composer insert / clipboard         300 s cap, status.lastError/hasLastTake
```

- `start` spawns `pw-record` into a WAV file; `stop` SIGTERMs it, runs `whisper-cli` and returns the transcript; the GUI inserts it into the composer.
- `status` reports `recording`, `seconds` and `lastError` — the GUI mirrors state across windows and surfaces failures on the pill.
- Startup RPC reads retry with backoff, so the GUI still loads its prefs during a cold service boot.

## 日本語

OpenCode Desktop に **完全ローカル** の音声入力を追加するプラグインです。

- トリガーは4種類: composer 常駐ピル（状態と経過時間表示）・ヘッダーボタン・コマンドパレット・`Ctrl+Shift+M`。
- 録音中はフローティングオーバーレイに **リアルタイムレベルメーター**（マイク音量の波形アニメーション）・経過時間・停止／キャンセルボタンを表示。`Esc` で中止。
- 話し出し後の **無音約2.5秒で自動停止**。まったく無音なら「マイクが死んでいる」と判断して自動キャンセル＋警告表示。
- 録音開始／終了時に **短いビープ音**（設定でオフ可）。
- 録音は PipeWire（`pw-record`）、文字起こしは **whisper.cpp**（例: large-v3-turbo）でローカル実行。クラウド STT は使いません。無音時の恒常的ハルシネーション（「ご視聴ありがとうございました」等）は除去します。
- 認識結果は即送信せず **composer に挿入**されるため、必ず内容を確認してから送信できます。セッション未表示時はクリップボードへ退避。「直前の文字起こしをコピー」コマンドで再コピーも可能。
- **文字起こし失敗時も録音音声は破棄せず保持**。オーバーレイにエラー内容と**再試行**ボタン（`Esc`/破棄で削除）、ピルも再試行ショートカットに変化 — 録り直しなしで同じ音声から再文字起こしできます。
- 言語（ja/en/auto）・スレッド数・whisper のバイナリ/モデルパス・ビープ音は設定パネルから変更でき、サーバー側に保存されます。失敗原因是 idle ピルの警告タイトルに表示されます。

前提: Ubuntu + PipeWire + whisper.cpp（非root導入手順は上の Requirements 参照）。xrdp ではオーディオリダイレクト有効時に `xrdp-source`/`xrdp-sink` がマイク／スピーカーとして使えます（`wpctl set-default` で既定に）。

**インストール後はバックグラウンドサービスごと再起動してください**（ウィンドウを閉じるだけでは不十分）:
`~/.config/ai.opencode.desktop/cli/*/opencode-cli service restart` — GUI 部分はサービスの起動時にのみ登録されます。

## License

MIT
