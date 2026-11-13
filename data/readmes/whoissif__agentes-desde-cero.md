# Agentes desde cero

Curso online interactivo en español para aprender sistemas de agentes desde la
base: qué es un agente, cómo se le dan instrucciones, herramientas, permisos,
subagentes, skills, MCP, herramientas CLI en Python y cómo publicar una web app
en producción.

Pensado para quien ya usa ChatGPT, Claude, Gemini o un bot de Discord/Slack y
quiere dar el salto a agentes que leen archivos, ejecutan comandos y verifican su
propio trabajo. Nivel intermedio.

El recorrido de instalación usa **OpenCode Escritorio**: la app con interfaz
gráfica, sin terminal ni Node.js. Las herramientas se presentan como CLI: es la
forma normal de que un agente invoque código, y el curso explica lo mínimo para
usarlas.

Descargas oficiales de escritorio: <https://opencode.ai/v2/docs/#desktop>.

- **12 módulos**, **37 lecciones**, **19 herramientas CLI en Python** con tests
  de comportamiento y de contrato.
- Laboratorios ejecutables de verdad en el navegador con **Pyodide** (sin cuenta,
  sin API key, sin servidor).
- Progreso guardado en `localStorage` (sin login ni base de datos).
- Contenido como módulos TypeScript tipados: fácil de editar y versionar.
- Desplegable en **Vercel** con un repositorio de **GitHub**.

## Stack

| Pieza | Versión |
| --- | --- |
| Next.js (App Router) | 16.4.5 |
| React | 19.3.1 |
| TypeScript | 5.9.3 |
| Tailwind CSS | 4.3.4 |
| react-markdown + remark-gfm | 10.1.0 / 4.0.1 |
| highlight.js | 11.12.0 |
| Pyodide | 0.29.5 (CDN) |

## Empezar en local

Requisitos: **Node.js 20.9 o superior** y npm.

```bash
npm install
npm run dev
```

Abre <http://localhost:3000>.

Scripts disponibles:

| Comando | Qué hace |
| --- | --- |
| `npm run dev` | Servidor de desarrollo con recarga en caliente |
| `npm run build` | Compila el sitio para producción |
| `npm start` | Sirve la compilación de producción |
| `npm run typecheck` | Comprueba TypeScript sin emitir archivos |

## Estructura del proyecto

```
app/                     Rutas (App Router)
  page.tsx               Portada
  curso/                 Temario y navegación
  curso/[modulo]/        Índice del módulo
  curso/[modulo]/[leccion]/  Lección
  progreso/              Progreso, exportar e importar
  certificado/           Certificado imprimible
  recursos/              Chuletas y plantillas
components/              UI: lecciones, laboratorios, quiz, bloques
content/
  course.ts              Metadatos, fases, FAQ, audiencia
  types.ts               Contrato de bloques, módulos y herramientas
  tool-contracts.ts      Contrato CLI de las 19 herramientas
  index.ts               Registro ordenado de módulos
  modules/m01.ts…m12.ts  Contenido de cada módulo
lib/
  course.ts              Estadísticas y navegación
  tool-contract.ts       Tests genéricos del contrato CLI
  progress.ts            Estado persistido en localStorage
public/
  pyodide-worker.js      Python y contrato CLI en un Web Worker
  chuleta.md             Chuleta descargable
```

## Cómo editar el contenido

El contenido no es MDX: cada módulo es un objeto TypeScript tipado. Un módulo
tiene lecciones y cada lección una lista de bloques (`md`, `code`, `callout`,
`steps`, `quiz`, `checklist`, `python`, etc.). El contrato está en
`content/types.ts`.

Para añadir un módulo:

1. Crea `content/modules/mXX.ts` con `export default module`.
2. Impórtalo en `content/index.ts` y añádelo al array `modules`.
3. Comprueba los tipos con `npm run typecheck`.

Los módulos se ordenan por `number`, así que el orden del array no es crítico,
pero mantenlo legible. Cada herramienta incluye su función inicial, la solución,
los tests de comportamiento y un contrato CLI en `content/tool-contracts.ts`.

### Herramientas CLI

Cada bloque `python` es una herramienta que el agente invoca por shell:

