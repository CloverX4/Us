# ⚡ Complexity Cheat Sheet

> Quick reference during problem solving. Print this. Memorize this.

---

## 🕐 Time Complexity Guide

### What Fits in the Constraints?
| n (input size) | Max Acceptable Complexity | Common Algorithms |
|----------------|--------------------------|------------------|
| n ≤ 10 | O(n!) | Permutations, brute force |
| n ≤ 20 | O(2^n) | Bitmask, backtracking with pruning |
| n ≤ 100 | O(n³) | Floyd-Warshall, 3 nested loops |
| n ≤ 1,000 | O(n²) | Brute force pairs, simple DP |
| n ≤ 10^5 | O(n log n) | Sorting, divide & conquer, heap |
| n ≤ 10^6 | O(n) | Linear scan, hashing, sliding window |
| n ≤ 10^9 | O(log n) or O(√n) | Binary search, math |
| n ≤ 10^18 | O(log n) | Binary exponentiation |

---

## 📊 Data Structure Operations

| Structure | Access | Search | Insert | Delete | Notes |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(1) append amortized |
| Linked List | O(n) | O(n) | O(1)* | O(1)* | *at known position |
| Hash Map | — | O(1)† | O(1)† | O(1)† | †average case |
| Hash Set | — | O(1)† | O(1)† | O(1)† | †average case |
| Stack | O(n) | O(n) | O(1) | O(1) | LIFO |
| Queue | O(n) | O(n) | O(1) | O(1) | FIFO |
| Heap | — | O(n) | O(log n) | O(log n) | O(1) peek min/max |
| BST (balanced) | — | O(log n) | O(log n) | O(log n) | Sorted order |
| Trie | — | O(L) | O(L) | O(L) | L = word length |

---

## 🔢 Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable? |
|-----------|------|---------|-------|-------|---------|
| Python `sort()` | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Bucket Sort | O(n) | O(n) | O(n²) | O(n) | Yes |

---

## 🌳 Tree / Graph Complexities

| Algorithm | Time | Space | When to Use |
|-----------|------|-------|-------------|
| DFS | O(V + E) | O(V) | Explore all, path finding |
| BFS | O(V + E) | O(V) | Shortest path (unweighted) |
| Topological Sort | O(V + E) | O(V) | Ordering with dependencies |
| Dijkstra | O(E log V) | O(V) | Shortest path (weighted, no negatives) |
| Bellman-Ford | O(V × E) | O(V) | Shortest path (with negatives) |
| Union Find | O(α(n)) ≈ O(1) | O(n) | Connected components |
| Prim's MST | O(E log V) | O(V) | Minimum spanning tree |
| Kruskal's MST | O(E log E) | O(V) | MST (with Union Find) |

---

## 🧠 Pattern → Complexity Quick Map

| Pattern | Typical Time | Typical Space |
|---------|-------------|---------------|
| Two Pointers | O(n) | O(1) |
| Sliding Window | O(n) | O(k) or O(1) |
| Binary Search | O(log n) | O(1) |
| BFS/DFS | O(V + E) | O(V) |
| Backtracking | O(2^n) or O(n!) | O(n) |
| DP (1D) | O(n) | O(n) → O(1) |
| DP (2D) | O(n × m) | O(n × m) → O(n) |
| Heap operations | O(n log k) | O(k) |
| Trie | O(sum of lengths) | O(sum of lengths) |
| Union Find | O(n × α(n)) | O(n) |

---

## 🐍 Python-Specific Tips

```python
# Collections you should know
from collections import defaultdict, Counter, deque, OrderedDict
from heapq import heappush, heappop, heapify
from functools import lru_cache
from bisect import bisect_left, bisect_right
from itertools import combinations, permutations
import math

# Useful Python tricks
float('inf')              # Positive infinity
float('-inf')             # Negative infinity
divmod(a, b)              # Returns (a // b, a % b)
sorted(arr, key=lambda x: x[1])  # Sort by second element
"".join(list_of_chars)    # Efficient string building
```

---

## 📏 Space Complexity Rules of Thumb

- **Recursion** uses O(depth) call stack space
- **Most sorting** uses O(n) extra space (except heap sort)
- **Hash map/set** uses O(n) space
- **DP table** uses O(states) — often optimizable
- **BFS queue** can hold O(width of level) nodes
- **DFS stack** holds O(depth) nodes

---

*Keep this handy during every session!*
