# OpenCode Config Template

[![validate](https://github.com/YOUR_ORG/opencode-config-template/actions/workflows/validate.yml/badge.svg)](https://github.com/YOUR_ORG/opencode-config-template/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenCode v2](https://img.shields.io/badge/OpenCode-v2-blue)](https://opencode.ai)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20WSL%20%7C%20macOS%20%7C%20Windows-lightgrey)](#установка)

Обезличенный шаблон конфигурации **OpenCode v2**: default-профиль без MCP, семь
именных профилей, инструкции для агентов, ~100 скиллов, локальные плагины,
команды, установщики и тесты.

Репозиторий — стартовая точка, а не чужой рабочий конфиг. Скопируйте его,
замените плейсхолдеры на свои значения и запустите `setup.sh`.

## Содержание

- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Что внутри](#что-внутри)
- [Профили и MCP](#профили-и-mcp)
- [Установка](#установка)
- [macOS (Apple Silicon)](#macos-apple-silicon)
- [WSL и OpenCode Desktop](#wsl-и-opencode-desktop)
- [Проверка](#проверка)
- [Документация](#документация)
- [Участие](#участие)
- [Безопасность](#безопасность)
- [Лицензия](#лицензия)

## Возможности

- **Восемь профилей** — `default`, `dev`, `infra`, `net`, `sec`, `ot`, `mgnt`,
  `design`; у каждого свои MCP-серверы, агенты, модель и права.
- **Изоляция инструментов** — default намеренно без MCP; тяжёлые серверы
  подключаются только в нужной роли.
- **Кастомные агенты** — ревью, архитектура, AppSec, SRE, сети, CTF, АСУ ТП,
  продуктовые роли, UI/UX.
- **~100 скиллов** — TDD, планирование, ревью, rollout, отладка, Vault,
  веб-скрапинг, дизайн-системы и другие процедуры.
- **Управление контекстом** — нативная компакция, DCP, ленивые references,
  контекст-леджер (`INDEX` → `current` → `decisions`).
- **Плагины** — синхронизация конфига, SuperMemory, handoff, usage-monitor,
  per-session наборы MCP (`/mcp`).
- **Проектный слой** — один проект на нескольких профилях через
  `opencode.jsonc`, без копирования глобальных конфигов.
- **Проверяемость** — схема конфигов, тесты гигиены репозитория, проверка ссылок
  и согласованности матрицы профилей; всё запускается в CI.

## Быстрый старт

1. Нажмите **Use this template** на GitHub или сделайте fork.
2. Клонируйте свою копию:

   ```bash
   git clone https://github.com/YOUR_ORG/opencode-config-template.git
   cd opencode-config-template
   ```

3. Замените плейсхолдеры:

   ```bash
   rg -n "YOUR_ORG|YOURUSER|YOURHOST|YOUR_PROJECT" .
   ```

4. Проверьте и установите:

   ```bash
   bash setup.sh --dry-run
   bash setup.sh
   source ~/.zshrc   # или ~/.bashrc
   ```

5. Запустите OpenCode:

   ```bash
   oc          # default-профиль
   ocp dev     # именной профиль
   ```

### Плейсхолдеры

| Плейсхолдер | Что заменить |
|---|---|
| `YOUR_ORG` | ваш GitHub-логин или организация |
| `YOURUSER` | имя пользователя в путях `/home/YOURUSER` |
| `YOURHOST` | имя рабочей машины |
| `YOUR_PROJECT` | проект в Vault (`secret/agent/<project>/...`) |
| `anthropic/claude-sonnet-4-5` | модель по умолчанию для ваших провайдеров |
| примеры доменов и IP | ваши адреса GitLab, Proxmox, LM Studio и т. п. |

## Что внутри

| Компонент | Путь | Назначение |
|---|---|---|
| Default-профиль | `config/opencode.json` | общая работа, **без MCP** |
| Именные профили | `profiles/{dev,infra,net,sec,design,ot,mgnt}/` | роли, MCP, модели |
| Инструкции | `config/instructions/` | russian, workflow, rules, context-protocol |
| Скиллы | `config/skills/` | ~100 скиллов, канонический источник |
| Плагины | `config/plugins/` | локальные: `profile-badge`, `opencode-mcp-sets`, `folder-switcher` |
| Команды | `config/command/` | `/grill-me` и профильные команды |
| Установка | `setup.sh`, `setup.ps1` | Linux/WSL, macOS и Windows native |
| Проверки | `tests/` | схема, гигиена, миграции, ссылки, матрица |

## Профили и MCP

`default` (алиас `oc`) — базовый набор инструментов, MCP-серверы **не подключены**.
MCP живут в именных профилях. Состав, алиасы и роли —
в [docs/profiles-agents-matrix.md](docs/profiles-agents-matrix.md); MCP-колонка
генерируется из `profiles/*/opencode.jsonc` скриптом `scripts/gen-mcp-matrix.py`.

Алиасы профилей запускают `opencode --standalone --continue`: в v2 конфигурацией
владеет фоновый сервис, и без `--standalone` выбранный профиль не применяется.
`--continue` продолжает последнюю сессию проекта; новая сессия — `leader+n` в TUI.

Все профили по умолчанию используют `anthropic/claude-sonnet-4-5`. Поменять модель
можно в `config/opencode.json` и `profiles/*/opencode.jsonc` (`model` и
`small_model`), либо задать `PUBLIC_MODEL` при экспорте из приватного репозитория.

Секреты MCP передаются только через `{env:...}` или HashiCorp Vault; в репозитории
нет паролей и токенов.

Переключение профилей — `scripts/ocp`:

```bash
ocp            # fzf-меню
ocp infra      # запуск в профиле infra
ocp default    # лёгкий профиль без MCP
```

## Установка

```bash
git clone https://github.com/YOUR_ORG/opencode-config-template.git
cd opencode-config-template
bash setup.sh --dry-run     # посмотреть план
bash setup.sh               # Linux/WSL/macOS, интерактивно
```

macOS (Apple Silicon): `xcode-select --install`, Homebrew, затем `bash setup.sh`
— подробности в [docs/macos.md](docs/macos.md).

Windows native: `.\setup.ps1` (рекомендуется WSL2).

Скрипт раскладывает конфиги в `~/.config/opencode/` и `~/.config/opencode-<profile>/`,
скиллы — в `~/.config/opencode/skills/`, настраивает алиасы `oc`, `oc-dev`,
`oc-infra`, `oc-net`, `oc-sec`, `oc-ot`, `oc-mgnt`, `oc-design`.

Требования:

| Компонент | Обязательно | Примечание |
|---|---|---|
| `git`, `curl` | да | установка и обновления |
| OpenCode v2 | да | `setup.sh` ставит через `opencode.ai/v2/install` |
| Node.js | нет | нужен только части MCP-серверов и плагинов |
| WSL 2 | для Desktop | WSL 1 не поддерживается Desktop-приложением |
| Xcode CLT + Homebrew | для macOS | `setup.sh` ставит пакеты через brew |
| Docker / podman | для части MCP | Docker, GitLab/GitHub MCP, security tooling |

## macOS (Apple Silicon)

```bash
xcode-select --install
brew install git gh jq fzf ripgrep
bash setup.sh
```

`setup.sh` определяет `Darwin`/`arm64`, ставит кроссплатформенные пакеты,
OpenTofu из brew и `kubectl` под `darwin/arm64`; Linux-only пакеты пропускаются.
Desktop: `brew install --cask opencode-desktop`. Профили — `ocp`; для Desktop
используйте проектный `opencode.jsonc`. Подробности и диагностика —
[docs/macos.md](docs/macos.md).

## WSL и OpenCode Desktop

Desktop на Windows подключается к серверу внутри WSL: **Settings → Servers →
Add WSL server**. Профили `ocp` там не работают (сервер не читает shell-rc),
поэтому роли добавляются проектным `opencode.jsonc`:

```bash
cd ~/projects/my-service
oc-project-init.py --profiles dev,infra
```

Затем откройте проект по WSL-пути и перезапустите сервер. Подробности, ограничения
и диагностика — [docs/wsl-desktop.md](docs/wsl-desktop.md).

## Проверка

```bash
python3 tests/validate_configs.py config profiles   # схема v2 + политика путей
python3 -m pytest tests -q                          # гигиена, ссылки, матрица, миграции
```

То же выполняет GitHub Actions: [`.github/workflows/validate.yml`](.github/workflows/validate.yml)
плюс проверка утечек через gitleaks.

## Документация

- [AGENTS.md](AGENTS.md) — как работать с репозиторием
- [config/AGENTS.md](config/AGENTS.md) — профиль агента по умолчанию
- [docs/usage-scenarios.md](docs/usage-scenarios.md) — сценарии: новый проект,
  подключение существующего, перенос, передача, секреты
- [docs/USAGE.md](docs/USAGE.md) — подробное руководство
- [docs/profiles-agents-matrix.md](docs/profiles-agents-matrix.md) — профили, агенты, MCP
- [docs/multi-profile-projects.md](docs/multi-profile-projects.md) — один проект на нескольких профилях
- [docs/context-management.md](docs/context-management.md) — компакция, DCP, ledger
- [docs/mcp-sets.md](docs/mcp-sets.md) — `/mcp off|only|reset`
- [docs/macos.md](docs/macos.md) — macOS (Apple Silicon): установка, профили, Desktop
- [docs/wsl-desktop.md](docs/wsl-desktop.md) — WSL 2 и Desktop
- [docs/skill-management.md](docs/skill-management.md) — управление скиллами
- [docs/profiles-migration.md](docs/profiles-migration.md) — карта профилей
- [docs/config-migration.md](docs/config-migration.md) — legacy-ключи и почему они остались

## Участие

См. [CONTRIBUTING.md](CONTRIBUTING.md). Коротко: fork → ветка → тесты → PR.
Приветствуются исправления шаблона, документации и CI; личные конфигурации и
секреты не принимаются.

## Безопасность

Не открывайте публичный issue для уязвимостей. Порядок описан в
[SECURITY.md](SECURITY.md). Секреты — только `{env:...}` или Vault; в git им
места нет.

## Лицензия

[MIT](LICENSE). Copyright (c) 2026 opencode-config-template contributors.

## Происхождение

Шаблон собран из приватной рабочей конфигурации скриптом экспорта: личные и
корпоративные данные, внутренние адреса и документы удалены, идентификаторы
заменены плейсхолдерами. Публичная копия — build artifact: правки в сгенерированные
файлы могут быть перезаписаны при следующем экспорте.
