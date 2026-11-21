# Francesco

<p align="center">
  <i>🇮🇹 <a href="README.it.md">Parli solo rabbia e salsicce? Clicca qui.</a></i>
</p>

<p align="center">
  <img src="characters/francesco.svg" width="100%" alt="Francesco — il revisore contabile">
</p>

> **35 years old. Round glasses. Distant stare. Maniacal precision.**
>
> Francesco is not a genius. He doesn't try to be. He's the human robot you hire when the numbers must check out — 3 times? 30? He doesn't know. He'll check anyway.

---

## Quick Start

After installation, invoke Francesco by name:

> **`/francesco`** — orchestrator (shows menu, picks the right flow)
> **`/francesco-bilancio`** — balance sheet checks
> **`/francesco-estratto`** — bank reconciliation
> **`/francesco-revisione`** — audit documentation

The orchestrator greets you, runs preflight, then asks what you need. Tell him directly — he picks the right workflow. Sub-skills skip the menu and go straight to work.

---

## What Francesco Can Do

| Say this... | He runs... |
|---|---|
| "revisione" / "audit" / "verbale" | Full audit session: identify → plan → exec → triple-check → close |
| "check" / "controlla" | Validates docs: data, dates, signatures, logs |
| "bilancio" / "quadratura" | Balance sheet: SP=CE ties, cross-foot, nota integrativa tie-out |
| "benford" / "numeri truccati" | Anti-manipulation: Benford χ², round-number bias, duplicates, patterns |
| "estratto conto" / "riconciliazione" | Bank reconciliation: match movements, catch discrepancies |
| "inizializza" / "nuova societa" | New company setup: scan → identify → propose → approve |
| "normativa" / "leggi" | Regulation archive by country/type/sector (builds offline) |
| "triage" / "stato" | Quick company state scan |
| "riepilogo" / "report" | Generates DOCX summary report |

---

## Why Francesco Exists

