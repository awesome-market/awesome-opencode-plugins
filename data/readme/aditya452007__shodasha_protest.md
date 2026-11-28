# Shodasha — Jantar Mantar Public Civic Discussion Platform

> A transparent public civic discussion and community publishing forum for Jantar Mantar, New Delhi.

## Tech Stack

- **Frontend**: Next.js 16 (React 19)
- **Backend**: Fastify (Node.js)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Database**: PostgreSQL (via Supabase)
- **ORM**: Drizzle ORM
- **Cache**: Redis
- **Shared Package**: `@shodasha/shared` (Zod schemas, types, constants)
- **Package Manager**: npm (workspaces)

## Getting Started

```bash
# Install dependencies
npm install

# Start Docker services (PostgreSQL, PgBouncer, Redis)
npm run services:up

# Run database migration
npm run db:migrate

# Seed initial categories and sample posts
npm run db:seed

# Run development server (server + web concurrently)
npm run dev
```

## Project Structure

```
├── apps/
│   ├── server/        # Fastify API server (port 4000)
│   └── web/           # Next.js 16 frontend (port 3000)
├── packages/
│   └── shared/        # Shared types, Zod schemas, constants
├── docker/            # Docker configuration
├── .agent/            # AI agent skills and commands
├── context/           # Project context files
├── Agent.md           # Agent execution protocol
├── Skills.py          # Skill installer
└── README.md          # This file
```

## Skills

Skills are in `.agent/` — run `python Skills.py` to install AI agent design and development skills. See `.agent/AGENTS.md` for details.

## License

MIT
