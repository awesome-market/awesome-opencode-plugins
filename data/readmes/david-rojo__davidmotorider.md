# 🏍️ 🌍 DavidMotoRider

[![Deploy to GitHub Pages](https://github.com/david-rojo/davidmotorider/actions/workflows/deploy.yml/badge.svg)](https://github.com/david-rojo/davidmotorider/actions/workflows/deploy.yml)
[![CI](https://github.com/david-rojo/davidmotorider/actions/workflows/ci.yaml/badge.svg)](https://github.com/david-rojo/davidmotorider/actions/workflows/ci.yaml)
[![Lighthouse](https://github.com/david-rojo/davidmotorider/actions/workflows/lighthouse.yml/badge.svg)](https://github.com/david-rojo/davidmotorider/actions/workflows/lighthouse.yml)
[![Astro](https://img.shields.io/badge/Astro-7.x-BC52EE?logo=astro&logoColor=white)](https://astro.build/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.x-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

Web personal sobre viajes en moto trail, recursos y rutas desde Madrid.

Sitio publicado: <https://davidmotorider.com/>

## 🗺️ Sobre El Proyecto

DavidMotoRider es una web personal en español dedicada a viajes en moto, rutas trail, recursos prácticos y preparación de aventuras.

El contenido principal gira en torno a:

- Viajes en moto
- Rutas desde Madrid
- Destinos nacionales como Picos de Europa
- Destinos internacionales como Marruecos, Transpirenaica
- Equipamiento trail
- BMW F850GS

## ⚙️ Stack

- Astro 7.
- Tailwind CSS 4.
- TypeScript.
- Markdown/MDX para contenido.
- GitHub Pages con salida estática (Node.js `>=22.23.4`).

## 📁 Estructura Principal

- `src/pages/index.astro`: portada.
- `src/pages/viajes`: listado y detalle de viajes.
- `src/pages/recursos`: listado y detalle de recursos.
- `src/pages/donde-dormir`: recomendaciones de alojamiento.
- `src/pages/sobre-mi`: página personal.
- `src/content/trips`: contenido de viajes.
- `src/content/resources`: contenido de recursos.
- `public/images`: imágenes públicas del sitio.

## 🧰 Desarrollo

Instalar dependencias:

```bash
npm ci
```

Arrancar entorno local:

```bash
npm run dev
```

Verificar el proyecto:

```bash
npm run check
```

Generar build estático:

```bash
npm run build
```

Previsualizar el build:

```bash
npm run preview
```

## ✅ Calidad

La verificación completa ejecuta:

- `astro check`.
- `eslint .`.
- `prettier --check .`.

Para aplicar arreglos automáticos:

```bash
npm run fix
```

## 🤖 Desarrollo Asistido Por IA

Este proyecto se desarrolla con apoyo de herramientas de inteligencia artificial como OpenCode y OpenAI para acelerar tareas de análisis, implementación, documentación y revisión.

Las decisiones de producto, contenido, diseño y publicación se revisan manualmente para mantener la coherencia con el objetivo de DavidMotoRider: una web personal, útil y cuidada sobre viajes en moto trail.

## 🚀 Despliegue

El proyecto está configurado para GitHub Pages con dominio propio en `astro.config.ts`:

- `site: https://davidmotorider.com`.
- `base: /`.
- `output: static`.

La publicación se realiza mediante GitHub Actions al hacer push a `main`.

## 🔗 Nota Sobre Rutas

Usar `import.meta.env.BASE_URL` o utilidades internas para rutas y assets, manteniendo compatibilidad con la configuración de Astro.
