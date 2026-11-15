#AI #Агенты #Coding #Skills #MCP #Инструменты

# Ponytail

Режим «ленивого сеньора» для AI-агентов: меньше кода, ниже стоимость и быстрее ответы - без потери безопасности, валидации и доступности.

Ponytail встраивает в агента лестницу решений: не писать лишнее, переиспользовать существующее, брать stdlib и нативные возможности платформы, и только потом - минимум, который работает.

По бенчмаркам на реальных агентных сессиях (FastAPI + React): около **54% меньше кода**, **~20% дешевле**, **~27% быстрее**, при **100%** сохранении safety-гардов.

## Возможности

- Лестница YAGNI: от «не нужно» до «одна строка» и минимального рабочего решения
- Работает с ~20 агентными средами: Claude Code, Codex, Copilot CLI, Cursor, OpenCode, Gemini, Pi, Qoder, Hermes и другими
- Уровни интенсивности: `lite` / `full` / `ultra` / `off`
- Команды ревью, аудита, долга и «gain»: `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`
- Хуки жизненного цикла и skills, плюс `AGENTS.md` для instruction-only режима
- Не режет trust-boundary валидацию, обработку потери данных, security и a11y

## Стек

- JavaScript / Node.js (плагины, hooks, skills, MCP)
- Markdown-правила и манифесты для Cursor, Codex, Claude Code, OpenCode, Gemini и других
- Тесты на встроенном `node --test`

## Быстрый старт

Клонируйте зеркало и подключите к агенту:

```bash
git clone https://github.com/best-radar/bradar-ponytail.git
cd bradar-ponytail
```

### Claude Code

```text
/plugin marketplace add best-radar/bradar-ponytail
/plugin install ponytail@bradar-ponytail
```

Две команды - двумя отдельными сообщениями.

### Codex

```bash
codex plugin marketplace add best-radar/bradar-ponytail
codex plugin add ponytail@bradar-ponytail
```

Затем в `codex` откройте `/hooks`, доверьте lifecycle hooks и начните новый тред.

### GitHub Copilot CLI

```bash
copilot plugin marketplace add best-radar/bradar-ponytail
copilot plugin install ponytail@bradar-ponytail
```

### Pi

```text
pi install git:github.com/best-radar/bradar-ponytail
```

### OpenCode

Из checkout репозитория в `opencode.json`:

```json
{ "plugin": ["./.opencode/plugins/ponytail.mjs"] }
```

### Gemini CLI

```bash
gemini extensions install https://github.com/best-radar/bradar-ponytail
```

### Cursor / Windsurf / Cline и другие

Скопируйте соответствующий rules-файл из репозитория (`.cursor/rules/`, `.windsurf/rules/`, `.clinerules/`, `AGENTS.md` и т.д.). Подробности - в [docs/agent-portability.md](docs/agent-portability.md).

Для Claude Code и Codex нужен `node` в PATH non-interactive shell: иначе skills работают, а always-on активация молчит.

Уровень по умолчанию: `full`. Можно задать через `PONYTAIL_DEFAULT_MODE` или `~/.config/ponytail/config.json`.

## Как это работает

Перед написанием кода агент останавливается на первой ступени, которая держит:

```text
1. Нужно ли это вообще?        -> нет: не пишем (YAGNI)
2. Уже есть в кодовой базе?    -> переиспользуем
3. Есть в stdlib?              -> используем
4. Нативная фича платформы?    -> используем
5. Уже установленная зависимость? -> используем
6. Хватает одной строки?       -> одна строка
7. Иначе: минимум, который работает
```

Лестница идёт после понимания задачи: агент читает затронутый код и реальный поток, а не вместо чтения.

## Команды

| Команда | Назначение |
|---------|------------|
| `/ponytail [lite \| full \| ultra \| off]` | Уровень интенсивности или выключение |
| `/ponytail-review [target]` | Ревью в стиле ponytail |
| `/ponytail-audit [target]` | Аудит раздутости |
| `/ponytail-debt` | Техдолг, который стоит упростить |
| `/ponytail-gain` | Где упрощение даст выигрыш |
| `/ponytail-help` | Справка |

## Примеры

Вместо тяжёлого date-picker компонента:

```html
<!-- ponytail: в браузере уже есть -->
<input type="date">
```

Больше примеров - в [examples/](examples/). Бенчмарки - в [benchmarks/](benchmarks/).

## Лицензия

MIT. Файл `LICENSE` сохранён вместе с исходными копирайтами.
