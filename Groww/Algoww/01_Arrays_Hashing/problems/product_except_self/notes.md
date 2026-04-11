# Product of Array Except Self — Notes

## Pattern: Prefix/Suffix Product (Two-Pass)

## Approach: O(1) Extra Space
1. **Pass 1 (left→right)**: Fill `res[i]` with product of everything LEFT of `i`
2. **Pass 2 (right→left)**: Multiply `res[i]` by running product of everything RIGHT of `i`
3. Both passes start with `curr_fix = 1` (identity for multiplication)

## Key Insight
`answer[i] = (product of all left of i) × (product of all right of i)`

No need for two separate arrays — first pass builds left products into the result, second pass multiplies in right products using a single running variable.

## Why Division is Banned
- Division breaks when array contains **zero(s)**
- One zero: product = 0, dividing by 0 → crash
- Two zeros: every answer should be 0

## Complexity
- **Time**: O(n) — two linear passes
- **Space**: O(1) extra — one variable `curr_fix`. Output array doesn't count.

## Bugs I Hit
- None! Clean solve. ✅

## Growth Observations
- Pattern was already familiar — immediate recognition of prefix/suffix approach
- Went directly for the O(1) space follow-up without needing the two-array version first
- Named the running variable `curr_fix` for clarity — good habit of self-documenting code
- Third consecutive clean solve (Valid Sudoku → Product Except Self → streak continues)
