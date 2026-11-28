# OpenCode Config — skills & plugins

A personal distribution of my [OpenCode](https://opencode.ai) configuration:
32 agent skills, 10 plugins, and the matching `opencode.json` / `cli.json`.
Runs anywhere OpenCode runs — including Android via
[Termux](https://termux.dev).

Available in [Russian / Русский](#readme-русский).

## What's inside

| Path | Contents |
|------|----------|
| `opencode.json` | main config (plugins: ponytail, headroom, omniroute, antigravity bridge) |
| `cli.json` | terminal UI settings (gruvbox theme, session/diff prefs) |
| `.gitignore` | excludes all credential files |
| `skills/` | 32 skills: artifacts-builder, canvas-design, docx, pdf, pptx, xlsx, mcp-builder, text-to-lottie, slack-gif-creator, webapp-testing, and more |
| `plugins/` | ponytail suite (mode tracker, hooks, statusline, /commands), omniroute model-catalog sync, antigravity bridge, headroom |

## Installation

1. **Install OpenCode**

   ```sh
   # npm
   npm install -g opencode-ai

   # or via the install script
   curl -fsSL https://opencode.ai/install | bash
   ```

2. **Clone this repo into your config directory**

   Merge into an existing config, or replace it entirely:

   ```sh
   git clone https://github.com/Collalaoo/opencode-config.git /tmp/oc-cfg
   cp -rv /tmp/oc-cfg/{opencode.json,cli.json,skills,plugins} ~/.config/opencode/
   ```

   (On Termux the path is `~/.config/opencode/` the same way — emulated home,
   no root needed.)

3. **Install plugin npm dependencies** (used by some plugins/skills)

   ```sh
   cd ~/.config/opencode
   npm install            # uses the committed package-lock.json
   ```

4. **Restart OpenCode**. Skills appear under `/skills`, plugins load from
   `~/.config/opencode/plugins/`.

### Notes

- Some skills have Python/Node helper scripts (`skills/*/scripts`). They are
  used on demand by the agent; nothing to install globally.
- The omniroute plugin expects a local service at `http://localhost:20128`
  (see its `SKILL.md` if you don't run one).
- The antigravity plugin is a thin bridge over the npm package
  [`opencode-antigravity-auth`](https://www.npmjs.com/package/opencode-antigravity-auth).

## Security

This repo **contains no credentials**. The following files exist only on disk
and are excluded via `.gitignore`:

- `antigravity-accounts.json` — OAuth reconnect tokens / account emails
- `service-android-termux.json` — local service password
- `cligochi-state.json`, `lib/`, `node_modules/`

If you fork/clone and re-publish, keep those ignores in place.

## Licensing

- The repository (my own scripts and setup) is licensed under
  **GPL-3.0-or-later** — see [`LICENSE`](./LICENSE).
- `skills/` — the Anthropic-derived skills ship their own **Apache-2.0**
  `LICENSE.txt` files; those are separate works licensed under Apache 2.0
  (GPLv3-compatible). Their license files are preserved.
- `plugins/skills/ponytail` and the ponytail suite — **MIT** (kept intact).
- Bundled fonts in `skills/canvas-design/canvas-fonts/` — **SIL OFL 1.1**,
  license texts included.

This project is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version, without warranty of any kind.

---

# README (Русский)

# Конфигурация OpenCode — скиллы и плагины

Личная сборка моей конфигурации [OpenCode](https://opencode.ai): 32 скилла,
10 плагинов и соответствующие `opencode.json` / `cli.json`. Запускается везде,
где работает OpenCode — включая Android через
[Termux](https://termux.dev).

[English version](#readme) above.

## Что внутри

| Путь | Содержимое |
|------|------------|
| `opencode.json` | основной конфиг (плагины: ponytail, headroom, omniroute, antigravity) |
| `cli.json` | настройки терминала (тема gruvbox, сессии, диффы) |
| `.gitignore` | исключает все файлы с кредами |
| `skills/` | 32 скилла: artifacts-builder, canvas-design, docx, pdf, pptx, xlsx, mcp-builder, text-to-lottie, slack-gif-creator, webapp-testing и другие |
| `plugins/` | набор ponytail (режимы, хуки, статусбар, /команды), синхронизация моделей omniroute, мост antigravity |

## Установка

1. **Установите OpenCode**

   ```sh
   # через npm
   npm install -g opencode-ai

   # или скриптом
   curl -fsSL https://opencode.ai/install | bash
   ```

2. **Клонируйте репозиторий в каталог конфигурации**

   Объединить с существующим конфигом или заменить целиком:

   ```sh
   git clone https://github.com/Collalaoo/opencode-config.git /tmp/oc-cfg
   cp -rv /tmp/oc-cfg/{opencode.json,cli.json,skills,plugins} ~/.config/opencode/
   ```

   (В Termux путь тот же — `~/.config/opencode/`, root не нужен.)

3. **Установите npm-зависимости плагинов**

   ```sh
   cd ~/.config/opencode
   npm install            # в репо есть package-lock.json
   ```

4. **Перезапустите OpenCode**. Скиллы появятся в `/skills`, плагины
   подхватятся из `~/.config/opencode/plugins/`.

### Примечания

- У части скиллов есть Python/Node-скрипты (`skills/*/scripts`) — они
  используются агентом по мере необходимости, глобально ставить ничего не надо.
- Плагин omniroute ожидает локальный сервис на `http://localhost:20128`.
- Плагин antigravity — тонкая обёртка над npm-пакетом
  [`opencode-antigravity-auth`](https://www.npmjs.com/package/opencode-antigravity-auth).

## Безопасность

В репозитории **нет никаких учётных данных**. Следующие файлы существуют
только на диске и исключены через `.gitignore`:

- `antigravity-accounts.json` — OAuth-токены / почты аккаунтов
- `service-android-termux.json` — пароль локального сервиса
- `cligochi-state.json`, `lib/`, `node_modules/`

Если делаете форк/клон и публикуете заново — не убирайте эти игноры.

## Лицензия

- Репозиторий (мои скрипты и сборка) — **GPL-3.0-or-later**,
  см. [`LICENSE`](./LICENSE).
- Скиллы из `skills/` поставляются со своими файлами **Apache-2.0**
  (`LICENSE.txt` сохранены) — это отдельные произведения под Apache 2.0,
  совместимой с GPLv3.
- Плагины `ponytail` — **MIT**.
- Шрифты в `skills/canvas-design/canvas-fonts/` — **SIL OFL 1.1**.

Это свободное ПО: вы можете распространять и/или изменять его в соответствии
с условиями GNU General Public License, опубликованной Free Software
Foundation — либо версии 3, либо (по вашему выбору) любой более поздней,
без каких-либо гарантий.
