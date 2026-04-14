/**
 * About page data — timeline, toolkit skills, and driving factors.
 * Edit content here, the about.astro page loops over these arrays.
 */
import type { TimelineEntry, Skill, Drive } from './types';

// ── Timeline ──

export const timeline: TimelineEntry[] = [
  {
    id: 'nitw',
    dateRange: '2019 – 2023',
    title: 'NIT Warangal',
    summary: "B.Tech in CSE. fell in love with databases, SQL, and somehow also photography. the most fun phase of my life, no contest.",
    color: 'var(--color-teal)',
    pun: "soo... i love trees. traversing them in code?? absolute dread.",
    details: [
      {
        label: 'databases & SQL',
        text: "first time i saw data aggregations work, i was gone. been in love with SQL ever since.",
      },
      {
        label: 'photography',
        text: "my phone storage has been crying ever since. don't even need a reason to go out and shoot. getting myself a real camera is still on the list though.",
        link: { href: 'personal/', text: 'see my shots →' },
      },
      {
        label: 'people skills',
        text: "realized i'm genuinely good with people. made friends for life, found my crowd, learned what matters beyond code.",
      },
    ],
  },
  {
    id: 'gep',
    dateRange: '2023 – present',
    title: 'GEP Worldwide',
    summary: "software engineer on enterprise analytics. migrations, AI systems, incident resolution, and a lot of learning at scale. but the real discovery?? i love the product side more than the code side.",
    color: 'var(--color-coral)',
    pun: "while i thought... claude code would help, manual debugging?? never left the scene.",
    details: [
      {
        label: 'DAX → SQL migration',
        text: "contributed to migrating the analytics engine from DAX to SQL across 180+ customers. wrote automation scripts for onboarding that cut down manual effort and delivery timelines big time.",
      },
      {
        label: 'AI-driven reporting (RAG)',
        text: "built a system where users could do 28+ visualization and data operations in plain english. charts, colors, aggregations, all of it. consultants loved using it on their excel data.",
      },
      {
        label: 'duplicate name detection',
        text: "built product rule changes for detecting duplicate document names across reports and dashboards. sounds simple?? it's not. the rule logic got wildly complex, edge cases on edge cases.",
      },
      {
        label: 'incident resolution',
        text: "resolved 70+ production incidents in 3 months. nothing teaches you a system faster than debugging it at 2am.",
      },
    ],
  },
  {
    id: 'next',
    dateRange: "what's next",
    title: 'the product pivot',
    summary: "exploring the intersection of engineering and product. i want to own decisions, design experiences, and build things people actually love. this site?? it's part of that journey.",
    color: 'var(--color-amber)',
  },
];

// ── Toolkit ──

export const toolkit: Skill[] = [
  { label: 'SQL', accent: 'var(--color-teal)' },
  { label: 'Python', accent: 'var(--color-amber)' },
  { label: 'C#/.NET', accent: 'var(--color-coral)' },
  { label: 'JavaScript', accent: 'var(--color-amber)' },
  { label: 'DAX', accent: 'var(--color-teal)' },
  { label: 'Azure', accent: 'var(--color-coral)' },
  { label: 'Power BI', accent: 'var(--color-amber)' },
  { label: 'RAG / LLMs', accent: 'var(--color-teal)' },
  { label: 'Git', accent: 'var(--color-coral)' },
  { label: 'Astro', accent: 'var(--color-amber)' },
  { label: 'Tailwind', accent: 'var(--color-teal)' },
  { label: 'GSAP', accent: 'var(--color-coral)' },
];

// ── What drives me ──

export const drives: Drive[] = [
  { emoji: '🎯', text: 'ownership over decisions' },
  { emoji: '🔄', text: 'user feedback loops' },
  { emoji: '🤝', text: 'collaboration > solo execution' },
  { emoji: '⚖️', text: 'work-life balance (non-negotiable!!)' },
  { emoji: '💭', text: 'thinking in systems and flows' },
  { emoji: '✨', text: 'making things people go "waaaww" about' },
];
