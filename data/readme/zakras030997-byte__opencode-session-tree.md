# opencode-session-tree

Дерево «проекты → треды» для сайдбара OpenCode TUI: клики мышью (левый — открыть/развернуть,
правый — меню), «+» для создания, клавиатурный паритет через палитру и слэш-команды.
Проекты создаются плагином автоматически внутри `~/.local/share/opencode/projects/`.

## Установка

```sh
opencode plugin add github:zakras030997-byte/opencode-session-tree
```

Затем перезапустите OpenCode. Проверить: в правой панели появится секция `─ ПРОЕКТЫ ─`.

Отключить: удалить пакет (`opencode plugin remove opencode-session-tree`) или добавить
`-opencode-session-tree` в `plugins` конфига.

## Управление

## Где живут проекты

```
~/.local/share/opencode/projects/
└── <проект>/threads/<тред>/      ← тред: сессия + рабочий каталог агента
```

Корень переопределяется опцией `projectsRoot` в `opencode.json`:

```jsonc
{ "plugins": [{ "package": "./plugins/session-tree", "options": { "projectsRoot": "~/my-projects" } }] }
```

## Управление

**Мышь** (штатные обработчики OpenTUI):
- `[+]` в строке `ПРОЕКТЫ` — создать проект.
- `[+]` у проекта — новый тред (создаётся `threads/<slug>/` + сессия в нём, сразу открывается).
- Левый клик по проекту — развернуть/свернуть; по треду — открыть.
- **Правый клик** по проекту — меню: новый тред / переименовать / удалить (полная зачистка).
- **Правый клик** по треду — меню: открыть / переименовать / удалить.
- **Перетаскивание проекта** — зажмите строку проекта и отпустите над другой строкой: проект
  встаёт на её место (вниз — под цель, вверх — над целью). Порядок запоминается в
  `<projectsRoot>/.session-tree-order.json` и сохраняется между запусками.

**Клавиатура** (полный паритет): палитра `Ctrl+P` → `session-tree.*`, слэш-команды `/tree`, `/tree-new`, `/tree-project-new`.

## Удаление

- **Тред**: сессия + папка `threads/<slug>/` (после подтверждения; только при маркере владения).
- **Проект**: все сессии проекта (сабагенты удаляются рекурсивно), история, папка с тредами и файлами — необратимо, после подтверждения.
- **Переименование проекта**: папка переименовывается, все сессии перепривязываются на новые пути (`session.move`).

## Защиты

- Проекты и треды удаляются только внутри каталога проектов; симлинки не переходятся.
- Папка треда удаляется только при маркере `.session-tree-thread.json` с совпадающим sessionID.
- `threads/` с чужими папками (без маркеров) не трогается — создание треда вернёт `occupied`.

## Файлы

| Файл | Роль |
|---|---|
| `index.ts` | серверная часть: RPC `listTree/createProject/renameProject/deleteProject/reorderProject/createThread/deleteThread/...`, файловые операции |
| `rpc.ts` | типизированный контракт |
| `tui.tsx` | дерево в сайдбаре, клики, «+», меню, команды палитры |

Каталог `~/.config/opencode/plugins/session-tree/` подхватывается автодискавери.

## Отключение

Удалить/переименовать каталог `session-tree/`, либо `-local.session-tree` в `plugins` конфига, либо `opencode plugin remove local.session-tree`.

## Проверено на живом сервере (2.0.32)

createProject → createThread (папка+маркер+сессия с location) → renameProject (папка+`session.move`) →
deleteThread → deleteProject (`removedSessions:1, removedFolder:true`, папка удалена, сессий нет).

## Остаток (P1/P2)

Курсорная навигация внутри панели, закрепление, фильтр `/`, `date-slug`, привязка «без проекта» к проекту, удалённый сервер.

## Для разработки

`package.json` сознательно **не содержит** `devDependencies` и `scripts` — OpenCode
устанавливает git-плагины через внутренний npm, и они ломают подготовку git-зависимости.
Для сборки используется Bun:

```sh
bun add -d @opencode/plugin @opentui/core '@opentui/solid>=0.6.6' 'solid-js>=1.9.0'
bun build.ts        # компилирует tui.tsx -> dist/tui.js (Solid-JSX заранее)
```

После правок: bump версии в `package.json`, commit, push, затем локально:

```sh
opencode plugin remove github:zakras030997-byte/opencode-session-tree
rm -rf ~/.cache/opencode/npm/git-opencode-session-tree-*
opencode plugin add github:zakras030997-byte/opencode-session-tree
```

(Кэш npm и git-ref кэш держат старый коммит ~минуту — чистая переустановка надёжнее `plugin update`.)
