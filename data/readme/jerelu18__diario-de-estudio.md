# 📓 Diario de Estudio — Spec-Driven Agentic Development
🔗 **Demo en vivo:** https://jerelu18.github.io/diario-de-estudio/

> Aplicación web *Zero-Dependencies* construida y mantenida mediante desarrollo asistido por agentes con **OpenCode**, gobernanza estricta (**Constitución y AGENTS.md**) y desarrollo guiado por especificaciones (**Spec-Driven Development**).

[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-blue.svg)]()
[![Pure JS](https://img.shields.io/badge/JavaScript-Vanilla%20ES6+-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-node%20--test-brightgreen.svg)]()
[![Architecture](https://img.shields.io/badge/governance-Spec--Driven-orange.svg)]()

---

## 🌟 Descripción General

**Diario de Estudio** es una aplicación web (SPA ligera) diseñada para registrar hábitos de estudio, calcular rachas de constancia, visualizar mapas de calor de actividad y gestionar metas semanales.

El proyecto destaca por dos pilares:
1. **Excelencia técnica minimalista**: Cero frameworks, cero empaquetadores y cero dependencias externas. Funciona de inmediato al abrir `index.html` en cualquier navegador.
2. **Ingeniería asistida por Inteligencia Artificial (OpenCode)**: Desarrollado aplicando un flujo estricto de agentes autónomos, especificaciones formales, memoria de proyecto y pruebas automatizadas.

---

## 🤖 Metodología y Uso de OpenCode

El desarrollo de este software no consistió en prompts aislados, sino en un proceso disciplinado de **Agentic Software Engineering**:

### 1. Gobernanza y Reglas del Sistema
- **`opencode.json`**: Configuración de entorno y herramientas MCP (*Model Context Protocol*), integrando `chrome-devtools-mcp` para inspección automatizada del DOM, consola y pruebas visuales móviles.
- **`docs/constitution.md`**: Constitución inmutable del proyecto con principios innegociables (simplicidad, especificación activa previa al código, lógica pura separada del DOM y pruebas obligatorias).
- **`AGENTS.md`**: Contexto maestro que define la arquitectura, límites operativos, convenciones de idioma y reglas de persistencia.
- **`.opencode/agents/`**: Configuración de subagentes especializados (por ejemplo, agentes revisores `reviewer.md` para auditorías de calidad).

### 2. Memoria del Proyecto (`MEMORY.md`)
- Registro evolutivo breve y conciso de cada versión del proyecto.
- Permite a los agentes mantener el contexto entre distintas sesiones de trabajo, documentar decisiones arquitectónicas y evitar regresiones.

### 3. Desarrollo Guiado por Especificaciones (Spec-Driven Development)
Cada funcionalidad compleja se desarrolló dentro del directorio `specs/` siguiendo un ciclo formal:
- **`spec.md`**: Requisitos funcionales (RF), requisitos no funcionales (RNF), casos límite y criterios de aceptación.
- **`plan.md`**: Decisiones de diseño y modelado de datos antes de programar.
- **`tasks.md`**: Desglose granular de tareas dependientes y condiciones de término.

**Especificaciones implementadas:**
- `specs/001-heat-map/`: Mapa de calor de 12 semanas (84 días).
- `specs/002-semanal-objetivo/`: Sistema de objetivo semanal con ventana móvil de 7 días.
### 4. Agentes y flujo SDD
| Agente | Rol |
| --- | --- |
| `coordinator` | Dirige el flujo y exige aprobación humana de spec y plan. No edita código. |
| `planner` | Redacta spec, plan y tareas. |
| `implementer` | Ejecuta una tarea por vez, con tests en verde. |
| `reviewer` | Hace QA de la spec y valida requisito por requisito. |

Comando `/feature`: planifica cambios pequeños sin tocar código hasta aprobar el plan.

---

## 🧠 Arquitectura y Lógica de Negocio

Toda la lógica de cálculo reside en funciones puras, desacopladas del DOM y de `localStorage`:

- **Manejo Estricto de Fechas Locales**: Formato uniforme `YYYY-MM-DD` sin conversiones a UTC ni `toISOString()` para evitar desajustes por zona horaria.
- **Racha Actual con Tolerancia Diaria (`calculateStreak`)**: Considera un día válido si tiene al menos una sesión. Si el usuario aún no ha estudiado hoy pero sí lo hizo ayer, la racha se mantiene activa.
- **Mejor Racha Histórica (`calculateBestStreak`)**: Análisis algorítmico sobre fechas únicas ordenadas cronológicamente para registrar el récord histórico del estudiante sin contar días futuros.
- **Objetivo Semanal y Ventana Móvil de 7 Días (`calcularMinutos7Dias`)**: Suma minutos estudiados en el rango `[hoy - 6 días, hoy]`.
- **Progreso y Metas (`calcularProgreso`)**: Cálculo porcentual con manejo de casos límite (meta 0 = 100% cumplido, sin meta = estado neutro).
- **Mapa de Calor de 84 Días (`get84DayRange`, `getColorLevel`)**: Generación de matriz visual de 12 semanas con 4 niveles de intensidad cromática.
- **Persistencia y Migración Retrocompatible**: Gestión defensiva en `localStorage` con sanitización de datos (XSS prevention vía `escapeHtml`).

---

## 📁 Estructura del Repositorio

```text
├── index.html            # Estructura semántica y contenedores accesibles
├── styles.css            # Diseño responsivo y variables CSS
├── app.js                # Lógica de negocio, controladores y DOM
├── AGENTS.md             # Instrucciones maestras de gobernanza para agentes
├── MEMORY.md             # Historial y memoria persistente del proyecto
├── opencode.json         # Configuración del entorno y MCPs de OpenCode
├── .gitignore            # Exclusiones de Git
├── docs/
│   └── constitution.md   # Principios inmutables del proyecto
├── specs/                # Especificaciones funcionales y planes técnicos
│   ├── 001-heat-map/
│   └── 002-semanal-objetivo/
└── tests/                # Suites de pruebas unitarias
    ├── heat_map.test.js
    └── objetivo-test.js
```

---

## 🧪 Pruebas Unitarias

El proyecto utiliza el corredor nativo de Node.js, sin requerir librerías externas (`jest`, `mocha`, etc.):

```bash
node --test
```

---

## 🚀 Cómo Ejecutar la Aplicación

1. **Directamente en el navegador**:
   Haz doble clic sobre `index.html` o ábrelo en cualquier navegador (Chrome, Edge, Firefox, Safari).

2. **Mediante un servidor local (opcional)**:
   ```bash
   # Con Python:
   python -m http.server 8000

   # O con npx:
   npx serve .
   ```
   Luego visita `http://localhost:8000`.

