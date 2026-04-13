# src/pages/

Every file here becomes a URL. This is Astro's file-based routing.

## Route Map

| File | URL | What it is |
|------|-----|-----------|
| `index.astro` | `/Us/` | Landing page — hero + palette grid |
| `about.astro` | `/Us/about` | About Indira |
| `personal.astro` | `/Us/personal` | Personal stuff — anime, hobbies, photography |
| `lets-talk.astro` | `/Us/lets-talk` | Contact page |
| `til/index.astro` | `/Us/til` | TIL listing page |
| `til/[slug].astro` | `/Us/til/hello-world` | Individual TIL post |
| `product/index.astro` | `/Us/product` | Product thinking listing page |
| `product/[slug].astro` | `/Us/product/why-product` | Individual product post |
| `builds/index.astro` | `/Us/builds` | Builds showcase listing |
| `builds/[slug].astro` | `/Us/builds/floww` | Individual build post |

## How Dynamic Routes Work

`[slug].astro` files use Astro's `getStaticPaths()` to generate one page per MDX post:

```astro
---
export async function getStaticPaths() {
  const posts = await getCollection('til');
  return posts.map(post => ({
    params: { slug: post.id },
    props: { post },
  }));
}
---
```

The slug comes from the MDX filename (e.g., `hello-world.mdx` → slug is `hello-world`).

## Layouts

Pages wrap themselves in layouts from `src/layouts/`:
- **BaseLayout** — every page uses this (HTML shell, fonts, nav, cursor glow)
- **SectionLayout** — listing pages (index pages for til, product, builds)
- **PostLayout** — individual MDX posts
