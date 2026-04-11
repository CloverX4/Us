# 📊 Progress Tracker

> **Started**: March 4, 2026 | **Current Week**: 3 | **Current Phase**: Trees + Graphs (reordered — energy-driven)

---

## 📌 Amazon OA — Completed April 1, 2026 (Rejected)

> Took the OA at Week 3 of prep. Friend assisted on call. Q1 (domino coloring — combinatorics) understood after explanation. Q2 (binary string propagation + simulation) didn't fully click. Syntax error on Q2.
> **Lesson**: Independent problem-solving pipeline (see → pattern → approach → code) not yet built for unfamiliar patterns. Normal at this stage. The plan addresses this over Weeks 3-10.

---

## �🔥 Streak & Stats

| Metric | Value |
|--------|-------|
| **Current Streak** | 13 days |
| **Longest Streak** | 13 days |
| **Total Problems Solved** | 22 |
| **Easy Solved** | 6 |
| **Medium Solved** | 13 |
| **Hard Solved** | 1 |
| **Mock Interviews Done** | 0 |
| **Best Mock Score** | — |

---

## 🎯 Confidence Levels Per Topic (Update Weekly)

Rate 1-10: (1 = no clue, 5 = can solve with hints, 8 = solve independently, 10 = can teach it)

| Topic | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 | Week 7 | Week 8 |
|-------|--------|--------|--------|--------|--------|--------|--------|--------|
| Arrays & Hashing | 8 | 8 | | | | | | |
| Two Pointers | — | 7 | | | | | | |
| Sliding Window | — | 7 | | | | | | |
| Stack | — | | | | | | | |
| Binary Search | — | | | | | | | |
| Linked Lists | — | | | | | | | |
| Trees | — | 3 | | | | | | |
| Tries | — | | | | | | | |
| Heap / Priority Queue | — | | | | | | | |
| Backtracking | — | | | | | | | |
| Graphs | — | 3 | | | | | | |
| Dynamic Programming | — | | | | | | | |
| Greedy | — | | | | | | | |
| Intervals | — | | | | | | | |
| Bit Manipulation | — | | | | | | | |

---

## 📝 Daily Log

### Week 1: Arrays & Hashing

#### Day 1 — March 4-5, 2026
- **Problems**: Contains Duplicate ✅, Valid Anagram ✅
- **Time Spent**: ~1.5h (Phase 0 walkthrough + 2 problems)
- **Key Learnings**: Hash function → array index → O(1) lookup; complement pattern; set vs dict vs Counter choice; always mention BOTH time and space; `.get(key, 0)` to avoid KeyError; single-map +1/-1 trick for frequency compare; `all()` / `any()` builtins; bounded alphabet = O(1) space argument
- **Struggled With**: Forgot to handle missing keys in dict (KeyError). Caught and fixed with `.get()`. Not yet familiar with `all()`/`any()`.
- **Confidence After**: 5/10 Good instinct for early exits and single-pass optimization. Naturally cross-connected patterns (set → graph visited). Chose manual dict over Counter to show understanding — good interview instinct.

#### Day 2 — March 7, 2026
- **Problems**: Two Sum ✅, Group Anagrams ✅ (first Medium!)
- **Time Spent**: ~1.5h
- **Key Learnings**: Complement pattern in action; check-before-store order matters for duplicates; read constraints as hints; sorted string as hashmap key; `defaultdict(list)`; `ord(ch) - ord('a')` for alphabet indexing; use separate variables (n, k) for multi-dimension complexity
- **Struggled With**: Initially confused complement-as-key vs num-as-key (both valid). Forgot lists can't be dict keys.
- **Confidence After**: 6/10
- **Notes**: First Medium solved clean with no bugs. Tradeoff analysis between sort vs frequency approaches was strong. Growing interview instincts — mentioned special character limitation of frequency approach unprompted.

