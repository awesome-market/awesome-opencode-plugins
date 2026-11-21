# Horizon modding skill

**Version:** 0.1.0

An Agent Skill for building mods for **Horizon** — Minecraft: Java Edition 26.3 rewritten in Rust
(`https://playhorizon.dev`, source at `github.com/horizon-rust/horizon`).

It covers both mod kinds end to end — scaffolding, the data formats, the Rust hook-point API,
testing, packaging, the registry — and porting existing Fabric / Forge / NeoForge / Quilt mods to
Horizon.

## Install

### Universal Agent Prompt (Works with ANY AI Agent or IDE)

Copy and paste this prompt into your AI agent's chat (Claude Code, Antigravity, Cursor, Windsurf, Roo Code, Cline, Copilot, or Aider):

```text
Install and activate the `horizon-modding` skill from GitHub:
Repository: https://github.com/amandeepintl/horizon-modding.git

Instructions:
1. If you have shell execution tools:
   - Determine your active workspace or platform skill directory (e.g., `skills/horizon-modding`, `.claude/skills/horizon-modding`, `.gemini/config/skills/horizon-modding`, or `.cursor/skills/horizon-modding`).
   - Clone the repository:
     git clone https://github.com/amandeepintl/horizon-modding.git <destination>
     (If it already exists, run `git pull` inside it).
2. If you do not have shell tools but have file writing tools:
   - Create a `skills/horizon-modding` directory in this workspace and download or reference `SKILL.md` and `references/` from https://raw.githubusercontent.com/amandeepintl/horizon-modding/main/SKILL.md.
3. Once available, read `SKILL.md` to load the Horizon modding knowledge base. Confirm when ready to build native (.hnmod) or content (.hmod) mods, or port Java Minecraft mods.
```

### For System Prompts, Custom Instructions, or IDE Rules (`.cursorrules`, `CLAUDE.md`, `.windsurfrules`)

If you want an agent to always have this capability without re-installing:

```markdown
## Horizon Modding Skill
You have access to the Horizon modding knowledge base from https://github.com/amandeepintl/horizon-modding.
When building Horizon mods or porting Minecraft Java mods:
- Consult `SKILL.md` for task routing (native vs. content modding, porting workflow).
- Native mods (`.hnmod`): Rust helpers, hook points, thin helpers delegating to module functions.
- Content mods (`.hmod`): Data-only blocks, items, recipes, tags in singular 1.21 format.
- Porting: Inspect JARs with `node scripts/inspect-jar.js`, evaluate mixins method-by-method, never invent APIs.
```

### Direct Terminal Commands

**macOS / Linux:**
```sh
mkdir -p skills && git clone https://github.com/amandeepintl/horizon-modding.git skills/horizon-modding
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path skills | Out-Null; git clone https://github.com/amandeepintl/horizon-modding.git skills/horizon-modding
```

The skill is just files — `SKILL.md` plus `references/`, `assets/` and `scripts/`. Nothing to build.

## Layout

```
horizon-modding/
├── SKILL.md                      entry point: pick a kind, environment, rules, verify, publish
├── SOURCES.md                    provenance ledger: every page ingested, what it fed, what is
│                                 inferred rather than sourced, contradictions on record
├── references/
│   ├── content-mods.md           .hmod — manifest, blocks, items, states, shapes, signs, pipes,
│   │                             components, tabs, mob effects, entity types, menus, tags,
│   │                             structures, biome modifiers, namespaces, limits
│   ├── native-mods.md            .hnmod — bundle, horizon-mixin.toml, compatibility.json,
│   │                             pinning, crates, data files, post-build, packaging
│   ├── hook-points.md            how hook points and helpers work, which `hooks` level to ask for,
│   │                             and the complete Playtime worked example
│   ├── hook-catalog.md           generated: all 386 hook points + 113 helpers with contract, side,
│   │                             API level and the exact Rust signature, plus 98 host methods
│   │                             (JSON beside it)
│   ├── horizon-architecture.md   crates, the game loop, the three runtime paths and their seams,
│   │                             where a mod attaches and in what order, parity tooling
│   ├── trait-mods.md             the `impl Hooks` shape: `[api]` package, events, dispatch,
│   │                             hosts, own injections, mod dependencies, attachments, tests
│   ├── java-modding.md           reading a Java mod: six parts, Fabric/Quilt/Forge/NeoForge,
│   │                             vanilla concepts, bytecode limits, what never maps
│   ├── troubleshooting.md        symptom → cause → fix for content, bundle, trait and port failures
│   ├── examples/
│   │   ├── native-block-interaction.md   block + interaction, the content/native split
│   │   ├── port-fabric-mod.md            a small Fabric mod end to end, with the seam checklist
│   │   ├── analyse-mixin-mod.md          turning 293 @Mixin classes into a decision per injection
│   │   └── debug-broken-mod.md           six planted defects and the order to find them in
│   ├── java-to-horizon.json      Java → Horizon mapping: 19 feature families, content files, hooks,
│   │                             complexity, differences, what is not portable
│   ├── porting.md                Java → Horizon: the one command, verdicts, class/tier table,
│   │                             carry rules, the 1.21.1→26.3 upgrade table, the Java→Horizon
│   │                             API mapping, licence policy
│   ├── testing.md                unit tests, the check matrix, in-game checklists, failure decoding
│   ├── publishing.md             versioning, packaging, minisign, submission, review, updates
│   ├── registry.md               index.json schema 1, entry fields, .hpack, registry CI
│   └── pitfalls.md               contradictions between site/repo/code, traps, known gaps
├── assets/
│   ├── content-mod/              a working content-mod template (__MOD_ID__ placeholders)
│   └── native-mod/               the Playtime bundle from the docs, complete
├── scripts/
│   ├── scaffold.sh               copy a template, rename it, make placeholder textures
│   ├── inspect-jar.js            static analysis of a Java mod jar: loader, MC version, census,
│   │                             bytecode, verdict estimate — no Java, no network, no decompiler
│   ├── plan-port.js              jar → feature inventory → compatibility plan + hooks needed
│   ├── fetch-hooks.js            regenerate the hook catalog from the Horizon source
│   ├── port-java-mod.sh          port a Java mod: inspect it, carry it, report the verdict
│   └── lib/                      zip reader/writer + Java class-file and bytecode reader
└── tests/
    ├── run-tests.sh              the acceptance suite
    ├── build-fixtures.js         writes the fixture jars (real zips, no Java needed)
    ├── build-java-fixture.js     compiles a real mod with javac and jars it
    ├── skill-eval.md             four tasks that score the skill itself, with pass/fail criteria
    └── fixtures/                 fabric / fabric-with-bytecode / neoforge / 1.16 / code-only / bad
```

