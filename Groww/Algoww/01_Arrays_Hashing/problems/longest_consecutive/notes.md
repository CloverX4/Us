# Longest Consecutive Sequence — Notes

## Pattern: Set + Sequence Start Detection

## Approach: O(n) with Set
1. Convert array to a **set** (deduplication + O(1) lookups)
2. For each num: if `num - 1` NOT in set → it's a **sequence start**
3. From each start, count forward (`num+1`, `num+2`, ...) while they exist in set
4. Track max length

## Key Insight: `num - 1 not in set` Identifies Sequence Starts
- Without this check: every element tries to count forward → O(n²) worst case
- With this check: only sequence starts trigger the inner while loop
- Each element is visited at most twice (once in for loop, once in a while count) → O(n)

## Why Not Sort?
- Sorting works (O(n log n)) but problem requires O(n)
- Set approach avoids sorting entirely — just existence checks

## Initial Wrong Instinct
- First thought: "sliding pointer, check arr[i+1] == arr[i] + 1" — this solves **consecutive subarray**, not **consecutive sequence**
- Sequence means elements can be **anywhere** in the array — order doesn't matter, only existence
- **Lesson**: Read the problem carefully. "Sequence" ≠ "subarray". Asked for clarification before coding — good instinct.

## Complexity
- **Time**: O(n) — set construction O(n) + each element visited at most twice O(n)
- **Space**: O(n) — the set

## Bugs I Hit
- None! Clean solve. ✅

## Growth Observations
- **Five consecutive clean solves** counting the revision (Valid Sudoku → Product Except Self → Encode/Decode → Longest Consecutive → Top K revision)
- Asked clarifying question about "sequence vs subarray" before coding — this is exactly what you do in interviews
- Immediately grasped the `num - 1` trick after explanation — pattern absorption speed is increasing
- Revision of Top K: zero bugs, used `Counter`, `reversed()`, `res[:k]` — all three original bugs corrected from memory
