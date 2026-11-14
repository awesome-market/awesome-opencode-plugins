# Web Programming Final Project

A high-performance, visually stunning personal portfolio website for Gojo Satoru, built with Svelte 5 and SvelteKit.

## Features

- **Svelte 5**: Powered by the latest Svelte features and runes.
- **Tailwind CSS v4**: Using the modern utility-first CSS framework for rapid UI development.
- **i18n**: Integrated with Paraglide-js for multi-language support (English and Indonesian).
- **MDSveX**: Markdown support for articles and blog posts.
- **Testing**: Comprehensive testing suite with Vitest for unit tests and Playwright for E2E tests.

## Development

To recreate this project with the same configuration:

```sh
bun x sv create --template library --types ts --add prettier eslint vitest="usages:unit,component" playwright tailwindcss="plugins:typography,forms" sveltekit-adapter="adapter:auto" devtools-json mdsvex paraglide="languageTags:en,id" mcp="ide:opencode+setup:local" --install bun designer_web
```

Once dependencies are installed, start the development server:

```sh
bun run dev
```

## Building

To build the production version of the app:

```sh
bun run build
```

You can preview the production build with `bun run preview`.

## Testing

Run all tests:

```sh
bun test
```

Or run specific test suites:

```sh
bun run test:unit
bun run test:e2e
```
