# CTQ Extraction — AI Skill for Engineering Drawings & GD&T Analysis

> **Automatically extract Critical-To-Quality (CTQ) parameters, GD&T feature control frames, and manufacturing tolerances from engineering drawings using any AI coding agent.**

[![agentskills.io compatible](https://img.shields.io/badge/agentskills.io-compatible-brightgreen)](https://agentskills.io)
[![Works with Antigravity](https://img.shields.io/badge/Google%20Antigravity-supported-4285F4)](https://developers.google.com/gemini)
[![Works with Claude Code](https://img.shields.io/badge/Claude%20Code-supported-D97757)](https://docs.anthropic.com/en/docs/claude-code)
[![Works with Cursor](https://img.shields.io/badge/Cursor-supported-000000)](https://cursor.sh)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)

---

## What Is This?

`ctq-extraction` is an **AI agent skill** that turns any LLM-powered coding assistant into a **Manufacturing Quality Engineer**. Point it at an engineering drawing, CAD export, or process control plan and it returns a structured JSON object containing every inspectable requirement — tolerances verbatim, GD&T callouts parsed, and visual bounding-box coordinates mapped.

**Supported document types:**
- 2D/3D engineering drawings (PDF, PNG, JPEG, TIFF)
- Process control plans and FMEA tables
- GD&T-annotated CAD views (section views, detail views)
- Manufacturing control plan spreadsheets

---

## Features

| Capability | Detail |
| :--- | :--- |
| **Product CTQ Extraction** | Dimensions, bilateral/unilateral tolerances, surface finish (`Ra`), thread specs, radii, chamfers |
| **Process CTQ Extraction** | Heat treatment, hardness (`HRC 58-62`), coatings, torque values, weld specs |
| **GD&T Interpretation** | All 14 ASME Y14.5 / ISO 1101 characteristic symbols — Straightness ⎯, Flatness ⏥, Position ⌖, Runout ⌕, and more |
| **Verbatim Tolerances** | Unilateral `+0.05/-0.00` preserved exactly — never rounded or converted to `±` form |
| **Bounding Box Coordinates** | Percentage-based `[x%, y%]` coordinates for every callout, ready for overlay UIs |
| **Structured JSON Output** | Consistent schema for downstream quality systems, ERP, or inspection apps |
| **Schema Validation** | Built-in Python validator to verify extracted JSON conforms to the schema |

---

## Multi-Platform Support

This skill is distributed using a **single canonical source** (`skills/ctq-extraction/SKILL.md`) with directory symlinks for each agent platform — zero content duplication.

| Platform | Entry Point | Discovery Path |
| :--- | :--- | :--- |
| **Google Antigravity / Gemini** | [`GEMINI.md`](./GEMINI.md) | `.agents/skills/ctq-extraction/SKILL.md` |
| **Anthropic Claude Code** | [`CLAUDE.md`](./CLAUDE.md) | `.claude/skills/ctq-extraction/SKILL.md` |
| **OpenCode Interpreter** | [`OPENCODE.md`](./OPENCODE.md) | `.agents/skills/ctq-extraction/SKILL.md` |
| **Cursor AI** | [`.cursorrules`](./.cursorrules) | `.cursor/rules/ctq-extraction.mdc` |
| **AgentSkills standard** | — | `skills/ctq-extraction/SKILL.md` |

---

## Output Schema

Every extraction returns a single JSON object:

```json
{
  "page_number": 1,
  "product_ctqs": [
    {
      "ctq_id": "CTQ-001",
      "ctq_type": "dimension",
      "requirement": "Overall Width",
      "limit_tolerance": "400 ± 0.2",
      "source": "Main view dimension callout",
      "confidence": "high",
      "bbox": [50.0, 24.3]
    },
    {
      "ctq_id": "CTQ-002",
      "ctq_type": "geometry",
      "requirement": "Position ⌖ control frame relative to Datum A, B, and C",
      "limit_tolerance": "Ø0.05 (MMC) A B C",
      "source": "Bore feature control frame",
      "confidence": "high",
      "bbox": [65.4, 42.1]
    }
  ],
  "process_ctqs": [
    {
      "ctq_id": "CTQ-P01",
      "ctq_type": "process",
      "requirement": "Carburize and Harden",
      "limit_tolerance": "HRC 58-62, Case depth 0.8-1.2mm",
      "source": "Drawing Note 3",
      "confidence": "high",
      "bbox": [15.0, 85.0]
    }
  ],
  "unlegible_notes": []
}
```

See [`skills/ctq-extraction/examples/sample_drawing_output.json`](./skills/ctq-extraction/examples/sample_drawing_output.json) for a complete benchmark example.

---

## Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/your-org/CTQ-extraction.git
cd CTQ-extraction
```

### 2. Use in your agent workspace

The skill is **auto-discovered** based on which agent you use:

- **Antigravity / OpenCode:** opens `.agents/skills/ctq-extraction/SKILL.md` automatically.
- **Claude Code:** reads `CLAUDE.md` and `.claude/skills/ctq-extraction/SKILL.md`.
- **Cursor:** picks up `.cursor/rules/ctq-extraction.mdc`.

### 3. Validate extracted JSON output

```bash
python3 scripts/validate_schema.py path/to/your_output.json
# ✅ CTQ JSON is valid!
```

### 4. Run the test suite

```bash
python3 -m unittest discover -s scripts
# Ran 2 tests in 0.000s — OK
```

---

## Repository Structure

```
CTQ-extraction/
├── skills/
│   └── ctq-extraction/
│       ├── SKILL.md                 # Canonical skill — agentskills.io compatible
│       ├── references/
│       │   └── gdt_symbols.md       # ASME Y14.5 / ISO 1101 GD&T symbol lookup table
│       └── examples/
│           └── sample_drawing_output.json   # Benchmark JSON output
├── scripts/
│   ├── validate_schema.py           # CLI schema validator
│   └── test_validate_schema.py      # Automated unit tests
├── .agents/skills → ../skills       # Symlink: Antigravity / OpenCode
├── .claude/skills → ../skills       # Symlink: Claude Code
├── .cursor/rules/
│   └── ctq-extraction.mdc → …      # Symlink: Cursor AI
├── GEMINI.md                        # Antigravity workspace rules
├── CLAUDE.md                        # Claude Code workspace rules
├── OPENCODE.md                      # OpenCode workspace rules
├── .cursorrules                     # Cursor AI directives
└── README.md
```

---

## GD&T Symbol Support

The skill supports all 14 geometric characteristic symbols from **ASME Y14.5** and **ISO 1101**:

| Category | Symbols |
| :--- | :--- |
| Form | Straightness ⎯, Flatness ⏥, Circularity ⌯, Cylindricity ⌭ |
| Profile | Profile of a Line ⌒, Profile of a Surface ⌓ |
| Orientation | Perpendicularity ⊥, Parallelism ∥, Angularity ∠ |
| Location | Position ⌖, Concentricity ◎ |
| Runout | Circular Runout ↗, Total Runout ⌕ |

See the full reference with descriptions in [`skills/ctq-extraction/references/gdt_symbols.md`](./skills/ctq-extraction/references/gdt_symbols.md).

---

## Key Rules for Accurate Extraction

- **Verbatim tolerances** — `+0.05/-0.00` is never converted to `±0.05`
- **Exclude reference dimensions** — parenthesized values like `(120)` are skipped
- **Unlegible callouts** go into `unlegible_notes` with view and location context
- **Process chart rows** get `"bbox": null` (no coordinates for tabular documents)

---

## Related Standards

- [ASME Y14.5-2018](https://www.asme.org/codes-standards/find-codes-standards/y14-5-dimensioning-and-tolerancing) — Dimensioning and Tolerancing
- [ISO 1101:2017](https://www.iso.org/standard/66777.html) — Geometrical tolerancing
- [ISO 2768](https://www.iso.org/standard/4028.html) — General tolerances
- [agentskills.io specification](https://agentskills.io/specification) — Agent skill authoring standard

---

## Contributing

1. Fork this repository.
2. Update `skills/ctq-extraction/SKILL.md` — all platform symlinks update automatically.
3. Validate your changes: `python3 -m unittest discover -s scripts`
4. Submit a pull request.

---

## License

MIT