Every audit produces the same pain:
- **Spreadsheets with missing quarters**
- **Signatures that don't match dates**
- **"I'm sure I saved that file"** (you didn't)

Francesco is purpose-built for one job: **audit documentation, done right, every time.** He doesn't get bored, doesn't rush, and triple-checks everything — including his own triple check.

---

## Features

| Feature | What it means |
|---|---|
| **Audit Workflow** | Full audit cycle: context extraction, planning, execution, triple check, closure |
| **Document Validation** | Cross-checks data, dates, signatures, import amounts across all sources |
| **Personal Archive** | Local regulation database built per-jurisdiction, per-company-type, per-sector. Works offline. |
| **Triple Check** | Execute → verify → re-verify → read one more file just in case |
| **Context Extraction** | Scans existing docs to reconstruct jurisdiction, company type, mandate, audit state |
| **OCR + Docling** | Scanned PDFs? Francesco reads them. DOCX, XLSX? Native. |
| **Auto-Logging** | Every session writes a dated log. `PROCESSO_REVISIONE.md` always current. |
| **Cross-Platform** | Works on Linux, macOS, Windows. OpenCode, Claude Code, Cursor, others. |
| **Balance Check** | Quadratura SP/CE, cross-foot, nota integrativa tie-out, scelte contabili |
| **Benford / Anti-Manipulation** | χ² test, Z per digit, round-number bias, duplicated amounts, terminal-digit, threshold clustering |
| **Bank Reconciliation** | Match movements, categorize unreconciled, reconcile saldo, cross-check cassa |

---

## How It Works

Orchestrator (`/francesco`) runs this loop every session:

```
Check frustration → Preflight → Capisci richiesta → Carica comando → Esegui → Verifica output → Triplo check → Chiudi
```

1. **Frustration check** — detects frustration/cursing (IT + EN patterns); 1-2 hits → calm message; 3+ consecutive → skip, go straight to action
2. **Preflight** — finds the company dir, checks deps (docling, libreoffice, skills), validates directory structure, reads last log
3. **What to do?** — if you haven't said anything, introduces himself and asks what you need; confirms understanding before proceeding
4. **Picks the right command** — maps your request to a workflow
5. **Executes** — runs the chosen command
6. **Verifies output** — opens produced files, checks log was written
7. **Triple checks** — 4 passes (exec → verify → safety → re-read last log line)
8. **Closes** — writes log, updates `PROCESSO_REVISIONE.md`, offers DOCX report

**Sub-skills** (`/francesco-bilancio`, `/francesco-estratto`, `/francesco-revisione`) skip step 3 and go straight to their flow — fully standalone, with their own triple check and closure.

### 1. Safety Preflight

Before touching anything, Francesco:
1. Checks if the company directory exists
2. Creates `AGENTS.md` if missing
3. Creates `Revisione/PROCESSO_REVISIONE.md` if missing
4. Tests file readability (`.docx`, `.xlsx`, scanned PDFs)
5. Verifies last log date is coherent

If something doesn't add up, he stops and asks. Never proceeds blind.

### 2. Audit Flow

```
Identify  →  Plan  →  Execute  →  Triple-Check  →  Close
  │           │          │             │              │
  │           │          │             │              ├─ Write dated log
  │           │          │             │              ├─ Update PROCESSO_REVISIONE.md
  │           │          │             │              └─ Validate output files
  │           │          │             │
  │           │          │             └─ 1st: execute
  │           │          │                2nd: verify everything
  │           │          │                3rd: if doubt → ask; if sure → do it again
  │           │          │                4th: re-read last log line
  │           │          │
  │           │          └─ OCR? docling. DOCX? docx skill. XLSX? xlsx skill.
  │           │
  │           └─ What needs doing today? What NOT to touch?
  │
  └─ Jurisdiction? Company type? Mandate? Sector?
```

### 3. Personal Normative Archive

Francesco doesn't keep every law in his head. On every job:

1. Detects jurisdiction (IT, DE, FR, US, ...) from company docs
2. Checks `normative/` for existing regulation by country + company type + sector
3. Complete → proceed. Missing → searches the right official sources:
   - **Italy**: Normattiva, Gazzetta Ufficiale, CNDCEC
   - **Germany**: Bundesanzeiger, Handelsregister, IDW
   - **France**: Légifrance, Journal Officiel, CNCC
   - **US**: SEC.gov, FASB, state corporation registries
4. Saves locally per-country. Next time it's there. Works offline.

> No central database. No PRs to update a regulation. His stuff. Local. Updated when needed.

---

## Token Discipline

During analysis, OCR, source reading, and intermediate checks, Francesco writes in compressed `caveman ultra` style — short phrases, no narrative fluff, preserve all numbers/dates/names/references.

**Full readability reserved for:** user questions, critical warnings, official logs, formal documents, and final summary.

---

> *"N.d. is better than a lie. Doubt is better than a rushed certainty."*
> — Francesco, every single session

---

## Installation

```bash
# Auto-detect (recommended)
bash <(curl -fsSL https://raw.githubusercontent.com/xh74d82hl/francesco/main/install.sh) xh74d82hl/francesco

# Via npx skills, explicit agent
npx skills add xh74d82hl/francesco --global --skill francesco --agent opencode

# Manual
git clone https://github.com/xh74d82hl/francesco.git ~/.agents/skills/francesco
```

Replace `opencode` with `claude-code`, `cursor`, or your harness of choice.

### Flags

| Flag | What it does |
|---|---|
| `--agent <name>` | Target a specific harness |
| `--yes` | Skip prompts (only when 1 agent detected) |
| `--list` | Show detected harnesses |
| `--dev-copy` | Copy local files for testing |

### Windows

```powershell
irm https://raw.githubusercontent.com/xh74d82hl/francesco/main/install.ps1 | iex
# Then if needed:
.\install.ps1 xh74d82hl/francesco
```

### Dev Copy

```bash
bash install.sh --dev-copy --target ~/.agents/skills
```

Preserves existing `normative/` and `scripts/`. Safe for iterative development.

---

## Structure

```
~/.agents/skills/francesco/
  SKILL.md              — orchestrator (shared rules + menu)
  README.md             — this file (English)
  README.it.md          — Italian version
  install.sh            — installer for Linux/macOS
  install.ps1           — installer for Windows
  DIRECTION.md          — roadmap
  characters/
    francesco.svg       — the face
  commands/             — shared reusable instructions
    revisione.md        — full audit session flow
    check.md            — document validation
    bilancio_check.md   — balance sheet checks + Benford/patterns
    estratto_check.md   — bank reconciliation
    normativa.md        — regulation archive + auto-update
    triage.md           — quick company scan
    inizializza.md      — new company commissioning
    setup.md            — dependency install
    riepilogo.md        — DOCX summary report
    struttura.md        — directory structure validation
  skills/               — specialized skill entries (direct load)
    francesco-revisione/
      SKILL.md          — audit workflow
    francesco-bilancio/
      SKILL.md          — balance sheet checks + anti-manipulation
    francesco-estratto/
      SKILL.md          — bank reconciliation
  normative/            — per-company regulation archive (gitignored)
  scripts/              — local utility scripts (gitignored)
```

---

## Requirements

- **OpenCode**, **Claude Code**, **Cursor**, or compatible agent
- `npx` available in PATH
- Optional: `docling` MCP for scanned PDFs
- Optional: LibreOffice for legacy `.doc` files

---

## License

[MIT](LICENSE)

---

## Credits

Style inspired by **Ralph** — because when a bro does good work, you say it.


Built with ❤️ for auditors, accountants, and everyone who triple-checks their triple check.
