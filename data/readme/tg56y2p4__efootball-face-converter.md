# efootball-face-converter

按球员、球队、年代及发型寻找已有脸模。找到可用模型时转换为球员工坊 GLB。找不到合适资源时，从实拍生成四视图，经用户确认后重建脸模。也可直接用用户指定的照片开始四视图审核。

当前版本为 **v1.2.0**。两条路线都输出 **1 个 mesh、1 个 primitive、1 个 material** 的 GLB，内嵌 PNG 图集和 166 关节工坊骨架。

## 安装

从 [GitHub Releases](https://github.com/tg56y2p4/efootball-face-converter/releases) 下载技能 ZIP，解压后把完整的 `efootball-face-converter` 目录放入所用工具的 skills 目录。

- **Codex**：`~/.codex/skills/efootball-face-converter`
- **Antigravity**：`~/.gemini/config/skills/efootball-face-converter`（全局）或项目根目录 `.agents/skills/efootball-face-converter`
- **Claude Code**：`~/.claude/skills/efootball-face-converter`

也可以直接克隆本仓库作为技能目录。运行转换前，在独立 Python 环境中安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
```

下列示例中的 `python` 指已安装依赖的 Python（macOS/Linux 可使用 `.venv/bin/python`）。解压 RAR/7z 还需要支持对应归档格式的 `tar`（例如 Windows 自带的 `bsdtar`；普通 GNU tar 不保证能解 RAR），ZIP 不需要外部解包器。当前实测环境为 Windows，跨系统支持可在对应环境运行回归测试验证。

如需离线三向预览（正面 / 侧面 / 背面）：

```powershell
python -m pip install -r scripts/requirements-preview.txt
python -m playwright install chromium
```

## 用法

### 1. 通过 Agent 调用

直接对 Agent 说：

> 用 `$efootball-face-converter` 做巴黎时期粉发内马尔的脸模。先查现有资源，找不到合适的就先给我审核四视图。

你也可以附上照片并说「按我给的照片做这个人的脸模，先让我审核四视图」。照片中目标明确时可以直接开始。没有实拍覆盖的角度会在审核时标注推定部位。用户确认当前版本后才进入建模。

从已有资源转换需要网页检索、Python 和图片查看能力。从照片重建还需要 ImageGen 或可传入实拍参考的对应图像工具。详见 [四视图审核](references/turnaround-review.md) 和 [重建与导出](references/reconstruction-export.md)。四视图、几何拟合、贴图烘焙及目视检查由 Agent 按流程完成，命令行脚本负责审核版本记录、可选的初始拟合和 GLB 导出。

使用 DAD-3DHeads 做初始拟合时，另装可选依赖并按 [重建说明](references/reconstruction-export.md) 获取对应的权重与拓扑。

```powershell
python -m pip install -r scripts/requirements-reconstruction.txt
```

### 2. 直接运行命令行脚本

用下列命令转换已下载的原包。

```powershell
python scripts/face_convert.py convert --input "path/to/face.rar" --player "内马尔" --name NeymarPSG2020Pink --appearance "巴黎时期粉色头发" --output-dir "output/Neymar" --work-dir "work/Neymar"
python scripts/inspect_glb.py "output/Neymar/NeymarPSG2020Pink_工坊单网格.glb" --report "work/structure.json"
python scripts/preview_glb.py "output/Neymar/NeymarPSG2020Pink_工坊单网格.glb" --output-dir "work/preview"
```

- **目录隔离**：`--output-dir` 和 `--work-dir` 必须是不同的新目录，且位于输入目录之外；重跑时请换新目录，确保原始素材不被修改。
- **多版本选择**：含多球员、多 CPK 或多个版本的原包，应先查看目录（如 `python scripts/face_convert.py inspect-cpk "path/to/pack.cpk"`），再用 `--face-id`、`--cpk-member`、`--subdir` 或 `--member-prefix` 明确指定版本。
- **自定义眼位**：默认通过标准 PES 脸图 UV 拟合眼位；特殊 UV 可传 `--eye-centers '{"r":[x,y,z],"l":[x,y,z]}'` 或 JSON 文件路径。

## 支持范围

- **PES 2018–2021**：FMDL 与完整 FTEX / PNG 同伴目录。
- **PES 2014–2017**：MODEL、材质 XML/MTL 与 DDS。
- **已有工坊骨架 GLB**：带 166 关节工坊骨架的 GLB 图集重打包与贴图限幅。
- **外层容器**：ZIP、RAR、7z、CPK、FPK，详见 [格式说明](references/formats-and-repairs.md)。

普通 OBJ/FBX、FIFA RX3/FBMOD、PES2013 BIN、原生手游 UE 资源需要另行适配。支持格式不代表任意作者包都能免修复直接转换。

## 更新记录

### 1.2.0

- 合并现有脸模检索、转换和照片重建。先找符合时期与造型且可转换的现有资源。
- 无合适资源时用实拍生成四视图，用户明确确认后才拟合、贴图并导出工坊 GLB。
- 支持用户指定照片直接进入四视图流程。审核记录与 PNG 的 SHA-256 绑定。
- 新增审核记录、可选初始拟合及重建导出脚本，共用原有工坊骨架和验证工具。

### 1.1.1

- `--eye-centers` 同时支持直接传入 JSON 字符串与 JSON 文件路径，与 `SKILL.md` 指令保持一致。
- 单脸模包显式传入 `--face-id` 时同样强制校验目录匹配；省略 `--face-id` 时自动从目录或纹理路径提取真实 `sourceFaceId`。
- `pes.py` 匹配 `/face/real/<id>/` 前先规范化反斜杠与末尾斜杠，避免部分作者 FMDL 纹理目录无末尾斜杠时触发断言错误。
- `fetch_face.py` 支持分块流式响应首包小于 6 字节的场景，并在不支持硬链接的文件系统（如 exFAT）上自动回退为安全移动。
- `containers.py` 兼容非 UTF-8 归档文件名编码，解包时自动跳过可执行文件与快捷方式（`.exe` / `.bat` / `.url` 等），并关闭所有 `Pillow` 图像句柄。
- 新增 GitHub Actions 跨平台自动测试（Windows & Ubuntu）并扩充回归测试套件。

### 1.1.0

- 根据原 shader 与真实 alpha 识别 Hair2 脸图叠层，保留胡须、眉毛及头皮透明度。
- 对原双面发片烘焙反向面和翻转法线，保持皮肤单面，避免颈部背面多显示一层；新增几何计入模型信息，重复打包不重复增加反向面。
- 提供通用的可选工坊原始解析器检查脚本，无需个人项目路径。

可运行不含球员素材的单元测试：

```powershell
python -m unittest discover -s tests -v
```

## 可选：原始工坊解析器检查

如果你本机已安装球员工坊 EXE，可在 Python 3.12 环境中安装 `scripts/requirements-workshop.txt` 后运行：

```powershell
python scripts/verify_workshop.py "output/Neymar/NeymarPSG2020Pink_工坊单网格.glb" --workshop-exe "path/to/球员工坊.exe" --work-dir "work/workshop-check"
```

该脚本离线加载受检的 `native_glb` 模块，验证单网格、内嵌图像和 accessor。已验证工坊 2.1.7 和 2.7.3 的相应解析器布局。转换、结构检查和浏览器预览均可独立运行。

## 验证与来源

结构检查、浏览器渲染、人工目视、原工坊解析、项目接合、游戏内验证分别独立记录。新增的中性眼球、辅助骨回退及省略的游戏 shader 叠层会在 `模型信息.json` 中说明；未迁移原游戏完整表情或眼部 shader。

发布包包含技能文档、转换和重建脚本、解析器、骨架模板和离线预览库。球员素材及初始拟合所需的模型权重、拓扑分别按来源获取并注明出处。

第三方来源和许可说明见 [third-party-sources.md](references/third-party-sources.md)；Three.js 的 MIT 许可证随库保留，其他第三方组件与骨架模板未被统一重新许可。
