/**
 * Personal page data — anime shelf, interests, fun facts, photography.
 * Edit content here, the personal.astro page loops over these arrays.
 */
import type { AnimeCard, Interest, Photo } from './types';

// ── Anime shelf ──

export const animeShelf: AnimeCard[] = [
  { title: 'currently watching', note: 'add your current anime here!!', color: 'var(--color-coral)' },
  { title: 'all-time fav', note: 'that one anime that changed everything', color: 'var(--color-teal)' },
  { title: 'comfort rewatch', note: "the one you go back to when life's weird", color: 'var(--color-amber)' },
];

// ── Photography ──
// Drop images in src/data/photography/ and add entries here.
// 'file' is just the filename — the component resolves the full path.

export const photography: Photo[] = [
  // { file: 'sunset.jpg', caption: 'golden hour never disappoints' },
  // { file: 'street.jpg', caption: 'random walk in the city' },
  // { file: 'food.jpg' },
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
