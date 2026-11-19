# mccode-plugin — Minecraft development for opencode

Minecraft-first [opencode](https://github.com/anomalyco/opencode) plugin. Adds a **`minecraft` agent** and `/mcnew` + `/mcstatus` commands. Interviews you (edition → platform → verified version → build tool → deps like Vault/PlaceholderAPI), verifies every version online, writes `plans/<feature>/README.md` before code, then builds **Paper/Spigot/Purpur/Folia** plugins, **Fabric/NeoForge** mods, **Skript**, **Bedrock** addons and **Discord bots**.

## Install — works even if you don't have opencode

```bash
# 1. install opencode + plugin in one go
npm i -g opencode-ai mccode-plugin

# 2. register plugin
opencode plugin mccode-plugin -g
# or manually add to ~/.config/opencode/opencode.json:
# { "plugin": ["mccode-plugin"] }
```

Already have opencode? Just:

```bash
opencode plugin mccode-plugin -g
```

> Requires `opencode >=1.18.0`, `Node >=22` or `Bun >=1.4`.

## Use

- `opencode` → `Tab` shows `minecraft`, `build`, `plan`
- **New project:** `/mcnew make a shop plugin with Vault` — intake → `plans/<feature>/README.md` → builds
- **Existing plugin:** `Tab` → `minecraft` → chat: `add a /heal command` (auto-detects `plugin.yml`/`build.gradle`/`pom.xml`, skips intake)
- **Status:** `/mcstatus` — reports progress from `plans/`

## License

MIT
