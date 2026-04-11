# 🔥 Amazon OA Sprint — Instruction File

> **Deadline**: April 1, 2026
> **Email received**: March 25, 2026
> **Duration**: 2 hours — 2 coding problems (70-90 min) + Workstyle Assessment (Leadership Principles)
> **Post-OA**: Revert to original 2-month DSA plan. No guilt. This is a calculated detour.
> **Source Intel**: Reddit r/leetcode, r/cscareerquestions, GFG, Amazon.jobs official prep page, LeetCode discuss, community reports (March 2026)
> **Demo Test**: Available at HackerRank ("Amazon Coding Demo") — safe to take anytime, saves for Day 4-5 mock

---

## 🎯 Mission

Maximize the probability of clearing Amazon's OA in 6 days. Not "learn everything" — **learn the RIGHT things at the RIGHT depth**. Every hour of prep must earn its place.

---

## 🧠 Mentor Mode: Amazon Sprint

During this sprint, the mentor operates differently from normal sessions:

### What Changes
- **Speed over depth** — understand the pattern well enough to CODE it under pressure. Deep intuition-building is secondary.
- **Amazon question framing** — present problems in Amazon's long-winded corporate style. Student practices extracting the core problem.
- **Pattern labels ARE allowed** — during OA sprint, knowing "this is BFS" fast matters. Labels help here.
- **Timed practice** — from Day 3 onward, every problem has a timer. 20 min for medium, 30 min for medium-hard.
- **Multiple problems per session** — aim for 2-3 problems/day instead of the usual 1-2 deep dives.
- **Test-driven** — write test cases FIRST, then code. Amazon OA has hidden test cases — passing all examples isn't enough.

### What Stays The Same
- Student codes first, mentor guides
- Trace through examples before trusting code
- Complexity analysis after every problem
- Log everything in progress tracker

---

## 📖 Amazon OA Question Decoding Framework

### The 3-Step Extract
Amazon wraps simple algorithms in corporate-sounding stories. Cut through it:

1. **Find the input type**: array? string? grid? graph (nodes + edges)?
2. **Find the output type**: single number? array? boolean? string?
3. **Find the constraint**: minimize? maximize? count? within a limit?

### Read Order
1. Look at **examples FIRST** — input/output, try to guess the pattern
2. Skim the **constraints** (array size, value range) — this hints at expected complexity
3. THEN read the story to confirm

### Amazon Story → Pattern Dictionary
```
"Warehouse / packages / trucks / delivery"     → Arrays + Greedy/Sorting
"Network of servers / connections / nodes"      → Graph (BFS/DFS)
"Customer preferences / groups / similar items" → Hashing or Union-Find
"Minimize cost / maximize profit"              → Sliding Window or DP
"Find optimal route / shortest path"           → BFS (unweighted) or Dijkstra (weighted)
"Process requests in order / dependency"        → Stack or Topological Sort
"Find pairs / triplets that satisfy condition"  → Two Pointers / Hashing
"Substring / subarray with property"           → Sliding Window
"Binary decision / search space"               → Binary Search
"Tree structure / hierarchy / org chart"        → Tree BFS/DFS
"Most frequent / top K / priority"             → Heap / Hashing + Sort
```

### Constraint → Complexity Hint
```
n ≤ 20          → O(2^n) backtracking/brute OK
n ≤ 100         → O(n^3) OK
n ≤ 1,000       → O(n^2) OK
n ≤ 10,000      → O(n log n) needed
n ≤ 100,000     → O(n) or O(n log n) needed
n ≤ 1,000,000   → O(n) needed
```

---

## 📋 5-Day Sprint Plan (Revised from Reddit/GFG Intel)

> **Key insight from Reddit**: OA has 2 coding problems (1 easy-medium, 1 medium-hard) + Workstyle Assessment.
> Workstyle is reportedly as important or MORE important than coding. Cannot skip.
> Problems are super wordy — Amazon scenario wrapping. Extracting the algorithm IS the test.
> Partial credit exists — 12/15 test cases can still advance you.

### Today — March 26: REST
You did a 3+ hour SD session. Don't burn out before the sprint starts. Rest is prep too.

