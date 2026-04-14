/**
 * Personal page data — anime shelf, interests, fun facts, photography.
 * Edit content here, the personal.astro page loops over these arrays.
 */
import type { AnimeCard, Interest, Photo } from './types';

// ── Anime shelf ──
// Drop cover art in src/data/anime/ and set the 'image' field to the filename.
// Leave image blank to show the 📺 placeholder.

export const animeShelf: AnimeCard[] = [
  { title: 'currently watching', note: 'add your current anime here!!', color: 'var(--color-coral)' },
  { title: 'all-time fav', note: 'that one anime that changed everything', color: 'var(--color-teal)' },
  { title: 'comfort rewatch', note: "the one you go back to when life's weird", color: 'var(--color-amber)' },
];

// ── Photography ──
// Option 1: Drop images in src/data/photography/ and use 'file'
// Option 2: Use 'url' for external/hosted images
// Caption is optional.

export const photography: Photo[] = [
  { url: 'https://picsum.photos/seed/about-knoww/700/500', caption: 'test shot one' },
  { url: 'https://picsum.photos/seed/til-knoww/600/400', caption: 'test shot two' },
  { url: 'https://picsum.photos/seed/product-knoww/600/400', caption: 'test shot three' },
  { url: 'https://picsum.photos/seed/personal-vibes/600/500' },
  { url: 'https://picsum.photos/seed/builds-knoww/700/400', caption: 'test shot five' },
  { url: 'https://picsum.photos/seed/talk-knoww/500/400' },
];

// ── Interests ──

export const interests: Interest[] = [
  { emoji: '🎵', label: 'music', vibe: 'eclectic taste' },
  { emoji: '☕', label: 'coffee', vibe: 'fuel for everything' },
  { emoji: '📚', label: 'reading', vibe: 'mostly non-fiction' },
  { emoji: '🎮', label: 'gaming', vibe: 'casual but competitive' },
  { emoji: '🌏', label: 'exploring', vibe: 'new food, new places' },
  { emoji: '💬', label: 'conversations', vibe: 'the deep kind' },
];

// ── Random facts ──

export const funFacts: string[] = [
  "i started GEP Pulse, an in-house company radio for music and office news because why not",
  "won 2nd place in a Techathon building a Graphical Password Authenticator as an NPM package",
  "i genuinely think the best ideas come from the most random conversations",
  "this entire website is my rebellion against making yet another boring portfolio",
];
