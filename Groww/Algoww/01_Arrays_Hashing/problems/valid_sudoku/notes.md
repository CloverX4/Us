# Valid Sudoku — Notes

## Pattern: Set per Constraint Group (Row / Col / Box)

## Approach: Single-Pass with 27 Sets
1. Create `defaultdict(set)` for rows, cols, and boxes
2. Single pass over all 81 cells
3. Skip `'.'`
4. If number already in row[r], col[c], or box[(r//3, c//3)] → invalid
5. Otherwise add to all three sets
6. Finish loop → valid

## Key Insight: `(r // 3, c // 3)` maps any cell to its 3×3 box
- Integer division groups `0,1,2 → 0` and `3,4,5 → 1` and `6,7,8 → 2`
- Don't confuse with `% 3` (modulo cycles back: 0,1,2,0,1,2...)

## Complexity
- **Time**: O(81) = O(1) — board is always 9×9
- **Space**: O(27 × 9) = O(1) — 27 sets, max 9 elements each = 243 values max

## Space Concern — Resolved
- 27 sets sounds like a lot, but max 243 values (~2KB) is constant
- **Rule**: If it doesn't scale with input, it's free. Worry about space only when it grows with n.
- Alternative: 3-pass with 1 reused set — same complexity, more code, more bug surface

## Alternative: 3-Pass (Tiled Iteration for Boxes)
- Pass 1: Check rows (straightforward)
- Pass 2: Check cols (swap r/c)
- Pass 3: Check boxes using **block decomposition**:
  - Outer: `range(0, 9, 3)` for row/col start → anchor points
  - Inner: `range(anchor, anchor + 3)` → fills in the 3×3 block

## Patterns Learned
- **Tiled/Block iteration**: `range(0, n, step)` for anchors + `range(anchor, anchor + step)` for block contents
- **Bound checking trick**: Plug in n=5 with small k to verify bounds. Don't memorize formulas.
- **`range()` gotcha**: Last valid index is `n-k`, but `range` excludes upper bound, so use `range(n - k + 1)`
- **Merging loops**: When multiple checks share the same iteration space, merge into one pass with parallel data structures

## Bugs I Hit
- None! First clean solve. ✅

## Growth Observations
- **First zero-bug solve** — shows the debugging muscles from Top K (same session) are already paying off. Reading code more carefully before running.
- **Questioned the "standard" approach** — felt 27 sets was wasteful and asked if there's a better way. That's an engineer's instinct: don't blindly accept solutions, interrogate them. Resolved through quantitative analysis (243 values = ~2KB = nothing).
- **Asked to learn the alternative approach even after solving it** — intellectual curiosity beyond "just pass the test." Understanding WHY one approach wins over another is what separates interviewees who memorize from those who reason.
- **Caught the `//` vs `%` confusion before coding** — self-corrected during planning phase, not debugging phase. That's the goal: catch mistakes on paper, not in code.
- **Connected patterns across problems** — recognized tiled iteration reappears in graphs, sliding window, and backtracking. Building a mental web, not isolated solutions.
