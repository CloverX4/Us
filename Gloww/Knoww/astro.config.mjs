// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://cloverx4.github.io',
  base: '/Us/',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
  output: 'static',
});
