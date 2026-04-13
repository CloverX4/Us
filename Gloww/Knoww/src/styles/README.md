# src/styles/

Global styles for the entire site.

## global.css

The one CSS file. Contains:

1. **Tailwind directives** — `@import "tailwindcss"` pulls in utility classes
2. **@font-face rules** — loads Clash Display and Satoshi from `public/fonts/`
3. **Base resets** — background color (cream `#FFF8F0`), text color (navy), smooth scrolling
4. **Typography plugin config** — prose styles for MDX content via `@tailwindcss/typography`

## Where Styles Live

Most styling is **not** in this file. It's in:
- **Tailwind classes** directly on HTML elements in `.astro` files
- **`<style>` blocks** inside individual components (scoped by default in Astro)
- **Inline styles** for dynamic/complex things (like the tile grid layout)
