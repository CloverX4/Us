# 04 — Stack

## 🧠 Core Intuition
A stack is **LIFO (Last In, First Out)**. Think of it as: "I need to remember something, and I'll need the most recent thing first."

**The golden rule**: Use a stack when you need to **match or compare with the most recent unresolved element**.

## 🔑 Key Patterns

### 1. Matching / Balancing
- **When**: Parentheses matching, tag matching, undo operations
- **How**: Push opening elements, pop when you find a closing match
```python
stack = []
for char in s:
    if char in '({[':
        stack.append(char)
    else:
        if not stack or not matches(stack[-1], char):
            return False
        stack.pop()
return len(stack) == 0
```

### 2. Monotonic Stack
- **When**: "Next greater/smaller element", "daily temperatures", "largest rectangle"
- **How**: Maintain a stack where elements are always increasing (or decreasing)
- **Key insight**: When a new element breaks the monotonic property, pop and process
```python
stack = []  # stores indices
result = [0] * len(nums)
for i, num in enumerate(nums):
    while stack and nums[stack[-1]] < num:
        idx = stack.pop()
        result[idx] = num  # num is the next greater element for nums[idx]
    stack.append(i)
```

### 3. Expression Evaluation
- **When**: Evaluate postfix, infix expressions, calculate results
- **How**: Push operands, pop when you see an operator

### 4. Stack for Simulation
- **When**: Car fleet, asteroid collision — simulate a process
- **How**: Push elements, process collisions/merges with stack top

## ⚡ Monotonic Stack Cheat Sheet
| Want | Stack Order | Pop When |
|------|-------------|----------|
| Next Greater Element | Decreasing | New > top |
| Next Smaller Element | Increasing | New < top |
| Previous Greater | Decreasing | New > top |
| Previous Smaller | Increasing | New < top |

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Valid Parentheses | Easy | ⬜ | Matching |
| 2 | Min Stack | Medium | ⬜ | Auxiliary stack |
| 3 | Evaluate Reverse Polish Notation | Medium | ⬜ | Expression eval |
| 4 | Daily Temperatures | Medium | ⬜ | Monotonic stack |
| 5 | Car Fleet | Medium | ⬜ | Stack simulation |
| 6 | Largest Rectangle in Histogram | Hard | ⬜ | Monotonic stack |

## 💡 Interview Tips
- If you see "next greater/smaller" — it's monotonic stack, 100%
- Stack problems often have O(n) time even though they look O(n²) — each element is pushed and popped at most once
- In Python, use `list` as a stack: `append()` to push, `pop()` to pop, `[-1]` to peek

## 🔗 Connections to Other Patterns
- Monotonic stack → used in **Sliding Window Maximum** (deque variant)
- Expression evaluation → foundation for **Tree** traversals (iterative)
- DFS uses a stack (explicitly or via recursion)