### Day 1 — March 27: Grid BFS/DFS (THE #1 Amazon Pattern)
| Problem | Approach | Time Target | Folder |
|---------|----------|-------------|--------|
| Number of Islands | BFS/DFS grid traversal | 25 min | 11_Graphs |
| Flood Fill | BFS/DFS grid traversal | 15 min | 11_Graphs |
| Rotting Oranges | Multi-source BFS | 25 min | 11_Graphs |
| Number of Distinct Islands (LC 694) | DFS + shape hashing | 25 min | 11_Graphs |

**Templates to lock**: Grid 4-direction traversal, visited tracking (modify in-place vs set), BFS with deque, multi-source BFS (add ALL sources to queue first).

> **Intel update (Mar 27)**: LC 694 (Distinct Islands) keeps recurring in Amazon interviews. Same DFS template as Number of Islands, but you track the SHAPE of each island to count unique ones. High ROI addition.

### Day 2 — March 28 (Sat): Trees + Graph Basics
| Problem | Approach | Time Target | Folder |
|---------|----------|-------------|--------|
| Maximum Depth of Binary Tree | DFS recursive | 10 min | 07_Trees |
| Binary Tree Level Order Traversal | BFS with deque | 20 min | 07_Trees |
| Validate BST | DFS with bounds | 20 min | 07_Trees |
| Boundary of Binary Tree (LC 545) | DFS left/right boundary + leaves | 25 min | 07_Trees |
| Number of Connected Components (or similar) | DFS/BFS on adjacency list | 20 min | 11_Graphs |

**Templates to lock**: DFS recursive template, BFS queue template, adjacency list traversal.

> **Intel update (Mar 27)**: LC 545 (Boundary Traversal) is a recurring Amazon favorite. Tests tree DFS from multiple angles in one problem.

### Day 3 — March 29 (Sun): Amazon-Style Practice (YOUR Strong Patterns)
- 3-4 Amazon-style wordy problems using arrays, hashing, sliding window, two pointers
- Framed as corporate scenarios — practice the EXTRACTION skill
- Timed: 25 min per problem
- These are patterns you KNOW but need to recognize under Amazon's wrapping
- Also: quick revision of BFS/DFS from Day 1-2
- **Bonus**: Sliding Window Maximum (LC 239) — keeps appearing in Amazon interviews, and you already know sliding window. Monotonic deque variant. Worth 30 min of investment.

### Day 4 — March 30: Amazon-Style Practice (Mixed Patterns) + Workstyle Prep
- 2-3 timed Amazon-style problems mixing grid BFS/DFS, trees, arrays
- Pattern identification speed drill: 10 problem descriptions → name the pattern in 30 sec each
- **Evening: Leadership Principles study** (see Workstyle section below)

### Day 5 — March 31: Full Mock OA + Final Prep
- **Morning**: 2 unseen problems, 90 min timer, Amazon-style descriptions, NO hints
- **Afternoon**: Review mistakes, shore up weak spots
- **Evening**: Re-read Leadership Principles, light pattern cheat sheet review
- **Early sleep**

### OA Day — April 1
- Light revision in morning (pattern cheat sheet + LP quick review)
- No new problems on OA day
- Take it in evening, rested
- Read examples first, extract pattern, code clean, test edge cases

---

## 🏷️ Problem Labels (Sprint Only)

During this sprint, problems CAN be labeled with patterns involved:
```
[Stack] Valid Parentheses
[Stack, Design] Min Stack
[Binary Search] Search in Rotated Array
[BFS, Tree] Level Order Traversal
[BFS, Grid, Multi-source] Rotting Oranges
```

For mixed-pattern Amazon-style problems that don't fit a single folder → put in `Amazon_OA/` folder.

---

## 🧪 Amazon-Specific Testing Habits

1. **Edge cases to ALWAYS check**:
   - Empty input ([], "", 0)
   - Single element
   - All same elements
   - Already sorted / reverse sorted
   - Maximum constraint values (will it TLE?)
   - Negative numbers (if applicable)

2. **Amazon OA hidden test cases** — passing visible examples ≠ passing. Always think:
   - "What input would break my solution?"
   - "What's the biggest input? Would my O(n²) TLE?"

3. **Partial credit exists** — if stuck, submit brute force. Better than 0.

---

## 📊 Pattern Priority Matrix (Revised from Reddit/GFG Intel)

