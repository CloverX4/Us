# 01 — Arrays & Hashing

## 🧠 Core Intuition
Arrays and hash maps are the **bread and butter** of interviews. Nearly every problem touches them. The key insight: **hash maps trade space for time** — when you need O(1) lookups, think hashmap.

## 🔑 Key Patterns

### 1. Frequency Counting
- **When**: Problems about duplicates, anagrams, "most frequent", "top K"
- **How**: Use `collections.Counter` or a `defaultdict(int)`
- **Template**:
```python
from collections import Counter
freq = Counter(nums)
# Now freq[x] gives count of x in O(1)
```

### 2. Two-Pass with HashMap
- **When**: "Find two elements that satisfy X" (Two Sum is the classic)
- **How**: First pass builds the map, second pass queries it (or single pass)
- **Key Insight**: Instead of checking all pairs O(n²), ask "does the complement exist?"

### 3. Index Mapping
- **When**: Need to remember where elements are
- **How**: `{value: index}` mapping

### 4. Prefix Sum
- **When**: "Sum of subarray", "product except self"
- **How**: Build cumulative sum array, then range_sum(i,j) = prefix[j] - prefix[i-1]

### 5. Set for O(1) Existence
- **When**: "Does X exist in the collection?"
- **How**: Convert list to set for O(1) lookup

## ⚡ Complexity Cheat Sheet
| Operation | Array | HashMap | Set |
|-----------|-------|---------|-----|
| Access by index | O(1) | — | — |
| Search | O(n) | O(1) avg | O(1) avg |
| Insert | O(n)* | O(1) avg | O(1) avg |
| Delete | O(n) | O(1) avg | O(1) avg |

*O(1) amortized for append at end

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Contains Duplicate | Easy | ✅ | Set |
| 2 | Valid Anagram | Easy | ✅ | Frequency Count |
| 3 | Two Sum | Easy | ✅ | HashMap Complement |
| 4 | Group Anagrams | Medium | ✅ | Sorted Key HashMap |
| 5 | Top K Frequent Elements | Medium | ✅ | Frequency + Bucket Sort |
| 6 | Valid Sudoku | Medium | ✅ | Set per row/col/box |
| 7 | Product of Array Except Self | Medium | ✅ | Prefix/Suffix |
| 8 | Encode and Decode Strings | Medium | ✅ | Delimiter Design |
| 9 | Longest Consecutive Sequence | Medium | ✅ | Set + Sequence Start |

## 💡 Interview Tips
- Always ask: "Can I use extra space?" — this opens the door to hashmaps
- Sorting is O(n log n) — sometimes a hashmap gives you O(n)
- Python's `defaultdict` and `Counter` are your best friends
- When you see "subarray sum equals K" → think prefix sum + hashmap

## 🔗 Connections to Other Patterns
- Frequency counting → directly feeds into **Heap/Top-K** problems
- Prefix sum → foundation for **Sliding Window** optimization
- Hash sets → used heavily in **Graph** visited tracking
