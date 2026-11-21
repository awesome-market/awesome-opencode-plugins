# OpenspecApp

Guía interactiva de OpenSpec construida **con OpenSpec** (dogfooding). App Angular que documenta el flujo spec-driven usando el mismo flujo spec-driven para crearse.

## Stack

| Capa | Tecnología |
|------|-----------|
| Framework | Angular v22 |
| Lenguaje | TypeScript v6 |
| Testing | Vitest v4 |
| Metodología | OpenSpec spec-driven |
| AI assistant | OpenCode AI + MCP Angular CLI |

## Workflow OpenSpec

El proyecto sigue el ciclo spec-driven. Los comandos disponibles via OpenCode AI:

| Comando | Propósito |
|---------|-----------|
| `/opsx:explore` | Explorar ideas, investigar problemas, clarificar requisitos |
| `/opsx:propose` | Crear propuesta completa con diseño, especs y tareas |
| `/opsx:apply` | Implementar tareas de un change |
| `/opsx:sync` | Sincronizar delta specs a main specs |
| `/opsx:update` | Revisar artefactos de planificación |
| `/opsx:archive` | Archivar un change completado |

Ciclo típico: **explore → propose → apply → sync → archive**

## Estructura del proyecto

```
openspec-app/
├── openspec/           # Artefactos OpenSpec
│   ├── config.yaml     # Configuración del proyecto
│   ├── specs/          # 11 specs principales
│   └── changes/        # Changes activos y archive
├── .opencode/          # Config OpenCode AI + skills
│   ├── commands/       # Comandos opsx
│   └── skills/         # 6 skills openspec-*
├── .agents/skills/     # 8 skills auxiliares
├── src/
│   └── app/
│       ├── components/
│       │   ├── section/    # hero, concept, flow, commands, pros-cons, cta
│       │   └── shared/     # header, footer, card, terminal
│       ├── interfaces/
│       ├── layouts/
│       ├── pages/          # Páginas (lazy-loaded)
│       ├── services/
│       ├── data/           # Datos estáticos JSON
│       └── utils/          # Theme toggle, utilidades
```

## Comandos

```bash
ng serve        # Servidor de desarrollo
ng test         # Tests unitarios (Vitest)
ng build        # Build producción
```

## Skills instaladas

**Desarrollo (.agents/skills/):** Angular developer, Frontend Design, Vitest, TypeScript advanced types, adev-writing-guide, reference-core, reference-compiler-cli, reference-signal-forms

**OpenSpec (.opencode/skills/):** openspec-propose, openspec-apply-change, openspec-sync-specs, openspec-update-change, openspec-archive-change, openspec-explore
