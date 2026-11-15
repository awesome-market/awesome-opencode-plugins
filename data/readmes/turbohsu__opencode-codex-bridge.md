# opencode-codex-bridge

An OpenCode plugin that makes a custom `@ai-sdk/openai` provider send Codex-shaped requests through your own proxy.

**This plugin effectively fixes prompt caching for Codex models when used via LLM proxies (e.g., new-api).**
This saves you real money! You may check the last section to see the results.

It does three things:

- injects `session_id` and `x-client-request-id`
- ensures `prompt_cache_key` is present
- rewrites the leading `system` / `developer` prefix into top-level `instructions`

## Install

Install via `npm i -g opencode-codex-bridge@latest` and add to your config:

```json
{
  "plugin": [
    "opencode-codex-bridge"
  ]
}
```

If u want to install from a local path, use the `file://` prefix.

## Config

Mark the provider you want the bridge to attach to with `useCodexBridge: true`.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "opencode-codex-bridge"
  ],
  "provider": {
    "your-proxy-site": {
      "npm": "@ai-sdk/openai",
      "name": "your-proxy-site",
      "options": {
        "baseURL": "https://your-proxy-site.com/v1",
        "useCodexBridge": true,
        "rewriteInstructions": true,
        "promptCache": true,
        "zeroCost": true
      },
      "models": {
        "gpt-5": {},
        "gpt-5-codex": {},
        "gpt-5-codex-mini": {}
      }
    }
  }
}
```

Important: this plugin does not inherit OpenAI's built-in model catalog. Define the models you want under `provider.<id>.models`.

## Login

This bridge is API-key only.

```bash
opencode providers login --provider your-proxy-site
```

Then enter the proxy API key when prompted.

## Options

These values live under `provider.<id>.options`:

- `baseURL`: OpenAI-style endpoint root such as `https://host/v1`
- `useCodexBridge`: mark this provider as the one handled by the bridge
- `originator`: optional `originator` header, default `opencode`
- `sessionHeader`: optional session header name, default `session_id`
- `requestHeader`: optional request id header name, default `x-client-request-id`
- `zeroCost`: force configured model costs to zero, default `true`
- `rewriteInstructions`: move the leading `system` / `developer` prefix into top-level `instructions`, default `true`
- `promptCache`: force `prompt_cache_key`, default `true`

## Does it really work?

Yes, at least based on my setup. I have a `new-api` proxy running with `Codex (via OAuth)` as provider channel.

U can check prompt caching status with following commands:

```bash
opencode db "with m as (select session_id, json_extract(data,'$.agent') as agent, json_extract(data,'$.providerID')||'/'||json_extract(data,'$.modelID') as model, cast(json_extract(data,'$.tokens.input') as integer) as input_tokens, cast(json_extract(data,'$.tokens.cache.read') as integer) as cache_tokens from message where json_extract(data,'$.role')='assistant') select m.session_id, s.time_created as session_time, m.agent, m.model, sum(m.input_tokens) as input_tokens, sum(m.cache_tokens) as cache_tokens, round(100.0*sum(m.cache_tokens)/nullif(sum(m.input_tokens)+sum(m.cache_tokens),0),1) as cache_share_pct from m join session s on s.id = m.session_id group by m.session_id, s.time_created, m.agent, m.model order by s.time_created desc limit 100;" --format tsv | awk -F'\t' 'BEGIN { print "┌──────────────────────┬─────────────────────┬────────────────────────────┬──────────────────────────┬──────────┬──────────┬────────────┐"; print "| session              | session_time         | agent                      | model                    |     input |     cache | cache_share |"; print "├──────────────────────┼─────────────────────┼────────────────────────────┼──────────────────────────┼──────────┼──────────┼────────────┤" } NR==1 { next } { sid=substr($1,1,20); st=substr($2,1,19); agent=substr($3,1,28); model=substr($4,1,26); printf "| %-20s | %-19s | %-28s | %-26s | %10d | %10d | %9.1f%% |\n", sid, st, agent, model, $5+0, $6+0, $7+0 } END { print "└──────────────────────┴─────────────────────┴────────────────────────────┴──────────────────────────┴──────────┴──────────┴────────────┘" }'
```

Or for whatever reason you are using god damn `Windows`:

```powershell
opencode db "with m as (select session_id, json_extract(data,'$.agent') as agent, json_extract(data,'$.providerID')||'/'||json_extract(data,'$.modelID') as model, cast(json_extract(data,'$.tokens.input') as integer) as input_tokens, cast(json_extract(data,'$.tokens.cache.read') as integer) as cache_tokens from message where json_extract(data,'$.role')='assistant') select m.session_id, s.time_created as session_time, m.agent, m.model, sum(m.input_tokens) as input_tokens, sum(m.cache_tokens) as cache_tokens, round(100.0*sum(m.cache_tokens)/nullif(sum(m.input_tokens)+sum(m.cache_tokens),0),1) as cache_share_pct from m join session s on s.id = m.session_id group by m.session_id, s.time_created, m.agent, m.model order by s.time_created desc limit 100;" --format tsv | ConvertFrom-Csv -Delimiter "`t" | ft @{N='session';E={$_.session_id}}, @{N='session_time';E={$_.session_time}}, agent, model, @{N='input';E={[int]$_.input_tokens}}, @{N='cache';E={[int]$_.cache_tokens}}, @{N='cache_share';E={"{0:F1}%" -f [double]$_.cache_share_pct}}
```

Here comes some comparison:

- Before

```text
ses_2fb00cd83ffeZIV6X6gz3Im6Uh 1773905326716 Sisyphus (Ultraworker)  0v0/gpt-5.4                 1212415        0 0.0%
```

- After

```text
ses_2f3efb67affe7jtXhf0n5ognGx 1774023887237 Sisyphus (Ultraworker)  0v0/gpt-5.4                   98817   126720 56.2% 
```

Looks like its cooking!
