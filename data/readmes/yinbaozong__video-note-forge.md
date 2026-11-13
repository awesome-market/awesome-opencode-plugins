# 视学工坊 · Video Note Forge

把 YouTube、Bilibili 视频整理为适合 Obsidian 长期学习的中文笔记，保留独立 SRT、视频封面和与讲解对应的关键截图。

**当前版本：v4.3.0** · [完整示例：ScanRuler](docs/examples/scanruler.md) · [发布说明](docs/releases/v4.3.0.md)

当前源码为 **v4.3.0开发预览**，展示名改为“视学工坊”；插件ID与配置不变。新增Bilibili普通投稿/分P适配及两个任务并行，真实跨平台双文章生成验收尚未完成，详见[版本说明](docs/releases/v4.3.0.md)。下方安装和使用步骤继续适用，旧名称对应同一插件。

术语表现在同时保留缩写与全称，例如：视觉语言动作模型｜**VLA**｜**Vision-Language-Action**｜结合视觉、语言与动作的模型。没有通用缩写的术语填“—”，不编造。

验证范围：[多视频并行与 Bilibili 计划、实测及验收清单](docs/multivideo-bilibili-plan.md)。开发预览包含相应代码，但不代表真实双视频端到端验收已通过。

## 笔记是什么样的

- **解释型正文**：沿着问题、原理、案例与限制展开，不把字幕压缩成零散提纲。
- **按信息密度展开**：约25分钟的高密度视频目标5000—7000字，短视频相应收敛，不靠重复凑篇幅。
- **自动判断视频重心**：教程侧重步骤与原因，评测保留测试条件和能力边界，观点内容说明论据；不强套同一种文章结构。
- **截图作为证据**：放在对应段落旁，图注说明画面能证明什么；没有截图的重要内容仍须解释。
- **两张 Mermaid 图**：可视化总结与学习图谱，分别梳理流程或逻辑，以及概念关系。
- **中英术语**：首次出现给出英文全称，适用时附缩写，文末术语表解释具体语境。
- **明确区分 AI 补充**：仅在启用“允许 AI 延伸解读”时生成，单独标注，不冒充视频实测或作者观点。

[ScanRuler 完整示例](docs/examples/scanruler.md)包含八张原视频截图、两张图和术语表，保留赞助披露与证据边界。封面仅在成功取得时插入，不以封面替代关键帧。

## 工作方式

```text
Chrome 当前视频页 → YouTube 阅读器 → Obsidian YouTube Note Reader
  → youtube-transcript Skill → 模型 API → 当前 Vault 的学习笔记与素材
```

完整阅读器无需 OpenCode 或独立桌面伴侣。Obsidian 编排既有提取流程，Skill 与插件提示词采用一致的写作要求。详细边界见 [v4 架构](docs/architecture-v4.md)。

## Windows 安装

### 1. 准备依赖

Windows 10/11、Chrome、Obsidian 桌面版 **1.11.4+**、**Python 3.10+**、**FFmpeg**、**Node.js**，以及可用的 OpenAI-compatible 模型 API Key。确保可访问 YouTube 与所选模型服务。

在 PowerShell 检查依赖已加入 PATH：

```powershell
python --version
ffmpeg -version
node --version
```

完整发布包 `youtube-reader-chrome-obsidian-v4.3.0.zip` 含编译好的插件；普通安装不需要 npm。使用源码且缺少编译产物时，安装器会用 npm 安装并构建插件。

### 2. 安装到 Vault

