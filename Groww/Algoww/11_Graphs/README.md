# 11 — Graphs

## 🧠 Core Intuition
Graphs are about **connections between things**. The two fundamental operations:
1. **Traversal**: Visit all reachable nodes (DFS or BFS)
2. **Path-finding**: Find the best/shortest path between nodes

**Mental model**: "If I can model the problem as nodes and edges, it's a graph problem."

## 🔑 Key Patterns

### 1. Graph Representation
```python
# Adjacency List (most common in interviews)
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # undirected

# Grid as implicit graph
# Neighbors of (r, c): (r±1, c), (r, c±1)
directions = [(0,1), (0,-1), (1,0), (-1,0)]
```

### 2. DFS (Depth-First Search)
- **When**: "Find if path exists", "explore all connected", "detect cycle"
```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

### 3. BFS (Breadth-First Search)
- **When**: **Shortest path in unweighted graph**, level-by-level traversal
```python
from collections import deque
def bfs(start):
    queue = deque([start])
    visited = {start}
    distance = 0
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        distance += 1
```
**Remember: BFS = shortest path in unweighted graphs. ALWAYS.**

### 4. Topological Sort
- **When**: "Order of tasks with dependencies", "course schedule"
- **Key**: Only works on **DAGs** (Directed Acyclic Graphs)
```python
# Kahn's Algorithm (BFS-based)
def topo_sort(n, edges):
    in_degree = [0] * n
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else []  # empty = cycle!
```

### 5. Union Find (Disjoint Set Union)
- **When**: "Connected components", "redundant connection", "accounts merge"
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

### 6. Cycle Detection
- **Undirected**: DFS, if neighbor is visited AND not parent → cycle
- **Directed**: DFS with 3 colors (white/gray/black) or topological sort

## ⚡ BFS vs DFS Decision Guide
| Need | Use |
|------|-----|
| Shortest path (unweighted) | BFS |
| Shortest path (weighted) | Dijkstra (BFS + heap) |
| Explore all paths | DFS |
| Connected components | Either (DFS simpler) |
| Topological sort | BFS (Kahn's) or DFS |
| Detect cycle (directed) | DFS (3 colors) |
| Detect cycle (undirected) | DFS or Union Find |

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Number of Islands | Medium | ⬜ | Grid DFS/BFS |
| 2 | Clone Graph | Medium | ⬜ | DFS + HashMap |
| 3 | Rotting Oranges | Medium | ⬜ | Multi-source BFS |
| 4 | Pacific Atlantic Water Flow | Medium | ⬜ | Reverse BFS/DFS |
| 5 | Course Schedule | Medium | ⬜ | Cycle detection (directed) |
| 6 | Course Schedule II | Medium | ⬜ | Topological sort |
| 7 | Number of Connected Components | Medium | ⬜ | Union Find or DFS |
| 8 | Redundant Connection | Medium | ⬜ | Union Find |
| 9 | Accounts Merge | Medium | ⬜ | Union Find + HashMap (real-world context) |
| 10 | Graph Valid Tree | Medium | ⬜ | n-1 edges + connected |
| 11 | Word Ladder | Hard | ⬜ | BFS shortest path |
| 12 | Alien Dictionary | Hard | ⬜ | Topological sort |

## 💡 Interview Tips
- ALWAYS clarify: "Is the graph directed or undirected? Can there be cycles? Is it weighted?"
- For grid problems: the grid IS your adjacency representation — no need to build a graph
- Visited set is CRUCIAL — forgetting it = infinite loop
- BFS guarantees shortest path in unweighted graphs — DFS does NOT
- Space: BFS = O(width of graph), DFS = O(height/depth). For grids, BFS can use more memory.

## 🔗 Connections to Other Patterns
- Grid DFS → same as **Backtracking** on a grid
- BFS → same technique as **Tree** level-order traversal
- Dijkstra = BFS + **Heap**
- Topological sort → prerequisite for some **DP** on DAGs
