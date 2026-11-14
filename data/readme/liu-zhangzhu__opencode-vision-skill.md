# opencode-vision-skill

[English](#english) | [中文](#中文)

---

## English

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey)]()

> **Give pure-text LLMs the ability to see.**

DeepSeek and other text-only LLMs cannot natively read PDFs, images, or PPTs. This skill gives them eyes — it reads the file, **describes what it sees** (objects, layout, arrows, diagrams), extracts text via OCR, and returns everything as structured Markdown.

![demo](demo.png)

### What It Does

| File Type | Capability |
|-----------|-----------|
| PDF | Extract text, headings, tables → Markdown |
| Images | **Visual description** (AI "sees" objects, arrows, boxes) + OCR text |
| PPT/PPTX | Extract slide text, bullet points, tables |
| Screenshot | Capture screen → auto-describe via image-reader |

### Quick Start

```cmd
git clone https://github.com/Liu-Zhangzhu/opencode-vision-skill.git
cd opencode-vision-skill
setup
```

Or:

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

```bash
# macOS / Linux
bash setup.sh
```

**What `setup` does automatically:**
1. Installs all Python dependencies
2. Downloads the Florence-2 model (~400MB, one time)
3. Detects which AI agents you have installed (opencode / Claude Code / Codex) and deploys `SKILL.md` to each

> To skip auto-deployment for a specific agent, edit the setup script and remove its section.

### Manual Install

```bash
pip install -r requirements.txt
```
Then copy `SKILL.md` to your agent's skill directory manually.

### Skill Paths

| AI Agent | macOS / Linux | Windows |
|----------|--------------|---------|
| **opencode** | `~/.config/opencode/skills/vision/SKILL.md` | `%USERPROFILE%\.config\opencode\skills\vision\SKILL.md` |
| **Claude Code** | `~/.claude/skills/vision/SKILL.md` | `%USERPROFILE%\.claude\skills\vision\SKILL.md` |
| **Codex** | `~/.codex/skills/vision/SKILL.md` | `%USERPROFILE%\.codex\skills\vision\SKILL.md` |

Restart your agent, then say:

> "Read this PDF: /path/to/file.pdf"  
> "What's in this image?"  
> "Take a screenshot"

### Hardware Requirements

| Component | Disk | RAM/VRAM |
|-----------|------|----------|
| Python dependencies | ~3 GB | — |
| Florence-2-base model | ~400 MB | ~2 GB (CPU) or ~2 GB VRAM (GPU) |
| **Total** | **~3.5 GB** | **~3 GB RAM** |

- **GPU not required** — runs on CPU, just slower (~30s vs ~5s per image)
- NVIDIA GPU (4GB+ VRAM) recommended for better speed
- Apple Silicon (MPS) also supported

### How It Works

```
Image → Pillow (metadata) → Florence-2 (visual description) → easyocr (text) → Markdown
                                                                     ↓ (fallback)
                                                               pytesseract (if installed)
```

```
PDF → PyMuPDF (primary) → pdfplumber (fallback) → Markdown with tables
```

### FAQ

**Q: Do I need a GPU?**  
A: No. CPU works, just slower. GPU (NVIDIA/MPS) makes Florence-2 ~5x faster.

**Q: What file formats are supported?**  
A: PDF, PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP, PPTX.

**Q: Why local instead of API?**  
A: Privacy — files never leave your machine. No API key needed. No rate limits.

**Q: Can I use it without Florence-2?**  
A: Yes. `image-reader` falls back gracefully — metadata + OCR but no visual description.

**Q: How to improve OCR accuracy?**  
A: Install Tesseract OCR system-wide:  
  - Windows: `winget install UB-Mannheim.TesseractOCR`  
  - macOS: `brew install tesseract tesseract-lang`  
  - Ubuntu: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

**Q: Screenshot doesn't work on Linux?**  
A: Install system dependencies: `sudo apt install scrot python3-tk python3-dev` (Ubuntu/Debian).

**Q: Setup fails with pip or package errors?**  
A: Drop the project folder into your AI agent's chat and say "install the dependencies for this project". The agent can diagnose and fix most environment issues (broken pip launcher, path conflicts, etc.) better than a generic script.

### Acknowledgments

