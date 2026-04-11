# 08 — Tries (Prefix Trees)

## 🧠 Core Intuition
A Trie is a **tree where each path from root to a node represents a prefix**. It's the optimal structure when you need to:
- Search for words by prefix
- Autocomplete
- Check if any word starts with a given prefix

Think of it as a **glorified dictionary organized by characters**.

## 🔑 Key Patterns

### 1. Basic Trie Implementation
```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    
    def _find(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### 2. Trie + DFS (Word Search II pattern)
- **When**: Find all words from a dictionary in a grid
- **How**: Build trie from word list, DFS from each cell using trie for pruning

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Implement Trie | Medium | ⬜ | Basic implementation |
| 2 | Design Add and Search Words | Medium | ⬜ | Trie + DFS (wildcard) |
| 3 | Word Search II | Hard | ⬜ | Trie + Grid DFS |

## 💡 Interview Tips
- Time complexity: O(L) for insert/search where L = word length
- Space can be large — mention this tradeoff
- Trie vs HashMap of prefixes: Trie is better when you need prefix operations frequently

## 🔗 Connections to Other Patterns
- Trie + DFS = **Backtracking** on a trie
- Word Search II combines **Trie** + **Graph/Grid DFS** + **Backtracking**
