/** Shared type definitions for all data files. */

// ── Sections (Hero, PaletteGrid, FloatingNav) ──

export interface Section {
  id: string;
  title: string;
  subtitle: string;
  peek: string;
  icon: string;
  path: string;
  hex: string;
  cssColor: string;
  gradientDir: string;
  img: string;
  fade: number;
  bleedOrigin?: string;
  navColor: string;
}

// ── About page ──

export interface TimelineEntry {
  id: string;
  dateRange: string;
  title: string;
  summary: string;
  color: string;
  pun?: string;
  details?: TimelineDetail[];
}

export interface TimelineDetail {
  label: string;
  text: string;
  link?: { href: string; text: string };
}

export interface Skill {
  label: string;
  accent: string;
}

export interface Drive {
  emoji: string;
  text: string;
}

// ── Personal page ──

export interface AnimeCard {
  title: string;
  note: string;
  color: string;
}

export interface Interest {
  emoji: string;
  label: string;
  vibe: string;
}

export interface Photo {
  file: string;      // filename in src/data/photography/ (e.g. 'sunset.jpg')
  caption?: string;
}

// ── Contact ──

export interface SocialLink {
  label: string;
  url: string;
}
