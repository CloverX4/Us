# 05 — Binary Search

## 🧠 Core Intuition
Binary search isn't just "search in a sorted array." It's about **eliminating half the search space with each decision**.

**The deeper insight**: Binary search works whenever you have a **monotonic predicate** — a condition that goes from False to True (or True to False) at some point. You're finding that transition point.

## 🔑 Key Patterns

### 1. Classic Binary Search
- **When**: Find a target in a sorted array
```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoid overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### 2. Binary Search on Answer (Parametric Search)
- **When**: "Minimum/maximum value that satisfies a condition"
- **How**: Instead of searching an array, search the **answer space**
- **Template**:
```python
def binary_search_on_answer(lo, hi):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if condition(mid):  # can we achieve it with `mid`?
            hi = mid        # try smaller
        else:
            lo = mid + 1    # need bigger
    return lo
```
- **Examples**: Koko Eating Bananas, Split Array Largest Sum, Capacity to Ship

### 3. Rotated/Modified Array Search
- **When**: Sorted array with a twist (rotation, duplicates)
- **Key**: One half is always sorted. Determine which half, then decide.

### 4. Bisect Left / Bisect Right
- **When**: Find insertion point, find first/last occurrence
```python
import bisect
# bisect_left: first position where target can be inserted
# bisect_right: last position where target can be inserted
```

## ⚡ The Three Templates
| Template | Loop Condition | Update | Returns |
|----------|---------------|--------|---------|
| Exact match | `lo <= hi` | `lo = mid+1` / `hi = mid-1` | exact index or -1 |
| Left boundary | `lo < hi` | `lo = mid+1` / `hi = mid` | first True |
| Right boundary | `lo < hi` | `lo = mid` / `hi = mid-1` | last True (careful!) |

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Binary Search | Easy | ⬜ | Classic |
| 2 | Search a 2D Matrix | Medium | ⬜ | Flatten to 1D binary search |
| 3 | Koko Eating Bananas | Medium | ⬜ | Binary search on answer |
| 4 | Search in Rotated Sorted Array | Medium | ⬜ | Modified array |
| 5 | Find Minimum in Rotated Sorted Array | Medium | ⬜ | Modified array |
| 6 | Time Based Key-Value Store | Medium | ⬜ | Bisect right |
| 7 | Median of Two Sorted Arrays | Hard | ⬜ | Binary search on partition |

## 💡 Interview Tips
- **ALWAYS** use `mid = lo + (hi - lo) // 2` instead of `(lo + hi) // 2` (overflow safe)
- When stuck: ask "Can I binary search the answer?" — surprisingly often, YES
- Off-by-one errors are the #1 bug. Trace through with a 2-element array to verify
- If constraints say n ≤ 10^5 and you need better than O(n) → binary search

## 🔗 Connections to Other Patterns
- Binary search on answer → used in **Greedy** verification problems
- Matrix search → connects to **2D array** problems
- Used inside **Trees** (BST operations are binary search!)
