# CreatorCrawl Skill

An agent skill for fetching current public social data, researching creators, and generating API integrations across TikTok, Instagram, YouTube, LinkedIn, Twitter/X, Reddit, and Facebook.

## Install

```bash
npx skills add creatorcrawl/creatorcrawl-skill
```

Choose your agent and installation scope. The default is a project installation. For a global skill available across projects:

```bash
npx skills add creatorcrawl/creatorcrawl-skill --global
```

The package contains `SKILL.md`, seven platform endpoint references, an API behavior reference, and five research workflows. It does not install a CLI or configure MCP. Node.js is needed to run the installer; the installed skill uses standard HTTP requests and does not need Node.js at runtime.

## Set up API access

Sign in at [app.creatorcrawl.com](https://app.creatorcrawl.com), create an API key, and configure it in your agent's environment:

```bash
export CREATORCRAWL_API_KEY='YOUR_API_KEY'
```

Keep the key out of chat and source control. New accounts include 50 free credits with no card. The skill verifies authentication using the free `/api/validate-key` endpoint before fetching data.

## Use it

Ask your agent:

- “Audit this creator's TikTok and Instagram accounts.”
- “Fetch this YouTube video's transcript and identify its opening hook.”
- “Find fitness creators on TikTok and compare their recent engagement.”
- “Write a Python script that fetches Reddit posts about this topic.”

The agent reads the relevant reference and calls the API directly with `curl` or your existing HTTP client. Responses use the API's normalized JSON; no standalone CLI is required.

## What's included

- `references/`: endpoint paths, parameters, response descriptions, credits, pagination, and error handling.
- `workflows/`: creator audits, viral analysis, trend research, competitor comparisons, and influencer prospecting.
- `SKILL.md`: authentication, endpoint selection, request examples, and workflow routing.

References are a snapshot. The [live OpenAPI schema](https://api.creatorcrawl.com/openapi.json) is authoritative for current parameters and response schemas.

## Standalone CLI and MCP

The [CreatorCrawl CLI](https://github.com/creatorcrawl/cli) is installed separately and provides the `creatorcrawl` terminal command. Its browser sign-in requires no API key:

```bash
curl -fsSL https://creatorcrawl.com/install.sh | sh
creatorcrawl auth login
creatorcrawl tiktok profile khaby.lame
```

For Claude mobile/Desktop and other MCP apps, add `https://api.creatorcrawl.com/mcp` and sign in through the browser. The skill, CLI, and MCP all use the same account, API data, and credits. [Setup guide](https://creatorcrawl.com/agents/).

## License

MIT
