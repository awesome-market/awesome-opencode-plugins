# receipt-organizer

English | [中文](README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Any%20agent%20with%20vision-blue)](#)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

> Turn a messy folder of receipt photos into a tidy Excel ledger — automatically.

A portable AI-agent skill that **reads handwritten receipts with vision**, **rotates and deskews them**, and embeds each photo back into a formatted Excel sheet with a running total. No OCR SaaS, no per-scan fee, no API key.

![Demo: generated Excel with embedded receipt images](assets/screenshot.png)

## ✨ Features

- **📝 Handwriting recognition** — reads handwritten amounts, dates, and item descriptions directly from phone photos (Chinese receipts, invoices, delivery notes, till slips). No pre-trained OCR model needed.
- **🔄 Auto-orientation & deskew** — detects vertical phone shots, rotates them upright, and fine-tunes tilted angles. A preview-then-confirm step guarantees nothing ends up upside-down in your spreadsheet.
- **📂 Batch processing** — point it at a folder with dozens or hundreds of photos; it walks through them one by one, extracts the three fields you care about (item, date, amount), and cross-checks uppercase vs. lowercase amounts.
- **📊 Ready-to-use Excel** — outputs a formatted `.xlsx` with item / date / amount columns, the original receipt photo embedded on each row, and an auto-summed total. Drop it straight into expense reporting, class-fund accounting, or small-business bookkeeping.

Works with any agent that has vision (to read the photos), shell access (to run Python), and file read/write — Claude Code, Codex, Cursor, Doubao, Workbuddy, DeepSeek, or your own agent loop.

## When would you use this?

- **Class / club treasurer** — collecting reimbursement receipts from parents or members and need a clean ledger with proof attached
- **Small-business owner** — dumping shoebox photos of supplier receipts into a monthly expense sheet
- **Personal expense tracking** — turning months of WeChat / Alipay paper slips into a searchable spreadsheet
- **Travel / project accounting** — tripping receipts into a report-ready Excel before reimbursement deadline

## Quick start

Just say to your agent:

> "Organize all the receipts in `D:\receipts\2026-10` into an Excel sheet"

or in Chinese:

> "整理一下 `D:\receipts\2026-10` 这个文件夹里的收据，做成 Excel"

The agent walks through the standard flow: scan folder → vision OCR → orientation preview → build xlsx → deliver.

## Install

Drop this folder wherever your agent loads user skills from (e.g. `.user_skills/receipt-organizer/`). Any agent that reads a `SKILL.md` frontmatter will pick it up. If your agent doesn't have a skills directory, just keep the two scripts handy — the agent can read `SKILL.md` as a plain instruction file:

```
receipt-organizer/
├── SKILL.md
└── scripts/
    ├── rotate_preview.py
    └── build_receipt_xlsx.py
```

On first run the agent will create a local `.venv` and install `openpyxl` + `Pillow` automatically.

## Requirements

- Python 3.10+
- `openpyxl`, `Pillow` (auto-installed into a local venv on first run)
- Optional: `pillow-heif` if your photos are HEIC

## How it works

```
photos/*.jpg
    │
    ▼
[agent] reads each photo with vision
    │  extracts item / date / amount
    │  guesses rotation (90/180/270 + small deskew)
    ▼
rotate_preview.py  ──►  preview/*.jpg
    │
    ▼
[agent] visually confirms each preview is upright
    │  adjusts rotation if needed
    ▼
build_receipt_xlsx.py  ──►  receipts.xlsx
    (rotates + embeds each photo, sums amounts)
```

The preview step is the key design choice: PIL's rotation direction is easy to get backwards, so we never embed based on intuition — every rotated photo is eyeballed first.

## Configuration

Both scripts take a small JSON config. See the header comments in:

- [`scripts/rotate_preview.py`](scripts/rotate_preview.py) — orientation preview
- [`scripts/build_receipt_xlsx.py`](scripts/build_receipt_xlsx.py) — final Excel build

## Keywords

receipt scanner, receipt OCR, expense tracker, invoice parser, receipt-to-excel, handwritten receipt, Chinese receipt, reimbursement, bookkeeping, class fund, petty cash, Claude Code skill, agent skill, Doubao skill, AI OCR, vision OCR, receipt organizer

## License

[MIT](LICENSE)
