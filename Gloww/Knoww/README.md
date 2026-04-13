# Knoww

Indira's personal capsule website — not a portfolio, not a blog, just *her* corner of the internet.

**Live:** [cloverx4.github.io/Us/](https://cloverx4.github.io/Us/)

---

## Quick Start (new machine)

### Prerequisites
- **Node.js 22+** — check with `node -v`
- **Git** — check with `git -v`
- **nvm** (recommended) — to manage Node versions

### Clone & Run

```bash
# clone the repo
git clone git@github.com:CloverX4/Us.git
cd Us/Gloww/Knoww

# install dependencies
npm install

# start dev server
npm run dev
# opens at http://localhost:4321/Us/
```

### Commands

| Command | What it does |
|---------|-------------|
| `npm run dev` | Local dev server at `localhost:4321` |
| `npm run build` | Production build to `./dist/` |
| `npm run preview` | Preview the production build locally |

---

## Tech Stack

| Tech | Role |
|------|------|
| [Astro v6](https://astro.build) | Static site generator — pages are `.astro` files |
| [Tailwind CSS v4](https://tailwindcss.com) | Utility-first styling |
| [MDX](https://mdxjs.com) | Blog posts as markdown files with component support |
| [GSAP](https://gsap.com) | Animations — scroll reveals, hover effects, page transitions |
| [Three.js](https://threejs.org) | Particle background on hero (desktop only) |

### Fonts (self-hosted)
- **Clash Display** — headings (bold, personality)
- **Satoshi** — body text (clean, readable)
- Files live in `public/fonts/`, loaded via `@font-face` in `src/styles/global.css`

### Color Palette

| Name | Hex | Where |
|------|-----|-------|
| Cream | `#FFF8F0` | Background |
| Navy | `#1A1A2E` | Text |
| Coral | `#FF6B6B` | Primary accent |
| Amber | `#FFB347` | Warm accent |
| Teal | `#4ECDC4` | Pop/surprise |
| Peach | `#F7E8D4` | Cards, subtle bg |

---

## Project Structure

```
Knoww/
├── astro.config.mjs        # Astro config (site URL, base path, plugins)
├── package.json             # Dependencies and scripts
├── public/
│   └── fonts/               # Clash Display + Satoshi woff2 files
├── src/
│   ├── components/          # Reusable UI pieces (see src/components/README.md)
│   ├── content/             # MDX blog posts (see src/content/README.md)
│   ├── content.config.ts    # Collection schemas (defines frontmatter fields)
│   ├── layouts/             # Page shells (see src/layouts/README.md)
│   ├── pages/               # Routes — each file = a URL (see src/pages/README.md)
│   ├── scripts/             # Client-side JS (not currently used — logic is inline)
│   ├── styles/
│   │   └── global.css       # Tailwind directives, @font-face, base resets
│   └── templates/           # MDX post templates (see src/templates/README.md)
└── .github/
    └── workflows/           # GitHub Actions — auto-deploys on push to main
```

---

## How Deployment Works

1. Push to `main` branch
2. GitHub Actions runs `npm run build` inside `Gloww/Knoww/`
3. Built files deploy to GitHub Pages
4. Live at `cloverx4.github.io/Us/`

No manual deploy needed — just push.

---

## How to Add a New Post

1. Pick a collection: `til/`, `product/`, or `builds/`
2. Copy the matching template from `src/templates/`
3. Paste it into `src/content/<collection>/your-slug.mdx`
4. Fill in the frontmatter and write your content
5. Set `draft: false` when ready to publish
6. Push to main — it's live

See `src/content/README.md` and `src/templates/README.md` for details.

---

## Making Changes

### Edit existing pages
Pages live in `src/pages/`. Each `.astro` file maps to a URL:
- `src/pages/index.astro` → `/Us/`
- `src/pages/about.astro` → `/Us/about`
- `src/pages/til/index.astro` → `/Us/til`

### Edit components
Reusable pieces live in `src/components/`. The landing page tiles, nav, footer, cursor glow — all here.

### Edit styles
Global styles in `src/styles/global.css`. Most styling is Tailwind classes directly in `.astro` files.

### Push changes
```bash
git add -A
git commit -m "describe what you changed"
git push origin main
# deployed automatically
```
