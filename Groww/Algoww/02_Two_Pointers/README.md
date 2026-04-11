# 02 — Two Pointers

## 🧠 Core Intuition
Two pointers work when you can **make a decision about what to do based on the values at the pointers**. Usually one of:
- Move left pointer right (to increase something)
- Move right pointer left (to decrease something)

The key: you're **eliminating possibilities** with each move, bringing O(n²) down to O(n).

## 🔑 Key Patterns

### 1. Opposite-End Pointers
- **When**: Sorted array, find pair with target sum, palindrome check
- **How**: Start at both ends, move inward based on comparison
- **Template**:
```python
left, right = 0, len(arr) - 1
while left < right:
    if condition_met:
        return result
    elif need_bigger:
        left += 1
    else:
        right -= 1
```

### 2. Same-Direction (Fast & Slow)
- **When**: Remove duplicates, cycle detection, partition
- **How**: Slow pointer marks the "write" position, fast pointer scans ahead
- **Template**:
```python
slow = 0
for fast in range(len(arr)):
    if arr[fast] != arr[slow]:
        slow += 1
        arr[slow] = arr[fast]
```

### 3. Three Pointers (Extension)
- **When**: 3Sum, Sort Colors (Dutch National Flag)
- **How**: Fix one pointer, use two-pointer on the rest

## ⚡ When to Use Two Pointers vs HashMap
- **Sorted input** → Two Pointers (O(1) space)
- **Unsorted, need O(n)** → HashMap (O(n) space)
- **Both work?** Mention both in interview, implement the one interviewer prefers

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Valid Palindrome | Easy | ⬜ | Opposite-end |
| 2 | Two Sum II (Sorted) | Medium | ⬜ | Opposite-end |
| 3 | 3Sum | Medium | ⬜ | Fix + two-pointer |
| 4 | Container With Most Water | Medium | ⬜ | Opposite-end, greedy move |
| 5 | Sort Colors | Medium | ⬜ | 3-way partition (Dutch National Flag) |
| 6 | Trapping Rain Water | Hard | ⬜ | Two-pointer with max tracking |

## 💡 Interview Tips
- Two pointers almost always requires **sorted input** (or the array has some order property)
- When they say "O(1) extra space" on an array problem → think two pointers
- Always handle the edge case: what if array has < 2 elements?
- For 3Sum: sort first, then fix one element and two-pointer the rest. Skip duplicates!

## 🔗 Connections to Other Patterns
- Fast & slow pointer → core technique in **Linked List** cycle problems
- Two-pointer shrinking → also used in **Sliding Window**
- Container With Most Water → greedy reasoning connects to **Greedy** pattern
