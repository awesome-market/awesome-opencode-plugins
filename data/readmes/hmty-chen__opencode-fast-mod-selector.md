# OpenCode Fast Mod Selector

[简体中文](README.md) · [English](README.en.md) · [Français](README.fr.md)

为 **OpenCode Desktop V2** 添加独立的 API 速度选择器。无需创建额外的 Fast 模型，可在保留当前模型和推理强度的同时选择 `Standard`、`Fast` 或 `Ultrafast`。

![界面示意](docs/UI-preview.svg)

## 适用范围

- Windows，OpenCode Desktop V2；当前目标版本为 **2.0.21**。
- 已在 OpenCode 中配置的 **API key 提供商**，支持 OpenAI-compatible Chat Completions 或 Responses。
- 可选速度及 `service_tier` 值由模型配置决定，上游接口须提供相应服务等级。
- 不适用于 ChatGPT/Codex OAuth、V1、终端 TUI 或远程 OpenCode。macOS/Linux 桌面加载暂不支持。

扩展通过外置 CDP 加载器与 V2 服务端插件集成，不修改 OpenCode 安装包。版本更新可能需要适配，详见[兼容性](docs/COMPATIBILITY.zh.md)。

## 安装与配置

需要 **Python 3.11+、Node.js 22+** 和 OpenCode Desktop V2。

```powershell
git clone https://github.com/hmty-CHEN/opencode-fast-mod-selector.git
cd opencode-fast-mod-selector
npm ci --ignore-scripts
Copy-Item settings.example.json settings.json
```

编辑本机 `settings.json`：

```json
{
  "schema": 1,
  "debug_port": 9337,
  "service_url": "http://127.0.0.1:49374",
  "app_path": "",
  "providers": {
    "example-api": {
      "models": {
        "example-model": {
          "name": "Example API Model",
          "modes": ["standard", "fast"],
          "tiers": {"fast": "priority"}
        }
      }
    }
  }
}
```

- `app_path`：你的 `OpenCode.exe` 完整路径。
- `service_url`：本机 OpenCode 后台服务地址；`49374` 为常见默认端口，可通过 V2 CLI `service status` 查询。
- `example-api` / `example-model`：替换为 OpenCode 中的提供商 ID 和目录模型 ID。
- `name`：模型选择器中的准确展示名称。
- `modes` / `tiers`：配置上游支持的速度及对应请求值。例如 Fast 使用 `priority` 或 `fast`；Ultrafast 按模型支持情况添加。

API key 和上游地址继续由 OpenCode 管理，**不要写入本扩展配置或提交到仓库**。完整说明见[配置文档](docs/CONFIGURATION.zh.md)。

注册插件：

```powershell
python install.py
```

安装器只添加一个插件入口，不修改全局 `opencode.json(c)`。请保留仓库所在位置。非默认配置目录可用 `--config-dir` 指定。

## 使用

1. 保存当前工作，手动退出 OpenCode Desktop。
2. 双击 `start.cmd` 启动，保持加载器控制台开启。
3. 在输入栏的 `Speed` 菜单选择速度。

若已通过加载器启动，可用 `attach.cmd` 重新附着。

可选：运行以下命令创建带 OpenCode 图标的桌面快捷方式。

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\create-shortcut.ps1
```

`Standard` 保留原请求默认行为；`Fast` / `Ultrafast` 修改主请求的 `service_tier`，不改变模型或推理强度。费用和实际性能以提供商规则为准。

## 卸载与安全

```powershell
python rollback.py
```

也可双击 `rollback.cmd`。它停用扩展并移除本安装拥有的入口，不重置 OpenCode 配置或会话。之后手动退出应用，使用原 OpenCode 快捷方式启动。

CDP 调试端口具有较高权限，**只能监听本机回环地址，不要转发或对外开放**。只停止加载器不等于停用服务端加速；完整停用请使用 rollback。详见[安全说明](SECURITY.zh.md)。

## 文档与主要参考

[配置](docs/CONFIGURATION.zh.md) · [兼容性](docs/COMPATIBILITY.zh.md) · [架构](docs/ARCHITECTURE.zh.md) · [更新日志](CHANGELOG.zh.md) · [贡献](CONTRIBUTING.zh.md)

- **[Snownee/shuaqii](https://github.com/Snownee/shuaqii)**：外置 Python/CDP 加载设计参考；本项目的 V2 集成独立实现。
- **[OpenCode V2 Plugin API](https://opencode.ai/v2/docs/build/plugins/)** 与 **[RPC API](https://opencode.ai/v2/docs/build/plugins/rpc/)**：服务端集成接口。
- **[Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)**：桌面脚本加载与请求适配协议。

[来源与致谢](THIRD_PARTY_NOTICES.zh.md) · [MIT 许可](LICENSE)
