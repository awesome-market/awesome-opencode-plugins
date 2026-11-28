# opencode-desktop-notes

A notes, side-question and todo panel for [OpenCode Desktop](https://opencode.ai).

Jot things down while the agent works, ask the model side questions without touching the main chat, quote parts of the conversation, keep a todo list, and send any of it back to the agent when you're ready.

<p align="center">
  <img src="docs/demo.gif" width="960" alt="Adding notes, annotating a chat passage, asking /btw, using todos, session context, search and Notes only in OpenCode Desktop">
</p>

> [!NOTE]
> OpenCode's GUI plugin API is **experimental**. This plugin is built against OpenCode **2.2.x** and may need an update when that API changes.

## Install

One line:

```sh
curl -fsSL https://raw.githubusercontent.com/wannabemrrobot/opencode-desktop-notes/main/install.sh | sh
```

The script finds the OpenCode CLI, including the copy that ships inside OpenCode Desktop, and runs:

```sh
opencode plugin add github:wannabemrrobot/opencode-desktop-notes
```

You can run that yourself if `opencode` is on your `PATH`.

<details>
<summary>Manual install</summary>

Add the plugin to your **global** config, `~/.config/opencode/opencode.json` or `opencode.jsonc`. OpenCode Desktop only loads GUI plugins from the global config.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": ["github:wannabemrrobot/opencode-desktop-notes"]
}
```

Config changes load without a restart. If the panel doesn't appear, run `/reload`.

</details>

<details>
<summary>Install from a local checkout</summary>

```sh
git clone https://github.com/wannabemrrobot/opencode-desktop-notes.git
cd opencode-desktop-notes
bun install && bun run bundle
```

Then point your global config at the folder:

```jsonc
{ "plugins": ["/absolute/path/to/opencode-desktop-notes"] }
```

</details>

### Open the panel

In a session, press **+** in the side panel and choose **Session notes** or **Project notes**. You can also search the command palette for "Notes".

### Update or remove

```sh
opencode plugin update github:wannabemrrobot/opencode-desktop-notes
opencode plugin remove github:wannabemrrobot/opencode-desktop-notes
```

**Settings > Extensions > Plugins** shows whether the plugin loaded and has a switch to turn its UI off.

## Features

### Notes and side questions (/btw)

Every row has a small badge in its top-right corner:

| Badge | Row |
|---|---|
| Pen | A note |
| Quote | A note attached to a passage from the chat |
| `/btw` | A side question and its answer |
| Quote + `/btw` | A side question about a chat passage |

- **Add a note:** type in the box at the bottom and press **Enter**. **Shift+Enter** starts a new line. The box grows with your text up to a third of the window, then scrolls.
- **Edit a note:** hover it and click **Edit** to edit it right where it is, with the same formatting toolbar. **Enter** or **Save** saves it, **Esc** or **Cancel** leaves it as it was.
- **Formatting:** the box is a small rich-text editor. Use the toolbar, <kbd>⌘</kbd><kbd>B</kbd> / <kbd>I</kbd> / <kbd>E</kbd> / <kbd>K</kbd>, or type Markdown (`**bold**`, `_italic_`, `` `code` ``, `~~strike~~`, `- ` for a list) and it turns into formatting as you type. Notes are saved and shown as Markdown.
- **Ask /btw:** type a question and press **/btw**. The answer comes from the session's context, but nothing is written to the chat history and the running turn isn't interrupted.
- **Threads:** each /btw includes your notes and the earlier side Q&A, so the thread builds on itself. Use **Follow-up /btw** on an answer to keep going.
- **Model picker:** the picker inside the prompt box chooses the model for /btw. **Session model** uses the session's own context. Any other model gets the chat's text (not tool calls or reasoning) plus your notes.
- **Times:** every row shows when it was added, such as "Today, 10:04".

Hover a row to show its action buttons:

| Button | What it does |
|---|---|
| **Ask /btw** (notes) or **Follow-up /btw** (answers) | Asks a side question about that row. Uses the text box as the question, or asks in a dialog if it's empty. |
| **Send to chat** | Posts the row to the agent as a queued message, with anything in the text box added as your comment. |
| **Delete** | Removes the row. |

### Annotate the chat

Select text in the conversation, then press **Annotate** (or <kbd>⌘</kbd><kbd>⌥</kbd><kbd>N</kbd>). The quote attaches to the next note or /btw you write. Click a quote to scroll back to that spot in the chat.


### Todos

Open **Todo** under the search bar. Add items, tick them off, clear finished ones. The **Todo 2/4** count stays on the button while it's closed.

You can also add a todo without opening the list: type `/todo Write retry tests` in the notes box, or run it in the chat prompt. A todo from the chat prompt goes to that session's list. The count updates right away.

Hover a todo and press **Agent** to hand it to the agent with optional instructions. It goes in as a queued message, so a running turn finishes first.


### Session context

**Note session context** shows the session's model, context usage, tokens in and out, cost, and how many notes and /btw questions the tab holds. Only one of **Todo** and **Note session context** is open at a time.


### Search, sort and export

- **Search** filters notes, questions, answers and quotes, and highlights the matches.
- **Notes only** hides /btw rows.
- **Delete all** (the trash icon beside Notes only) clears every note and /btw in the tab, after asking. Todos are kept.
- **Sort** switches between oldest and newest first.
- **Export** saves what's on screen as a Markdown file.
- **Rename** gives the tab its own title.


### Session and project tabs

**Session notes** belong to one session. **Project notes** are shared by every session in the same project folder. Notes, todos and titles are kept separately for each, and survive restarts.

## Costs and limits

- **/btw costs tokens.** With **Session model**, each question re-sends the session context and counts toward the session's totals. Other models are billed to that model.
- **Jump-to-quote** searches the visible chat, so it can miss text from messages the app hasn't loaded yet in a very long session.
- **Highlights** don't mark a match that's split across formatting, such as half a word in bold.
- **Experimental API:** see the note at the top.

## Development

```sh
bun install
bun run bundle     # build dist/gui-experimental.cjs
bun run dev        # rebuild on every change; OpenCode reloads the panel by itself
bun run typecheck
bun run demo       # build a browser preview with a mock host, in demo/dist
```

- `src/gui.tsx` is the whole plugin. It builds to `dist/gui-experimental.cjs`, the file OpenCode loads.
- `dist/` is committed so installing from GitHub needs no build step. Rebuild before you commit.
- `demo/` runs the real panel against a small mock of the OpenCode host, for quick UI work without the desktop app. Build it with `bun run demo`, serve `demo/dist`, and open `index.html` (add `?theme=dark` for the dark theme).

## License

[MIT](LICENSE)
