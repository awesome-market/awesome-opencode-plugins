# LoopyLuci Skills

A curated collection of **10,000+ AI agent skills** built for [Hermes Agent](https://hermes-agent.nousresearch.com/) and compatible with any agent that supports the [agentskills.io](https://agentskills.io/) open standard.

These skills cover every major domain: software development, data/AI, cybersecurity, cloud, business, science, creative, education, government, engineering, and more. Skills are loaded on-demand by AI agents.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/LoopyLuci/Skills.git ~/LoopyLuci-skills

# Option A: External Directory (Hermes Agent - recommended)
# Add to ~/.hermes/config.yaml:
#   skills:
#     external_dirs:
#       - ~/LoopyLuci-skills/skills

# Option B: Skill Tap (hub-managed updates)
hermes skills tap add LoopyLuci/Skills
# Then edit ~/.hermes/.hub/taps.json: {"taps": [{"repo": "LoopyLuci/Skills", "path": "skills/"}]}

# Option C: Direct URL install
hermes skills install https://raw.githubusercontent.com/LoopyLuci/Skills/main/skills/<skill-name>/SKILL.md
```

All skills are instantly available as slash commands. No per-skill install needed.

---

## How to Find a Skill

Skills are organized as flat directories. Find the right skill using:

1. **By name**: `skills/<category>-<topic>/SKILL.md`
2. **By tag**: Search frontmatter `metadata.hermes.tags`
3. **By category**: Browse the index below
4. **By search**: `hermes skills search <query>`

---

## Complete Category Index

### Software Development & Engineering (1,781 skills)

- **database** (299) — SQL, NoSQL, modeling, optimization, migrations
- **backend** (261) — APIs, microservices, server architecture
- **docker** (154) — Containers, Compose, registries, best practices
- **embedded** (121) — Firmware, RTOS, Arduino, STM32, IoT devices
- **android** (119) — Android development, Kotlin, Jetpack
- **api** (82) — REST, GraphQL, gRPC, API design
- **blockchain** (76) — Smart contracts, DeFi, Web3
- **crypto** (45) — Cryptography, encryption, PKI
- **container** (44) — Kubernetes, container orchestration
- **ci** (38) — CI/CD, GitHub Actions, GitLab CI, Jenkins
- **django** (35) — Django, Django REST, ORM
- **angular** (33) — Angular, RxJS, NgRx
- **datadog** (30) — Monitoring, APM, observability
- **github** (28) — Git, GitHub Actions, API
- **fastapi** (26) — FastAPI, async, OpenAPI
- **expressjs** (26) — Express, middleware, Node.js
- **python** (24) — Python idioms, packaging, tooling
- **git** (24) — Version control, branching, workflows
- **elasticsearch** (19) — Search, indexing, ELK stack
- **windows** (18) — Windows development, Win32, COM
- **powershell** (15) — PowerShell scripting, automation
- **architecture** (15) — Software architecture, DDD, patterns
- **react** (11) — React, hooks, state management
- **rust** (8) — Rust, ownership, async
- **nodejs** (8) — Node.js, event loop, streams
- **kubernetes** (7) — K8s, Helm, operators
- **security** (6) — Secure coding, OWASP
- **javascript** (6) — ES6+, DOM, async
- **devops** (6) — DevOps, SRE, infrastructure
- **typescript** (5) — TypeScript, type system
- **performance** (5) — Profiling, optimization, caching
- **envoy** (5) — Service mesh, Envoy proxy
- **encryption** (5) — Cryptographic implementations
- **vscode** (4) — VS Code extensions, debugging
- **linux** (4) — Linux kernel, sysadmin
- **graphql** (4) — GraphQL schemas, resolvers
- **cypress** (4) — E2E testing, Cypress
- **consul** (4) — Service mesh, Consul
- **terraform** (3) — IaC, Terraform
- **sql** (3) — SQL queries, optimization
- **kotlin** (3) — Kotlin, coroutines
- **frontend** (3) — Frontend development
- **flutter** (3) — Flutter, Dart
- **firewall** (3) — Network security, iptables

### Business, Product & Management (898 skills)

- **email** (392) — Email marketing, deliverability, automation
- **accounting** (145) — Bookkeeping, GAAP, financial reporting
- **content** (90) — Content strategy, creation, management
- **customer** (87) — Customer success, support, experience
- **business** (83) — Strategy, operations, planning
- **brand** (28) — Brand strategy, identity, management
- **product** (15) — Product management, roadmapping
- **crm** (10) — CRM systems, Salesforce, HubSpot
- **finance** (8) — Corporate finance, FP&A
- **marketing** (7) — Digital marketing, growth
- **sales** (5) — Sales process, CRM
- **conversion** (5) — CRO, A/B testing
- **project** (3) — Project management, PMBOK
- **saas** (2) — SaaS metrics, pricing
- **logistics** (2) — Logistics, transportation
- **legal** (2) — Business law, contracts
- **lean** (2) — Lean, Six Sigma, Kaizen
- **fundraising** (2) — Venture capital, fundraising

### Cloud & Infrastructure (631 skills)

- **aws** (383) — AWS services, architecture, best practices
- **azure** (95) — Azure, Microsoft cloud
- **ansible** (58) — Ansible, automation, playbooks
- **cloud** (53) — Cloud architecture, multi-cloud
- **gke** (24) — Google Kubernetes Engine
- **dns** (6) — DNS, Route53, Cloudflare
- **circleci** (5) — CircleCI, CI/CD
- **gcp** (3) — Google Cloud Platform
- **jenkins** (1) — Jenkins, CI/CD pipelines

### Science, Research & Healthcare (626 skills)

- **biotech** (258) — Biotechnology, pharma, life sciences
- **bioinformatics** (76) — Computational biology, genomics
- **crispr** (65) — Gene editing, CRISPR, molecular biology
- **biomedical** (50) — Biomedical engineering, devices
- **cardiology** (46) — Cardiology, cardiovascular
- **clinical** (45) — Clinical research, trials
- **dentistry** (25) — Dental practice, oral health
- **epidemiology** (19) — Epidemiology, public health
- **fda** (16) — FDA regulatory, submissions
- **research** (5) — Research methodology, academic
- **endocrinology** (5) — Endocrinology, hormones
- **ema** (4) — EMA, European regulatory
- **dermatology** (4) — Dermatology, skin
- **physics** (2) — Physics, mechanics
- **regulatory** (1) — Regulatory affairs
- **psychology** (1) — Psychology, behavioral

### Engineering & Manufacturing (624 skills)

- **aviation** (190) — Aviation, aerospace, flight
- **aerospace** (172) — Spacecraft, orbital mechanics
- **automotive** (78) — Automotive engineering, EVs
- **chemical** (68) — Chemical engineering, processes
- **civil** (45) — Civil engineering, structural
- **electrical** (41) — Electrical engineering, circuits
- **quantum** (8) — Quantum computing, quantum info
- **engineering** (5) — General engineering
- **casting** (4) — Casting, foundry
- **marine** (3) — Marine engineering, naval
- **scada** (1) — SCADA, industrial control
- **plc** (1) — PLC programming, automation
- **mqtt** (1) — MQTT, IoT messaging
- **mes** (1) — MES, manufacturing execution

### Data Science, AI & Machine Learning (434 skills)

- **data** (324) — Data engineering, pipelines, modeling
- **ai** (55) — Artificial intelligence, agents
- **embedding** (10) — Embeddings, vector search
- **duckdb** (9) — DuckDB, analytical DB
- **ml** (6) — Machine learning, training
- **model** (5) — ML models, serving
- **pytorch** (3) — PyTorch, deep learning
- **llm** (3) — Large language models
- **vector** (2) — Vector databases, similarity
- **rag** (2) — RAG, retrieval augmented generation

### Cybersecurity (106 skills)

- **pentest** (30) — Penetration testing, offensive security
- **vulnerability** (15) — Vulnerability management
- **incident** (10) — Incident response, forensics
- **threat** (8) — Threat intelligence, hunting
- **crypto** (7) — Cryptography, encryption
- **compliance** (7) — Compliance, audit, governance
- **audit** (5) — Security audit, assessment
- **malware** (4) — Malware analysis, reverse engineering
- **hipaa** (2) — HIPAA compliance
- **gdpr** (2) — GDPR, privacy
- **soc** (2) — SOC operations

### Creative, Design & Media (159 skills)

- **design** (39) — UI/UX design, design systems
- **animation** (18) — 2D/3D animation
- **music** (15) — Music production, audio
- **video** (13) — Video editing, production
- **photo** (12) — Photography, editing
- **creative** (12) — Creative direction, ideation
- **graphic** (11) — Graphic design, visual
- **illustration** (8) — Illustration, drawing
- **typography** (6) — Typography, type design
- **color** (6) — Color theory, palettes
- **figma** (3) — Figma, prototyping
- **sketch** (2) — Sketch, prototyping
- **brand** (2) — Brand design

### Education & Personal Development (11 skills)

- **learning** (3) — Learning science, study skills
- **meditation** (2) — Meditation, mindfulness
- **yoga** (2) — Yoga, wellness
- **writing** (2) — Writing, communication
- **fitness** (1) — Fitness, training
- **nutrition** (1) — Nutrition, diet

### Government, Law & Public Policy (9 skills)

- **government** (3) — Public administration, policy
- **law** (2) — Legal research, practice
- **policy** (2) — Public policy, regulation
- **compliance** (1) — Regulatory compliance
- **ethics** (1) — Ethics, governance

### Other Notable Categories

- **email** (392) — Email systems, SMTP, delivery
- **climate** (230) — Climate science, sustainability
- **energy** (59) — Energy, renewables, oil & gas
- **agri** (138) — Agriculture, agritech
- **aviation** (190) — Aviation, aerospace
- **fashion** (179) — Fashion, apparel, design
- **accounting** (145) — Accounting, bookkeeping
- **beauty** (80) — Beauty, skincare, cosmetics
- **automotive** (78) — Automotive, vehicles
- **digital** (76) — Digital transformation
- **blockchain** (76) — Blockchain, crypto, Web3
- **chemical** (68) — Chemical engineering
- **crispr** (65) — CRISPR, gene editing
- **civil** (45) — Civil engineering
- **construction** (41) — Construction, building
- **carbon** (45) — Carbon, emissions, climate
- **feature** (40) — Feature engineering
- **desktop** (40) — Desktop applications
- **drug** (39) — Drug discovery, pharma
- **google** (35) — Google Cloud, APIs
- **faith** (35) — Faith, religion, spirituality
- **event** (30) — Event planning
- **cell** (27) — Cell biology
- **crop** (22) — Crop science
- **demand** (21) — Demand planning
- **edge** (20) — Edge computing
- **color** (20) — Color theory
- **autonomous** (20) — Autonomous systems
- **application** (20) — Application development
- **cognitive** (18) — Cognitive science
- **computational** (18) — Computational methods
- **battery** (17) — Battery technology

---

## Skill Format Specification

### Directory Structure

```
skills/<category>-<topic>/          # e.g., skills/python-web-scaffold/
├── SKILL.md                        # Required — skill definition
├── references/                     # Optional — additional docs
│   └── <topic>.md
├── templates/                      # Optional — output templates
│   └── <template>.<ext>
├── scripts/                        # Optional — helper scripts
│   └── <script>.<ext>
├── assets/                         # Optional — images, data
│   └── <file>.<ext>
└── examples/                       # Optional — example outputs
    └── <example>.<ext>
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name              # Required — kebab-case, matches directory
description: Brief description (≤120 chars)  # Required — one sentence
version: 1.0.0                # Required — semver
author: Name/Handle            # Required
license: MIT                   # Required — SPDX identifier
platforms: [any]               # Required — [linux, macos, windows, any]
metadata:
  hermes:
    tags: [tag1, tag2]         # Required — 2-5 lowercase tags
    related_skills: [other]    # Optional — related skill names
---
```

### Body Structure

```markdown
# Skill Title

One-sentence summary of what this skill does.

## Trigger
- Conditions that activate this skill
- User intent patterns

## Core Concepts
- Key terminology and domain vocabulary
- Fundamental principles and mental models

## Step-by-Step Workflow
1. **Phase Name** — What happens, why, expected output
2. **Phase Name** — What happens, why, expected output

## Tools & Technologies
- Specific tools, libraries, platforms
- APIs and integrations

## Best Practices
- Patterns that work (with rationale)
- Common anti-patterns to avoid

## Common Pitfalls
- Mistake → consequence → fix

## Related Skills
- Cross-references to complementary skills
```

### Tag Guidelines

- Use 2-5 tags per skill
- Lowercase, kebab-case for multi-word: `machine-learning`, `data-engineering`
- Be specific: `react` > `frontend`, `postgresql` > `database`
- Reference existing tags for consistency

---

## Skill Generator Toolkit

Tools for creating, validating, bulk-generating, and enriching skills.

### Quick Commands

```bash
# Generate a single skill
python scripts/skill-generator/generate_skill.py generate \
  --name my-skill \
  --description "Does X, Y, Z" \
  --tags python,cli \
  --apply

# Bulk generate from JSON
python scripts/skill-generator/bulk_generate.py skills.json --apply

# Validate all skills
python scripts/skill-generator/validate_skill.py

# Enrich boilerplate skills with real content
python scripts/skill-generator/generate_skill.py enrich --apply
```

### Bulk JSON Format

```json
[
  {"name": "my-skill", "description": "Does X", "tags": ["python", "cli"]},
  {"name": "other-skill", "description": "Does Y", "tags": ["web", "react"]}
]
```

### Bulk CSV Format

```csv
name,description,tags
my-skill,Does X,"python, cli"
other-skill,Does Y,"web, react"
```

### Category Detection

The generator auto-detects categories from name keywords:
- `python-*`, `react-*`, `api-*` → **software-development**
- `security-*`, `pentest-*`, `crypto-*` → **security**
- `aws-*`, `kubernetes-*`, `docker-*` → **cloud**
- `data-*`, `sql-*`, `ml-*` → **data**
- `ai-*`, `llm-*`, `model-*` → **ai**

Each category uses a different content template with domain-specific workflow, tools, and pitfalls.

---

## Automatic Updates

This repository syncs bidirectionally with Hermes Agent instances via cron:

```bash
# Pull latest
cd ~/LoopyLuci-skills && git pull

# Push (automatic via sync script)
./scripts/sync-from-hermes.sh --force
```

Sync runs hourly on connected machines. New skills added in Hermes are auto-committed and pushed to GitHub.

---

## Contributing

1. **Add skills** — Use the generator or create manually following the format
2. **Validate** — Run `validate_skill.py` to check format
3. **Commit** — Skills are auto-synced; manual commits welcome
4. **Push** — Sync script handles push; PRs accepted for bulk additions

---

## License

MIT — free to use, share, and contribute.
