# Two Sum — Notes

## Pattern Used
**Complement pattern with HashMap (Index Mapping)**

## Key Insight
Don't search for pairs. For each number, compute `target - num` (complement) and check if you've already seen it. Check BEFORE storing to handle duplicate values like [3,3].

## Approach
- Single pass through array
- For each element: compute complement, check map, then store `{num: index}`
- Check before store order is critical for duplicate values

## Things to Remember
- **Read constraints carefully** — "exactly one solution" means no edge case handling for 0 or multiple answers
- "May not use the same element twice" → check before store
- Set = existence only. Dict = existence + associated data (index, count)
- The unnecessary guard `if nums[i] not in idx_map` — not needed since check happens before store and exactly one solution guaranteed. Less code = fewer bugs.
- Both `{num: index}` and `{complement: index}` approaches work — pick one and be consistent

## Bugs / Learnings
- Initially confused complement-as-key vs num-as-key — both valid, different mental models
- Constraint "exactly one solution" is a HINT, not fluff — always read them

## Complexity
- **Time**: O(n) — single pass
- **Space**: O(n) — hashmap stores up to n elements
