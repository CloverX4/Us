# Minimum Window Substring — Notes

## Pattern
Variable-Size Sliding Window + Frequency Map + Have/Need Counter

## Core Insight
- Track `have` (chars meeting required frequency) vs `need` (unique chars in t)
- Window is **valid** when `have == need`
- **Shrink while valid** (opposite of longest-type problems where you shrink when invalid)
- Goal: find the **smallest** valid window

## Key Difference: Minimum vs Maximum Sliding Window
| | Maximum (e.g., Longest Substring) | Minimum (this problem) |
|---|---|---|
| **Expand** | Always (r moves each iteration) | Always (r moves each iteration) |
| **Shrink** | When window is **invalid** | When window is **valid** |
| **Goal** | Largest valid window | Smallest valid window |
| **Update answer** | After ensuring valid | While window is still valid (during shrink) |

## Have/Need Pattern
```python
need = len(t_freq_map)        # unique chars required
have = 0                       # unique chars currently satisfied

# On add (expand right):
if window_freq[c] == t_freq[c]:   # just reached required count
    have += 1

# On remove (shrink left):
if window_freq[c] < t_freq[c]:    # just dropped below required
    have -= 1
```

This is the same concept as the `matches` counter from Permutation in String — but here it feels natural because you NEED it to know when the window is valid.

## Complexity
- **Time**: O(m + n) — O(n) to build t_freq_map, O(m) for sliding window (l and r each traverse s at most once)
- **Space**: O(n + m) worst case for freq maps — but bounded by character set size, so effectively O(1) for alphabet-constrained inputs

## What I Struggled With
- Initially confused about what makes the window valid/invalid
- First attempt had bugs:
  - Compared `matches_count == len(t)` instead of `len(t_freq_map)` (unique chars, not total)
  - Tracked best window outside the shrink loop (missed smaller valid windows during shrink)
  - `.keys` vs `.keys()` (method call needs parentheses)
  - Used `!=` instead of `<` for shrink condition (must be "dropped below", not "any mismatch")
- Fixed iteratively during the session

## Connection to Previous Problems
- **Permutation in String**: Same frequency matching concept, but fixed-size window with exact match
- **Longest Substring Without Repeating**: Same variable-size template, but opposite shrink condition (shrink when invalid, not when valid)
- **Longest Repeating Char Replacement**: Same have/need intuition but expressed differently (max_freq instead of explicit counter)

## Interview Tips
- State upfront: "This is a minimum window problem, so I'll shrink while the window is valid"
- Mention O(m + n) complexity — interviewers appreciate the separate terms
- The `have/need` pattern is reusable — mention it: "I'm using a have/need counter to avoid O(52) comparison each step"