## Scaffold

```sh
./scripts/scaffold.sh content my_mod "My Mod"          # -> ./my_mod
./scripts/scaffold.sh native  my_mod "My Mod"          # -> ./my_mod
./scripts/scaffold.sh content my_mod "My Mod" /tmp/x   # -> /tmp/x
```

Content mods get 16×16 placeholder textures if `python3` is available. Replace the templates with
real art before publishing.

## Port

```sh
./scripts/port-java-mod.sh ~/Downloads/some_mod.jar        # -> ./ports/some_mod/
```

Finds `horizon-port-pack` on `PATH`, or through `HORIZON_SRC=/path/to/horizon`, or in `./horizon`,
and tells you the three other ways to get it if none of those exist. Output: `carry/` (a loadable
content mod) and `check.json` (the verdict). If `node` is present it inspects the jar first, so you see
the loader and Minecraft version before the port rather than after it.

## Inspect a jar

```sh
node scripts/inspect-jar.js ~/Downloads/some_mod.jar          # human summary
node scripts/inspect-jar.js ~/Downloads/some_mod.jar --json   # for a script
```

Reads the zip directly — no Java, no `unzip`, no network. Prints the detected loader, the Minecraft
version, the licence, a census of blocks/items/recipes/mixins/access wideners, a verdict estimate, and
a bytecode summary: class count, methods, reference edges, top packages, supertypes, `@Mixin` classes
and registration calls.

The bytecode reader is `scripts/lib/classfile.js`, in plain Node: constant pool, fields, methods,
hierarchy, annotations, `Code` attribute decoding and invokedynamic resolution. It reads the metadata
`javap` prints — names, descriptors, edges — and never reconstructs source.

## Plan a port

```sh
node scripts/plan-port.js ~/Downloads/some_mod.jar --out out/
```

Writes `out/port-plan.md` and `out/port-plan.json`: every feature family found with its evidence, a
status per feature (`FULLY PORTED` / `PARTIALLY PORTED` / `NOT SUPPORTED`), the hooks the port needs
with their real signatures, and the `hooks` level to declare. Every hook is resolved against the
generated catalog — an id that does not exist is a hard error, not a skipped row.

## Provenance

Compiled on **2026-11-03** from:

- `https://playhorizon.dev/docs/` — `make-a-mod`, `mod-manifest`, `mod-code`, `content-mods`,
  `test-a-mod`, `publish-a-mod`, `mods`, `modpacks`, `agents`, `apis`, `api`, `api/stability`,
  `api/mod-index`, `api/data-formats`, `install`, `settings`, `how-horizon-is-built`, `faq`, and the
  sitemap for reachability.
- `github.com/horizon-rust/horizon/docs/` — `mods.md`, `native-mods.md`, `api/mod-index.md`.
- `github.com/horizon-rust/horizon-mods` — `README.md`, `native/` layout.
- `github.com/horizon-rust/horizon` at `main`, read as **source** rather than docs — `native-hooks.json`
  and `crates/horizon-client/src/game/native_hooks.rs` (`NATIVE_HOOKS_API = 359`, 386 hook points,
  113 helpers), and `mod_api.rs` for the trait-mod surface. `references/hook-catalog.md` is generated
  from the first two.

Horizon ships several times a day. `references/pitfalls.md` records every place the sources disagree
and how to resolve it; prefer the source at a pinned commit over all of this.
