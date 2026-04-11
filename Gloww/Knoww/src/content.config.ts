import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const til = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/til' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    description: z.string(),
    tags: z.array(z.string()).default([]),
    emoji: z.string().default('🧠'),
    draft: z.boolean().default(false),
  }),
});

const product = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/product' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    description: z.string(),
    type: z.enum(['teardown', 'case-study', 'thought']),
    company: z.string().optional(),
    tags: z.array(z.string()).default([]),
    coverImage: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

const builds = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/builds' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    techStack: z.array(z.string()),
    github: z.string().optional(),
    liveUrl: z.string().optional(),
    status: z.enum(['active', 'archived', 'wip']),
    coverImage: z.string().optional(),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

export const collections = { til, product, builds };
