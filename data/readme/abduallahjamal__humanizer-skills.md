<div align="center">

<img src="assets/banner.svg" alt="humanizer-skills — Bilingual EN & AR Anti-Slop & AI Text Humanization Suite" width="100%"/>

<br/>

**Bilingual (English + Arabic) anti-slop & AI-writing humanization suite — 5 [Agent Skills](https://agentskills.io), `/humanize` router command, and 4 zero-dependency Python verification CLIs distilled from 10 open-source humanizer repositories for OpenCode, Claude Code, Codex CLI, and DeepSeek Harness (`dsh`).**

[![CI](https://github.com/abduallahJamal/humanizer-skills/actions/workflows/validate.yml/badge.svg?label=CI)](https://github.com/abduallahJamal/humanizer-skills/actions/workflows/validate.yml)
[![Skills](https://img.shields.io/badge/Skills-5%20%2B%20%2Fhumanize-38BDF8)](#the-five-agent-skills)
[![CLIs](https://img.shields.io/badge/Dependencies-Zero%20(Python%20Stdlib)-818CF8)](#deterministic-cli-tools)
[![Languages](https://img.shields.io/badge/Prose-English%20%26%20Arabic-A78BFA)](#bilingual-arabic--english-coverage)
[![OpenCode](https://img.shields.io/badge/OpenCode-ready-111827)](#installation)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-ready-D97757)](#installation)
[![Codex CLI](https://img.shields.io/badge/Codex%20CLI-ready-10A37F)](#installation)
[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-ready-2563EB)](#installation)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E.svg)](LICENSE)
[![Arabic Docs](https://img.shields.io/badge/%D8%A7%D9%84%D8%AA%D9%88%D8%AB%D9%8A%D9%82-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-1E293B)](README.ar.md)

**🇬🇧 English** · **[🇪🇬 العربية](README.ar.md)**

</div>

---

## 📌 Why a Modular Suite Instead of One Mega-Prompt?

Single-prompt humanizers fail in predictable ways: casualizing a research paper introduces contractions and drops inline citations; prepending *"Moreover,"* to sound academic triggers modern detectors; and running prose rules on a codebase corrupts Markdown fences or leaves `// Fetch user from DB` comments untouched.

`humanizer-skills` splits the problem into **specialized, non-conflicting skills** backed by **deterministic local Python scripts** so mechanical counting, burstiness math, digit-preservation checks, and code-fence masking run in code rather than LLM guesswork.

| Skill | Role | Bundled CLI Gate / Analyzer | Upstream DNA Distilled |
| :--- | :--- | :--- | :--- |
| **[`humanize`](skills/humanize/SKILL.md)** | Smart orchestrator (`/humanize`) routing by intent & register | Dispatches to specialist skill | Progressive-disclosure routing |
| **[`humanize-text`](skills/humanize-text/SKILL.md)** | 3-pass + 9-lever prose rewriter with 5 voice profiles & zero-invention lock | `humanize_gate.py` | `blader/humanizer`, `lguz/humanize-writing-skill`, `harshaneel/humanize`, `haidrrrry/humanize-ai-writing`, `ZAYUVALYA`, `ADEMOLA200` |
| **[`ai-writing-detector`](skills/ai-writing-detector/SKILL.md)** | **Detect-only** forensic audit: 12 stylometric metrics + 9-signal rubric (`0–27`) & sentence heatmap | `detect_ai_metrics.py` | `conorbronsdon/avoid-ai-writing`, `harshaneel/humanize` (`ai-check`), `rudra496/StealthHumanizer` |
| **[`anti-slop-coder`](skills/anti-slop-coder/SKILL.md)** | Proactive & surgical cleanup for `README.md`, docs, PRs, commits, thread replies & code comments | `repo_slop_scan.py` | `ofershap/ai-humanizer`, `blader/humanizer` (§19–§26), `conorbronsdon/avoid-ai-writing` (`edit` mode) |
| **[`academic-humanizer`](skills/academic-humanizer/SKILL.md)** | Formal/scholarly rewriter (EN & MSA Arabic) with 100% citation, LaTeX & number lock + word-level diff | `academic_prep.py` | `DadaNanjesha/AI-Text-Humanizer-App`, `rudra496/StealthHumanizer` (`academic-inversion`), `ZAYUVALYA` |

---

## 🚀 Installation

Zero external packages required (`bash` + `Python 3.9+` standard library).

```bash
git clone https://github.com/abduallahJamal/humanizer-skills.git
cd humanizer-skills

# Install globally for ALL 4 harnesses (OpenCode, Claude Code, Codex CLI & DeepSeek Harness)
./install.sh --all --global

# Or install into a single project repository
./install.sh --all --project /path/to/your-project

# Or target one specific harness
./install.sh --dsh --global
./install.sh --claude --global
./install.sh --codex --global
./install.sh --opencode --global
```

**Windows PowerShell:**

```powershell
.\install.ps1 --target all --scope global
```

---

## 🛠️ Multi-Harness Compatibility Matrix

| Agent Harness | Project Path | Global Path | Invocation | Platform Specifics Included |
| :--- | :--- | :--- | :--- | :--- |
| **OpenCode** | `.opencode/skills/` | `~/.config/opencode/skills/` | `/humanize` or auto-trigger | Quoted single-line YAML frontmatter + `.opencode/commands/humanize.md` |
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | `/humanize-text`, `/ai-writing-detector`, … | `.claude-plugin/plugin.json` & `marketplace.json` (no `$schema` warning) |
| **OpenAI Codex CLI** | `.agents/skills/` & `.codex/skills/` | `~/.agents/skills/` & `~/.codex/skills/` | `$humanize`, `$humanize-text`, … | `agents/openai.yaml` sidecar per skill + `.agents/plugins/marketplace.json` |
| **DeepSeek Harness (`dsh`)** | `.dsh/skills/` (rank 100) | `~/.dsh/skills/` (`$DSH_HOME/skills`) | `skill({ name })` / Palette | Strict **depth-1 flat layout** for `@deepseek-ai/dsh-skill-filesystem` & `dsh-agent-skills` |

---

## 🌍 Bilingual Arabic & English Coverage

Beyond English Wikipedia/RLHF tells (`delve`, `tapestry`, `leverage`, `Not X, but Y`, prose em-dashes `—`, uniform 15-word pulse, mini-aphorism closers), the suite ships native **Arabic AI-slop detection and rewriting rules** ([`ar-patterns.md`](skills/humanize-text/references/ar-patterns.md)):

- **Translation calques (`الركاكة المترجمة`):** Eliminates excessive `تم + المصدر` passive calques, `يقوم بـ + المصدر` verb padding, repetitive `بشكل + صفة` adverbs, and literal `لا يقتصر الأمر على X فحسب، بل يتعداه إلى Y` negative parallelisms.
- **Canned openers & closers:** Strips *«في ظل التطورات المتسارعة»*, *«مما لا شك فيه»*, *«يلعب دوراً محورياً»*, *«علاوة على ذلك»* paragraph stacks, and *«وفي الختام يمكن القول»*.
- **Sacred, legal & fixed-term shield:** Locks Quranic/hadith quotes, legal terminology, proper nouns, inline citations, and numbers across both Arabic-Indic (`٠-٩`) and Western (`0-9`) numerals.

---

## 🧪 Deterministic CLI Tools

Every script runs standalone from the terminal as well as inside agent sessions:

```bash
# 1. Score any English or Arabic draft (12 metrics + flagged sentence heatmap)
python3 skills/ai-writing-detector/scripts/detect_ai_metrics.py --file draft.txt

# 2. Verify a humanized rewrite against hard gates + fact/number preservation
python3 skills/humanize-text/scripts/humanize_gate.py --original raw.txt --rewritten clean.txt

# 3. Scan docs, source comments & commit messages for developer AI slop
python3 skills/anti-slop-coder/scripts/repo_slop_scan.py README.md src/

# 4. Prep academic prose & verify 100% survival of citations, equations & numbers + diff
python3 skills/academic-humanizer/scripts/academic_prep.py prep -i paper.txt -o prepped.txt
python3 skills/academic-humanizer/scripts/academic_prep.py verify -o paper.txt -r final.txt -d diff.md
```

---

## 📂 Repository Structure

```text
humanizer-skills/
├── assets/banner.svg                  # Repository header graphic
├── skills/                            # Canonical flat depth-1 skills source
│   ├── humanize/                      # Orchestrator router skill
│   ├── humanize-text/                 # EN/AR 3-pass humanizer + humanize_gate.py
│   ├── ai-writing-detector/           # Detect-only 12-metric + 9-signal audit
│   ├── anti-slop-coder/               # Docs, commits, PRs & code comments guard
│   └── academic-humanizer/            # Scholarly humanizer + citation/digit lock & diff
├── .opencode/                         # Mirrored OpenCode skills + /humanize command
├── .claude/ & .claude-plugin/         # Mirrored Claude Code skills + plugin manifests
├── .agents/                           # Mirrored Codex CLI skills + marketplace manifest
├── .dsh/                              # Mirrored DeepSeek Harness depth-1 skills
├── scripts/
│   ├── sync-platforms.sh              # SHA-256 parity sync across all 4 agent roots
│   └── validate.py                    # Schema, link & end-to-end CLI test suite
├── install.sh / install.ps1 / install.py
├── README.md                          # English documentation
└── README.ar.md                       # Arabic RTL documentation
```

---

## 🙏 Credits & Upstream Inspiration

Synthesized from the open-source work of:
[`blader/humanizer`](https://github.com/blader/humanizer) ·
[`conorbronsdon/avoid-ai-writing`](https://github.com/conorbronsdon/avoid-ai-writing) ·
[`ofershap/ai-humanizer`](https://github.com/ofershap/ai-humanizer) ·
[`haidrrrry/humanize-ai-writing`](https://github.com/haidrrrry/humanize-ai-writing) ·
[`lguz/humanize-writing-skill`](https://github.com/lguz/humanize-writing-skill) ·
[`harshaneel/humanize`](https://github.com/harshaneel/humanize) ·
[`rudra496/StealthHumanizer`](https://github.com/rudra496/StealthHumanizer) ·
[`ADEMOLA200/Humanize-AI`](https://github.com/ADEMOLA200/Humanize-AI) ·
[`ZAYUVALYA/AI-Text-Humanizer`](https://github.com/ZAYUVALYA/AI-Text-Humanizer) ·
[`DadaNanjesha/AI-Text-Humanizer-App`](https://github.com/DadaNanjesha/AI-Text-Humanizer-App).

> **Responsible-use note:** These skills improve natural clarity, rhythm, and editorial precision, and explain stylometric signals with transparent evidence. No tool guarantees 100% evasion of commercial classifiers, which also exhibit high false-positive rates on human writing.

## 📄 License

Released under the [MIT License](LICENSE) — Copyright © 2026 Abduallah Jamal.
