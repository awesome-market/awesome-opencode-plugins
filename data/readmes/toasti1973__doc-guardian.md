# Doc Guardian - OhMyOpenCode Skill

Automatically generates code documentation (JSDoc, TSDoc comments) and creates a CHANGELOG.md file with all changes made during the task. Supports configurable documentation language.

## Features

- **Code Documentation** - Automatically generates JSDoc/TSDoc comments
- **Changelog Generation** - Creates/updates CHANGELOG.md with task changes
- **Multi-language Support** - Configurable documentation language
- **Git Integration** - Reads git commits for changelog

## Installation

### Automatic Installation (once published to OhMyOpenCode Skill Registry)

```bash
opencode skill install doc-guardian
```

### Manual Installation

1. Clone this repository or copy the `doc-guardian` folder to:
   - **Project**: `.opencode/skills/doc-guardian/`
   - **Global**: `~/.config/opencode/skills/doc-guardian/`

## Usage

### Load as Skill

```typescript
task(
  load_skills=["doc-guardian"],
  ...
)
```

### Generate Documentation

```bash
npx doc-guardian generate
npx doc-guardian generate --files src/*.ts
```

### Generate Changelog

```bash
npx doc-guardian changelog
```

### Both at Once

```bash
npx doc-guardian all
```

## Configuration

Create `.doc-guardian.json` in your project root:

```json
{
  "language": "en",
  "changelog": {
    "includeAuthor": true,
    "commitTypes": ["feat", "fix", "docs", "refactor"],
    "outputFile": "CHANGELOG.md"
  },
  "documentation": {
    "includeExamples": true
  }
}
```

## Supported Languages

| Code | Language |
|------|----------|
| en | English |
| de | German |
| es | Spanish |
| fr | French |
| it | Italian |
| pt | Portuguese |
| nl | Dutch |
| pl | Polish |
| ru | Russian |
| zh | Chinese |
| ja | Japanese |
| ko | Korean |

## Note on .gitignore

The CHANGELOG.md file is NOT added to .gitignore by default. If you want to exclude it:

```bash
echo "CHANGELOG.md" >> .gitignore
```

## License

MIT
