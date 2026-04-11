# 📅 2-Month DSA Mastery Plan (v2 — Adaptive)

> **Start Date**: March 4, 2026
> **End Date**: May 24, 2026 (10 weeks + honest buffer for real-life pacing)
> **Daily Commitment**: 1.5–2.5 hours (flex up on weekends)
> **Language**: Python
> **Goal**: Top MNC-ready (Google, Meta, Amazon, Apple) with deep intuition + interview hardness

---

## 🧬 What Changed From v1 (and Why)

| Area | v1 (Old) | v2 (This Plan) | Why |
|------|----------|-----------------|-----|
| Topic pacing | Rigid 7 days each | **Adaptive**: 4-day min, extend for hard topics | Sliding Window ≠ DP in difficulty — treat them differently |
| DP allocation | 6 days | **12 days (2 full weeks)** | DP is the #1 interview topic at Google/Meta. 6 days is suicide |
| Hard problems | Almost none until Week 8 | **1 Hard every 2 weeks from Week 3** | You need to see Hard-level tricks early so they don't shock you |
| Pattern mixing | Only during mocks | **🃏 Wild Card Wednesday** every week | Real interviews don't label the pattern — train for that |
| Long/ambiguous statements | Never | **📜 Scenario Problem** weekly from Week 3 | Amazon loves these. Google loves follow-ups. You need this skill |
| Mocks | 3 total | **6 total** (Weeks 3, 4, 5, 6, 8, 9) | More reps = less interview anxiety |
| Greedy/Intervals/Bits | Full week | **Compressed to 4 days** | These are lighter; DP needs the stolen time |
| Timeline | 8 weeks + 1 buffer | **8 weeks + 2 week buffer/extension** | Realistic for Google-tier; no cramming |

---

## 📈 Phase Overview

| Phase | Weeks | Focus | Goal |
|-------|-------|-------|------|
| **Foundation** | 1–2 | Arrays, Hashing, Two Pointers, Sliding Window | Build confidence, nail the basics |
| **Core Structures** | 3–4 | Stacks, Binary Search, Linked Lists, Trees | Master fundamental data structures |
| **Advanced Patterns** | 5–6 | Heaps, Backtracking, Graphs, Tries | Tackle the patterns that scare you |
| **DP Deep Dive** | 7–8 | Dynamic Programming (full 2 weeks!) | The boss level — conquer DP with proper time |
| **Mastery & Interview Readiness** | 9–10 | Greedy, Intervals, Bits + Mocks + Weak Areas | Compress light topics, stress-test everything |

---

## 🔑 New Weekly Rituals

### 🃏 Wild Card Wednesday (Every Week from Week 3)
- **What**: One problem from a *previously completed* topic, chosen without telling you the category
- **Why**: Trains pattern identification — the #1 skill that separates people who "know the patterns" from people who can *recognize* them in a new problem
- **How**: Mentor picks a problem, presents it as a raw problem statement. You figure out the pattern, approach, and solve it.
- **Time**: ~30 min, replaces part of that day's session

### 📜 Scenario Problem (Every Week from Week 3)
- **What**: A problem wrapped in a real-world story (Amazon/Google style) — long statement, irrelevant details, implicit constraints
- **Why**: Half the battle in real interviews is *understanding what you're being asked*
- **How**: Mentor presents a 200+ word "scenario." You must: extract the core problem, ask clarifying questions, identify constraints, then solve
- **Time**: ~30 min, added to one session that week (usually Day 2 or Day 4)
- **Example themes**: "You're building a delivery system..." (→ graph/shortest path), "Your e-commerce platform needs to..." (→ sliding window / heap)

