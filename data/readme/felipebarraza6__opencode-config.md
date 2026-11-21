# ⚙️ Mi configuración de OpenCode

> 👋 ¡Hola! Bienvenido.
>
> Acá dejo mi setup personal de [OpenCode V2](https://opencode.ai): los agentes con los que trabajo, las reglas que me ordenan el día y los skills que me ahorran tiempo. Lo tengo público porque a mí me habría gustado encontrar algo así cuando empecé. Si te sirve, **cópialo, róbalo, méjoralo y hazlo tuyo** 🚀

---

## ✨ Qué hay adentro

| Archivo | Para qué sirve |
|---|---|
| `opencode.jsonc` | Modelo por defecto, permisos y los 5 agentes del equipo |
| `cli.json` | Tema y preferencias de la terminal |
| `dcp.jsonc` | Dynamic Context Pruning: menos tokens, misma memoria |
| `rules/` | Mis reglas globales: idioma y método de ingeniería |
| `skills/` | Skills propias del flujo de trabajo |
| `AGENTS.md` | Convenciones que todo agente debe respetar |
| `scripts/validate.sh` | Revisa que la config esté sana antes de commitear |

---

## 🚀 Cómo usarla

```sh
git clone https://github.com/felipebarraza6/opencode-config.git ~/.config/opencode
opencode auth login
opencode
```

Y listo 🎉 El plugin se instala solo en el primer arranque.

Si ya tienes una carpeta ahí:

```sh
mv ~/.config/opencode ~/.config/opencode.old
git clone https://github.com/felipebarraza6/opencode-config.git ~/.config/opencode
```

---

## 🤖 El equipo

Cinco agentes con roles separados, porque el que escribe el código no debería aprobarlo solo:

| Agente | Rol |
|---|---|
| 🧭 **orchestrator** | Entiende, planifica y define criterios de aceptación |
| 🔨 **builder** | Implementa el plan aprobado y escribe tests |
| ✅ **verifier** | Corre lint, tipos y tests. Solo reporta evidencia |
| 🔍 **reviewer** | Revisa el diff, seguridad y calidad |
| 🚢 **deployer** | Prepara el release. Nunca despliega sin un humano |

---

## 💸 Perfil de ahorro

Optimizado para sesiones largas sin que la cuenta llore:

| Agente | Modelo | USD in/out por millón |
|---|---|---|
| default / orchestrator / builder | `deepseek-v4.1-flash` | 0.15 / 0.60 |
| verifier / deployer | `mimo-v2.6-flash` | 0.14 / 0.28 |
| reviewer | `qwen3.8-flash` | 0.15 / 0.47 |

El truco no es solo el precio por token: es la **caché de lectura**. `deepseek-v4.1-flash` cobra $0.003 por millón en caché, contra $0.19 de otros modelos. En conversaciones largas, esa es la diferencia entre gastar poco y gastar de más.

¿Necesitas más músculo puntual? `/models` en la TUI y listo.

---

## 🗂️ Mis proyectos

Si llegaste hasta acá, pásate a mirar lo que estoy construyendo 👇

### 🌱 La base

| Proyecto | Qué es |
|---|---|
| **[Yggdra](https://github.com/felipebarraza6/yggdra-web)** | El backend transversal que sostiene todo lo demás. Portafolio vivo de las apps que corren sobre él. |
| **[Muninn](https://github.com/felipebarraza6/muninn)** | Agentes de IA especializados. Mi laboratorio de automatización. |

### 🏗️ Apps sobre Yggdra

| Proyecto | Qué es |
|---|---|
| **[Nxord](https://github.com/felipebarraza6/nxord)** | 💧 Gestión hídrica con telemetría en tiempo real. React 19 + Vite + Tailwind. |
| **[FRIG](https://github.com/felipebarraza6/frig)** | 🍽️ Punto de venta gastronómico multi-tenant, white-label. |
| **[HEIR](https://github.com/felipebarraza6/heir)** | 🩺 Agenda, pagos y agente conversacional para profesionales de la salud. |
| **[Forja](https://github.com/felipebarraza6/forja)** | 🏋️ Plataforma para personal trainers: venta de servicios y gestión de alumnos. |
| **[Gungir](https://github.com/felipebarraza6/gungir)** | 🛒 Comercio general: landing, cotizador y panel de administración. |

### 🌾 Territorio y comunidad

| Proyecto | Qué es |
|---|---|
| **[Proyecto 90](https://github.com/felipebarraza6/proyecto-90)** | 🎯 Landing, inscripción y panel del desafío de 90 días. |
| **[nxrd_apr](https://github.com/felipebarraza6/nxrd_apr)** | 🚰 Ciclo del agua potable rural: socio, medidor, lectura, tarifa y cobro. |
| **[Asociación Laja-Diguillín](https://github.com/felipebarraza6/asociacion-laja-diguillin)** | 🏛️ Sitio institucional de la asociación de municipalidades del territorio de riego. |

---

## 🧪 Antes de commitear

```sh
./scripts/validate.sh
```

Verifica que el JSONC parsee, que no queden campos V1 deprecated y que agentes y permisos estén completos.

---

## 📌 Notas

- Las credenciales **no** se versionan: cada equipo hace su propio `opencode auth login`.
- `service.json` se regenera solo en cada máquina.
- Los plugins rotos se fueron de vacaciones permanentes 🏖️

---

<p align="center">
  Hecho con café, terminal y demasiadas pestañas abiertas ☕💻
  <br /><br />
  <b>¿Te sirvió? Déjame una estrella ⭐ y pásate a ver mis proyectos.</b>
</p>
