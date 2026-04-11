# 10 — Backtracking

## 🧠 Core Intuition
Backtracking = **"Try everything, undo when it doesn't work."**

It's a systematic way to explore all possibilities using recursion. The key:
1. **Choose** — make a decision
2. **Explore** — recurse with that decision
3. **Un-choose** — undo the decision (backtrack)

**When to use**: "Generate ALL possible..." / "Find ALL combinations/permutations/subsets"

## 🔑 Key Patterns

### 1. The Backtracking Template
```python
def backtrack(state, choices):
    if is_goal(state):
        result.append(state.copy())  # IMPORTANT: copy!
        return
    
    for choice in choices:
        if is_valid(choice):
            state.append(choice)      # CHOOSE
            backtrack(state, ...)      # EXPLORE
            state.pop()               # UN-CHOOSE (backtrack!)
```

### 2. Subsets Pattern
- **When**: Generate all subsets
- **Decision**: For each element, include it or don't
```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

### 3. Permutations Pattern
- **When**: Generate all orderings
- **Decision**: Which unused element to place next
```python
def permutations(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

### 4. Combination Sum Pattern
- **When**: Find combinations that sum to target (can reuse elements)
- **Key**: Pass `start` index to avoid duplicates

### 5. Grid Backtracking
- **When**: Word search, N-Queens, Sudoku solver
- **How**: Mark cell visited, explore neighbors, unmark

## ⚡ Subsets vs Permutations vs Combinations
| Type | Order matters? | Reuse? | Use `start` param? |
|------|---------------|--------|-------------------|
| Subsets | No | No | Yes |
| Combinations | No | Depends | Yes |
| Permutations | Yes | No | No (use `used[]`) |

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Subsets | Medium | ⬜ | Subsets template |
| 2 | Subsets II (with duplicates) | Medium | ⬜ | Skip duplicates |
| 3 | Combination Sum | Medium | ⬜ | Combination + reuse |
| 4 | Combination Sum II | Medium | ⬜ | Combination + no reuse |
| 5 | Generate Parentheses | Medium | ⬜ | Constrained combination (open/close tracking) |
| 6 | Permutations | Medium | ⬜ | Permutation template |
| 7 | Word Search | Medium | ⬜ | Grid backtracking |
| 8 | Palindrome Partitioning | Medium | ⬜ | Partitioning |
| 9 | Letter Combinations of Phone Number | Medium | ⬜ | Combination |
| 10 | N-Queens | Hard | ⬜ | Grid + constraint check |

## 💡 Interview Tips
- **Time complexity is usually exponential** — that's EXPECTED. Mention it upfront.
  - Subsets: O(2^n), Permutations: O(n!), Combinations: O(C(n,k))
- Handling duplicates: Sort first, then skip `if i > start and nums[i] == nums[i-1]`
- Always `.copy()` or `[:]` the path before adding to result — classic bug!
- Visualize the recursion tree on paper

## 🔗 Connections to Other Patterns
- Backtracking on tree = **DFS** on **Trees**
- Grid backtracking = **Graph DFS** with visited marking
- Pruning in backtracking → similar to constraint checking in **DP**
- Some backtracking problems can be optimized with **DP** (e.g., Word Break)