| Pattern | Amazon OA Frequency | Your Level | ROI | Sprint Action |
|---------|---------------------|------------|-----|---------------|
| Grid BFS/DFS | ★★★★★ | Not started | **CRITICAL** | Day 1 — learn template + 3 problems |
| Trees BFS/DFS | ★★★★☆ | Conceptual | **HIGH** | Day 2 — 3-4 problems |
| Graph traversal | ★★★★☆ | Not started | **HIGH** | Day 2 — adjacency list basics |
| Arrays + Hashing | ★★★★★ | Strong (8/10) | Practice translation | Day 3 — Amazon-style wrapping |
| Two Pointers | ★★★☆☆ | Good (7/10) | Practice translation | Day 3 — Amazon-style wrapping |
| Sliding Window | ★★★☆☆ | Good (7/10) | Practice translation | Day 3 — Amazon-style wrapping |
| Binary Search | ★★☆☆☆ (rare on OA) | Not started | LOW for OA | Skip — not worth a full day |
| Stack | ★★☆☆☆ (rare on OA) | Not started | LOW for OA | Skip — learn if time on Day 4 |
| DP | ★★★☆☆ | Not started | TOO DEEP | Skip |
| Bit Manipulation | ★☆☆☆☆ (surprise) | Not started | Skip | Skip — one Redditor got blindsided, but too rare to prep |
| **Workstyle/LP** | **★★★★★** | Not prepped | **CRITICAL** | Day 4 evening — Leadership Principles study |

---

## 🏢 Workstyle Assessment — Leadership Principles

> Reddit consensus: this section is **as important or MORE important** than coding.
> You can ace coding and still fail if workstyle is poor.
> **Student has taken Amazon OA before (~Feb/March 2025)** — familiar with format (inbox sim, RCA, scenario questions).
> Previous approach may have been too "escalate to manager" / consensus-seeking. Recalibrate to ownership-first.

### OA Workstyle Format (from prior experience — ~Feb/March 2025)
- **Inbox simulation** — prioritize emails/tasks from different stakeholders
- **RCA/Log analysis** — emails with transaction logs, find why something failed based on transaction ID. Tests Dive Deep LP.
- **A/B test analysis** — two algorithms compared with raw data (e.g. delivery agents split across 2 weeks). Analyze tradeoffs from raw performance data. Tests analytical thinking.
- **Video scenarios** — teammates appear in video, discuss requirements, send tasks to inbox
- **Algo comparison** — given 2 approaches with real results, justify which is better with tradeoff reasoning
- **Teammate conflict scenarios** — what would you do?

### A/B Analysis Framework (for algo comparison questions)
```
1. Define the metric: What matters most? (avg? worst case? cost? reliability?)
2. Look at variance, not just averages (consistent 8/10 > random 10/10 and 2/10)
3. Look for edge cases in data (bad weather? holiday spike? outliers?)
4. State tradeoff explicitly: "Algo A is better for X but worse for Y"
5. Recommend: "I'd choose [X] because [customer impact reason]"
6. Acknowledge downside: "The risk is [Z], I'd mitigate by [Y]"
```
Amazon prefers CONSISTENCY over burst performance (customer obsession = reliable > occasionally fast).

### Amazon's Key Leadership Principles (most tested)
1. **Customer Obsession** — Start with the customer and work backwards
2. **Ownership** — Act on behalf of the entire company, never say "that's not my job"
3. **Invent and Simplify** — Expect innovation, find ways to simplify
4. **Bias for Action** — Speed matters. Many decisions are reversible — don't over-analyze
5. **Deliver Results** — Focus on key inputs, deliver with the right quality and in a timely fashion
6. **Dive Deep** — Stay connected to details, audit frequently
7. **Earn Trust** — Listen attentively, speak candidly
8. **Have Backbone; Disagree and Commit** — Respectfully challenge decisions, then fully commit

### How to Answer Workstyle Questions
- They're typically "what would you do in this situation" multiple choice
- Choose answers that align with LPs: customer-first, take ownership, act fast, deliver
- **AVOID**: answers that pass blame, wait for instructions, avoid conflict, prioritize process over results, escalate to manager BEFORE trying to solve yourself
- **PREFER**: answers that take initiative, focus on customer impact, own mistakes, act decisively, have direct conversations with teammates before escalating
- When torn between two options: pick the one that's more ACTION-oriented and CUSTOMER-focused

