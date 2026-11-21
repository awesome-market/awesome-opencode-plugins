# opencode-peek

**Vista rápida de los archivos que el asistente menciona en sus respuestas**, para [OpenCode](https://opencode.ai) v2 (TUI).

Basado en el plugin **Quick Peek** de [better-claude](https://github.com/midudev/better-claude), de [midudev](https://github.com/midudev) — mismo concepto, adaptado a la API de plugins TUI de OpenCode. Créditos del diseño original a él.

## Qué hace

Cuando el asistente responde mencionando archivos (`src/app.ts`, `docs/nota.md`, una imagen…), este plugin te deja **previsualizarlos sin salir del chat**: un selector de dos paneles con la lista de archivos a la izquierda y una vista previa en vivo a la derecha, más un preview grande con acciones sobre el archivo.

```
┌ Vista rápida — 7 archivos en la última respuesta ────────────────┐
│ ▸ test/peek-core.test.ts │ peek-core.ts                          │
│   texto · 3.1 KB · 2 h   │ texto · 6.9 KB · hace 2 min           │
│   src/peek.tsx           │                                      │
│   texto · 14 KB · 2 min  │   1│ // Núcleo puro de opencode-peek… │
│   README.md              │   2│ import fs from "node:fs"         │
│   /tmp/muestra.png       │   3│ …                                │
│                          │ ┌────────┐ ← imágenes inline          │
│                          │ └────────┘                            │
│ ↑↓/jk navegar · hover previsualiza · click/⏎ abre · Esc cerrar  │
└──────────────────────────────────────────────────────────────────┘
```

## Diferencia con el original de Claude Code

El plugin de midudev en Claude Code funciona **pasando el mouse por encima de una ruta en la conversación**: aparece un preview flotante junto al puntero y un click la abre en Finder.

**Eso no es posible en OpenCode**: la API de plugins TUI (v2) no expone eventos de mouse sobre el transcript — los mensajes los renderiza el host y un plugin no puede intervenirlos. Lo más parecido que la API permite es capturar el mouse dentro de una UI propia.

Este plugin adapta el concepto a lo que OpenCode sí soporta:

| Quick Peek (Claude Code) | opencode-peek (OpenCode) |
| --- | --- |
| Hover sobre la ruta en el chat | **Hover sobre la fila del selector** — el preview cambia en vivo al lado |
| Preview flotante junto al puntero | Panel de preview junto a la lista + preview grande |
| Click abre en Finder | Click o `⏎` abre el preview con acciones: abrir, revelar, copiar |

## Cómo se usa

### Comandos

| Comando | Qué hace |
| --- | --- |
| `/peek` | Abre el **selector** con los archivos de la última respuesta del asistente que mencione rutas |
| `/vista` | Alias en español de `/peek` |
| `/peek <ruta>` | Preview directo de una ruta (`/peek src/app.ts`) |
| `/peek <n>` | Preview de la n-ésima ruta de la respuesta (`1` = la última mencionada) |
| `alt+p` | Preview del **último** archivo mencionado, sin escribir nada |

Si la última respuesta no menciona archivos, `/peek` retrocede por las respuestas anteriores del asistente (hasta 15) hasta encontrar rutas — el título del selector te dice de cuál viene (`…en una respuesta anterior (−2)`). También está en la paleta de comandos (`Ctrl+P` → "Vista rápida").

### En el selector

- `↑↓` o `j`/`k` — navegar; el panel derecho muestra el preview del archivo marcado
- **Pasar el mouse** por las filas — mismo efecto, en vivo
- **Rueda del mouse** — mueve la selección
- **Click** en una fila o `⏎` — abre el preview grande
- `Esc` — cierra

### En el preview grande

- `o` — abrir el archivo con la aplicación asociada del sistema (`xdg-open`)
- `r` — revelarlo **seleccionado** en el gestor de archivos (DBus `ShowItems`; fallback: abrir la carpeta)
- `c` — copiar la ruta al portapapeles (`wl-copy` / `xclip` / `xsel`)
- `Esc` — **volver al selector** conservando tu posición, si viniste de él; si no, cierra
- Los botones del pie (`[o] abrir`, `[r] revelar`, `[c] copiar ruta`) también responden al mouse

Así podés explorar varios archivos en cadena: `⏎` → mirás → `Esc` → volvés al selector → `⏎` en otro → … y cuando encontrás el que buscabas, `o` lo abre y cierra todo.

### Imágenes

Los formatos comunes (`png`, `jpg`, `webp`, `gif`, …) se muestran inline:

- El **preview grande** usa Kitty graphics o Sixel si tu terminal los soporta (Konsole/yakuake ≥ 21.12, kitty, ghostty, wezterm…), con fallback automático a bloques Unicode.
- El **panel lateral** del selector usa siempre bloques Unicode — portátil y sin artefactos dentro del layout de dos paneles.

### Qué se detecta

Rutas absolutas (`/etc/hostname`), relativas al proyecto (`src/app.ts`), con `~` (`~/.config/opencode/…`), nombres con extensión (`README.md`), dentro de backticks o con puntuación pegada. Se filtran URLs, rutas inexistentes y directorios. En la lista, la **última mencionada queda primera**; la descripción de cada fila muestra tipo · tamaño · antigüedad.

## Instalación

### Desde npm (cuando esté publicado)

```sh
opencode plugin add @pistonex/opencode-peek
```

### Desde este repo (GitHub)

```sh
opencode plugin add github:pistonex/opencode-peek
```

### Local (desarrollo)

```sh
git clone https://github.com/pistonex/opencode-peek.git
ln -s "$(pwd)/opencode-peek" ~/.config/opencode/plugins/opencode-peek
```

El entry `tui.ts` de la raíz es el que descubre la TUI de OpenCode; la implementación vive en `src/peek.tsx`. **Tras cambiar el código, reiniciá OpenCode** — el hot-reload de plugins TUI no siempre toma.

Requiere OpenCode ≥ 2.0 y Linux (las acciones `abrir`/`revelar` usan `xdg-open` y DBus; el resto funciona en cualquier plataforma).

## Desarrollo

```sh
npm install
npm run typecheck   # tsc --noEmit
bun test            # tests del núcleo puro (extracción de rutas y metadatos)
```

- `src/peek-core.ts` — núcleo puro: extracción de rutas del texto, metadatos de archivos, formato en español. Sin dependencias de la TUI.
- `src/peek.tsx` — plugin TUI: comandos, diálogos, keymap, acciones.
- `src/virtual-modules.d.ts` — tipos de los módulos virtuales del host (evita duplicar el runtime de Solid; ver comentario del archivo).
- `docs/RESEARCH.md` — investigación de la API de OpenCode v2 y las lecciones duras de la implementación. **Lectura recomendada antes de tocar `src/peek.tsx`.**

## Licencia

MIT © Tony Pistone

Diseño original de Quick Peek: [better-claude](https://github.com/midudev/better-claude), MIT © Miguel Ángel Durán ([midudev](https://github.com/midudev)). Este port no está afiliado a midudev ni a Anthropic.