#### Day 3 — March 7, 2026
- **Problems**: Top K Frequent Elements ✅, Valid Sudoku ✅
- **Time Spent**: ~2h
- **Key Learnings**: Bucket sort uses frequency as array index to avoid O(n log n); in-place methods (.reverse(), .sort()) return None — use reversed()/sorted(); don't mutate function parameters; early termination > collect-then-slice; `Counter` is shorthand for frequency map; `(r//3, c//3)` maps cell to 3×3 box (integer division, NOT modulo); constant-size data structures = O(1) space regardless of count; tiled/block iteration pattern: `range(0, n, step)` + `range(start, start+step)`; bound checking: plug in n=5 to verify, don't memorize
- **Struggled With**: Top K: `.reverse()` returns None, off-by-one slice with wrong variable, mutating k. Valid Sudoku: initially confused `//` vs `%` for box mapping but corrected before coding.
- **Confidence After**: 7/10
- **Notes**: Top K had 3 bugs — all Python gotchas. Valid Sudoku: FIRST CLEAN SOLVE — zero bugs, first try all tests pass. Questioned space concern (27 sets) and resolved it through analysis (constant = free). Asked about alternative approaches unprompted — growing engineering curiosity. Two Mediums in one day. 

#### Day 4 — March 8, 2026
- **Problems**: Product of Array Except Self ✅, Encode and Decode Strings ✅
- **Time Spent**: ~1.5h
- **Key Learnings**: Prefix/suffix product two-pass with O(1) space; length-prefixed encoding (same as HTTP Content-Length); `str.find(char, start)` for scanning from position; strings are immutable — no `.append()`, use `+=` or `"".join()`; `str.join()` is called ON the separator with a list; simple delimiters fail when strings can contain any character
- **Struggled With**: Encode: confused list methods with string methods (.append on string, then .join misuse). Decode: forgot to init `i = 0`. All Python fluency issues, not algorithm issues.
- **Confidence After**: 7/10
- **Notes**: Product Except Self was a clean solve — immediately recognized prefix/suffix pattern and went straight for O(1) space version. Encode/Decode had 2 Python bugs but algorithm logic was solid. Recall quiz on Top K bugs scored 2.5/3 — rule is known but application needs reinforcement. Four problems today across 2 sessions. String method confusion is a recurring theme — needs focused practice. 

