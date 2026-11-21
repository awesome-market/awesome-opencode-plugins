# opencode-addins

[![skills.sh](https://skills.sh/b/BIMpraxis/opencode-addins)](https://skills.sh/BIMpraxis/opencode-addins)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> 🌐 **Idioma:** **Español** | [English](./README.en.md)

Skills, plugins y convenciones para [opencode](https://opencode.ai) que uso a diario para hacer ingeniería de verdad: pequeñas, fáciles de adaptar y componibles. Funcionan con cualquier modelo.

Están pensadas para instalarse, modificarse y hacerse tuyas. Si encuentras algo útil, cópialo y adáptalo sin miedo.

## Qué incluye

| Tipo   | Nombre                                                   | Para qué sirve                                                                                                                                                          | Dependencias                                    |
| ------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Skill  | [`aletheia`](./skills/aletheia/SKILL.md)                 | Para cuando no hay ideas: te ayuda a desbloquear, reenfocar o empezar desde el papel en blanco hasta lograr el efecto «¡guau, parece magia!» combinando técnicas de Wittgenstein, Shklovski, Duchamp, Eno y Derrida en un procedimiento inspirado en el círculo de quintas musical, adaptado a la creatividad para rearmonizar el proyecto. | ◐ `charla-socratica` · `verifica-fuentes`        |
| Skill  | [`charla-socratica`](./skills/charla-socratica/SKILL.md) | Dialoga al modo socrático —elenchus y mayéutica— para poner a prueba supuestos y destilar, rama a rama, la esencia de un plan o diseño hasta alcanzar conocimiento compartido. | ● Autónoma                                      |
| Skill  | [`cierra-ciclo`](./skills/cierra-ciclo/SKILL.md)         | Ejecuta el cierre de ciclo: actualiza PRD y `CONTEXT.md`, genera el handoff con `traspaso`, elimina los obsoletos y hace `git add -A`/commit/push verificado. | ◐ `lenguaje-ubicuo` · `traspaso`                |
| Skill  | [`hoja-de-ruta`](./skills/hoja-de-ruta/SKILL.md)         | Traduce el PRD/SPECS y el histórico de git en una hoja de ruta didáctica centrada en valor, con hitos, esfuerzo estimado y distinción entre MVP y más allá.            | ● Autónoma                                      |
| Skill  | [`lenguaje-ubicuo`](./skills/lenguaje-ubicuo/SKILL.md)   | Analiza `docs/`, PRD y `README.md` para extraer el lenguaje de dominio y mantener un `CONTEXT.md` coherente entre documentación y código.                             | ● Autónoma                                      |
| Skill  | [`optimiza-prompt`](./skills/optimiza-prompt/SKILL.md)   | Reescribe el prompt que le das en una versión optimizada: más clara y estructurada, con salvaguardas anti-error y sin perder ningún dato del original.                 | ● Autónoma                                      |
| Skill  | [`traspaso`](./skills/traspaso/SKILL.md)                 | Genera o retoma un handoff efímero intra-jornada (`handoff_YYYY-MM-DD_HH-mm.md`) para limpiar contexto y continuar sin pérdida entre sesiones.                         | ● Autónoma                                      |
| Skill  | [`verifica-fuentes`](./skills/verifica-fuentes/SKILL.md) | Obliga a investigar, triangular al menos dos fuentes independientes y citar antes de responder, evitando respuestas inventadas o desactualizadas.                        | ● Autónoma                                      |
| Plugin | [`zonalista`](./plugins/zonalista/LEEME.md)              | Vigila el consumo de tokens de la sesión —aviso al 90 % y acción en `session.idle`— y prepara un traspaso automático antes de agotar el contexto.                     | ◎ `traspaso`                                    |
| Agente | [`AGENTS.md`](./agents/AGENTS.md)                        | Convenciones globales para el agente: disciplina de trabajo (investigar antes de actuar, mini informe, aprobación previa de lo destructivo), delegación en subagentes, reglas de versiones y forma. | ● Autónoma                                      |

> **Leyenda — Dependencias:** `●` Autónoma — funciona al 100 % sin otras skills. `◐` Potenciada — autónoma, mejora si las skills indicadas están presentes (derivación opcional). `◎` Recomendada — autónoma, pero necesita la skill indicada para su propósito completo.

## Instalación

### Skills (vía skills.sh)

Las skills de este repo están listadas en **[skills.sh/bimpraxis/opencode-addins](https://skills.sh/bimpraxis/opencode-addins)**. Ten en cuenta que skills.sh solo distribuye las **skills**; el **plugin zonalista** y las **convenciones de `agents/AGENTS.md`** no aparecen ahí y requieren instalación manual (ver [Plugin zonalista](#plugin-zonalista) y [Convenciones globales del agente](#convenciones-globales-del-agente)).

```bash
npx skills add BIMpraxis/opencode-addins
```

El instalador te deja elegir qué skills llevar y a qué agentes instalarlas (opencode, Claude Code, Codex, Cursor y [muchos más](https://github.com/vercel-labs/skills#supported-agents)).

Para instalar una skill concreta:

```bash
npx skills add BIMpraxis/opencode-addins --skill traspaso
```

También puedes clonar el repo y copiar la carpeta de la skill a tu directorio de skills (por ejemplo `.opencode/skills/` o `~/.config/opencode/skills/`).

### Plugin zonalista

El plugin **no** se instala con `npx skills`. Es un plugin nativo de opencode. Consulta las instrucciones completas en [`plugins/zonalista/LEEME.md`](./plugins/zonalista/LEEME.md). En resumen:

1. Copia `zonalista.ts` y `zonalista.config.json` a tu carpeta de plugins:
   - Linux/macOS: `~/.config/opencode/plugins/`
   - Windows: `%USERPROFILE%\.config\opencode\plugins\`
2. Edita `model_thresholds` en `zonalista.config.json` con tus proveedores y modelos.
3. Reinicia opencode.

> Zonalista busca una skill de traspaso/handoff para ejecutar el relevo. La skill [`traspaso`](./skills/traspaso/SKILL.md) de este repo es la compañera recomendada.

### Convenciones globales del agente

[`agents/AGENTS.md`](./agents/AGENTS.md) reúne las reglas transversales que doy a opencode en cualquier repositorio. Se instala copiando el archivo a tu configuración global (opencode lo lee como `AGENTS.md`):

- Linux/macOS: `~/.config/opencode/AGENTS.md`
- Windows: `%USERPROFILE%\.config\opencode\AGENTS.md`

Si un proyecto tiene su propio `AGENTS.md`, sus reglas prevalecen sobre estas. Adáptalo a tu forma de trabajar: es un punto de partida, no un dogma.

## Estructura del repositorio

```
opencode-addins/
├── skills/                  # skills instalables con `npx skills add`
│   ├── aletheia/
│   ├── charla-socratica/
│   ├── cierra-ciclo/
│   ├── hoja-de-ruta/
│   ├── lenguaje-ubicuo/
│   ├── optimiza-prompt/
│   ├── traspaso/
│   └── verifica-fuentes/
├── agents/                  # convenciones globales del agente (instalación manual)
│   └── AGENTS.md
└── plugins/                 # plugins nativos de opencode (instalación manual)
    └── zonalista/
```

## Agradecimientos

Gran parte de la filosofía de este repo —skills pequeñas, componibles y centradas en ingeniería real en lugar de "vibe coding"— está inspirada en el trabajo de [Matt Pocock](https://github.com/mattpocock) y su repositorio [mattpocock/skills](https://github.com/mattpocock/skills). Si no lo conoces, échale un vistazo: es una de las mejores colecciones de skills para agentes que hay.

## Licencia

[MIT](./LICENSE). Úsalo, modifícalo y compártelo sin restricciones.
