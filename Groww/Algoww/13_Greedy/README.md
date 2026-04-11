# 13 — Greedy

## 🧠 Core Intuition
Greedy = **Make the locally optimal choice at each step, hoping it leads to a globally optimal solution.**

The tricky part: **proving it works**. Not all problems that look greedy are actually greedy. When in doubt, try DP first.

**When greedy works**: The problem has the **greedy choice property** — a locally optimal choice is part of a globally optimal solution.

## 🔑 Key Patterns

### 1. Interval Scheduling
- **When**: "Maximum non-overlapping intervals", "minimum rooms"
- **Greedy rule**: Sort by end time, always pick the earliest ending interval
```python
intervals.sort(key=lambda x: x[1])  # sort by end
count, end = 0, float('-inf')
for s, e in intervals:
    if s >= end:
        count += 1
        end = e
```

### 2. Greedy with Sorting
- **When**: Assign items optimally (meeting rooms, gas stations)
- **How**: Sort by some property, then make greedy choices

### 3. Jump Game Style
- **When**: "Can you reach the end?", "Minimum jumps"
- **How**: Track the farthest you can reach at each step
```python
def can_jump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest: return False
        farthest = max(farthest, i + nums[i])
    return True
```

### 4. Running Max/Min Decision
- **When**: "Maximum profit", "best time to buy/sell"
- **How**: Track running minimum/maximum, update answer

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Maximum Subarray (Kadane's) | Medium | ⬜ | Running sum |
| 2 | Jump Game | Medium | ⬜ | Farthest reach |
| 3 | Jump Game II | Medium | ⬜ | BFS-style greedy |
| 4 | Gas Station | Medium | ⬜ | Circular greedy |
| 5 | Hand of Straights | Medium | ⬜ | Greedy + HashMap |
| 6 | Partition Labels | Medium | ⬜ | Last occurrence greedy |

## 💡 Interview Tips
- If you think it's greedy, **verify with a counterexample** — try to break your greedy approach
- If you can't prove greedy works → fall back to DP
- Many greedy problems require **sorting first** — ask "What if I sort by X?"
- Kadane's algorithm is both greedy AND DP — understand both perspectives

## 🔗 Connections to Other Patterns
- Greedy with sorting → connects to **Intervals**
- Greedy vs DP → many problems can be solved both ways
- Greedy with heap → connects to **Heap/Priority Queue**
