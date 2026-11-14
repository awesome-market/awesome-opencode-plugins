# opencode-session-timestamps

> **Dates and times where OpenCode Desktop does not show them: session headers, Home and sidebar rows, session tabs, and every transcript turn.**  
> 🌐 *[Документация на русском языке (Russian documentation)](./README_RU.md)*

[![OpenCode Desktop](https://img.shields.io/badge/OpenCode_Desktop-v2.2.0+-blue.svg)](https://opencode.ai/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178c6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![SolidJS](https://img.shields.io/badge/SolidJS-1.9-2c4f7c.svg?logo=solid&logoColor=white)](https://www.solidjs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Why

OpenCode Desktop groups Home sessions into **Today / Yesterday / Older** and never renders a session row's date. The transcript shows a turn's duration, but not when it happened. That makes a session from last week and one from six months ago look the same until you open them.

This plugin adds those chronology anchors without touching the server: it reads `session.time.created/updated` and `message.time.created/completed` from the app's own synced data.

---

## ✨ Features

- **Session header** — `Created 12 Nov, 03:20 · Updated 13 Nov, 15:42` next to the session title, with the full timestamp in the tooltip; compact mode keeps only the last activity.
- **Home session list** — a right-aligned last-activity stamp on every row.
- **Sidebar session list** — the same stamp. Sidebar rows carry no session id in the DOM, so they are matched by their unique title; duplicate titles are skipped.
- **Session tabs** — a compact clock that reserves the app's 24px status area, so unread/attention dots and the close button never overlap it. Hidden on hover and in tabs narrower than 150px.
- **Tab hover preview** — separate **Created** and **Updated** lines with localized full dates.
- **Transcript turns** — `15:42 → 15:43` above each user message: when it was sent and when its answer finished. Running turns show the send time only.
- **Quick switch** — a clock button beside the sidebar toggle hides or shows every date without opening Settings (dimmed when off).
- **Settings → Session Timestamps** — master switch, a toggle per surface, friendly (`15:42`, `Yesterday, 09:05`, `12 Nov, 15:42`) or always-absolute dates, a 12/24-hour clock, and a live preview in the current language.
- **Localized** — English and Russian catalogs; the app language is followed live, with an English fallback.

All times follow the app language and update live when a session changes.

---

## 📸 Screenshots

### Home session list

![Home session list with a last-activity time on every row](assets/home-session-list.png)

Every row ends with the session's last activity, so a session from today, yesterday or last month no longer looks the same.

### Session header

![Created and updated times in the session header](assets/session-header.png)

A session's **Created** and **Updated** times sit beside its token and cost readout; the full date with seconds is in the tooltip.

### Settings

<img src="assets/settings.png" alt="Settings page for Session Timestamps" width="520" />

**Settings → Session Timestamps**: a master switch, one toggle per surface, friendly or always-absolute dates, a 12/24-hour clock, and a live preview in the app language.

### Quick switch

![Clock button beside the sidebar toggle](assets/sidebar-quick-toggle.png)

The clock button beside the panel toggle hides or shows every date in one click (dimmed when off).

### Tab hover preview

![Created and Updated lines in the tab hover preview](assets/tab-hover-preview.png)

The tab hover preview gains separate **Created** and **Updated** lines with full, localized dates.

---

## 📦 Installation

### Option A: install from GitHub

```bash
opencode plugin add github:Realmagnum/opencode-session-timestamps
```

### Option B: add to the config

```json
{
  "plugins": ["/absolute/path/to/opencode-session-timestamps"]
}
```

Then reload the window with `Cmd+R` — the GUI half is loaded per window. Requires OpenCode Desktop 2.2+.

---

## ⚙️ How it works

The session header uses the official `session.header` slot. Home/sidebar rows, tabs, the hover preview and transcript turns have no slot, so the plugin appends `<time>` nodes to the app's DOM and reconciles them with a `MutationObserver`; each pass re-adds what the app re-rendered away.

- Times for loaded sessions come from `ctx.servers[*].data.session` / `data.session.message` (reactive stores).
- Rows the store never loaded fall back to a bounded `session.list` index (500 newest per server), refreshed on execution, rename, archive and delete events.
- Sidebar rows are matched by unique title; tabs and their hover preview by the `href`'s `ses_...` id.
- The timeline turn clock maps the user message id to the last assistant `time.completed` of that turn.

---

## 🛠 Build

```bash
npm install
npm run build        # vite build + copy gui-experimental.cjs to the package root
npm run typecheck
npm test             # i18n key parity and fallback
npm run ci           # typecheck + test + build
```

---

## Known limits

- Sidebar rows with duplicate titles are not stamped. Home rows, headers, tabs and the transcript are unaffected.
- A transcript turn whose user message is outside the virtualized window has no stamp until it scrolls into view.
- Only the active timeline gets turn stamps; a cached, hidden timeline keeps the stamps it had.
- The tab clock is hidden while hovering a tab, where the app shows its close button in the same 24px.

---

## License

MIT
