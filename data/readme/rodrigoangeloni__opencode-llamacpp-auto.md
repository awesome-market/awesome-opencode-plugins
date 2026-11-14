# opencode-llamacpp-auto · Zero-config llama.cpp provider for OpenCode

**OpenCode detects your local llama.cpp server, publishes the model it has loaded with its real context window and capabilities, and follows you when you switch models — no config edits, no restarts.**

<p align="center">
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white">
  <img alt="OpenCode v2" src="https://img.shields.io/badge/OpenCode-v2-111111?style=for-the-badge">
  <img alt="llama.cpp" src="https://img.shields.io/badge/llama.cpp-local-E86A2E?style=for-the-badge">
  <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

<p align="center">
  <a href="#english"><b>🇬🇧 English</b></a> · <a href="#español"><b>🇪🇸 Español</b></a>
</p>

---

## English

### 📋 Overview

OpenCode works with cloud providers out of the box, but a local `llama-server` normally needs a hand-written provider entry, a fixed `baseURL` and a hardcoded context size. This plugin removes that work: it looks for a running server, reads what the server actually reports, and registers the loaded model under the `llamacpp` provider.

Switch to another model or restart the server on another port and the provider follows within 15 seconds, keeping its entry in the model picker.

### ✨ Features

| | |
|---|---|
| 🔍 | **Automatic discovery** — probes `8080`, `9931`, `1234` and `8000`, and accepts an endpoint only when `/health` returns `ok`. |
| 🧠 | **Real context window** — uses `n_ctx` from `/props` instead of assuming a default. |
| 🖼️ | **Modalities from the loaded server** — `image` and `video` appear only when the server reports them. |
| 🛠️ | **Tool calling** — follows `chat_template_caps.supports_tool_calls`. |
| 🎚️ | **Reasoning variants** — one variant per `reasoning_effort_levels` entry, or `none` / `thinking` when the template only exposes `enable_thinking`. |
| 🔄 | **Live refresh** — re-discovers every 15 seconds, so changing models needs no restart. |
| 🧹 | **No dead entries** — removes the provider after 20 consecutive misses (about 5 minutes). |

### ⚙️ How it works

1. Every 15 seconds the plugin probes the candidate ports, or `LLAMACPP_BASE_URL` when set.
2. `/health` must return `ok`. While the server is not ready, the last known inventory is kept instead of flapping.
3. It reads `/props` and `/v1/models`, skips models tagged `embedding`, and builds each model definition.
4. The `llamacpp` provider is registered through `ctx.provider.transform` using `@opencode/ai/providers/openai-compatible`.
5. A fingerprint of the discovered state decides whether `ctx.provider.reload()` runs.

### 🧠 Model metadata

| Signal | Source | Used for |
|---|---|---|
| Loaded model | `GET /v1/models` | model IDs and inventory |
| Display name | `/props` → `model_alias` | model picker entry |
| Context window | `/props` → `default_generation_settings.n_ctx` | `limit.context` |
| Vision and video | `/props` → `modalities` | `capabilities.input` |
| Tool calling | `/props` → `chat_template_caps.supports_tool_calls` | `capabilities.tools` |
| Reasoning | `/props` → `chat_template_caps.reasoning_effort_levels` | model variants |

### 📁 Project structure

```text
opencode-llamacpp-auto/
├── index.ts        # discovery, provider transform and refresh loop
├── package.json    # package metadata and exports
├── README.md
├── LICENSE
└── .gitignore
```

### ▶️ Getting started

#### Requirements

- OpenCode v2.
- A `llama-server` build that exposes `/health`, `/props` and `/v1/models`.

**Verified with**

| Component | Version |
|---|---|
| OpenCode | `2.2.7` |
| llama.cpp `llama-server` | `0.9.0-dev`, build `b12323`, commit `93cf736a8` |
| `@opencode/plugin` | `^2.2.6` (declared dependency) |

#### Install

As a Git package:

```sh
opencode plugin add github:rodrigoangeloni/opencode-llamacpp-auto
```

As a local plugin directory, which OpenCode loads automatically without a `plugins` entry:

```sh
git clone https://github.com/rodrigoangeloni/opencode-llamacpp-auto.git ~/.config/opencode/plugins/llamacpp-auto
```

Use one of the two. A package entry and a local directory with the same plugin id register the plugin twice.

#### Usage

```sh
llama-server -m model.gguf --alias Qwen3.8-27B --ctx-size 131072 --port 8080 --jinja
```

Pick `llama.cpp (local)` in `/models`, or call it directly:

```sh
opencode run -m "llamacpp/Qwen3.8-27B" "hello"
opencode run -m "llamacpp/Qwen3.8-27B#thinking" "hello"
```

#### Configuration

No configuration is required.

| Variable | Default | Description |
|---|---|---|
| `LLAMACPP_BASE_URL` | auto-detect | Force a single endpoint, for example `http://127.0.0.1:8080`. |

### ⚠️ Limitations

- Only the models reported by the server are published; a `llama-server` process serves the model it has loaded.
- When the server reports no context window, `32768` is used. The output limit is the smaller of `32768` and the context window.
- Reasoning variants describe what the chat template accepts. The server still decides its default through its own flags.

### 👨‍💻 Author