```bash
python herramienta.py --help
python herramienta.py --json '{"texto": "..."}'
```

El alumno implementa la función de dominio; el arnés impone la interfaz. La
salida es JSON por stdout y los códigos son `0` éxito, `1` error interno, `2`
argumentos, `3` JSON inválido y `4` errores de datos.

`content/tool-contracts.ts` declara nombre del ejecutable, parámetros, una
muestra válida y, cuando aplica, una entrada que debe fallar con código 4.
`lib/tool-contract.ts` genera las comprobaciones genéricas (`--help`, JSON
inválido, parámetros ausentes, muestra válida, error de dominio).

`public/pyodide-worker.js` carga Pyodide desde el CDN oficial y ejecuta el código
del alumno, sus tests y los del contrato en un Web Worker aislado. Si una
ejecución tarda más de 25 segundos, el worker se termina para no bloquear la
pestaña. La descarga inicial del intérprete tiene un límite aparte de dos
minutos, para que una conexión lenta no se confunda con un bucle infinito.

Los tests de comportamiento se escriben como fragmentos de Python que usan
`assert` y se ejecutan después del código del alumno. Los del contrato usan
`__cli([...])`, que devuelve `code`, `stdout` y `stderr`.

## Marca y metadatos

Los datos globales del curso están en `content/course.ts`:

```ts
export const courseMeta = {
  title: "Agentes desde cero",
  // …
  url: "https://agentes-desde-cero.vercel.app",
  repo: "https://github.com/whoissif/agentes-desde-cero",
} as const;
```

Si publicas una instancia propia, cambia `title`, `url` y `repo`, y revisa los
metadatos de las páginas en `app/` (`metadata` de cada ruta) y el `sitemap`.

## Progreso y certificado

- El progreso vive en `localStorage` bajo la clave
  `agentes-desde-cero:progress:v1`.
- Se puede exportar e importar como JSON desde `/progreso`.
- El certificado se desbloquea al completar las 37 lecciones. El nombre es
  autodeclarado y el PDF se genera desde el navegador con la impresión del
  sistema.

No hay backend ni cuentas: nadie más ve el progreso.

## Despliegue

**Sitio publicado:** <https://agentes-desde-cero.vercel.app>

**Repositorio:** <https://github.com/whoissif/agentes-desde-cero>

Proyecto de Vercel: `whoissif27/agentes-desde-cero`, conectado al repositorio de
GitHub. Cada push a `main` lanza un despliegue de producción automático.

Antes de publicar, sigue la checklist de
[`docs/REVISION-LOCAL.md`](docs/REVISION-LOCAL.md). La guía paso a paso para
GitHub y Vercel está en [`docs/DEPLOY.md`](docs/DEPLOY.md).

### Despliegue por CLI (sin repositorio Git)

Este proyecto se publicó sin GitHub, con Vercel CLI:

```bash
npx --yes vercel@latest login
npx --yes vercel@latest link --yes --project agentes-desde-cero
npx --yes vercel@latest deploy --prod --yes
```

El archivo `.vercelignore` excluye `alumno/` y `.next/` del despliegue: el
trabajo de práctica no forma parte del sitio y Vercel reconstruye desde el
código fuente.

### Despliegue desde GitHub

1. Sube el proyecto a GitHub.
2. Importa el repositorio en Vercel.
3. Vercel detecta Next.js y ejecuta `npm run build`.
4. Actualiza `content/course.ts` con la URL final.

El sitio es completamente estático salvo la generación de páginas en build: no
necesita variables de entorno para funcionar.

## Accesibilidad y rendimiento

- Navegación por teclado y foco visible en los controles.
- Contraste alto sobre fondo oscuro y texto redimensionable.
- Pyodide se carga solo cuando el alumno pulsa «Ejecutar».
- Las páginas de lección son estáticas y se generan en build.

## Licencia

Uso educativo. Puedes adaptar el contenido y la marca para tu propia formación.
Si lo publicas, atribuye el origen y revisa las licencias de las dependencias.

## Enlaces

- Documentación de OpenCode V2: <https://opencode.ai/v2/docs/>
- Next.js: <https://nextjs.org/docs>
- Vercel: <https://vercel.com/docs>
- Pyodide: <https://pyodide.org>
