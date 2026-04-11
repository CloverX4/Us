# 03 — Sliding Window

## 🧠 Core Intuition
Sliding window = **"I have a window of elements, and I'm sliding it across the array."**

The magic: instead of recalculating everything for each subarray from scratch (O(n×k)), you **add the new element and remove the old one** → O(n).

**Two types**:
1. **Fixed-size window**: Window size is given (k). Slide by adding right, removing left.
2. **Variable-size window**: Find the min/max window satisfying a condition. Expand right, shrink left.

## 🔑 Key Patterns

### 1. Fixed-Size Window
- **When**: "Maximum sum of subarray of size k", "average of subarrays of size k"
- **Template**:
```python
window_sum = sum(nums[:k])
max_sum = window_sum
for i in range(k, len(nums)):
    window_sum += nums[i] - nums[i - k]  # slide: add right, remove left
    max_sum = max(max_sum, window_sum)
```

### 2. Variable-Size Window (Shrinkable)
- **When**: "Longest/shortest subarray satisfying condition X"
- **Template**:
```python
left = 0
for right in range(len(s)):
    # expand: add s[right] to window state
    
    while window_is_invalid():
        # shrink: remove s[left] from window state
        left += 1
    
    # update answer (window is valid here)
    result = max(result, right - left + 1)
```

### 3. Window with HashMap/Counter
- **When**: Character frequency constraints
- **How**: Maintain a frequency map of the current window

## ⚡ The "Shrink" Decision
The hardest part is knowing **when to shrink**. Ask yourself:
- "If I add this element, does my window become invalid?"
- If yes → shrink from the left until valid again
- If no → expand and update the answer

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Best Time to Buy and Sell Stock | Easy | ⬜ | Track min, update max profit |
| 2 | Longest Substring Without Repeating Characters | Medium | ⬜ | Variable window + set |
| 3 | Longest Repeating Character Replacement | Medium | ⬜ | Variable window + freq count |
| 4 | Permutation in String | Medium | ⬜ | Fixed window + freq match |
| 5 | Minimum Window Substring | Hard | ⬜ | Variable window + freq map |
| 6 | Sliding Window Maximum | Hard | ⬜ | Monotonic deque |

## 💡 Interview Tips
- If the problem says "contiguous subarray/substring" → sliding window is likely
- Always clarify: is the window fixed or variable size?
- For variable windows: "longest" means expand as much as possible; "shortest" means shrink as much as possible
- Draw out the window on paper with 2-3 examples before coding!

## 🔗 Connections to Other Patterns
- Uses **Two Pointers** (left and right)
- Frequency maps connect to **Arrays & Hashing**
- Monotonic deque variant connects to **Stack** (monotonic structures)
- Kadane's algorithm is technically a sliding window!
