# src/layouts/

Page shells that wrap content. Think of them as nested frames.

## Layout Hierarchy

```
BaseLayout.astro          ← every page uses this
├── SectionLayout.astro   ← listing/index pages (til, product, builds)
└── PostLayout.astro      ← individual MDX posts
```

### BaseLayout.astro
The outermost shell. Provides:
- `<html>`, `<head>`, `<body>` tags
- Font loading, meta tags
- Floating nav (FloatingNav component)
- Cursor glow effect (CursorGlow component)
- Page transition animation (PageTransition component)
- `<slot />` where page content goes

### SectionLayout.astro
Wraps section index pages (e.g., `/Us/til`). Adds:
- Section heading with animation
- Back-to-grid link
- Consistent spacing/layout

### PostLayout.astro
Wraps individual MDX posts. Adds:
- Post title, date, tags
- Typography styles for prose content (`@tailwindcss/typography`)
- Back link to the section index
