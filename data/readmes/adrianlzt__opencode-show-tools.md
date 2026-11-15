# @adrianlzt/opencode-show-tools

An OpenCode plugin that adds a `/tools` slash command to list all available tools for a specific provider/model.

## Installation

```bash
npm install @adrianlzt/opencode-show-tools
```

Add to your `opencode.json`:

```json
{
  "plugin": ["@adrianlzt/opencode-show-tools"]
}
```

For local development:

```json
{
  "plugin": ["file:///path/to/opencode-show-tools/dist/index.js"]
}
```

## Usage

Once installed, use the `/tools` command in your OpenCode TUI session:

```
/tools
```

This will display a list of all available tools for the configured provider (zai/glm-5) with their descriptions:

```
# Available Tools

- **invalid** - Do not use
- **question** - Use this tool when you need to ask the user questions during execution
- **bash** - Executes a given bash command in a persistent shell session with optional timeout
- **read** - Read a file or directory from the local filesystem
...
```

**Note:** This command works only in the OpenCode TUI. The `opencode run --command tools` CLI mode does not display session messages.

## Development

```bash
# Install dependencies
npm install

# Type check
npx tsc --noEmit

# Build
npx vite build --mode production

# Lint
npx biome lint .
npx biome format .
```

## License

MIT
