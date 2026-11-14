# picgo-plugin-llm-rename

PicGo plugin that renames uploaded images to **semantic English filenames** using a vision LLM, driven through [opencode](https://opencode.ai) or any OpenAI-compatible endpoint. Batch uploads of several screenshots at once become readable, consistent names with zero manual naming effort.

Built as a `beforeUploadPlugins` hook, so it works with any uploader (GitHub, SMMS, S3, ...) and with PicGo GUI + PicGo-Core CLI.

## How it works

1. In the `beforeUploadPlugins` phase, the plugin collects all images in the current upload batch.
2. In a single batched call it asks a vision model for one semantic English filename per image, in order — either via `opencode run` with every image attached (`--file=...`), or via one `/chat/completions` request carrying the images as base64 `image_url` parts (`mode: oai`).
3. The suggested names are sanitized (lowercase kebab-case, length/word limits, collision suffixes).
4. Depending on the environment the names are confirmed or applied:

| Scenario | LLM succeeds | LLM fails |
| --- | --- | --- |
| PicGo GUI | apply names automatically | abort the upload with an error |
| CLI with TTY | confirm each name (accept / edit prefilled / keep original) | go straight to a manual input prompt |
| CLI without TTY (scripts/CI) | apply names automatically | abort the upload |

If PicGo's built-in timestamp rename (`settings.autoRename`) is enabled, the plugin refuses to run — it would silently overwrite the generated names.

## Requirements

- Either [opencode](https://opencode.ai) installed and on `PATH` (or set the `opencodeBinPath` config), authenticated with a provider that has a vision model; or any OpenAI-compatible endpoint with a vision model (`mode: oai`).
- PicGo-Core `>= 1.5.0` or PicGo GUI.

The default `opencode` mode uses the free `opencode/mimo-v2.5-free` (OpenCode Zen) model. UI strings are localized via PicGo i18n (`zh-CN` and `en`); switch with `picgo i18n` or the GUI language setting.

> Privacy note: `mimo-v2.5-free` is free while it lasts, and data collected during that period may be used to improve the model. If you prefer zero-retention, set the model to `opencode/x-preview-f-free` (also free, no training on your data).

## Install

```bash
picgo install llm-rename
# or
npm install picgo-plugin-llm-rename -g
```

## Configuration

Run `picgo set` and pick `picgo-plugin-llm-rename`, or edit the `picgo-plugin-llm-rename` key in `~/.picgo/config.json`:

```json
{
  "picgo-plugin-llm-rename": {
    "mode": "opencode",
    "model": "opencode/mimo-v2.5-free",
    "opencodeBinPath": "opencode",
    "oaiBaseURL": "",
    "oaiApiKey": "",
    "oaiModel": "",
    "style": "kebab",
    "maxLength": 60,
    "maxWords": 6,
    "confirm": "each",
    "timeout": 120000,
    "prompt": "You are a naming assistant for a personal tech blog. ..."
  }
}
```

| Option | Default | Description |
| --- | --- | --- |
| `mode` | `opencode` | `opencode` (spawns the opencode CLI) or `oai` (any OpenAI-compatible `/chat/completions` endpoint) |
| `model` | `opencode/mimo-v2.5-free` | opencode model in `provider/model` form, must support image input |
| `opencodeBinPath` | `opencode` | path to the opencode binary |
| `oaiBaseURL` | `''` | OAI mode: endpoint base URL, e.g. `https://api.openai.com/v1` or `http://localhost:11434/v1` |
| `oaiApiKey` | `''` | OAI mode: API key (sent as `Authorization: Bearer`) |
| `oaiModel` | `''` | OAI mode: model id, must accept image input |
| `style` | `kebab` | `kebab` or `snake` case |
| `maxLength` | `60` | max filename length |
| `maxWords` | `6` | max number of words |
| `confirm` | `each` | `each` = confirm per image, `once` = confirm whole batch, `off` = no confirmation |
| `timeout` | `120000` | LLM call timeout in ms |
| `prompt` | (built-in) | the LLM instruction prompt (editable) |

In `opencode` mode the plugin shells out to `opencode run` and uses your opencode authentication and model selection. In `oai` mode it POSTs the images (as base64 `image_url` parts) straight to the configured endpoint — the key is stored in the PicGo config like any uploader token. Both modes do a single batched call for the whole upload.

## Usage

Upload as usual:

```bash
# files
picgo upload ./shot1.png ./shot2.png

# clipboard image (requires xclip on Linux)
picgo upload
```

Clipboard uploads are supported: when there is no local file path, the plugin writes the buffer to a temp file before handing it to opencode.

## Development

```bash
npm install
npm run build
npm test          # e2e against a real opencode call (needs picgo installed globally)
```

## License

MIT
