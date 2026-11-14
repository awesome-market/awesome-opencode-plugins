# AI数字人口播

OPC-koubo 是橙哥出海（Twitter/X：[OPCchuhai](https://x.com/OPCchuhai)）开源的 Renoise Agent Skill，用于制作AI数字人口播短视频：同一形象出镜，按文案说话。项目以 [MIT](LICENSE) 许可发布，可免费使用。

一键复制本项目地址（[https://github.com/OPCchuhai/OPC-koubo](https://github.com/OPCchuhai/OPC-koubo)）到 Claude、ChatGPT 等可连接外部工具的 AI 产品直接对话即可，无需修改代码。

<table align="center">
  <tr>
    <td align="center" valign="top">
      <img src="docs/media/demo-koubo-poster.jpg" alt="AI数字人口播首帧封面" width="260"><br>
      <sub>首帧封面</sub>
    </td>
    <td align="center" valign="top">
      <img src="docs/media/demo-koubo.gif" alt="AI数字人口播效果演示" width="260"><br>
      <sub>效果演示</sub>
    </td>
  </tr>
</table>

## 特性

- 通过 Renoise 生成「同一个人出镜说话」的短视频
- MCP 地址固定，在浏览器中登录，无需 API key
- 写明 Claude、ChatGPT 的连接步骤，其它产品见技能正文
- `persona.json` 仅为占位，须用本人或已获授权的照片，在自己的账号中重建形象
- 报价并得到同意后再生成，成片标明由 AI 数字人演绎

## 适用

适用于带货、解读、教程、种草等需要同一人出镜讲解的短视频。

不适用于冒充真人、使用未经授权的照片，或写入他人账号的素材编号。

## 快速开始

使用前请准备：

- 可连接外部工具的对话产品：Claude、ChatGPT、WorkBuddy、豆包、千问、OpenClaw、Hermes，或其它同类产品
- 一个 Renoise 账号
- 一张本人照片，或已获授权、可用于制作数字人的照片

尚未注册或尚未登录时，打开注册链接：

https://www.renoise.ai/?utm_campaign=affiliate_program&utm_medium=affiliate&utm_source=rewardful&via=quantbang

然后将下面整段复制给正在使用的 AI：

```text
请安装并使用橙哥出海（Twitter/X：[OPCchuhai](https://x.com/OPCchuhai)）开源的「AI数字人口播」：
仓库 https://github.com/OPCchuhai/OPC-koubo
请先阅读并遵守 skills/digital-human-koubo/SKILL.md。

请先确认我正在用哪个 AI。如果还不能调用 Renoise 的 get_account，就按技能里「按产品连接 Renoise MCP」中对应的一节，带我安装并登录。
地址只用这一条，不要改：
https://renoise.tv/api/public/mcp

如果我还没登录，或需要注册，只发这一条注册链接：
https://www.renoise.ai/?utm_campaign=affiliate_program&utm_medium=affiliate&utm_source=rewardful&via=quantbang

连上之后，告诉我是哪个账号、还剩多少积分，再问我想做哪一种：产品广告、照着喜欢的视频复刻，还是从 Renoise 模板开始。如果要做AI数字人口播，接着走技能里的口播流程。

persona.json 只是占位。请用我自己的照片，在我的 Renoise 账号里重建形象，不要写入别人的素材编号。花积分前先报价，等我同意后再生成。成片要标明是 AI 数字人。
```

## 连接说明

各产品的步骤见技能正文「按产品连接 Renoise MCP」。MCP 地址只有这一条，不要更换：

https://renoise.tv/api/public/mcp

登录在浏览器中完成，无需准备 API key。

### Claude

打开下面的链接。页面会自动填好名称和地址，点击添加即可。在网页端添加后，Claude 桌面版也可以使用。

https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Renoise&connectorUrl=https%3A%2F%2Frenoise.tv%2Fapi%2Fpublic%2Fmcp

### ChatGPT

打开 https://chatgpt.com/plugins ，添加一个名为 Renoise 的自定义服务器，地址填写 `https://renoise.tv/api/public/mcp`，登录方式选择 OAuth。如果看不到添加入口，先到 Settings → Apps → Advanced settings，打开 Developer mode。

WorkBuddy、豆包、千问、OpenClaw、Hermes，以及 Cursor 等其它产品，按技能正文「按产品连接 Renoise MCP」中对应的一节操作。浏览器会打开 Renoise 页面，在该页登录并允许访问。

WorkBuddy 若授权已成功但工具列表仍为空，只运行一次手动脚本（仓库根目录 `bash skills/digital-human-koubo/scripts/renoise-manual-connect.sh`，说明见技能正文「WorkBuddy 已知问题与手动接入」），不要反复重新授权。

## 使用流程

1. `persona.json` 目前是占位。先用自己的照片，在自己的 Renoise 账号中建立数字人形象。
2. 生成前，AI 会说明大约需要多少积分。同意之后再开始。
3. 成片标明「内容由 AI 数字人演绎」。

## 致谢

灵感来自 Berryxia / andyhuo520 的开源项目 [digital-human-koubo](https://github.com/andyhuo520/digital-human-koubo)（MIT）。

本仓库由橙哥出海（Twitter/X：[OPCchuhai](https://x.com/OPCchuhai)）自行重写，不是上游文件的原样复制。仓库中没有他人的照片，也没有他人的素材编号。请使用自己的照片。

## 许可

[MIT License](LICENSE)。Copyright (c) 2026 OPCchuhai（橙哥出海）。
