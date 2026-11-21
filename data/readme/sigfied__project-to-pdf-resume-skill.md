# Project To PDF Resume Skill

[English](README.md) | [简体中文](README.zh-CN.md)

An evidence-first Agent Skill for turning local project folders into technical resume material, LaTeX-based resume sources, and verified PDF resumes.

The Skill is designed for resume workflows where an agent must inspect code before writing, separate code-backed facts from user-confirmed outcomes, and avoid inventing metrics, ownership, production usage, or business impact.

This repository uses the standard Skill shape: an installable directory containing `SKILL.md` with YAML frontmatter, plus optional bundled reference files. It is not tied to one specific agent runtime.

## About

`project-to-pdf-resume` is a portable Agent Skill for building technical resumes from real project repositories. It guides an AI agent through a disciplined workflow: inspect the code first, identify the project type, collect evidence, ask the user only for missing outcomes, draft resume bullets, and produce a verified PDF when requested.

The Skill is useful when resume content must be grounded in source code rather than memory or guesswork. It treats architecture, implementation details, file evidence, and technical highlights as code-backed facts, while requiring user confirmation for production usage, ownership, scale, metrics, business value, and launch outcomes.

The final workflow is designed to produce:

- an evidence package with project indexes, file evidence indexes, project evidence cards, claim ledgers, outcome questions, and bullet candidates
- role-targeted resume bullets that separate verified facts from assumptions
- LaTeX-first resume source when PDF output is requested
- rendered PDF verification guidance for page count, spacing, overflow, and readability
- English and Simplified Chinese documentation for the full workflow

## What It Does

- Scans one or more local project folders.
- Detects the dominant project type before deep analysis.
- Extracts architecture, implementation details, technical highlights, and evidence files.
- Builds a Markdown + JSON evidence package: Markdown stores detailed evidence, while JSON stores metadata, document indexes, claim links, statuses, and readiness.
- Labels claims as `Code evidence`, `Reasonable inference`, or `Needs user confirmation`.
- Asks targeted questions about production usage, scale, responsibility, metrics, and outcomes.
- Drafts resume bullets from verified evidence.
- Prefers LaTeX for final PDF typesetting and requires rendered PDF verification.
- Includes compact LaTeX layout guidance for Chinese technical resumes and user-provided PDF/TEX layout samples.
- Includes matching Simplified Chinese documentation for each Skill document.

## Repository Layout

```text
.
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
└── skills/
    └── project-to-pdf-resume/
        ├── SKILL.md
        ├── SKILL.cn.md
        └── references/
            ├── workflow.md
            ├── workflow.cn.md
            ├── intake-and-scan.md
            ├── intake-and-scan.cn.md
            ├── evidence-package.md
            ├── evidence-package.cn.md
            ├── architecture-and-materials.md
            ├── architecture-and-materials.cn.md
            ├── interview-and-writing.md
            ├── interview-and-writing.cn.md
            ├── layout-reference.md
            ├── layout-reference.cn.md
            ├── pdf-production.md
            └── pdf-production.cn.md
```

The installable Skill is contained in `skills/project-to-pdf-resume/`. The repository-level README and license are intentionally kept outside the Skill folder so the Skill itself stays compact and portable.

The Skill folder intentionally contains no runtime-specific metadata such as Codex-only or OpenAI-only configuration. If an agent runtime supports optional metadata, add that in your own environment without changing the portable Skill core.

`SKILL.md` contains the required Skill frontmatter. Each bundled reference also starts with lightweight YAML metadata (`title`, `description`, `lang`, `version`) so agents can quickly decide whether to load it.

## Installation

Clone the repository:

```bash
git clone https://github.com/Sigfied/project-to-pdf-resume-skill.git
```

Copy the installable Skill folder into the skills directory used by your agent runtime:

```bash
mkdir -p /path/to/your/skills
cp -R project-to-pdf-resume-skill/skills/project-to-pdf-resume /path/to/your/skills/
```

If your agent supports loading Skills from a repository path, point it at:

```text
skills/project-to-pdf-resume
```

Start a new agent session, reload skills, or follow your runtime's discovery process so `SKILL.md` is indexed.

### Runtime Examples

Codex-style local install:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R project-to-pdf-resume-skill/skills/project-to-pdf-resume "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Other runtimes:

```bash
cp -R project-to-pdf-resume-skill/skills/project-to-pdf-resume <your-agent-skills-directory>/
```

Use the directory that contains `SKILL.md`; do not copy only the Markdown file, because the Skill depends on `references/`.

## Usage Examples

Ask your agent to use the Skill on one or more local folders:

```text
Use the project-to-pdf-resume skill to analyze these project folders and turn them into a backend resume PDF.
```

```text
Use this Skill to inspect the code first, ask me only for missing production outcomes, then draft resume bullets and produce a LaTeX PDF.
```

```text
Use the Chinese docs for this Skill and generate resume material in Simplified Chinese.
```

## Workflow Summary

1. Confirm project folders, target role, resume language, and desired outputs.
2. Identify the dominant project type from file extensions and manifests.
3. Read high-signal files based on the project type.
4. Build an evidence package before drafting claims.
5. Ask the user for missing outcomes and responsibility details.
6. Write target-role-specific resume bullets.
7. Prefer LaTeX for final PDF typesetting.
8. Compile or render the PDF and visually verify the output.

## Verification

Basic local checks:

```bash
ruby -ryaml -e 's=File.read("skills/project-to-pdf-resume/SKILL.md"); fm=s[/\A---\n(.*?)\n---\n/m,1]; y=YAML.safe_load(fm); abort("bad name") unless y["name"] =~ /\A[a-z0-9-]+\z/; abort("missing description") if y["description"].to_s.empty?; puts "ok"'
```

If you have the official Skill validation script and its dependencies installed, run:

```bash
python3 path/to/quick_validate.py skills/project-to-pdf-resume
```

Expected portable Skill files:

```bash
find skills/project-to-pdf-resume -maxdepth 3 -type f | sort
```

## Privacy And Accuracy Rules

- Do not put private project details into reusable Skill documentation.
- Do not infer business impact from code alone.
- Treat metrics, production usage, ownership, scale, and business value as user-confirmed facts.
- Keep uncertain claims in notes, not final resume bullets.
- Generalize confidential names, customers, internal systems, and sensitive metrics unless the user explicitly approves exact wording.

## Chinese Documentation

Each primary Skill document has a Simplified Chinese counterpart:

- `SKILL.md` -> `SKILL.cn.md`
- `workflow.md` -> `workflow.cn.md`
- `intake-and-scan.md` -> `intake-and-scan.cn.md`
- `evidence-package.md` -> `evidence-package.cn.md`
- `architecture-and-materials.md` -> `architecture-and-materials.cn.md`
- `interview-and-writing.md` -> `interview-and-writing.cn.md`
- `layout-reference.md` -> `layout-reference.cn.md`
- `pdf-production.md` -> `pdf-production.cn.md`

## License

MIT License. See [LICENSE](LICENSE).
