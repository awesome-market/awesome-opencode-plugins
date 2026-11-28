> **Crédito principal a [davidkimai](https://github.com/davidkimai):** este kit se basa en su trabajo [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapta ese trabajo para iniciar y organizar bóvedas de Obsidian con ayuda de una IA.

> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 3–19: Este índice
> - Líneas 21–22: Introducción
> - Líneas 23–28: Obsidian Genesis: tu bóveda, configurada por una IA
> - Líneas 29–40: Qué es cada cosa
> - Líneas 41–59: Empezar en tres pasos
> - Líneas 60–68: Qué recibís
> - Líneas 69–76: Uso diario
> - Líneas 77–95: Guías
> - Líneas 96–111: Qué hay en la carpeta
> - Líneas 112–117: Estado del proyecto
> - Líneas 118–121: Privacidad
> - Líneas 122–125: Licencia
> - Líneas 126–129: Comunidad y soporte
> - Líneas 130–133: Apoyar el proyecto
> - Líneas 134–136: Sobre el desarrollo

**Idioma:** Español · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

# Obsidian Genesis: tu bóveda, configurada por una IA

Obsidian Genesis es un kit gratuito para empezar a usar [Obsidian](https://obsidian.md) sin saber cómo funciona. Le das esta carpeta a una IA que pueda leer y escribir archivos, respondés unas preguntas simples y la IA arma tu bóveda: tu primer proyecto, un panel para entrar y un índice que mantiene al día. No necesitás programar.

Sirve para estudio, trabajo o cualquier proyecto personal. El kit está en español; este README y la guía de documentos también están en inglés, alemán y chino.

## Qué es cada cosa

| Término | Qué es |
|---|---|
| Bóveda | La carpeta de notas que abrís con Obsidian. |
| Ficha del proyecto | Una nota con el objetivo, los datos comprobados y las próximas acciones de un proyecto. |
| Panel | La página de inicio: tus proyectos y tareas pendientes. |
| Índice general | `INDICE.md`, el mapa de todos los archivos. La IA lo lee primero y lo mantiene actualizado. |
| Nodo | Una carpeta temática con su propio índice, por ejemplo «Resúmenes de materias». |

La IA trabaja con las reglas y guías del kit: pregunta antes de escribir, te explica dónde va a guardar cada cosa y comprueba los archivos al terminar.

## Empezar en tres pasos

1. **Descargá y descomprimí** el repositorio: Code → Download ZIP.
2. **Abrí la carpeta en una IA que pueda leer y escribir archivos.** Elegí la que contiene este README y `AI-INSTRUCTIONS.md`.
3. **Pegá este mensaje y respondé sus preguntas:**

   > Quiero que configures mi bóveda de Obsidian con este kit. Leé primero `INDICE.md`, después `00_CORE/atoms/00_vault-rules.md` y `AI-INSTRUCTIONS.md`. No conozco Obsidian: guiame con preguntas simples, de a una o dos por vez, y encargate de los archivos según mis respuestas. Antes de escribir, explicame dónde vas a guardar todo y qué vas a crear. Mantené el índice principal actualizado. Si no tenés acceso para hacerlo, decímelo.

| Usás | Cómo abrir el kit |
|---|---|
| Claude Code | Abrí la carpeta y usá el mensaje anterior o `/configurar`. |
| OpenCode | Abrí la carpeta y usá el mensaje anterior o `/configurar`. [Guía](DOCS/opencode.md). |
| ChatGPT | Carpeta local con herramientas de archivos o copia adjunta. [Guía](DOCS/chatgpt.md). |
| Otra IA | Dale acceso a la carpeta y usá el mismo mensaje. |

La IA pregunta qué querés organizar, qué notas conservar y cuál es el objetivo. Podés responder «todavía no sé» o «no tengo fecha»: la primera tarea puede elegirse después. Si adjuntás un ZIP en lugar de dar acceso a la carpeta, el [inicio rápido](DOCS/QUICKSTART.md) explica qué podés recibir.

Si ya tenés una bóveda, el kit no la adapta: usalo en una carpeta nueva. Adaptar bóvedas existentes será un repositorio separado, todavía no disponible.

## Qué recibís

- Una carpeta lista para abrir como bóveda, con tu primer proyecto y su ficha.
- El **Panel** (`Panel.md`) para entrar a tus proyectos y tareas, y **Leer primero** (`LEER_PRIMERO.md`), que conecta el Panel con el índice general.
- Una vista simple: el explorador muestra tus notas y oculta los archivos técnicos del kit. La **Vista de gráfico** de Obsidian, desde su icono lateral, muestra cómo se conectan.
- Un **inventario de personalización** opcional y plegado: lo que respondiste, lo pendiente y lo que elegiste saltar. Podés completarlo cuando quieras con **«qué falta para personalizar mi bóveda»**. [Cómo funciona](00_CORE/protocols/personalizar-vault.md).

Para abrirla, instalá Obsidian desde [obsidian.md](https://obsidian.md), abrí la carpeta preparada como bóveda y entrá a `Panel.md`. La IA verifica los archivos; cómo se ve en Obsidian lo comprobás vos.

## Uso diario

- **Retomar:** decí **«Seguí con [proyecto]»** o usá `/empezar`. La IA lee el índice, las reglas y la ficha, y sigue con lo pendiente.
- **Otros pedidos:** otro proyecto, un borrador, una revisión o guardar el cierre del día. [Pedidos listos para usar](DOCS/usar-con-otras-ias.md).
- **Organizar más contenido:** pedí **«Agregá un nodo para resúmenes de mis materias»**. La IA crea su índice y lo conecta al mapa general. [Cómo funcionan los nodos](DOCS/indice-principal.md).

Claude Code y OpenCode incluyen `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` y `/cerrar`; en Claude, crear otro proyecto y cerrar se invocan a mano. Los permisos dependen del asistente. Si trabajás con adjuntos, compartí siempre las notas vigentes: no se sincronizan solas.

## Guías

| Si querés… | Leé |
|---|---|
| Ver las formas de darle la carpeta a una IA | [Inicio rápido](DOCS/QUICKSTART.md) |
| Usar ChatGPT | [Empezar con ChatGPT](DOCS/chatgpt.md) |
| Usar OpenCode | [Empezar con OpenCode](DOCS/opencode.md) |
| Resolver la conexión de Claude con Obsidian (MCP) | [Si Claude no conecta con el MCP](DOCS/mcp-claude.md) |
| Conocer los pedidos de uso diario | [Trabajar con una IA](DOCS/usar-con-otras-ias.md) |
| Crear un proyecto sin IA | [Tu primer proyecto a mano](DOCS/primer-proyecto.md) |
| Entender el Panel, las plantillas y la vista simple | [Plantillas y panel](DOCS/obsidian.md) |
| Agregar nodos y entender el mapa general | [Mapa general e índices de nodos](DOCS/indice-principal.md) |
| Saber cómo se registran y comprueban los cambios | [Mantenimiento](DOCS/mantenimiento.md) |
| Usar las cinco skills opcionales | [Skills opcionales](DOCS/skills-portables.md) |
| Resolver un problema | [Solución de problemas](DOCS/TROUBLESHOOTING.md) |
| Ver qué hace cada archivo del kit | [Guía de documentos y herramientas](DOCS/README.md) |

**Para asistentes y para desarrollar el kit:** [entrada para la IA](AI-INSTRUCTIONS.md) · [reglas de la bóveda](00_CORE/atoms/00_vault-rules.md) · [protocolo de configuración](00_CORE/protocols/configurar-vault.md) · [creador de proyectos](DOCS/creacion-para-asistentes.md) · [cómo contribuir](CONTRIBUTING.md) · [prueba con usuarios](DOCS/prueba-con-usuarios.md) · [publicación](DOCS/publicacion.md) · [historial de cambios](CHANGELOG.md).

## Qué hay en la carpeta

| Lugar | Para qué |
|---|---|
| `Panel.md` | Acceso a proyectos y tareas |
| `LEER_PRIMERO.md` | Entrada para la persona y conexión de los nodos generales |
| `INDICE.md` | Catálogo de archivos y proyectos; primera lectura de la IA |
| `00_CORE/` | Reglas, fichas, plantillas y herramientas |
| `PROJECT_TEMPLATE/` | Carpetas de un proyecto: fuentes, borradores, entregables y archivo |
| `skills/` | Cinco skills opcionales |
| `DOCS/` | Guías |

El ejemplo `aprender-python` es ficticio y está separado de tus proyectos. Tus datos salen de tus respuestas; lo que no sepas puede quedar vacío.

Python 3.8 o posterior automatiza la creación, la validación y el índice con la biblioteca estándar. Sin Python, la IA usa sus herramientas de archivos.

## Estado del proyecto

Versión 1.0, la primera publicable. Funcionan la configuración conversacional con perfil reanudable, el creador de proyectos, los nodos e índices conectados, el registro de cambios y la validación. Las pruebas automáticas pasan en Windows, macOS y Ubuntu con Python 3.8 y 3.13; eso no acredita que el kit sea fácil de usar.

Se comprobaron la configuración y la reanudación con Claude Code, y la configuración con ChatGPT web. Faltan la reanudación en ChatGPT web y OpenCode, una prueba con cinco principiantes y la revisión visual final en Obsidian. El detalle está en el [historial de cambios](CHANGELOG.md).

## Privacidad

El kit guarda archivos locales y no instala sincronización. La IA procesa lo compartido según su servicio y configuración: dale solo el contexto necesario.

## Licencia

[MIT](LICENSE), con los créditos de davidkimai y Albert Mestre. Adaptación independiente de Context Engineering, sin afiliación al proyecto original.

## Comunidad y soporte

Para dudas, ideas y experiencias, usá las [discusiones de la comunidad](https://github.com/Albertmestre1256/obsidian-genesis/discussions). Si algo falla, abrí un [reporte de error](https://github.com/Albertmestre1256/obsidian-genesis/issues) con la plantilla «No me funciona» y un ejemplo ficticio pequeño. [Cómo contribuir](CONTRIBUTING.md).

## Apoyar el proyecto

Obsidian Genesis es gratuito y lo seguirá siendo. Si te resulta útil, podés apoyarlo en [Patreon](https://www.patreon.com/obsidiangenesis). Los aportes ayudan a dedicar tiempo a guías para principiantes, pruebas con personas reales, traducciones y soporte. Son opcionales: no desbloquean funciones y todo el kit sigue siendo público.

## Sobre el desarrollo

Albert Mestre desarrolla esta adaptación con contribuciones importantes de **OpenCode, Claude y Codex (OpenAI)**, que ayudaron a construir una parte sustancial del código y apoyaron la documentación y las pruebas. Se los reconoce aquí como herramientas de IA contribuidoras al proyecto. Las propuestas se revisan y los resultados se verifican antes de integrarlos; el uso de IA no sustituye las pruebas con personas ni acredita por sí solo que el kit sea fácil de usar.