先用 Obsidian 创建或打开目标 Vault。解压完整发布包，在解压目录运行，替换为自己的 Vault 路径：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Vault "D:\Notes\MyVault"
```

安装器安装 `requirements.txt` 中的 Python 依赖（含 yt-dlp 浏览器指纹支持），并部署插件与 Skill。默认不安装语音识别；需要时在上述命令末尾追加 `-InstallAsr`。

重启 Obsidian，在“设置 → 第三方插件”启用 **YouTube Note Reader**。插件位于 `<Vault>\.obsidian\plugins\youtube-note-reader`，Skill 位于 `<Vault>\.obsidian\skills\youtube-transcript`。

### 3. 配置 API

进入 Obsidian 的 **YouTube Note Reader** 设置页：

| 设置 | 填写方式 |
| --- | --- |
| API Base | 服务商的 OpenAI-compatible 接口根地址，按服务商要求包含版本路径 |
| Model | 服务商提供的完整模型名 |
| API Key | 填写自己的密钥，保存后点击“验证 API Key” |
| Python | 通常为 `python`，或本机 Python 可执行文件路径 |
| Skill 目录 | 保持当前 Vault 内的默认安装路径 |
| 输出目录 | 默认 `YouTube video` |

API Key 保存在 Obsidian SecretStorage，Chrome 不读取密钥。验证会发送最小模型请求，可能产生费用；任务使用配置的模型，不自动切换服务商。

### 4. 加载 Chrome 扩展

1. 打开 `chrome://extensions`，开启“开发者模式”。
2. 点击“加载已解压的扩展程序”，选择发布包的 `extension` 文件夹。
3. 固定 **YouTube 阅读器**；打开“连接与设置”，确认已连接目标 Vault，且 API Key 验证成功。

扩展通过 `127.0.0.1:32191` 连接本机 Obsidian。连接失败时检查 Obsidian 是否打开、插件是否启用，以及端口是否被占用。

## 使用

1. 保持目标 Vault 与插件开启，在 Chrome 登录 YouTube 并打开视频。
2. 按需在插件设置中选择标准学习笔记、详细教程或通俗讲解，填写自定义要求，决定是否允许 AI 延伸解读。
3. 点击 **YouTube 阅读器 → 生成学习笔记**。一次处理一个视频，关闭弹窗不影响后台任务。
4. 完成后点击“在 Obsidian 打开”；任务中心可搜索历史笔记并打开原视频。

流程为字幕与素材提取、文章规划、定点抽帧、写作、校验。已有完整页面文字稿可复用；没有可用字幕时不会自动开启 ASR。只有显式点击“允许 ASR 并重试”才下载音频并进行本地识别，需要事先安装可选依赖。

页面采集不会自动展开描述或文字稿，也不会自动点击播放控件；在原有15秒总预算内观察已加载的字幕面板。字幕问题的已知原因和本地修复验证范围见[字幕采集排查](docs/caption-capture.md)。

模型超时或 Obsidian 中断后，使用继续入口复用已有素材。标准与通俗模式总时限为 8 分钟，详细模式为 12 分钟；网络、字幕可用性和模型响应仍可能导致失败。

```text
<Vault>/YouTube video/
  中文标题 - English Title.md
  transcripts/中文标题 - English Title.srt
  assets/<video-id>/cover.jpg       # 成功提取时保留
  assets/<video-id>/frame_*.jpg
```

原始字幕独立保存，不粘贴进正文。截图定点提取，不下载完整视频；ASR 会额外下载音频。Cookie 与素材留在本机，写作所需字幕等内容会发送给所配置的模型服务，请自行确认其数据政策。

## 更新与排错

升级后重新运行安装器，重启 Obsidian，并在 Chrome 扩展页重新加载阅读器。验证安装：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_install.ps1 -Vault "D:\Notes\MyVault"
```

失败时先查看具体阶段与错误；通过“复制诊断日志”定位本地日志，分享前检查隐私。不要把字幕下载失败直接理解为视频没有字幕，也不要发布 Cookie、API Key 或整份私人 Vault。

仅 Skill 用户可选择 `youtube-transcript-skill-v4.3.0.zip`，按 [SKILL.md](SKILL.md) 调用既有脚本；保留可选 OpenCode 入口，但不包含完整阅读器的浏览器同步与任务界面。

## 更多

[版本变化与验证边界](docs/releases/v4.3.0.md) · [完整学习笔记示例](docs/examples/scanruler.md) · [架构](docs/architecture-v4.md) · [MIT License](LICENSE)
