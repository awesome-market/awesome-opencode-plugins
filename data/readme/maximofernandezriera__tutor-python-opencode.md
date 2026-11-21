# Tutor de Python para OpenCode

Tutor socrático para alumnos que empiezan a programar en Python con el libro
[*Think Python*, 3.ª edición](https://allendowney.github.io/ThinkPython/) (Allen Downey).
Funciona dentro de [OpenCode](https://opencode.ai), en el terminal.

- Da **pistas por niveles** (idea → pasos → ejemplo paralelo) y **nunca la solución completa**,
  aunque el alumno insista («es por curiosidad», «tengo prisa», «el profe me deja»...).
- Durante un **examen** no da ni respuestas ni pistas.
- No usa nada que el alumno no haya visto todavía (por ejemplo, nada de `return` antes del capítulo 6).
- Puede **leer** los archivos `.py` del alumno, pero no puede editarlos, crear archivos ni ejecutar comandos.
- Responde en español o en catalán, según escriba el alumno.

## Instalación rápida (Linux y macOS)

Abre un terminal y pega:

```bash
curl -fsSL https://raw.githubusercontent.com/maximofernandezriera/tutor-python-opencode/main/instalar.sh | bash
```

Después cierra el terminal, ábrelo de nuevo y escribe:

```bash
cd carpeta-de-tus-ejercicios
opencode
```

No hace falta cuenta ni clave: usa un modelo gratuito de OpenCode.

## Documentación

| Para | Documento |
|---|---|
| Alumnos: instalar, usar y problemas frecuentes | [docs/ALUMNOS.md](docs/ALUMNOS.md) |
| Profesores: qué instala, cambiar el modelo, personalizar | [docs/PROFESORES.md](docs/PROFESORES.md) |
| Mensajes de prueba antes de usarlo en clase | [docs/PRUEBAS.md](docs/PRUEBAS.md) |

## Contenido del repositorio

```text
skills/tutor-python/SKILL.md   instrucciones del tutor (skill de OpenCode)
instalar.sh                    instala OpenCode, la skill y el agente "tutor"
desinstalar.sh                 quita la skill y el agente
tests/comprobar.sh             comprueba que la instalación es correcta
docs/                          guías para alumnos y profesores
```

## Licencia

[CC BY 4.0](LICENSE). Puedes usarlo y adaptarlo citando la fuente.