- [Florence-2](https://huggingface.co/microsoft/Florence-2-base) (Microsoft) — Visual understanding model
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) — PDF text extraction
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF table extraction
- [python-pptx](https://github.com/scanny/python-pptx) — PowerPoint parsing
- [easyocr](https://github.com/JaidedAI/EasyOCR) — OCR engine
- [PyAutoGUI](https://github.com/asweigart/pyautogui) — Screenshot capture
- [Pillow](https://github.com/python-pillow/Pillow) — Image processing

### License

MIT — See [LICENSE](LICENSE)

---

## 中文

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Win%20%7C%20Mac%20%7C%20Linux-lightgrey)]()

> **让纯文本大模型获得视觉能力。**

DeepSeek 等纯文本 LLM 无法直接读取 PDF、图片或 PPT。这个 skill 给它们装上眼睛——读取文件，**描述画面内容**（物体、布局、箭头、框图），OCR 提取文字，全部输出为结构化 Markdown。

![demo](demo.png)

### 功能一览

| 文件类型 | 能力 |
|----------|------|
| PDF | 提取文字、标题、表格 → Markdown |
| 图片 | **视觉描述**（AI 识别箭头、框、布局）+ OCR 文字 |
| PPT/PPTX | 提取幻灯片文字、列表、表格 |
| 截图 | 截屏 → 自动调 image-reader 描述 |

### 一键安装

```cmd
git clone https://github.com/Liu-Zhangzhu/opencode-vision-skill.git
cd opencode-vision-skill
setup
```

或者：

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

```bash
# macOS / Linux
bash setup.sh
```

**setup 脚本自动完成：**
1. 安装所有 Python 依赖
2. 下载 Florence-2 模型（~400MB，一次性）
3. 检测你装了哪些 AI agent（opencode / Claude Code / Codex），自动把 SKILL.md 部署到对应目录

> 如果不想装到某个 agent，编辑 setup 脚本删掉对应段落即可。

### 手动安装

```bash
pip install -r requirements.txt
```
然后手动复制 `SKILL.md` 到 agent 的 skill 目录。

### 技能路径

| AI Agent | macOS / Linux | Windows |
|----------|--------------|---------|
| **opencode** | `~/.config/opencode/skills/vision/SKILL.md` | `%USERPROFILE%\.config\opencode\skills\vision\SKILL.md` |
| **Claude Code** | `~/.claude/skills/vision/SKILL.md` | `%USERPROFILE%\.claude\skills\vision\SKILL.md` |
| **Codex** | `~/.codex/skills/vision/SKILL.md` | `%USERPROFILE%\.codex\skills\vision\SKILL.md` |

重启 AI agent，然后说：

> "读一下这个 PDF"  
> "这张图里有什么？"  
> "截个图"

### 硬件需求

| 组件 | 磁盘 | 内存/显存 |
|------|------|----------|
| Python 依赖 | ~3 GB | — |
| Florence-2 模型 | ~400 MB | ~2 GB（CPU）或 ~2 GB 显存（GPU）|
| **总计** | **~3.5 GB** | **~3 GB** |

- **不需要 GPU** — CPU 能跑，只是慢些（30 秒 vs 5 秒/张）
- 推荐 NVIDIA 显卡（4GB+ 显存）加速
- 支持 Apple Silicon（MPS）

### 原理

```
图片 → Pillow(元数据) → Florence-2(视觉描述) → easyocr(文字识别) → Markdown
                                                         ↓ (备用)
                                                   pytesseract（需安装）
```

```
PDF → PyMuPDF(主引擎) → pdfplumber(备用) → 含表格的 Markdown
```

### 常见问题

**Q: 需要 GPU 吗？**  
A: 不需要。CPU 也能跑，只是慢 5 倍左右。

**Q: 支持哪些格式？**  
A: PDF、PNG、JPG、JPEG、GIF、BMP、TIFF、WEBP、PPTX。

**Q: 为什么用本地模型而非 API？**  
A: 隐私安全——文件不离开你的电脑，不需要 API key，没有调用次数限制。

**Q: 不装 Florence-2 能用吗？**  
A: 能。`image-reader` 会自动降级——只输出元数据 + OCR，没有视觉描述。

**Q: 如何提高 OCR 准确率？**  
A: 安装系统级 Tesseract OCR：  
  - Windows: `winget install UB-Mannheim.TesseractOCR`  
  - macOS: `brew install tesseract tesseract-lang`  
  - Ubuntu: `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

**Q: Linux 截图不工作？**  
A: 安装系统依赖：`sudo apt install scrot python3-tk python3-dev`（Ubuntu/Debian）。

**Q: 安装时 pip 或依赖报错？**  
A: 把项目文件夹拖到 AI agent 对话里，说"帮我装一下这个项目的依赖"。AI agent 能比通用脚本更好地诊断和修复环境问题（pip launcher 损坏、路径冲突等）。

### 致谢

- [Florence-2](https://huggingface.co/microsoft/Florence-2-base)（微软）— 视觉理解模型
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) — PDF 文字提取
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF 表格提取
- [python-pptx](https://github.com/scanny/python-pptx) — PowerPoint 解析
- [easyocr](https://github.com/JaidedAI/EasyOCR) — 光学字符识别
- [PyAutoGUI](https://github.com/asweigart/pyautogui) — 屏幕截图
- [Pillow](https://github.com/python-pillow/Pillow) — 图像处理

### 许可证

MIT — 详见 [LICENSE](LICENSE)
