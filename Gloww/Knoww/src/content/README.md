# src/content/

MDX blog posts organized into three collections. Each folder = one collection.

## Collections

### `til/` — Today I Learned
Quick "aha moment" posts. Short, casual, frequent.

**Frontmatter:**
```yaml
title: "what you learned"          # required
pubDate: 2026-04-11                # required — YYYY-MM-DD
description: "one-line summary"    # required
tags: ["tag1", "tag2"]             # optional, defaults to []
emoji: "🧠"                        # optional, defaults to 🧠
draft: true                        # optional, defaults to false
```

### `product/` — Product Thinking
Thoughts, teardowns, and case studies about product stuff.

**Frontmatter:**
```yaml
title: "your title"                # required
pubDate: 2026-04-11                # required
description: "one-line hook"       # required
type: "thought"                    # required — "thought" | "teardown" | "case-study"
company: "Company Name"            # optional — for teardowns/case studies
tags: ["tag1"]                     # optional
coverImage: "/Us/images/cover.jpg" # optional
draft: false                       # optional
```

### `builds/` — Things I've Built
Project showcases — what, why, how, tech stack.

**Frontmatter:**
```yaml
title: "Project Name"              # required
description: "what it does"        # required
techStack: ["Python", "FastAPI"]   # required
github: "https://github.com/..."   # optional
liveUrl: "https://..."             # optional
status: "wip"                      # required — "active" | "wip" | "archived"
coverImage: "/Us/images/cover.jpg" # optional
featured: true                     # optional, defaults to false
draft: false                       # optional
```

## Adding a New Post

1. Copy the matching template from `src/templates/`
2. Paste into the right folder with a slug filename: `my-post-slug.mdx`
3. Fill in frontmatter + write content
4. Set `draft: false` to publish

The slug (filename without `.mdx`) becomes the URL:
- `til/hello-world.mdx` → `/Us/til/hello-world`
- `builds/floww.mdx` → `/Us/builds/floww`

## Schemas

All frontmatter is validated by `src/content.config.ts`. If you add a field that isn't in the schema, it gets ignored. If you miss a required field, the build fails with a clear error.
