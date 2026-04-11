# 16 — Math & Geometry

## 🧠 Core Intuition
These problems test mathematical reasoning. No fancy data structures — just logic, modular arithmetic, and geometric thinking.

## 🔑 Key Concepts

### Modular Arithmetic
```python
(a + b) % m = ((a % m) + (b % m)) % m
(a * b) % m = ((a % m) * (b % m)) % m
```

### Matrix Rotation
- **90° clockwise**: Transpose + reverse each row
- **90° counter-clockwise**: Reverse each row + transpose
```python
# 90° clockwise rotation
def rotate(matrix):
    n = len(matrix)
    # Transpose
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse rows
    for row in matrix:
        row.reverse()
```

### Spiral Traversal
- Use 4 boundaries (top, bottom, left, right), shrink inward

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Happy Number | Easy | ⬜ | Cycle detection (fast/slow) |
| 2 | Plus One | Easy | ⬜ | Carry simulation |
| 3 | Rotate Image | Medium | ⬜ | Transpose + reverse |
| 4 | Spiral Matrix | Medium | ⬜ | Boundary shrinking |
| 5 | Set Matrix Zeroes | Medium | ⬜ | In-place marking |
| 6 | Pow(x, n) | Medium | ⬜ | Fast exponentiation |
| 7 | Reverse Integer | Medium | ⬜ | Digit extraction + overflow handling |
| 8 | Multiply Strings | Medium | ⬜ | Grade-school multiplication |

## 💡 Interview Tips
- For rotation problems: Always try transpose + reverse first
- Spiral: track boundaries carefully, update after each direction
- Modular arithmetic: use it whenever numbers can overflow

## 🔗 Connections to Other Patterns
- Happy Number uses **Floyd's cycle detection** (**Linked List** pattern)
- Matrix problems use **2D array** traversal skills
- Pow(x, n) → **Divide and Conquer** / binary exponentiation