### Recalibration from Last Attempt
Previous approach was likely too collaborative/escalation-heavy. Amazon's ideal:
| Scenario | ❌ What you probably picked | ✅ What Amazon wants |
|---|---|---|
| Teammate not delivering | "Talk to manager about it" | "Have direct conversation with teammate first, understand blockers, help solve, THEN inform manager of outcome" |
| Conflicting priorities | "Discuss with team to reach consensus" | "Evaluate customer impact, make the call, inform team" |
| Something broke in production | "Escalate to on-call/manager" | "Investigate root cause yourself, fix what you can, THEN escalate with findings" |
| Ambiguous requirements | "Ask manager for clarification" | "Make best decision with available info, document assumptions, course-correct later" |

**The pattern**: ACT FIRST → OWN IT → INFORM LATER (not ask permission → wait → follow instructions)

### Quick LP Prep (Day 4 evening, 30 min)
- Read through all 14 LPs once
- For each, think of ONE real example from your work/projects where you demonstrated it
- Practice: "If two LPs conflict, which wins?" → Customer Obsession usually wins

---

## 🔁 Recurring Amazon LC Problems (Oct-Dec 2025 Reports)

> Source: 113-upvote Reddit post tracking Amazon interview questions across Leetcode, Glassdoor, Blind.
> "Amazon is one of the most repetitive companies — they keep the fundamental approach the same but change the problem scenario/framing."

| LC # | Problem | Core Pattern | Your Status |
|------|---------|-------------|-------------|
| 694 | Number of Distinct Islands | Grid DFS + shape tracking | Day 1 target |
| 675 | Cut Off Trees for Golf Event | BFS on grid + sorting | Day 3-4 stretch |
| 545 | Boundary of Binary Tree | Tree DFS (multi-angle) | Day 2 target |
| 239 | Sliding Window Maximum | Monotonic Deque | Day 3 bonus (you know SW) |
| 451 | Sort Characters By Frequency | Hashing + Sort | Already know pattern |
| 532 | K-diff Pairs in an Array | Hashing / Two Pointers | Already know pattern |
| 661 | Image Smoother | Grid traversal (easy) | Showed up in real AWS interview |
| 119 | Pascal's Triangle II | Array/Math | Quick solve if it appears |
| 536 | Construct Binary Tree from String | Tree + Stack/Recursion | Day 2 stretch |

**From interview comments** (actual 2025 questions):
- Smallest number in rotated sorted array (Binary Search)
- Alien Dictionary (Topological Sort — advanced)
- Peak Element (Binary Search)
- Course Schedule 2 (Topological Sort)
- Maximum Candies Allocated to K Children (Binary Search on answer)

**Pattern**: Amazon loves grid BFS/DFS, tree traversals, and wrapping familiar patterns (hashing, sliding window) in corporate scenarios.

---

## 🧘 Mindset Rules

1. **This is a drill, not a miracle.** 5 days won't make you an expert. But 5 days of FOCUSED prep on the RIGHT patterns is enough for an OA.
2. **OA ≠ final round.** It's a filter. You need to pass, not ace it. Solving 1.5/2 problems cleanly is usually enough.
3. **Brute force > blank screen.** If you can't find optimal, CODE the brute force. Partial credit is real (confirmed by Reddit — 12/15 test cases can advance).
4. **Read examples first, ALWAYS.** This is not optional. It's the #1 time-saver on Amazon OA.
5. **Workstyle is NOT optional.** Don't treat it as an afterthought. Prep LPs on Day 4.
6. **After April 1, this sprint ends.** Win or lose, revert to the 2-month plan. No regrets, no lingering.

---

## 🔁 Post-OA Revert Plan

After April 1:
- Resume original 2-month DSA plan from where we left off (Sliding Window Maximum)
- Resume SD sessions (APIs & Protocols next)
- All problems solved during sprint are banked — they count toward topic completion
- If Amazon advances → prepare for interviews (separate plan)
- If Amazon doesn't → lesson learned, apply learnings, keep building

---

*This file is the sprint's north star. Read it before every session. Updated daily.*
