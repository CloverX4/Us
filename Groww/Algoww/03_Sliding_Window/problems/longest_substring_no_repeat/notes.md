# Longest Substring Without Repeating Characters — Notes

## Pattern
Variable-size sliding window + set for tracking window contents.

## Core Insight
- `r` drives the outer `for` loop (expand)
- Inner `while` shrinks `l` until window is valid (no duplicates)
- Set tracks which characters are in the current window
- Update result after every valid window state

## Template Applied
```python
for r in range(len(s)):
    while s[r] in window_set:       # window invalid?
        window_set.remove(s[l])     # shrink from left
        l += 1
    window_set.add(s[r])            # expand right
    result = max(result, r - l + 1) # update answer
```

## Why O(n) — Not O(n²)
The inner `while` looks like it could make this O(n²), but `l` only moves forward
across the entire execution. Each element is added once and removed at most once.
Total operations: at most 2n → O(n). This is "amortized O(n)."

**Interview line**: "Both pointers only move forward, so each element is processed
at most twice — once when added, once when removed."

## Space Complexity
O(min(n, m)) where m = character set size.
For bounded ASCII (128 chars), can argue O(1). Mention this in interview.

## Window Length
`r - l + 1` (both inclusive) — idiomatic sliding window pattern.
`len(set)` also works in Python (O(1)) but `r - l + 1` is universal.

## Growth Note
Old attempt (Day 6) had `l` as outer driver → r got stuck.
New attempt (Day 12) used correct template → zero bugs, first try.
The difference: understanding that `r` MUST drive the outer loop.
