# Top K Frequent Elements — Notes

## Pattern: Frequency Counting + Bucket Sort

## Approach: Bucket Sort (O(n) time)
1. **Count frequencies** using `defaultdict(int)` → `{num: count}`
2. **Create bucket array** of size `n+1` (index = frequency, value = list of nums)
3. **Walk buckets backwards** (highest freq first), collect until we have k items
4. **Slice** `res[:k]` to return exactly k elements

## Why Bucket Sort?
- Sorting approach: O(n log n) — doesn't meet follow-up requirement
- Heap approach: O(n log k) — better, but needs heap knowledge
- Bucket sort: O(n) — uses frequency as array index, no comparison sorting needed
- **Key insight**: Max possible frequency = n (length of array), so bucket array is bounded

## Complexity
- **Time**: O(n) — frequency counting O(n) + bucket fill O(n) + collection O(n)
- **Space**: O(n) — frequency map O(n) + bucket array O(n)

## Bugs I Hit
1. **`buckets.reverse()` returns `None`** — in-place methods in Python return None. Use `reversed()` to iterate backwards without modifying the list.
2. **Off-by-one with `res[:target+1]`** — slicing by the wrong variable. `res[:k]` gives k elements (indices 0 to k-1).
3. **Mutating parameter `k` then needing original** — introduced `target` variable to compensate. Cleaner: keep `k` untouched and use `len(res) == k` for early exit.

## Key Takeaways
- **In-place vs return-value**: `.sort()`, `.reverse()`, `.append()` return `None`. `sorted()`, `reversed()` return new objects.
- **Don't mutate function parameters** — if you need a backup variable, rethink the loop.
- **Early termination** > collect-everything-then-slice: `return` as soon as you have k items.
- **Read the problem**: "answer is unique" = no ties at boundary, "any order" = no need to sort result.

## Alternative Approaches
- `Counter(nums).most_common(k)` — one-liner but uses heap internally (O(n log k))
- `sorted(freq.keys(), key=lambda x: freq[x], reverse=True)[:k]` — O(n log n)
- Heap with `heapq.nlargest(k, freq.keys(), key=freq.get)` — O(n log k)
