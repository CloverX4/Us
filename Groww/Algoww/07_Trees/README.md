# 07 — Trees

## 🧠 Core Intuition
Trees are **recursive data structures** — every subtree is itself a tree. This means most tree solutions follow a simple mental model:

> "If I know the answer for my left subtree and right subtree, can I compute the answer for the whole tree?"

If yes → **DFS (post-order)**. If you need to process level-by-level → **BFS**.

## 🔑 Key Patterns

### 1. DFS Traversals
```python
def dfs(node):
    if not node:
        return  # BASE CASE — always handle this first!
    
    # PRE-ORDER: process node, then children
    process(node)
    dfs(node.left)
    dfs(node.right)
    
    # IN-ORDER: left, process, right (gives sorted order for BST!)
    dfs(node.left)
    process(node)
    dfs(node.right)
    
    # POST-ORDER: children first, then process (bottom-up)
    dfs(node.left)
    dfs(node.right)
    process(node)
```

### 2. BFS (Level Order)
```python
from collections import deque
def bfs(root):
    if not root: return []
    queue = deque([root])
    result = []
    while queue:
        level_size = len(queue)  # KEY: process one level at a time
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

### 3. Return Value Pattern (Post-Order)
- **When**: Height, diameter, max path sum, balanced check
- **How**: Return computed value from children, combine at parent
```python
def height(node):
    if not node: return 0
    return 1 + max(height(node.left), height(node.right))
```

### 4. Pass-Down Pattern (Pre-Order)
- **When**: Path sum, range constraints (validate BST)
- **How**: Pass information DOWN to children via parameters
```python
def validate_bst(node, lo=float('-inf'), hi=float('inf')):
    if not node: return True
    if node.val <= lo or node.val >= hi:
        return False
    return (validate_bst(node.left, lo, node.val) and 
            validate_bst(node.right, node.val, hi))
```

### 5. BST Property
- Left subtree values < node < right subtree values
- **In-order traversal of BST = sorted order** — incredibly useful!

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Invert Binary Tree | Easy | ⬜ | DFS (pre-order) |
| 2 | Maximum Depth of Binary Tree | Easy | ⬜ | Return value (post-order) |
| 3 | Same Tree | Easy | ⬜ | Parallel DFS |
| 4 | Subtree of Another Tree | Easy | ⬜ | DFS + Same Tree |
| 5 | Diameter of Binary Tree | Easy | ⬜ | Return value + global var |
| 6 | Lowest Common Ancestor | Medium | ⬜ | Post-order decision |
| 7 | Binary Tree Level Order Traversal | Medium | ⬜ | BFS |
| 8 | Binary Tree Right Side View | Medium | ⬜ | BFS (last of each level) |
| 9 | Validate BST | Medium | ⬜ | Pass-down with bounds |
| 10 | Kth Smallest Element in BST | Medium | ⬜ | In-order traversal |
| 11 | Construct from Preorder + Inorder | Medium | ⬜ | Recursive construction |
| 12 | Binary Tree Max Path Sum | Hard | ⬜ | Return value + global max |
| 13 | Serialize/Deserialize Binary Tree | Hard | ⬜ | Pre-order + null markers |

## 💡 Interview Tips
- ALWAYS start with: "What if the node is None?" (base case first!)
- Ask yourself: "Am I passing info DOWN (pre-order) or UP (post-order)?"
- Most tree problems are 5-15 lines of code — the thinking is the hard part
- If asked about space complexity of DFS: O(h) where h = height. Worst case O(n) for skewed tree.

## 🔗 Connections to Other Patterns
- Tree DFS uses **recursion** (same skills as **Backtracking**)
- BST search is **Binary Search** on a tree
- Level order traversal is **BFS** (same as **Graphs**)
- Tree construction → connects to **Divide and Conquer**
