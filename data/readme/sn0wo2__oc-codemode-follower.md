# oc-codemode-follower

OpenCode V2 插件:跟随某个"触发器"MCP 的启用/禁用状态,自动批量切换一组 MCP 的 `codemode`。

典型用途:REA 有 229 个工具,必须走 Code Mode 才不撑爆上下文;REA 启用时让其他 MCP 一起蹭 Code Mode 的固定开销,REA 禁用时其他 MCP 回到原生工具直连。

## 安装

在 `opencode.jsonc` 的 `plugins` 数组中加入:

```jsonc
{
  "plugins": [
    {
      "package": "file:///D:/webProject/oc-codemode-follower",
      "options": {
        "triggers": ["rea"],
        "targetsMode": "exclude",
        "targets": ["rea"],
        "debug": true
      }
    }
  ]
}
```

通过 `/mcps` 面板连接/断开触发器即可热切换,无需重启服务。

## 选项

| 选项          | 默认        | 说明                                                                                   |
| ------------- | ----------- | -------------------------------------------------------------------------------------- |
| `triggers`    | `["rea"]`   | 触发器 server 名单,其启用状态决定开关                                                  |
| `triggerMode` | `"any"`     | `"any"`:任一触发器启用即 ON;`"all"`:全部启用才 ON                                      |
| `targets`     | `[]`        | 受控 server 名单;include 模式下支持 `"*"` 匹配全部                                     |
| `targetsMode` | `"include"` | `"include"`:只控制 `targets`;`"exclude"`:控制 `targets` 之外的全部(触发器自身永不受控) |
| `codemodeOn`  | `true`      | ON 时写入的 `codemode` 值                                                              |
| `codemodeOff` | `false`     | OFF 时写入的 `codemode` 值                                                             |
| `debug`       | `false`     | 把每次决策追加到 `~/.local/share/opencode/log/codemode-follower.log`                   |

## 行为说明

- 每 3 秒轮询一次 `ctx.mcp.list()` 的运行时状态:任一(`"all"` 模式下为全部)触发器 `connected` 即 ON;连续 4 次读到离线才 OFF,以跳过 reconcile 重建连接的短暂窗口。
- 一个 `ctx.mcp.transform` 承载全部决策:ON 时清除触发器的 `disabled` 标志并把受控 server 的 `codemode` 置为 ON 值,OFF 时相反。提交决策时重新注册该 transform 使其立即重放;配置文件始终不被修改。
- 名称匹配大小写不敏感,配置里不存在的名单项会被忽略。
- 插件热重载后会自动收敛到当前运行时状态。

## REA provider 参考(本机)

REA 的反编译 provider 用 **IDA Pro 9.4 headless**(无需打开 IDA GUI):

- 上游:`mrexodia/ida-pro-mcp` 快照 `c133c385`(v2.0.0,66 工具,含 headless supervisor API `idb_open/idb_list/idb_close`;正式 release 1.4.0 无此 API)。注意 mcp Python SDK 需钉在 1.x(2.x 改名 FastMCP 会导致其无法启动)。
- 注册:`~/.local/share/rea/ida-mcp.json`(`idalib-mcp --stdio --max-workers 1`,`IDADIR=D:\IDA Professional 9.4`),idalib 已用官方 `py-activate-idalib.py` 激活。
- 环境变量(用户级):`REA_IDA_MCP_CONFIG`、`REA_ANALYSIS_PROVIDER=ida`。opencode 服务若在写入前启动,需重启一次才能继承。
- 验证:`REA_IDA_MCP_CONFIG=~/.local/share/rea/ida-mcp.json REA_ANALYSIS_PROVIDER=ida bunx rea-agents doctor --provider ida` 应报 configured + available。
- jadx provider:`~/.local/share/rea/jadx-headless-mcp-0.8.0-all.jar`(env `REA_JADX_MCP_JAR` 已写入)。
- capa:插件 v10.0.0 + `flare-capa==10.0.0`(python-flirt 因 PyO3 未支持 3.15,以 `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` abi3 前向构建);规则库 1054 条在 `~/.local/share/capa/rules`,explorer 首次使用时选择该目录。
- rea 在 `opencode.jsonc` 中为 `disabled: true`(有意为之),通过 `/mcps` 面板连接触发本插件的 ON 切换;`rea_*` 不设权限 deny,否则其 229 个工具会从主 agent 目录中隐藏。
