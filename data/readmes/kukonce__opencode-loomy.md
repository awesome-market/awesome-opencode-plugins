# opencode-loomy

把 [Loomy](https://loomy.xunfei.cn)（讯飞 Loomy 桌面端）的账号接入 [OpenCode](https://opencode.ai)，作为模型提供方使用。

与 [dsh-loomy](https://github.com/kukonce/dsh-loomy)（DeepSeek Harness 版）同一套协议实现，针对 OpenCode 2.x 的插件体系重写：登录走**集成登录方法**（TUI 表单），模型走 **provider transform**，请求走 **aisdk sdk hook**。

```
@ai-sdk/openai-compatible   ← SDK 包
loomy / loomy-2 / ...       ← 每个账号一条 provider 路由
```

## 安装

把本目录放进 OpenCode 的插件目录：

```sh
# 全局插件目录（对所有项目生效）
mkdir -p ~/.config/opencode/plugins/opencode-loomy
cp -r * ~/.config/opencode/plugins/opencode-loomy/

# 或项目插件目录
mkdir -p .opencode/plugins/opencode-loomy
cp -r * .opencode/plugins/opencode-loomy/
```

重启 OpenCode 后，`opencode auth login` 的列表里会出现 **Loomy** 集成。

## 登录

三种方式，任选：

### 方式 A：导入本机 Loomy 桌面端登录（最快）

如果你的 Loomy 桌面端已经登录过，插件会直接读它的 `auth-session.json`（Windows 上在
`C:\Users\Public\Loomy\<sha256(用户名)[:12]>\userData\`）。运行 `opencode auth login`，
选 **Loomy → Import Loomy desktop login**，完成。

### 方式 B：短信验证码（两步）

1. `opencode auth login` → 选 **Loomy → Enter verification code** 前先设置手机号：
   选择 **Loomy** 集成下的 **key** 方法，key 填你的 11 位手机号
2. 运行 **Send SMS code**（发验证码）
3. 再运行 **Enter verification code**，填收到的验证码

### 方式 C：从 dsh-loomy 复用

如果同一台机器上已经用 [dsh-loomy](https://github.com/kukonce/dsh-loomy) 登录过，
账号表在 `~/.dsh/dsh-loomy/accounts.json`，本插件**不会**自动读它（OpenCode 的存储
独立）。要么用方式 A 重新导入，要么手动把 session 复制过来。

## 专用登录命令 `loomy`

不用在 OpenCode 里一层层选菜单——装好插件后有一个独立命令：

```sh
loomy login          # 导入本机 Loomy 桌面端登录（最快，一步完成）
loomy login --sms    # 用手机验证码登录（会提示输入手机号和验证码）
loomy status         # 看账号、积分、模型数量
loomy logout [id]    # 退出账号（默认第一个）
```

命令会把凭据同时写进两处：插件自己的账号表（`~/.opencode/loomy/accounts.json`）和
OpenCode 的 `auth.json`，所以登录后 OpenCode 的 `/auth` 列表里也显示为已登录。

**为什么是独立脚本而不是 OpenCode 插件内建命令**：OpenCode 2.x 的插件 API 没有办法
注册 CLI 命令（只有集成登录方法、provider transform、aisdk hook 三类扩展点）。要保持
「一条命令登录」，就得绕开插件 API 直接写它读的那两个文件——代价是命令要在 PATH 上，
所以 `package.json` 声明了 `bin` 字段。

安装到 PATH（任选其一）：

```sh
# npm 全局安装（把 bin 链接到 PATH）
npm install -g ./opencode-loomy

# 或者手动放一个 shim
```

---

## 每日 5000 积分

Loomy 的积分分两池：每日赠送（5000/天，优先消耗）和长期。让每日池回到 5000 的是
`POST /api/v1/points/first-login` —— 名字像「首次登录」，实际是幂等的「开始今天的
计费周期」。插件在启动后和每天本地零点各调一次。

## 模型

目录按账号实时拉取（`GET /api/v1/models`），每 20 分钟缓存。生图模型（`type: image`）
对对话请求一律 404，所以不进选择器。推理档位从目录的 `reasoning_efforts` 来，目录没
声明时（`auto` 模型）回退到标准五档 —— 上游实测五个档位都接受。

## 已知限制

- **非官方集成**：接口按官方桌面客户端行为逆出，无公开文档，随时可能变。
- **会话明文存储**：`~/.opencode/loomy/accounts.json`（0600）存 bearer session。
  Loomy 的 session 本身不加密，没有可用的加密层。
- **历史思考不回放**：只回放最新一条 assistant 的 reasoning。全量回放曾让 100 轮会话
  每轮 61 秒（245 KB 请求体），现在 8 秒。
- **内嵌客户端凭据**：`lib/loomy.js` 里有 iFlytek CAccount 的 app key（随每个 Loomy
  安装包分发，标识客户端应用而非用户），可用环境变量覆盖。

## 协议文档

完整协议（认证头矩阵、信封格式、SSE 事件、错误表）见
[dsh-loomy 的 docs/protocol.md](https://github.com/kukonce/dsh-loomy/blob/main/docs/protocol.md)。

## 许可证

MIT。Loomy / 讯飞 的名称归各自所有者，本项目与讯飞无隶属关系。