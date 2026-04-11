# 15 — Bit Manipulation

## 🧠 Core Intuition
Bit manipulation is about working with numbers at the **binary level**. It's fast (O(1) per operation) and uses no extra space.

**When to think bits**: "Single number", "power of 2", "subsets using bitmask", or when the problem involves XOR/AND/OR operations.

## 🔑 Key Operations

```python
# Basics
a & b     # AND — both bits 1
a | b     # OR — either bit 1
a ^ b     # XOR — bits differ
~a        # NOT — flip all bits
a << n    # Left shift — multiply by 2^n
a >> n    # Right shift — divide by 2^n

# Useful Tricks
n & (n - 1)      # Remove lowest set bit (check power of 2!)
n & (-n)          # Isolate lowest set bit
x ^ x == 0        # XOR with itself = 0 (Single Number!)
x ^ 0 == x        # XOR with 0 = x
bin(n).count('1')  # Count set bits (Python shortcut)
```

## 🔑 Key Patterns

### 1. XOR for Finding Unique
- **When**: "Find the single number" (all others appear twice)
- **Why**: a ^ a = 0, so pairs cancel out!
```python
result = 0
for num in nums:
    result ^= num
return result  # only the unique number remains
```

### 2. Bitmask for Subsets
- **When**: n ≤ 20 and need all subsets
- **How**: Each number from 0 to 2^n represents a subset
```python
for mask in range(1 << n):
    subset = [nums[i] for i in range(n) if mask & (1 << i)]
```

### 3. Counting Bits
- **When**: "Count 1-bits", "Hamming distance"
- **Brian Kernighan's trick**: `n &= (n-1)` removes one set bit each time

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Single Number | Easy | ⬜ | XOR |
| 2 | Number of 1 Bits | Easy | ⬜ | Count bits |
| 3 | Counting Bits | Easy | ⬜ | DP + bit |
| 4 | Reverse Bits | Easy | ⬜ | Bit shift |
| 5 | Missing Number | Easy | ⬜ | XOR or math |
| 6 | Sum of Two Integers | Medium | ⬜ | Bit addition |

## 💡 Interview Tips
- XOR is your best friend for "find the odd one out" problems
- `n & (n-1) == 0` checks if n is a power of 2 — classic one-liner
- Bitmask DP: when n is small (≤ 20), you can represent subsets as integers

## 🔗 Connections to Other Patterns
- Bitmask subsets → alternative to **Backtracking** for small n
- Bitmask DP → combines with **Dynamic Programming**
