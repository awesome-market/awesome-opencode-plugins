# Content Series para OpenCode

Skill de [OpenCode](https://opencode.ai) que **genera, programa y publica una serie de 30 días para LinkedIn**. Funciona para cualquier carrera o tema: mecatrónica, derecho, marketing, datos, medicina, arquitectura, etc.

La idea es simple: describes tu perfil y tu tema, la skill arma el temario, escribe un post por día y —si quieres— lo publica automáticamente 3 horas después de generarlo.

## Características

- **Onboarding conversacional:** no editas JSON a mano; el agente te hace 5–6 preguntas y crea todo.
- **Cualquier tema:** el motor es genérico; el contenido sale de tu `config.json` + `temario.md`.
- **Verificación de recursos:** valida cada video de YouTube con el endpoint oEmbed (HTTP 200) antes de incluirlo.
- **Modo manual o automático:**
  - Manual: genera el `.md` listo para copiar y pegar en LinkedIn.
  - Automático: publica vía [Composio](https://composio.dev) 3 horas después.
- **Anti-duplicado:** no genera dos posts con la misma fecha.
- **Logs:** cada ejecución queda registrada.
- **Presets:** plantillas de ejemplo para empezar rápido (mecatrónica, derecho).

## Requisitos

| Requisito | ¿Obligatorio? |
|---|---|
| OpenCode | Sí |
| Un modelo con crédito | Sí |
| Windows (para el horario automático) | Solo si quieres programar |
| Composio + cuenta de LinkedIn | Solo para publicación automática |

## Instalación rápida (una línea)

Copia este bloque y pégalo en el chat de oc:

```text
Instálame la skill content-series y el comando /serie.

1. Agrega a mi configuración global de OpenCode (opencode.json):
"skills": ["https://hugoariza-mechatronics.github.io/linkedin-ai-automation-opencode/"]

2. Agrega este comando:
"commands": {
  "serie": {
    "description": "Crea una serie de contenido para LinkedIn",
    "template": "Carga la skill content-series y ejecuta su onboarding completo."
  }
}

3. Muéstrame qué archivos modificaste.
```

Después escribe:

```text
/serie
```

Y responde las preguntas. Listo.

> El catálogo HTTP requiere que el repo esté publicado con GitHub Pages. Si acabas de clonarlo, usa la instalación manual.

## Instalación manual (desde el repo)

```bash
git clone https://github.com/HugoAriza-mechatronics/linkedin-ai-automation-opencode
```

1. Copia `content-series/` a:
   - Proyecto: `.opencode/skills/content-series/`
   - Global: `~/.config/opencode/skills/content-series/`
2. Copia `.opencode/commands/serie.md` a tu proyecto (`.opencode/commands/`).
3. Escribe `/serie`.

## Cómo funciona

```
/serie
  └─ onboarding: preguntas → contenido/config.json + contenido/temario.md
  └─ copia scripts a automatizacion/

09:00  run-dia.ps1
         └─ genera contenido/posts/dia-NN-slug.md

+3 h   publicar-dia.ps1
         └─ lee el .md y publica vía Composio
```

La hora de publicación se calcula al generar: si la tarea corre a las 10:00, publica a las 13:00.

## Configuración

Todo vive en `contenido/config.json`:

| Campo | Ejemplo | Qué hace |
|---|---|---|
| `creator.name` | `"María Pérez"` | Nombre del autor |
| `creator.headline` | `"Abogada laboral"` | Contexto para el tono |
| `creator.audience` | `"reclutadores y colegas"` | A quién le habla |
| `series.title` | `"30 días de legal tech"` | Título de la serie |
| `series.language` | `"es"` | Idioma de los posts |
| `content.maxChars` | `1800` | Longitud máxima |
| `content.resourcesLanguage` | `"es"` o `"en"` | Idioma de los videos |
| `publish.mode` | `"manual"` o `"auto"` | Publicar solo o no |
| `publish.offsetHours` | `3` | Horas entre generar y publicar |
| `linkedin.authorUrn` | `"urn:li:person:..."` | Tu ID de LinkedIn |
| `schedule.generateAt` | `"09:00"` | Hora de generación |

Referencia completa: [`content-series/references/config-reference.md`](content-series/references/config-reference.md).

## Presets

| Preset | Tema |
|---|---|
| `profiles/_template` | Base vacía para cualquier carrera |
| `profiles/mecatronica` | Herramientas de ingeniería mecatrónica |
| `profiles/derecho` | Práctica legal y legal tech |

Copia el `config.json` y `temario.md` del preset a `contenido/` y edita los datos personales.

## Modo automático (Composio)

1. Crea una cuenta en [Composio](https://composio.dev).
2. Conecta LinkedIn.
3. Agrega el MCP:

```bash
opencode mcp add composio --global --url https://connect.composio.dev/mcp
```

4. Autentica desde `/mcps`.
5. En `config.json` pon `publish.mode: "auto"` y tu `authorUrn`.

Guía: [`docs/composio.md`](docs/composio.md).

## Seguridad

- **Nunca** publiques sin que el usuario lo pida. La skill pregunta **"¿Deseas publicar?"** salvo que ya lo haya pedido o esté dentro del flujo automático aprobado.
- El modo por defecto es **manual**.
- No se guardan credenciales en el repo ni en `config.json`.
- El `authorUrn` es un identificador público, no un secreto.

## Estructura del repo

```
.
├── index.json                     Catálogo para OpenCode
├── content-series/                La skill
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   ├── profiles/
│   └── examples/
├── .opencode/commands/serie.md    Comando /serie
├── docs/
└── opencode.example.json
```

## Limitaciones

- El scheduling usa **Programador de tareas de Windows**. En Linux/macOS necesitas cron o systemd.
- La publicación automática depende de Composio y de la API de LinkedIn.
- La generación consume una ejecución del modelo por día (dos en modo automático).
- LinkedIn puede cambiar sus límites o permisos en cualquier momento.

## Licencia

[MIT](LICENSE). Puedes usar, modificar y distribuir el proyecto manteniendo el aviso de copyright.
