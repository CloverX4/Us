# 12 — Dynamic Programming

## 🧠 Core Intuition
DP = **Recursion + Memoization** (top-down) or **Building up from base cases** (bottom-up).

The key question: **"Can I break this problem into overlapping subproblems?"**

If yes, and the problem has **optimal substructure** (optimal solution uses optimal solutions to subproblems), it's DP.

### The DP Thinking Framework (Use This Every Time!)
1. **Define the state**: What does `dp[i]` (or `dp[i][j]`) represent?
2. **Find the recurrence**: How does `dp[i]` relate to smaller subproblems?
3. **Identify base cases**: What are the trivial cases?
4. **Determine order**: Bottom-up: fill smallest states first. Top-down: recurse + memo.
5. **Optimize space** (optional): Do I only need the previous row/state?

## 🔑 Key Patterns

### 1. Linear DP (1D)
- **When**: Decision at each step depends on previous steps
- **State**: `dp[i]` = answer considering first `i` elements
```python
# Climbing Stairs
dp[0] = 1; dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
```

### 2. Two-String DP (2D)
- **When**: Compare/match two strings or sequences
- **State**: `dp[i][j]` = answer for first `i` chars of s1 and first `j` chars of s2
```python
# Longest Common Subsequence
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

### 3. Knapsack Pattern
- **When**: "Select items with weight/cost constraint to maximize value"
- **0/1 Knapsack**: Each item used once → `dp[i][w]`
- **Unbounded Knapsack**: Items can be reused → `dp[w]`
```python
# 0/1 Knapsack
for i in range(1, n + 1):
    for w in range(W, weights[i-1] - 1, -1):  # reverse to avoid reuse
        dp[w] = max(dp[w], dp[w - weights[i-1]] + values[i-1])
```

### 4. Grid DP
- **When**: Paths in a grid, minimum cost path
- **State**: `dp[i][j]` = answer to reach cell (i, j)
```python
# Unique Paths
for i in range(m):
    for j in range(n):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

### 5. Decision Making DP
- **When**: At each step, choose to "take" or "skip"
- **Classic**: House Robber, Buy/Sell Stock
```python
# House Robber: rob or skip
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
```

### 6. Interval DP
- **When**: Optimal way to split/merge intervals
- **State**: `dp[i][j]` = answer for range [i, j]

## ⚡ Top-Down vs Bottom-Up
| Aspect | Top-Down (Memo) | Bottom-Up (Tabulation) |
|--------|----------------|----------------------|
| Style | Recursive | Iterative |
| Ease | More intuitive | More efficient |
| Space | Call stack + memo | Table only |
| When | Complex DP states | When you can define clear order |

```python
# TOP-DOWN
from functools import lru_cache
@lru_cache(maxsize=None)
def dp(i):
    if i <= 1: return i
    return dp(i-1) + dp(i-2)

# BOTTOM-UP
dp = [0] * (n + 1)
dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
```

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Climbing Stairs | Easy | ⬜ | Linear 1D |
| 2 | Min Cost Climbing Stairs | Easy | ⬜ | Linear 1D |
| 3 | House Robber | Medium | ⬜ | Decision (take/skip) |
| 4 | House Robber II | Medium | ⬜ | Circular + Decision |
| 5 | Longest Palindromic Substring | Medium | ⬜ | Expand or 2D |
| 6 | Decode Ways | Medium | ⬜ | Linear 1D (tricky) |
| 7 | Coin Change | Medium | ⬜ | Unbounded Knapsack |
| 8 | Coin Change II | Medium | ⬜ | Unbounded Knapsack (count ways, not min) |
| 9 | Maximum Product Subarray | Medium | ⬜ | Dual-state DP (track min AND max) |
| 10 | Unique Paths | Medium | ⬜ | Grid DP |
| 11 | Longest Common Subsequence | Medium | ⬜ | Two-string 2D |
| 12 | Word Break | Medium | ⬜ | Linear DP + set |
| 13 | Partition Equal Subset Sum | Medium | ⬜ | 0/1 Knapsack |
| 14 | Edit Distance | Medium | ⬜ | Two-string 2D |
| 15 | Longest Increasing Subsequence | Medium | ⬜ | Linear DP (or binary search) |
| 16 | Target Sum | Medium | ⬜ | Knapsack variant |
| 17 | Burst Balloons | Hard | ⬜ | Interval DP |

## 💡 Interview Tips
- **START with recursion** (brute force), then add memoization — interviewers love this progression
- ALWAYS define what `dp[i]` means before writing code. Say it out loud in the interview!
- If you can't figure out the recurrence: try small examples (n=1, 2, 3) and see the pattern
- Space optimization: if `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, use two variables!
- Common mistake: off-by-one in base cases. Always verify with the smallest input.

## 🔗 Connections to Other Patterns
- DP on strings → **Two Pointers** can sometimes give simpler solutions
- DP on trees → combine with **Tree DFS** (post-order)
- Knapsack → variant of **Backtracking** with pruning and memoization
- Some DP problems can be solved greedily → connects to **Greedy**
