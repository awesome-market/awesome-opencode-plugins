# mcp-kaneo

MCP server for Kaneo task management API. Lets your AI coding assistant manage tasks, projects, labels, and comments in Kaneo.

## Features

- **Tasks**: Create, read, update, delete tasks
- **Projects**: List and manage projects
- **Labels**: Create, update, delete labels; attach/detach from tasks
- **Comments**: Add and list comments on tasks
- **Search**: Search tasks, projects, and workspaces
- **Workspaces**: List workspaces and organizations
- **Task Relations**: Create subtask relations (links to Kaneo's native subtasks)

## Requirements

- [Node.js](https://nodejs.org/) v18 or later
- [Kaneo](https://kaneo.app/) account with API access

## Installation

### Using npx (recommended)

```bash
npx @fastman/mcp-kaneo
```

### Using npm

```bash
npm install -g @fastman/mcp-kaneo
npx @fastman/mcp-kaneo
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `KANEO_BASE_URL` | Yes | Kaneo API URL (e.g., `https://your-kaneo-instance.com/api`) |
| `KANEO_TOKEN` | Yes | Kaneo API token |
| `KANEO_TOOLSETS` | No | Comma-separated toolset names (default: `core`) |

### Toolsets

The server organizes tools into groups. By default only the `core` toolset is registered, keeping context size minimal.

| Toolset | Tools | Description |
|---------|-------|-------------|
| `core` | 11 | Task lifecycle, listing, search, subtasks |
| `collaboration` | 14 | Labels, comments, task relations |
| `admin` | 7 | Workspace and project CRUD |
| `legacy` | 6 | Field-specific task update tools (deprecated) |

**Configuration examples:**

```bash
# Default: core only (11 tools)
npx @fastman/mcp-kaneo

# Core + labels and comments
KANEO_TOOLSETS=core,collaboration npx @fastman/mcp-kaneo

# All non-legacy tools
KANEO_TOOLSETS=all npx @fastman/mcp-kaneo

# Everything including legacy field-specific updates
KANEO_TOOLSETS=all,legacy npx @fastman/mcp-kaneo
```

The `all` alias expands to `core,collaboration,admin` (excludes `legacy`).

### Codex

Add the server with the Codex CLI:

```bash
codex mcp add kaneo \
  --env KANEO_BASE_URL=https://your-kaneo-instance.com/api \
  --env KANEO_TOKEN=your-token \
  -- npx -y @fastman/mcp-kaneo
```

This stores the environment values in Codex's configuration. To keep the token
out of the configuration file, export the variables before starting Codex and
add the following to `~/.codex/config.toml` (or `.codex/config.toml` in a trusted
project):

```toml
[mcp_servers.kaneo]
command = "npx"
args = ["-y", "@fastman/mcp-kaneo"]
env_vars = ["KANEO_BASE_URL", "KANEO_TOKEN", "KANEO_TOOLSETS"]
```

For local development, build the project and replace the command and arguments:

```toml
[mcp_servers.kaneo]
command = "node"
args = ["/absolute/path/to/mcp-kaneo/dist/index.js"]
env_vars = ["KANEO_BASE_URL", "KANEO_TOKEN", "KANEO_TOOLSETS"]
```

Run `codex mcp list` to verify the configuration. In the Codex terminal UI, use
`/mcp` to confirm that the server is active and its tools are available.

### OpenCode

Add to your `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "kaneo": {
      "type": "local",
      "command": ["npx", "-y", "@fastman/mcp-kaneo"],
      "environment": {
        "KANEO_BASE_URL": "https://your-kaneo-instance.com/api",
        "KANEO_TOKEN": "${KANEO_TOKEN}"
      }
    }
  }
}
```

Or for local development:

```json
{
  "mcp": {
    "kaneo": {
      "type": "local",
      "command": ["node", "/path/to/mcp-kaneo/dist/index.js"],
      "environment": {
        "KANEO_BASE_URL": "https://your-kaneo-instance.com/api",
        "KANEO_TOKEN": "your-token"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add kaneo --scope user npx @fastman/mcp-kaneo
```

### Cline

Add to your MCP settings:

```json
{
  "mcpServers": {
    "kaneo": {
      "command": "npx",
      "args": ["-y", "@fastman/mcp-kaneo"]
    }
  }
}
```

### Cursor

Go to `Cursor Settings` → `MCP` → `New MCP Server`:

```json
{
  "command": "npx",
  "args": ["-y", "@fastman/mcp-kaneo"]
}
```

## Tools

### Core (default)

- `list_workspaces` - List all accessible workspaces
- `list_projects` - List projects in a workspace
- `list_columns` - List columns in a project
- `list_tasks` - List tasks in a project with columns and pagination
- `search` - Search tasks, projects, or comments
- `get_task` - Get task details
- `create_task` - Create a new task
- `update_task` - Update one or more task fields (partial update)
- `delete_task` - Delete a task
- `create_subtask` - Create a subtask linked to a parent (inherits parent status by default)
- `list_subtasks` - List subtasks for a parent task

### Collaboration (`KANEO_TOOLSETS=collaboration`)

- `list_labels` - List workspace labels
- `create_label` - Create a new label
- `update_label` - Update label name/color
- `delete_label` - Delete a label
- `attach_label` - Attach label to task
- `detach_label` - Detach label from task
- `list_task_labels` - List labels on a task
- `add_comment` - Add comment to task
- `list_comments` - List comments on task
- `edit_comment` - Edit a comment
- `delete_comment` - Delete a comment
- `create_task_relation` - Create a relation between tasks
- `list_task_relations` - List all relations for a task
- `delete_task_relation` - Delete a task relation

### Admin (`KANEO_TOOLSETS=admin`)

- `get_workspace` - Get workspace details
- `update_workspace` - Update a workspace
- `delete_workspace` - Delete a workspace
- `get_project` - Get project details
- `create_project` - Create a new project
- `update_project` - Update a project
- `delete_project` - Delete a project

### Legacy (`KANEO_TOOLSETS=legacy`)

Field-specific task update tools preserved for migration. Use `update_task` instead.

- `update_task_title` - Update task title
- `update_task_description` - Update task description
- `update_task_status` - Update task status
- `update_task_priority` - Update task priority
- `update_task_assignee` - Update task assignee
- `update_task_due_date` - Update task due date

## Usage Examples

### Create a task

```
Create a task in kaneo called "Fix login bug" with high priority
```

### Update multiple fields

```
Update task #123: set priority to urgent and move to in-progress
```

### Create a subtask

```
Create a subtask "Fix the login validation" for parent task #123
```

### List subtasks

```
List all subtasks for task #123
```

### Add a label (requires collaboration toolset)

```
Create a label called "bug" with color #ef4444 and attach it to the task
```

### Update task status

```
Move the task "Fix login bug" to in-progress
```

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Test
npm test

# Run locally
npm start
```

## License

MIT
