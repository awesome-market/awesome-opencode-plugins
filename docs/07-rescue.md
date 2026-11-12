# 07 — 离线救援通道（Rescue Runner）

GitHub Actions 的数据中心 IP 抓 `github.com/trending` 经常 504 限流，而家庭/
办公网络（住宅 IP）抓同一页面完全正常。救援通道让 CI 抓取失败时自动"摇人"：
服务器上的 cron 脚本接力完成采集、推送数据并触发部署。

## 消息流（issue 驱动）

```
CI daily-update
  └─ collect.py 结束 → 写 run_status.json（trending 页成功/失败计数）
  └─ ci_rescue.py 读状态：
        全败 → 无 open `rescue` issue 则新开（含 TRR-STATE 状态块）；已有则评论"仍在失败"
        正常 → 有 open `rescue` issue 则评论"已恢复"并关闭（自愈）

服务器 cron（每小时）
  └─ rescue.py
        读 is:open label:rescue 最新 issue → 解析 TRR-STATE
        attempts < max  → git sync → collect → rank → commit+push
                        → dispatch deploy_only → dispatch rescue-report
                        → github-actions bot 评论成功 → rescue-done → close
        每次失败        → dispatch rescue-report（bot 评论日志尾 + attempts+1）
        attempts ≥ max  → rescue-failed 标签 + close（不再重试）
```

> **bot 身份**：服务器 PAT 只做"读 issue + push + 发 dispatch"三件
> 事；所有 issue 上的可见动作（评论/标签/改状态/关单）都转发给
> `rescue-report.yml` 用内置 `GITHUB_TOKEN` 执行，作者显示
> `github-actions`，无需注册独立 bot 账号。

## Issue 约定

- **标签**：`rescue`（待救）/ `rescue-done`（成功）/ `rescue-failed`（放弃），脚本自动创建
- **状态**：body 顶部 `<!--TRR-STATE {...}-->`，字段
  `type / date / run_id / run_url / trending_fails / attempts / max_attempts`
- **日志**：每次救援尝试的结果都以 issue 评论追加，可完整审计

## 服务器部署

1. 准备专用克隆（脚本会 `git reset --hard origin/main`，**不能**用有未提交改动的目录）：

   ```bash
   git clone https://github.com/awesome-market/trending-rank-radar /data1/service/trending-rank-radar
   ```

2. 创建 fine-grained PAT（GitHub → Settings → Developer settings →
   Personal access tokens → Fine-grained），仅授权本仓库，权限：

   | 权限 | 用途 |
   |---|---|
   | Issues: Read | 轮询 open `rescue` issue（写操作走 rescue-report 中继） |
   | Contents: Read and write | `git push` 数据提交 |
   | Actions: Read and write | 触发 `deploy_only` 部署 + `rescue-report` 回写 |

3. 配置 cron（每小时）：

   ```cron
   0 * * * * GITHUB_TOKEN=github_pat_xxx /data1/service/trending-rank-radar/scripts/cron_wrap.sh /usr/bin/python3 scripts/rescue.py >> /data1/log/trending-rank-radar.log 2>&1
   ```

   `cron_wrap.sh` 会先 `git fetch` 把 worktree 同步到 origin/main 最新，
   再执行真实任务——推送到 main 的修复下一小时自动生效，无需手动 pull。
   （rescue.py 内部本来也会 fetch+reset，包装器让 rescue.py 自身也能用到新代码。）

   可选环境变量：`TRR_REPO`、`TRR_WORKDIR`（默认脚本所在仓库根）、
   `TRR_SITE_BASE`（默认 `https://zhuikan.com`）。

4. 验证：手动跑一次 `GITHUB_TOKEN=... python3 /data1/service/trending-rank-radar/scripts/rescue.py`，
   无 open rescue issue 时输出 `idle` 即正常。

## 注意

- PAT 只放在服务器的 cron 环境/secret 管理里，**不要写进仓库**。
- 一次救援 ≈ 完整 daily-update 采集（非扩展时段约 3–8 分钟；UTC 14 点档含
  扩展字段约 15–20 分钟）。hourly cron 加 fcntl 锁，重叠时自动跳过。
- 榜单在 trending 挂掉期间仍可运转（watchlist + Search API），救援通道
  恢复的是"当日新冒头仓库"的发现能力。
