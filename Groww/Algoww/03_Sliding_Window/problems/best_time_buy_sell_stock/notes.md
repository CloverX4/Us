# Best Time to Buy and Sell Stock — Notes

## Pattern
Sliding Window (variable) — but with an implicit left pointer (`min_so_far`).

## Core Insight
At each position, the max profit = current price - minimum price seen so far.
One pass: track `min_so_far` and `max_profit` simultaneously.

## Why It's Sliding Window
- `min_so_far` acts as the implicit left pointer (best buy day)
- The current index `i` is the right pointer (potential sell day)
- When we find a new minimum, we're "resetting" the window start — same as `l = r` in explicit two-pointer version
- The pattern is: expand right, reset left when window isn't useful

## Explicit Sliding Window Version
```python
l, r = 0, 1
while r < len(prices):
    if prices[r] > prices[l]:
        max_profit = max(max_profit, prices[r] - prices[l])
    else:
        l = r  # cheaper buy found — shrink/reset
    r += 1
```

## Key Lesson
Patterns are thinking frameworks, not rigid templates. The code can look different
but the decision-making process (expand right, shrink/reset left) is identical.

## Complexity
- Time: O(n) — single pass
- Space: O(1) — two variables

## Edge Cases
- Single element → 0 (can't sell)
- All same prices → 0
- Monotonically decreasing → 0 (min keeps updating, profit never positive)
- Monotonically increasing → buy first, sell last