Rodrigo Angeloni — [github.com/rodrigoangeloni](https://github.com/rodrigoangeloni)

### 📄 License

MIT — see [LICENSE](LICENSE).

---

## Español

### 📋 Descripción

OpenCode funciona con proveedores en la nube sin configuración, pero un `llama-server` local normalmente exige una entrada de proveedor escrita a mano, un `baseURL` fijo y un tamaño de contexto hardcodeado. Este plugin elimina ese trabajo: busca un servidor en ejecución, lee lo que el servidor realmente informa y registra el modelo cargado bajo el proveedor `llamacpp`.

Si cambiás de modelo o reiniciás el servidor en otro puerto, el proveedor también se actualiza en 15 segundos y conserva su entrada en el selector de modelos.

### ✨ Características

| | |
|---|---|
| 🔍 | **Detección automática** — prueba `8080`, `9931`, `1234` y `8000`, y acepta un endpoint solo cuando `/health` responde `ok`. |
| 🧠 | **Contexto real** — usa `n_ctx` de `/props` en lugar de asumir un valor por defecto. |
| 🖼️ | **Modalidades según el servidor** — `image` y `video` aparecen solo cuando el servidor las informa. |
| 🛠️ | **Tool calling** — respeta `chat_template_caps.supports_tool_calls`. |
| 🎚️ | **Variantes de razonamiento** — una variante por cada `reasoning_effort_levels`, o `none` / `thinking` cuando la plantilla solo expone `enable_thinking`. |
| 🔄 | **Refresco en vivo** — vuelve a detectar cada 15 segundos, así que cambiar de modelo no requiere reiniciar. |
| 🧹 | **Sin entradas muertas** — elimina el proveedor tras 20 fallos consecutivos (unos 5 minutos). |

### ⚙️ Cómo funciona

1. Cada 15 segundos el plugin prueba los puertos candidatos, o `LLAMACPP_BASE_URL` si está definido.
2. `/health` debe responder `ok`. Mientras el servidor no está listo, se conserva el último inventario conocido en lugar de parpadear.
3. Lee `/props` y `/v1/models`, descarta los modelos etiquetados como `embedding` y arma la definición de cada modelo.
4. Registra el proveedor `llamacpp` mediante `ctx.provider.transform` con `@opencode/ai/providers/openai-compatible`.
5. Una huella del estado detectado decide si se ejecuta `ctx.provider.reload()`.

### 🧠 Metadatos del modelo

| Señal | Origen | Se usa para |
|---|---|---|
| Modelo cargado | `GET /v1/models` | IDs e inventario |
| Nombre visible | `/props` → `model_alias` | entrada en el selector |
| Ventana de contexto | `/props` → `default_generation_settings.n_ctx` | `limit.context` |
| Visión y video | `/props` → `modalities` | `capabilities.input` |
| Tool calling | `/props` → `chat_template_caps.supports_tool_calls` | `capabilities.tools` |
| Razonamiento | `/props` → `chat_template_caps.reasoning_effort_levels` | variantes del modelo |

### 📁 Estructura del proyecto

```text
opencode-llamacpp-auto/
├── index.ts        # detección, transformación del proveedor y refresco
├── package.json    # metadatos del paquete y exports
├── README.md
├── LICENSE
└── .gitignore
```

### ▶️ Puesta en marcha

#### Requisitos

- OpenCode v2.
- Un build de `llama-server` que exponga `/health`, `/props` y `/v1/models`.

**Verificado con**

| Componente | Versión |
|---|---|
| OpenCode | `2.2.7` |
| llama.cpp `llama-server` | `0.9.0-dev`, build `b12323`, commit `93cf736a8` |
| `@opencode/plugin` | `^2.2.6` (dependencia declarada) |

#### Instalación

Como paquete Git:

```sh
opencode plugin add github:rodrigoangeloni/opencode-llamacpp-auto
```

Como directorio local, que OpenCode carga solo y sin entrada en `plugins`:

```sh
git clone https://github.com/rodrigoangeloni/opencode-llamacpp-auto.git ~/.config/opencode/plugins/llamacpp-auto
```

Usá una de las dos formas. Una entrada de paquete y un directorio local con el mismo id registran el plugin dos veces.

#### Uso

```sh
llama-server -m model.gguf --alias Qwen3.8-27B --ctx-size 131072 --port 8080 --jinja
```

Elegí `llama.cpp (local)` en `/models`, o llamalo directamente:

```sh
opencode run -m "llamacpp/Qwen3.8-27B" "hello"
opencode run -m "llamacpp/Qwen3.8-27B#thinking" "hello"
```

#### Configuración

No requiere configuración.

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `LLAMACPP_BASE_URL` | autodetección | Fuerza un único endpoint, por ejemplo `http://127.0.0.1:8080`. |

### ⚠️ Limitaciones

- Solo se publican los modelos que informa el servidor; un proceso `llama-server` sirve el modelo que tiene cargado.
- Si el servidor no informa contexto, se usa `32768`. El límite de salida es el menor entre `32768` y la ventana de contexto.
- Las variantes de razonamiento describen lo que acepta la plantilla. El servidor sigue decidiendo su valor por defecto con sus propios flags.

### 👨‍💻 Autor

Rodrigo Angeloni — [github.com/rodrigoangeloni](https://github.com/rodrigoangeloni)

### 📄 Licencia

MIT — ver [LICENSE](LICENSE).
