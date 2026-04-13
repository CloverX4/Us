# src/components/

Reusable UI pieces, organized by where they're used.

## Folder Map

```
components/
├── landing/          # Landing page (index.astro) only
│   ├── Hero.astro          # Full-screen hero — heading, bokeh particles, parallax, palette grid
│   ├── PaletteGrid.astro   # The interactive tile grid (THE main navigation feature)
│   ├── PaletteTile.astro   # Individual tile — gradient bg, icon, title, subtitle
│   └── ScrollCue.astro     # "scroll to explore" hint at bottom of hero
│
├── nav/              # Navigation across all pages
│   ├── FloatingNav.astro   # Expanding dot nav (bottom-right corner)
│   └── BackToGrid.astro    # "back" link on inner pages → returns to landing grid
│
├── shared/           # Used across multiple pages
│   ├── Card.astro           # Post listing card (used on TIL, Product, Builds index pages)
│   ├── CursorGlow.astro     # Warm radial glow that follows the cursor (desktop)
│   ├── Footer.astro         # Site footer
│   ├── PageTransition.astro # GSAP fade-up on page enter
│   └── SectionHeading.astro # Animated heading for section pages
│
├── about/            # About page components (empty — planned: Timeline.astro)
├── contact/          # Let's Talk page components (empty — planned: ContactCard.astro)
└── personal/         # Personal page components (empty — planned: AnimeShelf, InterestGrid)
```

## How Components Work in Astro

`.astro` files have two parts separated by `---`:
```astro
---
// server-side JS (runs at build time)
const { title } = Astro.props;
---
<!-- HTML template (rendered to static HTML) -->
<h1>{title}</h1>

<style>
  /* scoped CSS — only affects this component */
</style>

<script>
  /* client-side JS — runs in the browser */
</script>
```

## Key Patterns in This Project

- **Animations** are mostly in `<script>` tags using GSAP, not in separate `.ts` files
- **Styles** mix Tailwind classes (in the HTML) with `<style>` blocks for complex things
- **No framework components** (React/Vue/etc) — everything is plain Astro + vanilla JS
