# Longest Repeating Character Replacement — Notes

## Pattern
Variable-Size Sliding Window + Frequency Map

## Core Insight
- Track the frequency of each character in the current window
- The number of replacements needed = (window size) - (max frequency char count)
- If replacements > k → shrink window from left
- You only care about the COUNT of the most frequent char, not WHICH char it is — because the goal is to minimize replacements

## Key Formula
```
replacements_needed = (r - l + 1) - max_freq
if replacements_needed > k: shrink
```

## `while` vs `if` for shrinking
- `while` is always safe (standard sliding window)
- `if` also works here because:
  - r only moves by 1 each iteration → window grows by at most 1
  - `max_freq` never decreases (it's a historical max, not recalculated)
  - So the condition can overshoot by at most 1 → single shrink is enough
- With `if`, the window "slides" (holds size) when invalid, only grows when a better max_freq appears

### Trace: `if` behavior with s="aaabacdae", k=2
```
r=5 (c): l=0, window="aabacc", freq={a:4,b:1,c:1}, max_freq=4
         replacements=6-4=2 ≤ k ✓   result=6

r=6 (d): l=0, freq={a:4,b:1,c:1,d:1}, max_freq=4
         replacements=7-4=3 > k ✗
         if: remove s[0]='a', l=1 → window slides, size stays 6
         result=6

r=7 (a): l=1, freq={a:4,b:1,c:1,d:1}, max_freq=4
         replacements=7-4=3 > k ✗
         if: remove s[1]='a', l=2 → slides again, size stays 6
         result=6

r=8 (e): l=2, freq={a:3,b:1,c:1,d:1,e:1}, max_freq=4
         replacements=7-4=3 > k ✗
         if: remove s[2]='a', l=3 → slides again, size stays 6
         result=6 ✅
```
Key: once the window hits its best size, `if` just slides it forward (l and r both +1).
It can only GROW again when max_freq increases. No need to shrink further — we already recorded the best answer.

## Complexity
- **Time**: O(n) — both l and r traverse the string at most once
- **Space**: O(1) — frequency map bounded by 26 uppercase letters (constant)

## Compared to Longest Substring Without Repeating Characters
| | No Repeats | Character Replacement |
|---|---|---|
| **Data structure** | Set (track unique chars) | Frequency map (track counts) |
| **Window invariant** | All chars unique | replacements ≤ k |
| **Shrink trigger** | Duplicate char found | (window size - max_freq) > k |
| **What you track** | Presence of chars | Count of most frequent char |
| **Space** | O(min(n, m)) | O(1) — bounded by alphabet |

## What I Struggled With
- Couldn't initially visualize how to track the most frequent character in the window
- Needed the loop structure hint to realize: just update max_freq each iteration as r expands
- Key realization: you don't need the character itself, just its count

## Interview Tips
- "The map is bounded by alphabet size (26), so space is O(1)" — interviewers love this
- Google follow-up: "while vs if?" — explain why if works (max_freq never decreases + r moves by 1)
- Always state the invariant before coding: "The window is valid when replacements needed ≤ k"
