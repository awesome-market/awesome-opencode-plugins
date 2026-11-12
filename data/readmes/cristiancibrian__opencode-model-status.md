# opencode-model-status

Plugin TUI para [OpenCode](https://opencode.ai) que muestra en el sidebar el estado en vivo de un modelo de OpenCode Go y su historial de los últimos 7 días, usando la API pública de [status.opencode.ai](https://status.opencode.ai).

Por defecto sigue a **DeepSeek V4.1 Flash** en el plan **Go**, pero el modelo y el plan se configuran con opciones.

> English: an OpenCode TUI plugin that puts the live status and 7-day history of an OpenCode Go model in the sidebar. Install with `opencode plugin add github:cristiancibrian/opencode-model-status`.

## Vista

```
Estado del modelo
DeepSeek V4.1 Flash
● Operando normal
▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌ 7 d
Go · 1.3 s · 173 tok/s · hace unos segundos
```

Al pasar el mouse por cada segmento de la barra aparece un tooltip con el día, el rango horario en **America/Tijuana**, el estado, el motivo del incidente y su duración.

## Requisitos

- OpenCode 2.x con soporte de plugins TUI.
- Acceso a `https://status.opencode.ai` (la API es pública, no requiere autenticación).

## Instalación

```sh
opencode plugin add github:cristiancibrian/opencode-model-status
```

Para fijar una versión:

```sh
opencode plugin add 'github:cristiancibrian/opencode-model-status#v1.0.0'
```

El comando agrega el paquete a la configuración global (`~/.config/opencode/opencode.json`) y OpenCode lo instala. Si el bloque no aparece en el sidebar, cierra y vuelve a abrir OpenCode.

> No agregues el paquete también a `cli.json`: el CLI carga automáticamente el export `./tui` de los plugins configurados en `opencode.json`. Si antes usabas una copia local en `cli.json`, quita esa entrada para no ver el bloque duplicado.

## Configuración

Los valores por defecto ya apuntan a DeepSeek V4.1 Flash en el plan Go. Para cambiar el modelo, el plan o el intervalo, reemplaza la entrada del paquete por la forma de objeto en tu configuración global:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "github:cristiancibrian/opencode-model-status",
      "options": {
        "plan": "go",
        "model": "deepseek-v4.1-flash",
        "label": "DeepSeek V4.1 Flash",
        "refreshSeconds": 60,
        "historyGroup": 2
      }
    }
  ]
}
```

### Opciones

| Opción | Default | Descripción |
| --- | --- | --- |
| `plan` | `go` | Plan que publica la API: `go`, `payg` o `free`. |
| `model` | `deepseek-v4.1-flash` | ID del modelo dentro del `breakdown` de la API. |
| `label` | `DeepSeek V4.1 Flash` | Nombre visible en el sidebar. |
| `planLabel` | nombre del plan | Etiqueta del plan en la línea de detalle. |
| `refreshSeconds` | `60` | Intervalo de consulta en segundos (mínimo 30). |
| `historyGroup` | `2` | Periodos de 3 h que agrupa cada segmento de la barra. Con `2` cada segmento resume 6 h. |

## Qué hace

- Consulta `https://status.opencode.ai/api/status` cada minuto, con timeout de 10 s.
- Pinta el estado actual con el color semántico del tema activo: operando, degradado, caído o sin datos.
- Dibuja el historial de 7 días como 56 periodos de 3 h, agrupados para que quepan en el sidebar.
- Guarda el último resultado en el storage del plugin, así que al arrancar muestra datos de inmediato aunque la red falle. Si la consulta falla, indica **Sin conexión**, el último estado conocido y hace cuánto se actualizó.
- Muestra TTFT y tokens por segundo cuando el modelo está operativo.
- Registra el comando **Actualizar estado de DeepSeek V4.1 Flash** en la paleta de comandos, con un toast según el resultado.

## Cómo funciona la API

El plugin lee tres partes de la respuesta:

- `components[]`: busca el componente cuyo `service` coincide con el plan. Dentro de su `breakdown[]` busca la entrada del modelo para obtener `status`, `reason` y `speed` (`ttft`, `tps`).
- `history[]`: cada entrada trae `models[plan][model]` con el estado del periodo de 3 h.
- `incidents[]`: busca incidentes que afecten al plan y al modelo, y calcula el traslape con cada periodo para mostrar el motivo y la duración.

No hay build ni dependencias nativas: OpenCode ejecuta el TSX directamente.

## Desarrollo local

```sh
git clone https://github.com/cristiancibrian/opencode-model-status
```

Agrega la ruta del checkout a `~/.config/opencode/opencode.json`:

```jsonc
{
  "plugins": ["./ruta/a/opencode-model-status"]
}
```

También puedes copiar el directorio a `~/.config/opencode/plugins/model-status/`; OpenCode descubre `index.ts` y `tui.tsx` en la raíz del plugin.

El paquete no declara scripts `build`, `prepare` ni `prepublishOnly` a propósito: además de innecesarios, hoy rompen la instalación de paquetes Git en `opencode plugin add` (`git dep preparation failed`).

## Desinstalar

```sh
opencode plugin remove github:cristiancibrian/opencode-model-status
```

O elimina la entrada correspondiente de `~/.config/opencode/opencode.json`.

## Licencia

[MIT](LICENSE)
