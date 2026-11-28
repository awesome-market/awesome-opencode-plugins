# OpenCodeAutoPM

[![NPM Version](https://img.shields.io/npm/v/opencode-autopm)](https://www.npmjs.com/package/opencode-autopm)
[![NPM Downloads](https://img.shields.io/npm/dm/opencode-autopm)](https://www.npmjs.com/package/opencode-autopm)
[![MIT License](https://img.shields.io/badge/License-MIT-28a745)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/rafeekpro/OpenCodeAutoPM?style=social)](https://github.com/rafeekpro/OpenCodeAutoPM)

**AI-Powered Project Management Framework for OpenCode**

OpenCodeAutoPM transforms your development workflow with intelligent automation, 40 specialized AI agents, hybrid parallel execution, and complete GitHub/Azure DevOps integration.

---

## Quick Install

```bash
npm install -g opencode-autopm
cd your-project
opencode-autopm install
```

Choose your scenario during installation:
- **Minimal** - Core features, sequential execution
- **Docker** - Container development with Docker
- **Full** - All features, adaptive execution (recommended)
- **Performance** - Maximum parallelization with hybrid execution (5 concurrent agents)

---

## Quick Start

All commands run inside OpenCode (not terminal):

```bash
# Initialize context and testing
/context:create
/testing:prime

# Azure DevOps integration
/azure:init
/azure:us-new "User authentication"
/azure:task-list

# GitHub integration
/github:workflow-create

# Working with agents
@python-backend-engineer Build FastAPI endpoint
@test-runner execute all tests
@code-analyzer review recent changes
```

---

## 🎯 Variable Groups Management

**NEW: Automate Azure DevOps variable groups - No more manual UI clicking!**

The variable groups commands solve the critical problem of manually linking variable groups to pipelines in Azure DevOps UI.

**Quick Example**:
```bash
# Create variable group with secrets
/azure:vg-create production-vars --variables="APP_ENV=prod" --secrets="API_KEY=secret"

# Link to 3 pipelines (this was MANUAL before!)
/azure:vg-link <vg-id> --pipeline=51 --pipeline=52 --pipeline=53

# All done in 2 seconds! (used to take 5+ minutes of clicking)
```

**Key Features**:
- ✅ Create variable groups with secret support
- ✅ Link to multiple pipelines at once
- ✅ Export/import for backup and migration
- ✅ Validation and health checks
- ✅ Full CRUD operations

**All 10 Commands**:
- `/azure:vg-create` - Create variable groups
- `/azure:vg-link` - Link to pipelines ⭐
- `/azure:vg-list` - List all
- `/azure:vg-show` - Show details
- `/azure:vg-update` - Update
- `/azure:vg-delete` - Delete
- `/azure:vg-unlink` - Unlink
- `/azure:vg-export` - Export
- `/azure:vg-import` - Import
- `/azure:vg-validate` - Validate

**Learn More**: [Documentation](https://rafeekpro.github.io/OpenCodeAutoPM/)

---

## Features

### Plugin System

12 official plugins with 269 commands across all domains:

**Core** (7 commands)
- Context management (`/context:*`)
- Testing framework detection (`/testing:*`)
- Configuration (`/config:*`)
- MCP server setup (`/mcp:*`)

**PM System** (54 commands)
- PRD and Epic management
- Issue tracking and decomposition
- Git workflow integration
- Progress tracking

**Azure DevOps** (51 commands)
- **NEW: Variable Groups** (10 commands) - Manage variable groups with secrets
  - `/azure:vg-create` - Create variable groups with secrets
  - `/azure:vg-link` - **Link variable groups to pipelines (solves manual UI work!)**
  - `/azure:vg-list` - List all variable groups
  - `/azure:vg-show` - Show variable group details
  - `/azure:vg-update` - Update variable groups
  - `/azure:vg-delete` - Delete variable groups
  - `/azure:vg-unlink` - Unlink from pipelines
  - `/azure:vg-export` - Export for backup/migration
  - `/azure:vg-import` - Import from files
  - `/azure:vg-validate` - Validate configuration
- User Story management (`/azure:us-*`)
- Task management (`/azure:task-*`)
- Feature/Epic management (`/azure:feature-*`)
- Sprint planning and status

**GitHub** (18 commands)
- Workflow creation
- Issue and PR management
- Repository automation

**Languages** (3 commands)
- Python backend expert
- JavaScript frontend expert
- Node.js backend expert

**Frameworks** (6 commands)
- React UI components
- Tailwind CSS styling
- UX design analysis

**Testing** (3 commands)
- E2E test scaffolding
- Frontend testing
- Test execution

**DevOps** (8 commands)
- Docker containerization
- Kubernetes deployment
- Infrastructure setup
- SSH operations

**Cloud** (2 commands)
- Multi-cloud deployment
- Infrastructure automation

**Databases** (4 commands)
- PostgreSQL expert
- MongoDB expert
- Redis expert
- BigQuery expert

**AI/ML** (3 commands)
- LangGraph workflows
- OpenAI integration
- Data pipelines

**Data** (3 commands)
- Kedro pipelines
- Airflow orchestration

### Agent Registry

40 specialized AI agents organized by domain:

**Core Agents** (6)
- `agent-manager` - Create and manage agents
- `code-analyzer` - Code analysis and bug detection
- `test-runner` - Test execution and analysis
- `file-analyzer` - Large file summarization
- `parallel-worker` - Multi-agent coordination
- `mcp-manager` - MCP server infrastructure

**Language Agents** (4)
- `python-backend-engineer` - Python architecture and FastAPI
- `javascript-frontend-engineer` - Modern JavaScript/TypeScript
- `nodejs-backend-engineer` - Express, Fastify, NestJS
- `bash-scripting-expert` - Shell automation and scripting

**Framework Agents** (5)
- `react-frontend-engineer` - Full React applications
- `react-ui-expert` - UI components (MUI, Chakra, AntD)
- `tailwindcss-expert` - Utility-first CSS framework
- `ux-design-expert` - UX/UI design and accessibility
- `e2e-test-engineer` - Playwright and Cypress E2E tests

**Testing Agents** (1)
- `frontend-testing-engineer` - Component and integration tests

**Database Agents** (4)
- `postgresql-expert` - PostgreSQL design and optimization
- `mongodb-expert` - MongoDB schema and aggregation
- `redis-expert` - Caching and pub/sub messaging
- `bigquery-expert` - Data warehouse and analytics

**DevOps Agents** (6)
- `docker-containerization-expert` - Docker containers and compose
- `kubernetes-orchestrator` - K8s deployments and Helm
- `github-operations-specialist` - GitHub Actions and workflows
- `observability-engineer` - Prometheus, Grafana, ELK
- `traefik-proxy-expert` - Reverse proxy configuration
- `ssh-operations-expert` - Secure SSH operations

**Cloud Agents** (5)
- `aws-cloud-architect` - AWS infrastructure design
- `azure-cloud-architect` - Azure cloud architecture
- `gcp-cloud-architect` - GCP cloud design
- `terraform-infrastructure-expert` - Infrastructure as Code
- `gcp-cloud-functions-engineer` - Serverless functions

**Integration Agents** (2)
- `message-queue-engineer` - Kafka, RabbitMQ, SQS/SNS
- `nats-messaging-expert` - NATS pub/sub and queues

**Data/ML Agents** (3)
- `langgraph-workflow-expert` - LangGraph workflows
- `kedro-pipeline-expert` - Kedro data pipelines
- `airflow-orchestration-expert` - Airflow DAGs

**AI API Agents** (2)
- `openai-python-expert` - OpenAI API integration
- `gemini-api-expert` - Google Gemini API

### Provider Integration

- **GitHub** - Issues, PRs, Actions, Projects, Workflows
- **Azure DevOps** - Work Items, Boards, Pipelines, Sprints
- **Local** - Git-based workflow with markdown tracking

### Execution Strategies

- **Sequential** - Safe, predictable, resource-light
- **Adaptive** - Intelligent mode selection (default)
- **Hybrid** - Maximum parallelization

---

## Documentation

### Getting Started
- [Installation](https://rafeekpro.github.io/OpenCodeAutoPM/getting-started/installation)
- [First Project](https://rafeekpro.github.io/OpenCodeAutoPM/getting-started/first-project)
- [Configuration](https://rafeekpro.github.io/OpenCodeAutoPM/getting-started/configuration)

### User Guide
- [Command Overview](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/commands-overview)
- [Agent Registry](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/agents-overview)
- [PM System](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/pm-system)
- [Azure DevOps Integration](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/azure-devops)
- [GitHub Integration](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/github-integration)
- [MCP Servers](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/mcp-servers)
- [Best Practices](https://rafeekpro.github.io/OpenCodeAutoPM/user-guide/best-practices)

### Developer Guide
- [Architecture](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/architecture)
- [Plugin Development](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/plugin-development)
- [Agent Development](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/agent-development)
- [Command Development](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/command-development)
- [Testing](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/testing)
- [Contributing](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/contributing)

### Reference
- [CLI Reference](https://rafeekpro.github.io/OpenCodeAutoPM/commands/)
- [Agent Registry](https://rafeekpro.github.io/OpenCodeAutoPM/agents/)
- [Configuration Options](https://rafeekpro.github.io/OpenCodeAutoPM/reference/configuration)
- [Troubleshooting](https://rafeekpro.github.io/OpenCodeAutoPM/reference/troubleshooting)

---

## Why OpenCodeAutoPM?

| Feature | OpenCodeAutoPM | Traditional Tools |
|---------|--------------|-------------------|
| AI-native | Built for OpenCode | Adapted/retrofitted |
| Modular | 12 plugins, install what you need | Monolithic |
| Agents | 40 specialized experts | Generic or none |
| Workflow | Context to Production | Fragmented |
| Integration | GitHub + Azure DevOps | Limited |
| Documentation | Context7-verified, always current | Often outdated |

---

## Contributing

We welcome contributions! See [Contributing Guide](https://rafeekpro.github.io/OpenCodeAutoPM/developer-guide/contributing) for:
- Development setup
- Coding standards (TDD mandatory)
- Testing requirements
- Pull request process

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Links

- **Documentation**: [rafeekpro.github.io/OpenCodeAutoPM](https://rafeekpro.github.io/OpenCodeAutoPM/)
- **npm**: [npmjs.com/package/claude-open-autopm](https://www.npmjs.com/package/claude-open-autopm)
- **Issues**: [GitHub Issues](https://github.com/rafeekpro/OpenCodeAutoPM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rafeekpro/OpenCodeAutoPM/discussions)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

<p align="center">
  <b>Built for OpenCode community</b>
  <br>
  <sub>Star this repo if OpenCodeAutoPM helps your workflow!</sub>
</p>