### 🔀 Adaptive Pacing Rule
For every topic:
- **Minimum 4 days** before moving on (you can't skip fundamentals)
- **If confidence < 6/10 after Day 4**: Take 1-2 extra days, steal from buffer weeks or next topic's rest day
- **If confidence ≥ 8/10 after Day 4**: Use remaining days for harder variants, Wild Card problems, or start next topic early
- **DP always gets full 12 days** — non-negotiable

---

## 🗓️ Week-by-Week Breakdown

### ═══════════════════════════════════════
### PHASE 1: FOUNDATION (Weeks 1–2)
### ═══════════════════════════════════════

### Week 1: Arrays & Hashing (Mar 4 – Mar 10)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Array fundamentals + Hashing intro | Contains Duplicate, Valid Anagram | 1.5h |
| Day 2 | Hashing patterns | Two Sum, Group Anagrams | 1.5h |
| Day 3 | Frequency counting | Top K Frequent Elements, Valid Sudoku | 1.5h |
| Day 4 | Prefix techniques | Product of Array Except Self, Encode & Decode Strings | 1.5h |
| Day 5 | Challenge day | Longest Consecutive Sequence + 1 revision problem | 2h |
| Day 6 | 🔄 **Revision** + concept quiz | Subarray Sum Equals K (LC 560) + Longest Substring Without Repeating Chars (LC 3) — pattern reinforcement with new twists. Quiz on Week 1 concepts. | 1.5h |
| Day 7 | REST or light review | Read pattern notes, no coding pressure | 30m |

### Week 2: Two Pointers & Sliding Window (Mar 11 – Mar 17)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Two pointer basics | Valid Palindrome, Two Sum II | 1.5h |
| Day 2 | Three pointer / partition | 3Sum, Container With Most Water | 1.5h |
| Day 3 | Sliding window - fixed size | Best Time to Buy/Sell Stock, Max Subarray (Kadane's) | 1.5h |
| Day 4 | Sliding window - variable size | Longest Substring Without Repeating Chars, Longest Repeating Char Replacement | 2h |
| Day 5 | Challenge day | Minimum Window Substring, Trapping Rain Water | 2h |
| Day 6 | 🔄 **Revision** + Week 1 spot check | Revisit + mini quiz on hashing patterns | 1.5h |
| Day 7 | REST | | |

---

### ═══════════════════════════════════════
### PHASE 2: CORE STRUCTURES (Weeks 3–4)
### ═══════════════════════════════════════

### Week 3: Stack & Binary Search (Mar 18 – Mar 24)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Stack fundamentals | Valid Parentheses, Min Stack | 1.5h |
| Day 2 | Monotonic stack + 📜 **Scenario #1** | Daily Temperatures, Car Fleet + scenario problem (story-wrapped stack/queue) | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + Stack apps | 1 random problem from Weeks 1-2 (pattern unknown) + Evaluate Reverse Polish Notation | 2h |
| Day 4 | Binary search basics | Binary Search, Search a 2D Matrix | 1.5h |
| Day 5 | Binary search on answer + 🔥 **First Hard exposure** | Koko Eating Bananas, Search in Rotated Sorted Array + **Median of Two Sorted Arrays** (Hard — attempt, not perfection) | 2.5h |
| Day 6 | 🔄 **Revision** + Phase 1 quiz + 🎭 **Mini Mock #1** (30 min) | Revisit 2 old problems + 1 timed problem interview-style | 2h |
| Day 7 | REST | | |

### Week 4: Linked Lists & Trees (Mar 25 – Mar 31)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Linked list basics | Reverse Linked List, Merge Two Sorted Lists | 1.5h |
| Day 2 | Fast & slow pointers + 📜 **Scenario #2** | Linked List Cycle, Reorder List + scenario problem (story-wrapped linked list/pointer) | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + Tree traversals (DFS) | 1 random problem from Weeks 1-3 + Invert Binary Tree, Max Depth | 2h |
| Day 4 | Tree patterns | Same Tree, Subtree of Another Tree, Lowest Common Ancestor | 1.5h |
| Day 5 | BST + Level order | Validate BST, Level Order Traversal, Kth Smallest in BST | 2h |
| Day 6 | 🔄 **Revision** + 🎭 **Mini Mock #2** (45 min) | 2 problems from Weeks 1-4, interview style | 2h |
| Day 7 | REST | | |

---

### ═══════════════════════════════════════
### PHASE 3: ADVANCED PATTERNS (Weeks 5–6)
### ═══════════════════════════════════════

### Week 5: Heaps & Backtracking (Apr 1 – Apr 7)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Heap fundamentals + Top-K | Kth Largest Element, Last Stone Weight | 1.5h |
| Day 2 | Heap applications + 📜 **Scenario #3** | K Closest Points to Origin, Task Scheduler + scenario problem (priority-based story) | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + Find Median | 1 random from Weeks 1-4 + Median of Data Stream | 2h |
| Day 4 | Backtracking fundamentals | Subsets, Combination Sum | 1.5h |
| Day 5 | Backtracking patterns + 🔥 **Hard exposure** | Permutations, Word Search + **N-Queens** (attempt) | 2.5h |
| Day 6 | 🔄 **Revision** + concept quiz on trees & heaps + 🎭 **Mini Mock #3** (30 min) | Quiz + 1 timed problem from Weeks 1-5 | 2h |
| Day 7 | REST | | |

### Week 6: Graphs (Apr 8 – Apr 14)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Graph representation + DFS/BFS | Number of Islands, Clone Graph | 1.5h |
| Day 2 | BFS patterns + 📜 **Scenario #4** | Rotting Oranges, Pacific Atlantic Water Flow + scenario problem (navigation/network story) | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + Topological sort | 1 random from Weeks 1-5 + Course Schedule, Course Schedule II | 2h |
| Day 4 | Union Find | Redundant Connection, Number of Connected Components | 2h |
| Day 5 | Advanced graphs + 🔥 **Hard exposure** | Word Ladder + **Alien Dictionary** (Hard) | 2.5h |
| Day 6 | 🔄 **Revision** + 🎭 **Mini Mock #4** (45 min) | 2 problems from Weeks 1-6, interview style | 2h |
| Day 7 | REST | | |

---

### ═══════════════════════════════════════
### PHASE 4: DP DEEP DIVE (Weeks 7–8) — THE BOSS LEVEL
### ═══════════════════════════════════════

> DP gets 2 full weeks. This is non-negotiable. It's the #1 interview topic at Google/Meta
> and the #1 area where candidates fail. We're giving it the respect it deserves.

### Week 7: Dynamic Programming — Foundations (Apr 15 – Apr 21)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | DP mindset + 1D basics | Climbing Stairs, House Robber — focus on recognizing overlapping subproblems & optimal substructure | 2h |
| Day 2 | 1D DP continued + 📜 **Scenario #5** | House Robber II, Decode Ways + scenario problem (DP story — "You're planning a road trip budget...") | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + Palindromic DP | 1 random from Weeks 1-6 + Longest Palindromic Substring | 2h |
| Day 4 | Coin/target DP | Coin Change, Coin Change II (unbounded knapsack variant) | 2h |
| Day 5 | Word/string DP | Word Break, Longest Increasing Subsequence | 2h |
| Day 6 | 🔄 **Revision** + DP intuition quiz | Revisit hardest 2 DPs of the week — solve from scratch, no hints | 2h |
| Day 7 | REST — but read DP notes from the week | | 30m |

### Week 8: Dynamic Programming — Advanced (Apr 22 – Apr 28)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | 2D DP intro | Unique Paths, Longest Common Subsequence | 2h |
| Day 2 | DP on strings (edit operations) + 📜 **Scenario #6** | Edit Distance + scenario problem (2D DP story — "You're comparing DNA sequences...") | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + knapsack DP | 1 random from Weeks 1-7 + Partition Equal Subset Sum (0/1 knapsack) | 2h |
| Day 4 | DP challenge + 🔥 **Hard exposure** | **Burst Balloons** or **Regular Expression Matching** (Hard — guided walkthrough if needed) | 2.5h |
| Day 5 | DP pattern review — solve 3 DPs cold | Pick 3 from all DP problems done (no hints, timed 15 min each) | 2h |
| Day 6 | 🔄 **Revision** + 🎭 **Mini Mock #5** (45 min) — DP focused | 2 DP problems, interview style, cold | 2h |
| Day 7 | REST | | |

---

### ═══════════════════════════════════════
### PHASE 5: MASTERY & INTERVIEW READINESS (Weeks 9–10)
### ═══════════════════════════════════════

> Greedy, Intervals, and Bit Manipulation are lighter topics — compressed into ~4 days.
> The rest of this phase is ALL about mocks, weak areas, and interview hardening.

### Week 9: Greedy + Intervals + Tries + Bit Manipulation (Apr 29 – May 5)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | Greedy patterns | Maximum Subarray (Kadane's), Jump Game, Gas Station | 2h |
| Day 2 | Intervals + 📜 **Scenario #7** | Merge Intervals, Non-Overlapping Intervals, Meeting Rooms II + scenario (scheduling story) | 2h |
| Day 3 | 🃏 **Wild Card Wednesday** + Tries | 1 random from Weeks 1-8 + Implement Trie, Word Search II | 2h |
| Day 4 | Bit Manipulation | Single Number, Counting Bits, Number of 1 Bits + Sum of Two Integers | 1.5h |
| Day 5 | 🎭 **Full Mock Interview #1** | 3 problems (1 Medium crossover, 1 Medium-Hard, 1 Hard), 60 min, real interview conditions | 2h |
| Day 6 | Weak area deep-dive #1 | Based on mock #1 feedback, revisit weakest topic. Re-solve 2-3 problems from scratch | 2h |
| Day 7 | REST | | |

### Week 10: Final Push & Interview Hardening (May 6 – May 12)
| Day | Focus | Problems | Time |
|-----|-------|----------|------|
| Day 1 | 📜 **Scenario #8** (long Amazon-style) + weak area #2 | Scenario problem with heavy customization + weak topic problems | 2h |
| Day 2 | 🃏 **Wild Card Gauntlet** — 3 random problems, 3 different patterns | No labels, no hints on pattern. Timed 20 min each | 2h |
| Day 3 | 🎭 **Full Mock Interview #2** | 3 problems, 60 min, different patterns than Mock #1 | 2h |
| Day 4 | Weak area deep-dive #2 + pattern review | Based on mock #2 feedback + re-read ALL pattern READMEs | 2h |
| Day 5 | 🎭 **Final Mock Interview #3** — THE GAUNTLET | 3 problems, 70 min, hardest mix. 1 Easy warm-up → 1 Medium → 1 Hard. Full interview sim with behavioral cues | 2.5h |
| Day 6 | Reflection + confidence scores | Review entire journey. Rate every topic. Identify any remaining gaps | 1.5h |
| Day 7 | REST + celebrate how far you've come! 🎉 | | |

---

### ═══════════════════════════════════════
### BONUS: Days 71-75 Buffer (May 13 – May 17)
### ═══════════════════════════════════════

> Use ONLY if needed. If you're feeling ready, use these for extra mocks.

| Day | Focus |
|-----|-------|
| Day 1-2 | Revisit ALL red-flag areas from progress tracker — solve from scratch |
| Day 3 | 🎭 **Bonus Mock** — company-specific style (Google/Amazon/Meta — pick your target) |
| Day 4 | Speed drill — solve 5 Mediums in 75 min (15 min each). Build speed muscle |
| Day 5 | Confidence check. You are ready. Trust the process. Go get that offer. 🚀 |

---

## 📊 Weekly Metrics to Track

Each week, update these in PROGRESS_TRACKER.md:
- [ ] Problems solved this week: ___ / target
- [ ] Patterns practiced: ___
- [ ] Confidence level (1-10) per topic
- [ ] Biggest "aha" moment
- [ ] Weakest area to revisit
- [ ] Wild Card Wednesday result: identified pattern? solved independently?
- [ ] Scenario problem result: extracted core problem? asked good clarifying questions?

---

## 🎯 Milestone Checkpoints

| Milestone | When | Criteria |
|-----------|------|----------|
| **🟢 Green Belt** | End of Week 2 | Solve any Easy in < 15 min, can explain 4+ patterns |
| **🔵 Blue Belt** | End of Week 4 | Solve most Mediums with hints, comfortable with trees/search |
| **🟣 Purple Belt** | End of Week 6 | Solve Mediums independently, can attempt Hards, pass Mini Mock 6+/10 |
| **🟤 Brown Belt** | End of Week 8 | Solve DP Mediums independently, can explain 3+ DP sub-patterns, pass DP Mock 7+/10 |
| **⚫ Black Belt** | End of Week 10 | Full Mock score 8+/10, solve 2 Mediums in 40 min, can handle ambiguous problem statements |

---

## 📉 When to Use Adaptive Pacing

The plan is no longer "7 days per topic or else." Use this decision tree:

```
After Day 4 of any topic:
├── Confidence ≥ 8/10?
│   └── YES → Compress. Use remaining days for Wild Cards, Hard variants, or start next topic
│   └── NO ↓
├── Confidence 6-7/10?
│   └── Keep going as planned. Day 5-6 will solidify it
├── Confidence < 6/10?
│   └── EXTEND. Take 1-2 extra days. Steal from:
│       ├── Buffer week (first choice)
│       ├── Greedy/Intervals/Bits (they're lighter)
│       └── Next topic's rest day (last resort)
```

**DP is exempt from compression.** Even if confidence is 9/10 after Day 4, keep going. DP depth beats DP breadth.

---

## 🔥 Hard Problem Exposure Schedule

Don't fear Hard problems. The goal isn't to solve them perfectly — it's to *see the tricks* so they don't surprise you in interviews.

| Week | Hard Problem | Approach |
|------|-------------|----------|
| Week 3 | Median of Two Sorted Arrays | Attempt binary search approach. OK to get guided walkthrough |
| Week 5 | N-Queens | Classic backtracking Hard. Should be reachable after Subsets/Permutations |
| Week 6 | Alien Dictionary | Graph + topological sort Hard. Build on Course Schedule |
| Week 8 | Burst Balloons or Regex Matching | DP Hard. Guided if needed — the goal is seeing interval DP / state machines |
| Week 9 | Trapping Rain Water (revisit) + company-tagged Hards in mocks | Should be comfortable now |
| Week 10 | The Gauntlet Mock includes 1 Hard | Timed, cold, no hints. The real test |

---

## 📝 Total Problem Count Estimate

| Category | Count | Notes |
|----------|-------|-------|
| Core curriculum problems | ~70 | Same as v1 |
| Wild Card Wednesday problems | ~8 | Weeks 3-10, 1 per week |
| Scenario problems | ~8 | Weeks 3-10, 1 per week |
| Hard problem exposures | ~6 | Weeks 3, 5, 6, 8, 9, 10 |
| Mock interview problems | ~18 | 6 mocks × 2-3 problems each |
| **TOTAL** | **~110** | Up from ~75 in v1 — much closer to the 150+ sweet spot |

To reach 150+, optionally add: weekend bonus problems, LeetCode daily challenge, or extra problems during buffer weeks.

---

*This plan is adaptive. If a topic needs more time, we adjust. If you're flying, we push harder. The goal is UNDERSTANDING + INTERVIEW READINESS, not checkboxes.*