#### Day 5 — March 9, 2026
- **Problems**: Longest Consecutive Sequence ✅, Top K Frequent Elements (revision) ✅
- **Time Spent**: ~1.5h
- **Key Learnings**: Sequence ≠ subarray (order doesn't matter, only existence); `num - 1 not in set` detects sequence starts — ensures each element visited at most twice for O(n); set deduplication handles duplicates automatically; always ask clarifying questions before coding ("is this subarray or sequence?")
- **Struggled With**: Initially confused sequence vs subarray — asked for clarification before coding (good). Suggested finding min in set for sequence starts (O(n) per sequence = O(n²)) — corrected to `num-1` check.
- **Confidence After**: 8/10
- **Notes**: Longest Consecutive was a clean solve after understanding the problem. Top K revision: ZERO BUGS blind re-solve — all 3 original bugs (reverse(), off-by-one, parameter mutation) corrected from memory. Used Counter instead of manual dict, reversed() instead of .reverse(). Five consecutive clean solves. Arrays & Hashing section complete! 

#### Day 6 — March 10, 2026 (Revision Day)
- **Problems**: Smaller Numbers Than Current ✅ (warmup), Subarray Sum Equals K ✅, Longest Substring Without Repeating Chars ❌ (attempted, WIP)
- **Time Spent**: ~2h
- **Key Learnings**: Counting sort + prefix sum combined on new problem; prefix sum + hashmap complement + frequency counting combined for subarray sum; `{0:1}` base case for prefix complement problems; sliding window template: outer loop drives `r`, inner loop shrinks `l`; negatives break sliding window because expand/shrink logic becomes unpredictable
- **Struggled With**: Prefix sum accumulation (used `=` instead of `+=`); sliding window structure — put `l` as outer driver instead of `r`, causing `r` to get stuck. This is a new pattern not yet formally learned.
- **Confidence After**: 7/10
- **Notes**: Subarray Sum = K was a clean first-try solve — combined 3 patterns from the week. Warmup required debugging prefix logic. Sliding window is Week 2 material — attempted early as a preview, got the right data structure (set) and shrink logic but wrong loop structure. Will revisit with proper template in Week 2. Not every day is a peak day — showed up and did the work. 

---

### Week 2: Two Pointers & Sliding Window

#### Day 1 — March 13, 2026
- **Problems**: Valid Palindrome ✅ (clean first-try solve)
- **Time Spent**: ~45m (Phase 0 Two Pointers walkthrough + 1 problem)
- **Key Learnings**: Two Pointers = eliminating possibilities to go from O(n²) to O(n); opposite-end vs same-direction vs three-pointer sub-patterns; `char.isalnum()` for alphanumeric check; skip non-alnum inside loop = O(1) space vs cleaning string = O(n) space; strings are immutable — `s.lower()` always creates new string, even if reassigned to same variable; Two Pointers vs HashMap tradeoff: O(n log n)/O(1) vs O(n)/O(n)
- **Struggled With**: Nothing major — confused brute force (said two loops instead of clean+reverse). Needed reminder about duplicate-skipping in all-pairs template.
- **Confidence After**: 4/10 (just started the topic, one easy problem done)
- **Notes**: Clean first-try solve on Valid Palindrome. Phase 0 walkthrough was thorough — understands all 3 sub-patterns conceptually. Revision quiz on Subarray Sum = K: recalled pattern and sliding window limitation perfectly, needed walkthrough on {0:1} base case intuition but now owns it. Good session despite short time.

#### Day 2 — March 13-14, 2026
- **Problems**: Two Sum II ✅ (clean first-try), 3Sum ✅ (bugs fixed iteratively)
- **Time Spent**: ~1.5h
- **Key Learnings**: Two Sum II is Two Sum with free sort → O(1) space; 1-indexed output = just +1; 3Sum = sort + fix pivot + Two Sum on rest = O(n²); dedup at two levels: pivot skip (`nums[i]==nums[i-1]`) and inner pair skip; `while` loop requires manual `i += 1` — `for` manages it for you; `nums[r+1]` can IndexError when r is last index — need bounds guard `l < r < len(nums)-1`; chained comparison `a < b < c` in Python is legit; validate test cases against problem constraints before trusting them
- **Struggled With**: 3Sum had 3 bugs: used `while` instead of `for` (then committed to `while` but forgot `i += 1` causing infinite loop); skip logic outside else block needed bounds guard for `r+1`; initially used `while i in range(...)` which is membership check not iteration
- **Confidence After**: 5/10
- **Notes**: Two Sum II was textbook clean — immediate application of opposite-end template. 3Sum required 3 iterations to get right — all structural/Python bugs, algorithm logic was sound from the start. Challenged mentor on skip-outside-else placement and was right — it works for 3Sum with proper bounds. Caught a bad test case (two solutions violating uniqueness constraint). Growing debugging instincts and willingness to question assumptions.

#### Day 3 — March 14, 2026 (Light day)
- **Problems**: Container With Most Water ✅ (clean first-try solve)
- **Time Spent**: ~30m
- **Key Learnings**: Move the shorter-height pointer because width always decreases — only way to improve is finding a taller wall; greedy proof: when heights are equal, no inner pair with either line can beat current area (width shrinks, height capped by the equal value); `min(h[l], h[r]) * (r-l)` is the area formula; variable naming matters — `max_area` > `glob` for readability
- **Struggled With**: Understanding why equal-height ties don't matter — needed ELI5 walkthrough with swimming pool analogy. Got it after proof: both lines have peaked, neither can do better.
- **Confidence After**: 6/10
- **Notes**: Clean first-try solve. Asked deep clarifying questions about the greedy proof (ties) — not surface-level acceptance, genuine understanding. Light day but stayed consistent. Three consecutive clean solves across sessions.

#### Day 4 — March 15, 2026 (Theory only)
- **Problems**: None (Phase 0 Sliding Window walkthrough)
- **Time Spent**: ~20m
- **Key Learnings**: Fixed window = aggregate over known size k; variable window = find optimal window size (longest/shortest); `right` must be outer loop driver — guarantees O(n) because both pointers only move forward; "substring" (contiguous) vs "subsequence" (can skip) — sliding window is for contiguous only; Kadane's is sliding window where shrink = reset when sum goes negative
- **Struggled With**: Nothing — theory day, no coding
- **Confidence After**: 6/10 (same, no new problem solved)
- **Notes**: Showed up on a low-energy day for just a Phase 0 walkthrough. Consistency > intensity. Ready to tackle Best Time to Buy/Sell Stock tomorrow.

#### Day 5 — March 16, 2026
- **Problems**: Best Time to Buy and Sell Stock ✅ (clean first-try solve)
- **Time Spent**: ~30m
- **Key Learnings**: `min_so_far` acts as an implicit left pointer in sliding window; patterns are thinking frameworks not rigid templates — stock problem IS sliding window with implicit pointers; explicit two-pointer version uses `l = r` reset when cheaper buy found; `float('inf')` is the right init for tracking minimums; the "one piece of info you need" insight — at each position, profit = price - min_so_far
- **Struggled With**: Initial pseudocode had 3 issues (used index instead of value, missing second arg to max(), unnecessary while loop) — all caught and fixed before coding. Nothing in actual implementation.
- **Confidence After**: 7/10
- **Notes**: Clean first-try solve. Zero bugs in actual code. Asked the right question about why this is categorized as sliding window — showed genuine pattern curiosity. Understood implicit vs explicit pointer distinction. Six consecutive clean solves. Ready for Longest Substring Without Repeating Characters next.

- **Problems (continued)**: Longest Substring Without Repeating Characters ✅ (clean first-try solve — REVENGE ARC)
- **Time Spent**: ~30m (total day: ~1h)
- **Key Learnings**: Variable sliding window template — `r` outer `for`, inner `while` to shrink; amortized O(n) argument: both pointers only move forward, each element added/removed at most once = 2n ops; `r - l + 1` for window length is idiomatic over `len(set)`; space is O(min(n, m)) where m = charset size — bounded alphabet means O(1) argument; the "what makes the window invalid?" + "how do I shrink?" framework makes every sliding window problem the same template
- **Struggled With**: Nothing. Zero bugs. Correct template on first attempt.
- **Confidence After**: 7/10
- **Notes**: REVENGE SOLVE. Failed this exact problem on Day 6 (wrong loop driver, r got stuck). Today: textbook clean, 7 lines, zero bugs. Old attempt preserved in file for growth tracking. Seven consecutive clean solves. Two problems in one session. Sliding window template is clicking.

#### Day 6 — March 18-19, 2026
- **Problems**: Longest Repeating Character Replacement ✅ (needed loop structure hint)
- **Time Spent**: ~45m
- **Key Learnings**: Frequency map to track char counts in window; `(window size) - max_freq = replacements needed`; max_freq only increases (historical max) so `if` works instead of `while`; space is O(1) because map bounded by 26 uppercase letters; don't need the most frequent CHARACTER, just its COUNT — minimizing replacements is the goal
- **Struggled With**: Couldn't initially visualize how to track the most frequent char in the window — froze on translating the idea into a loop. Needed the loop structure hint to unblock. The "update max_freq each iteration" approach wasn't obvious.
- **Confidence After**: 7/10
- **Notes**: Algorithm understanding was solid — correctly identified that we need max frequency and that replacements = window - max_freq. The freeze was on translating to code, not on the concept. Good self-awareness: recognized the freeze and articulated what was blocking. Deep discussion on while vs if subtlety (Google-style follow-up). Complexity analysis was strong — correctly identified O(1) space from alphabet bound. Eight consecutive solves (streak includes hint-assisted). Side-by-side comparison with Longest Substring helped solidify both patterns.

#### Day 7 — March 19, 2026
- **Problems**: Permutation in String ✅ (two versions: brute → optimized sliding window)
- **Time Spent**: ~1h
- **Key Learnings**: Fixed-size sliding window — window size = `len(s1)` because permutations preserve length; permutation = same frequency map; precompute first window then slide (add right, remove left) instead of rebuilding Counter each step; `Counter` ignores zero-count keys in equality (safe to decrement without cleanup — plain dict would break); O(26) comparison per step is still O(n) overall; `matches` counter optimization exists for true O(1) per step
- **Struggled With**: Initially thought of variable window (expand on match, reset on miss) but correctly identified it should be fixed-size. v1 (rebuild Counter each step) came first naturally. Needed prompting to see the sliding optimization but implemented it cleanly.
- **Confidence After**: 7/10
- **Notes**: First fixed-size sliding window problem. Two working versions: v1 O(n*k) brute, v2 O(n) true sliding window. Both passed all tests. Good progression from brute to optimal within the session. Correctly identified Counter's zero-count equality behavior as a Python detail worth knowing. Matches optimization (v3) understood conceptually — will implement tomorrow. Nine consecutive solves. Sliding window confidence growing across all variants (variable + fixed).

#### Day 8 — March 21, 2026
- **Problems**: Permutation in String v3 (matches optimization) — attempted, WIP
- **Time Spent**: ~30m
- **Key Learnings**: `matches` counter tracks how many of 26 chars have equal frequency in both maps; before/after count change pattern for maintaining matches; the matches approach eliminates O(26) comparison per step → true O(1); v2 (Counter comparison) is interview-sufficient — matches is nice-to-know depth
- **Struggled With**: The before/after match tracking was unintuitive. Could code it mechanically but didn't own the intuition. Recognized the tradeoff: over-optimizing code at the expense of clarity isn't always worth it.
- **Confidence After**: 7/10
- **Notes**: Mature decision to recognize when an optimization is "nice to know" vs essential. v2 is the interview answer. Matches will click naturally when similar patterns appear later (Minimum Window Substring has/need counter). Also set up System Design parallel track today — restructured workspace into Algoww + Desinoww.

#### Day 9 — March 23-24, 2026
- **Problems**: Minimum Window Substring ✅ (first hard-level problem!)
- **Time Spent**: ~1.5h (single session spanning midnight)
- **Key Learnings**: Variable-size sliding window but SHRINK while valid (opposite of longest-type problems — minimize window); `have/need` counter pattern: `need` = unique chars in t, `have` = how many meet required frequency; window valid when `have == need`; shrink from left to find minimum valid window; track `best_l, best_r` separately from current `l, r`; pre-building partial window is unnecessary — start empty and expand; O(m + n) time: O(n) for t_freq_map + O(m) amortized for window
- **Struggled With**: Initial confusion on what makes window valid/invalid — needed the "expand when invalid, shrink when valid" framing. First attempt had bugs: wrong matches comparison (`len(t)` vs `len(t_freq_map)`), best window tracking outside shrink loop, `.keys` vs `.keys()`. Fixed iteratively during the session.
- **Confidence After**: 7/10
- **Notes**: First hard-level solve! Approach was self-derived — correctly identified `have/need` counter pattern independently (same concept as matches from Permutation in String, but it clicked here because it solves a real need). The "shrink while valid" insight is the key differentiator for minimum-type sliding window problems. Key difference from previous problems: for minimum-type you shrink while valid and update answer during shrink, for maximum-type you shrink when invalid and update answer after ensuring validity. Complexity understanding solid — O(m + n) amortized because l and r each traverse s at most once, plus O(n) for building t_freq_map. O(m) + O(n) = O(m+n) notation clicked. Persistent Systems DoSelect contest on Mar 22 (C# LLD + React) — real contest experience. Ten consecutive solves.

#### Day 10 — March 24, 2026
- **Problems**: Sliding Window Maximum — approach discussion + concept understanding (WIP, implementation tomorrow). Revision quiz on Minimum Window Substring (3.5/4).
- **Time Spent**: ~45m
- **Key Learnings**: Revision quiz reinforced: shrink-when-valid vs shrink-when-invalid is THE differentiator for min/max window problems; `len(t_freq_map)` not `len(t)` for have/need — concrete example: t="aa" breaks with len(t). Sliding Window Maximum: brute force O(n*k) too slow; can't just track max because removal of max leaves you blind to second-largest; monotonic deque maintains decreasing order — useless elements (smaller than new) get popped from back, expired elements popped from front; store INDICES not values (need position to check expiry); deque = O(1) for both ends = stack + queue hybrid.
- **Struggled With**: Initially thought O(n log n) was needed — O(n) is achievable with monotonic deque. Permutation in String mental model still mixing initial (variable expand/reset) approach with final (fixed-size slide) approach.
- **Confidence After**: 7/10
- **Notes**: Revision quiz was strong (3.5/4). Only miss: Permutation in String description reverted to the initial wrong approach instead of the actual fixed-size solution. Sliding Window Maximum concept understood — monotonic deque clicked quickly (had prior exposure). Key question "values or indices?" answered correctly with good reasoning. Implementation deferred to next session.

#### Day 11 — March 27, 2026 (Amazon OA Sprint Day 1)
- **Problems**: Number of Islands ✅, Flood Fill ✅
- **Time Spent**: ~30m (templates + coding)
- **Key Learnings**: DFS grid template: guard → mark → recurse 4 dirs; outer loop scans grid for unvisited `'1'` = new island → DFS sinks the whole connected chunk; DFS doesn't count — it just sinks, counting happens in outer loop; `or` vs `and` precedence trap in guard conditions; DFS recursive / DFS iterative (stack.pop) / BFS iterative (queue.popleft) are ALL interchangeable for "visit connected region" problems — same complexity, different traversal order; BFS only becomes necessary when you need shortest distance / level tracking (Rotting Oranges)
- **Struggled With**: Operator precedence in guard (`and` before `or` in Python). Initially tried to return count from DFS — realized DFS just sinks, counting is the outer loop's job. Verbalized fear of not being able to translate understanding to code — coded it anyway with headache and proved the fear wrong.
- **Confidence After**: 3/10 (first grid problem, template is fresh, needs repetition)
- **Notes**: Solved Number of Islands with a headache at night after saying "I can't code right now." Proved the fear wrong. Shared Google phone screen experience — same problem, took 40 min, visited-tracking insight came late. The gap isn't understanding, it's muscle memory. Templates built (DFS + BFS) and verified. Flood Fill solved in under 10 min — same template, caught the color==original_color infinite recursion edge case by adding `image[row][col] == color_new` guard. Also: deep research session updating sprint plan with recurring Amazon LC numbers from Reddit (113-upvote compilation). Tomorrow: Rotting Oranges + Distinct Islands + Trees.

#### Day 12 — April 5, 2026 (Trees + Graphs Phase 0)
- **Problems**: Binary Tree Islands (Google phone screen revisit — concept + solution, not coded)
- **Time Spent**: ~45m
- **Key Learnings**: Tree = graph with no cycles + connected; tree DFS needs no visited set (only one path to any node); pre/in/post order = where you process curr node relative to children; level order BFS uses `for _ in range(len(queue))` trick to group by level; grid DFS vs tree DFS comparison (neighbors = 4 dirs vs left/right, visited = grid mutation vs not needed); binary tree islands: detect `0 → 1` transitions by passing parent VALUE (not parent node); "think locally, trust globally" — only reason about current node, trust recursion handles the rest
- **Struggled With**: Initially confused about parent tracking (same confusion as Google interview). Resolved: for binary tree islands you only need parent's VALUE, not the node reference. Recursion visualization is still hard — "think locally, trust globally" framework introduced.
- **Confidence After**: Trees 3/10 (first session, concepts clicked but no coded problems yet), Graphs 3/10 (unchanged)
- **Notes**: Decided to reorder the plan — Trees → Graphs → DP as main arc, other topics on demand. Not abandoning the 2-month plan, just reordering by energy + interview weight. Competitive programmers don't learn linearly — they build intuition through exposure. Google phone screen question finally makes sense: the whole solution is just counting 0→1 transitions with parent_val parameter. SD session earlier same day fueled the motivation. Also did tree traversal templates (pre/in/post/level order).
- **⏭️ Next session opener**: "Want to try a problem where we practice the 'think locally, trust globally' recursion thinking? Or do you want to move on to something else in the trees + graphs space?"

---

## 🏆 Milestones

- [ ] 🟢 **Green Belt** — End of Week 2
- [ ] 🔵 **Blue Belt** — End of Week 4
- [ ] 🟣 **Purple Belt** — End of Week 6
- [ ] ⚫ **Black Belt** — End of Week 8

---

## 💡 "Aha!" Moments Journal

> Tags: 🔧 Trick | 🌉 Bridge (cross-domain) | 🧱 Foundation | 🔄 Reframe (understanding shifted) | 💀 Trap (mistake that revealed something)
> **Revision use:** Before re-solving any problem, read ONLY its Aha moment first — not the solution, not the notes. Just the insight. Then solve.

1. 🧱 **Hash maps are O(1) because the hash function converts keys into array indices** — it's just array access under the hood. (Arrays & Hashing, Day 1)

2. 🔧 **`num - 1 not in set` detects sequence starts** — ensures each element visited at most twice = O(n). Without it you'd have O(n²). (Arrays & Hashing, Day 5)

3. 💀 **Check-before-store order matters in Two Sum** — if you store first and THEN check, `target=0` with `[0]` returns the same index twice. Always check, then store. (Arrays & Hashing, Day 2)

4. 🔧 **Prefix sum + hashmap complement: `{0: 1}` base case** — without it you can't count subarrays starting from index 0. The "empty prefix has sum 0" idea. (Arrays & Hashing, Day 6)

5. 🔄 **Sliding window: `right` MUST be the outer loop driver** — guarantees O(n) because both pointers only move forward. If `left` drives the outer loop, `right` can get stuck. (Sliding Window, Day 4 theory)

6. 🔄 **`min_so_far` is an implicit left pointer** — Best Time to Buy/Sell Stock IS a sliding window. Patterns are thinking frameworks, not rigid templates. (Sliding Window, Day 5)

7. 🧱 **Variable window template = "what makes it invalid?" + "how do I shrink?"** — answer those two questions and every variable window problem uses the same template. (Sliding Window, Day 6)

8. 🔧 **`max_freq` never decreases — so `if` is safe over `while` in Longest Repeating Char Replacement** — `r` only moves right by 1 per step, so overshoot is at most 1. This is a lazy/historical max, not a live max. (Sliding Window, Day 6 Week 2)

9. 🔧 **Permutation = same frequency map = fixed-size sliding window** — window size is always `len(s1)` because permutations preserve length. (Sliding Window, Day 7 Week 2)

10. 💀 **`Counter` ignores zero-count keys in equality checks** — you can decrement below zero and Counter equality still works. Plain `dict` would break: `{'a': 0}` ≠ `{}`. (Sliding Window, Day 7 Week 2)

11. 🔄 **DFS doesn't count — counting is the outer loop's job** — DFS just sinks/visits the connected region. The counting logic lives OUTSIDE in the loop that calls DFS. (Graphs, Day 11)

12. 🌉 **Tree = graph with no cycles + connected** — so tree DFS needs no visited set. Only one path to any node means you can never revisit. Grid DFS needs visited because you CAN go back (right then left). (Trees, Day 12)

13. 🔄 **Binary tree islands: detect 0→1 transitions, not flood fill** — pass parent VALUE down. `parent_val == 0 and node.val == 1` = new island. No visited set, no flood fill, no parent node tracking. The tree structure guarantees each node has exactly one parent, so each island has exactly one entry point. (Trees, Day 12)

14. 🧱 **"Think locally, trust globally"** — when writing recursion, only think about ONE node: base case, what do I do here, assume children return correct answers, combine. The moment you trace into the recursive calls mentally, you're lost. (Trees, Day 12)

---

## 🕸️ Connection Web

> Log cross-domain connections here after every problem. This is your knowledge graph made visible.

| Problem | Connected To | Why |
|---------|-------------|-----|
| Longest Substring Without Repeating Chars | Rate limiter (SD) | Both track a "valid window" and shrink when a violation enters |
| Number of Islands | Connected components in network topology | Same DFS flood-fill — visit everything reachable, count disconnected clusters |
| Binary Tree Islands | Number of Islands (grid) | Same "count connected 1-clusters" but tree structure simplifies it — no visited set needed, just detect 0→1 transitions via parent value |
| Grid DFS (visited via mutation) | Tree DFS (no visited needed) | Both are DFS traversal. Grid needs visited tracking because movement is bidirectional. Tree doesn't because parent→child is one-way. |

---

## ⚠️ Recurring Mistakes

> Track patterns in your mistakes — this is where real growth happens

| Mistake Pattern | Frequency | Fix |
|----------------|-----------|-----|
| `while` vs `for` loop confusion | 1 | `for` manages iteration; `while` needs manual increment. Use `for` unless you need custom control |
| Forgetting `i += 1` in while loop | 1 | Always add increment at bottom of while body before moving on |
| Forgetting to handle missing dict keys | 1 | Use `.get(key, 0)` or `defaultdict(int)` |
| Forgetting to state space complexity | 1 | Always say BOTH time and space |

---

*Updated after every session by your mentor (Copilot)*
