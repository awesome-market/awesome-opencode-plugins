# opencode-image-parsing

[English](README.md) | [简体中文](README.zh-CN.md)

> ⚠️ This project is built on opencode's **skill + subagent** mechanism and **tested on opencode**. The mechanism itself is a general pattern — other agent frameworks with skill/subagent support (e.g. Claude Code) may work **in theory**, but the config paths, frontmatter fields, and model IDs (e.g. `opencode/mimo-v2.5-free`) are written for opencode. Adapt them to the target tool when migrating.

Let **text-only models** (e.g. DeepSeek V4 Flash) "see" images, via a skill + subagent.

When the model cannot parse an image, it automatically delegates the parsing to **MiMo-V2.5** (a vision-capable model), then continues answering based on the parsed text. Your chosen text model stays as the main model — only the "look at the image" step goes through MiMo.

## How it works

```
Text-only model (can't see images)
   │  skill "image-parsing" triggers
   ▼
Task invokes subagent mimo-vision (model: MiMo-V2.5)
   │  reads the image file with the Read tool
   ▼
Returns a detailed text description of the image
   ▼
Text-only model answers based on that text
```

- **Local images (drag & drop)** → the file path is passed directly to the subagent.
- **Clipboard-pasted images** → the base64 payload is decoded from the conversation data into a temp file, then passed to the subagent.

## One-line install

**Windows (PowerShell)**:

```powershell
$d = "$HOME\.config\opencode"
New-Item -ItemType Directory -Path "$d\agent", "$d\skills\image-parsing" -Force | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/starstarstars/opencode-image-parsing/main/agent/mimo-vision.md" -OutFile "$d\agent\mimo-vision.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/starstarstars/opencode-image-parsing/main/skills/image-parsing/SKILL.md" -OutFile "$d\skills\image-parsing\SKILL.md"
```

**macOS / Linux (bash/zsh)**:

```bash
mkdir -p ~/.config/opencode/skills/image-parsing ~/.config/opencode/agent
curl -fsSL -o ~/.config/opencode/agent/mimo-vision.md https://raw.githubusercontent.com/starstarstars/opencode-image-parsing/main/agent/mimo-vision.md
curl -fsSL -o ~/.config/opencode/skills/image-parsing/SKILL.md https://raw.githubusercontent.com/starstarstars/opencode-image-parsing/main/skills/image-parsing/SKILL.md
```

Restart **opencode** after installing.

## Manual install

Copy `skills/image-parsing/` and `agent/mimo-vision.md` to either location (or both):

**Global install** (all projects):

```
~/.config/opencode/skills/image-parsing/SKILL.md
~/.config/opencode/agent/mimo-vision.md
```

**Project-level install**:

```
.opencode/skills/image-parsing/SKILL.md
.opencode/agent/mimo-vision.md
```

## Auth (free)

The default subagent uses `opencode/mimo-v2.5-free`:

```
opencode auth login
```

One login gives you a free OpenCode Zen key. The model is **free** and supports image input — no opencode-go subscription needed.

## Switching models

To use a different model, change the `model` field in `agent/mimo-vision.md`:

| Scenario | model |
|---|---|
| Default (free) | `opencode/mimo-v2.5-free` |
| opencode-go subscriber | `opencode-go/mimo-v2.5` |
| Kenari (free tier) | `kenari/mimo-v2-5:free` |
| Xiaomi official API (key required) | `xiaomi/mimo-v2.5` |

> Restart opencode after changing the config.

## In action

After pasting a screenshot, the model outputs something like:

> Image detected (pasted) → invoking mimo-vision → parsed → continuing...
>
> This is an e-commerce product page: title "xxx", price ¥xx, xx in stock...

## Notes

- Internal details (base64 decoding, temp files, conversation-data extraction) are kept out of the output.
- If the subagent's model is not authorized, it will prompt you to run `opencode auth login` or switch models — it won't get stuck.

## License

[MIT](LICENSE) © starstarstars
