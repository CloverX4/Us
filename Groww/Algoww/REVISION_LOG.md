# 🔄 Revision Log & Quiz History

> Track all quizzes, revision sessions, and spaced repetition here.

---

## 📋 Quiz History

| # | Date | Type | Question | Your Answer | Correct? | Topic | Revisit? |
|---|------|------|----------|-------------|----------|-------|----------|
| 1 | Mar 12 | Concept | Subarray Sum = K: What pattern? Why not sliding window? What's the {0:1} base case? | Prefix sum + hashmap complement. Negatives break window shrink/expand logic. {0:1} = empty prefix so subarrays starting at idx 0 are counted. | 2.5/3 — pattern & sliding window reasoning perfect, base case needed walkthrough to own | Arrays & Hashing | No |
| 2 | Mar 17 | Spot Check (3Q) | Q1: Unsorted two-sum pattern+complexity. Q2: Group Anagrams hashmap key options. Q3: Can sliding window find subarray sum with negatives? | Q1: Hashmap complement O(n)/O(n), or sort+two-pointer O(n log n)/O(1) — perfect. Q2: Said "frequency map" but forgot it must be tuple (unhashable dict). Q3: No, negatives break shrink logic — perfect. | 2.5/3 — Q2 half credit: knew the idea, forgot tuple detail | Arrays & Hashing | Yes — review Group Anagrams key encoding |
| 3 | Mar 24 | Revision (4Q) | Q1: Longest substr with at most k distinct — shrink when? Q2: Why len(t_freq_map) not len(t)? Q3: Fill sliding window comparison table. Q4: Key insight for longest vs shortest window? | Q1: Shrink when invalid (distinct > k) — perfect. Q2: Right direction but no concrete example. Q3: Mostly correct, Permutation in String described with wrong approach (expand/reset instead of fixed-size). Q4: Shrink when invalid = max, shrink when valid = min — perfect. | 3.5/4 — Q2 half credit, Q3 Permutation in String needs review | Sliding Window | Yes — re-read Permutation in String notes |

---

## 🔁 Spaced Repetition Queue

Problems that need to be revisited (auto-populated during sessions):

### 🔴 Due for Revision (Overdue)
*(none)*

### 🟡 Coming Up This Week
- **Group Anagrams — key encoding** (Arrays & Hashing): When using a frequency map as a dict key, it must be a **tuple**, not a list or dict (unhashable types). `tuple(count)` where count is a 26-length frequency array. Flagged in Quiz #2 — half credit, knew the idea but forgot tuple detail. Revisit before Week 3 Day 6 quiz.

### 🟢 Mastered (No longer need revision)
*(none yet)*

---

## 📅 Revision Sessions

### Revision #1 — Date: ___
- **Problems Revisited**: 
- **Could solve without hints?**: 
- **Time taken vs original**: 
- **Notes**: 

---

## 🧠 Concept Quick-Reference (Built During Quizzes)

> When you get a quiz wrong, the correct answer gets added here for rapid review

### Arrays & Hashing
- *(concepts added as we go)*

### Two Pointers
- 

### Sliding Window
- `while` vs `if` for shrinking in Longest Repeating Character Replacement: `if` works because max_freq never decreases and r moves by 1 — overshoot is at most 1
- Space is O(1) when map keys are bounded by alphabet size (26), not input size

### Stack
- 

### Binary Search
- 

### Linked Lists
- 

### Trees
- 

### Heaps
- 

### Backtracking
- 

### Graphs
- 

### Dynamic Programming
- 

### Greedy
- 

---

*Updated after every quiz and revision session*
