# Ralph - Ultra-Minimal Opencode Agent Runner

**Run opencode agents indefinitely on Cloudflare. Deploy in 5 minutes. ~$9-15/month. 300 lines of code.**

[![Test](https://github.com/acoyfellow/ralph-complete/actions/workflows/test.yml/badge.svg)](https://github.com/acoyfellow/ralph-complete/actions/workflows/test.yml)
[![Deploy](https://github.com/acoyfellow/ralph-complete/actions/workflows/deploy.yml/badge.svg)](https://github.com/acoyfellow/ralph-complete/actions/workflows/deploy.yml)

🌐 **Live Demo:** https://ralph-complete.coy.workers.dev

Ralph runs opencode agents on your repos 24/7 to automate revenue generation. Control it from anywhere via web UI or API.

## Quick Start

```bash
cd ralph-minimal
bun install
bun run deploy
```

Your ralph is live at `https://ralph.your-account.workers.dev`

## What It Does

Ralph runs opencode indefinitely on your repos to make you money.

### Features
- ✅ Start/pause/resume from anywhere
- ✅ Steer mid-execution
- ✅ Live logs auto-refresh
- ✅ Remote terminal access (tmate)
- ✅ Web UI + API
- ✅ Mobile-friendly
- ✅ ~$9.50/month when running 24/7
- ✅ Zero infrastructure to manage

## Example Usage

```bash
# Start ralph
curl https://ralph.workers.dev/api/start -d '{
  "repo": "dcainsights",
  "prompt": "analyze traffic, write SEO content, add calculators, build affiliate links, optimize conversions"
}'

# Let it run for 24 hours

# Check what it built
curl https://ralph.workers.dev/api/logs
```

Ralph works while you sleep. You make money.

## Architecture

```
Browser/Phone
    ↓
Cloudflare Worker (routing + UI)
    ↓
Durable Object (lovely API)
    ↓
Container (tmux + opencode)
    ↓
Your repo (dcainsights, etc)
```

**Narrow surface area:** 21 total API methods  
**Lovely DX:** `ralph.start()`, `ralph.pause()`, etc  
**Actually works:** Deploy today, runs indefinitely

## Cost

- **Running 24/7:** ~$9.50/month
- **Running 8hr/day:** ~$6.50/month  
- **Only when working:** ~$6/month + usage

Includes Workers Paid plan ($5/mo base) + container resources. Container sleeps when idle.

## API

```bash
curl https://ralph.workers.dev/api/start    # Start agent
curl https://ralph.workers.dev/api/pause    # Pause
curl https://ralph.workers.dev/api/resume   # Resume
curl https://ralph.workers.dev/api/steer    # Send command
curl https://ralph.workers.dev/api/status   # Check status
curl https://ralph.workers.dev/api/logs     # Get logs
curl https://ralph.workers.dev/api/remote    # Get SSH URL
```

## Testing

### Production Smoke Tests

Run production smoke tests:

```bash
cd ralph-minimal
bun run test:prod
```

### End-to-End Test

Run complete end-to-end verification:

```bash
./test-e2e.sh
```

### Automated Testing

GitHub Actions automatically:
- ✅ Run production smoke tests on every push/PR
- ✅ Run daily health checks (2am UTC)
- ✅ Verify builds and type checking
- ✅ Deploy on main branch changes

View test status: [Actions](https://github.com/acoyfellow/ralph-complete/actions)

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Copy/paste commands to deploy now
- **[RALPH_SUMMARY.md](RALPH_SUMMARY.md)** - Complete overview, API docs, cost breakdown
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visual diagrams, data flows, design decisions

## Tech Stack

- **Cloudflare Workers** - Edge compute
- **Durable Objects** - State management
- **Cloudflare Containers** - Container runtime
- **TypeScript** - Type safety
- **Playwright** - Production testing
- **opencode** - AI agent runtime

## Design Principles

1. **Ultra-minimal** - 300 lines total
2. **Narrow surface** - 21 API methods
3. **Lovely DX** - Beautiful, type-safe API
4. **Zero infrastructure** - No servers, VMs, K8s
5. **Actually deployable** - Works right now
6. **Production-ready** - Handles failures, restarts
7. **Cost-effective** - ~$6-15/month
8. **Remote access** - SSH from anywhere
9. **Mobile-friendly** - Control from phone
10. **Make money** - That's the whole point

## License

MIT

## Contributing

PRs welcome. Keep it minimal.

---

**Deploy once. Let ralph work indefinitely. Make money while sleeping.**
