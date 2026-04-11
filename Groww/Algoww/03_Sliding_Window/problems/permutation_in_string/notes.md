# Permutation in String — Notes

## Pattern
Fixed-Size Sliding Window + Frequency Map Comparison

## Core Insight
- A permutation of s1 has the same frequency map as s1
- Window size is always `len(s1)` — fixed, because permutations have the same length
- Slide a fixed window across s2, compare frequency maps at each step

## Three Approaches (Brute → Optimal)

### v1: Rebuild Counter each step — O(n*k) time
- Slice the window and create a new Counter each iteration
- Simple but redundant — recomputes frequencies for overlapping substrings

### v2: True sliding window — O(n) time (with O(26) comparison)
- Precompute Counter for first window
- Each step: add right char, compare maps, remove left char
- Comparison is O(26) per step → O(26n) → O(n)

### v3 (TODO): Matches counter — O(n) time (true O(1) per step)
- Track a `matches` variable: how many of 26 chars have equal frequency in both maps
- On add/remove: only update the affected char's match status (±1)
- `matches == 26` → return True
- Eliminates the O(26) comparison entirely

## Python Detail
- `Counter({'a': 2, 'b': 0}) == Counter({'a': 2})` → **True**
- Counter ignores zero-count keys in equality — safe to decrement without cleanup
- A plain `dict` or `defaultdict` would NOT behave this way — zero-count keys break equality

## Complexity
| Version | Time | Space |
|---------|------|-------|
| v1 | O(n*k) | O(k) |
| v2 | O(26*n) = O(n) | O(1) — bounded by 26 |
| v3 | O(n) true | O(1) |

## What I Struggled With
- Initially thought of variable window (expand on match, reset on miss) — wrong for permutations
- Needed reminder that fixed-size is the right call because permutations have fixed length
- v2 came naturally once the fixed-size template clicked

## Interview Tips
- "Permutation = same frequency map" — state this immediately
- "Window size is fixed at len(s1) because permutations preserve length" — shows you identified the constraint
- Know the matches optimization exists even if you code v2 — mention it: "We could also track a matches variable for O(1) comparison"
