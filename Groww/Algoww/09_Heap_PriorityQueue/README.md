# 09 — Heap / Priority Queue

## 🧠 Core Intuition
A heap gives you **the min or max element in O(1)** and lets you insert/remove in **O(log n)**. 

**When to think heap**: "I need the K largest/smallest" or "I need to repeatedly get the minimum/maximum from a dynamic collection."

Python has `heapq` — it's a **min-heap** by default. For max-heap, negate values.

## 🔑 Key Patterns

### 1. Top-K Pattern
- **When**: "K-th largest", "K most frequent", "K closest"
- **Two approaches**:
  - **Min-heap of size K**: Push all, keep only K largest → O(n log k)
  - **Max-heap**: Push all, pop K times → O(n + k log n)
```python
import heapq
# K-th largest using min-heap of size K
def kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]  # k-th largest
```

### 2. Merge K Sorted Pattern
- **When**: Merge multiple sorted lists/streams
- **How**: Push first element of each, pop min, push next from that list
```python
import heapq
def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0].val, i, lst[0]))
    # pop min, push its next...
```

### 3. Two-Heap Pattern (Median)
- **When**: Running median, sliding window median
- **How**: Max-heap for left half, min-heap for right half, balance sizes
```python
# max_heap (negate values) | min_heap
# [1, 2, 3]               | [4, 5, 6]
# max of left = median candidate, min of right = other candidate
```

### 4. Greedy with Heap
- **When**: Scheduling, task assignment, "process highest priority first"
- **How**: Push tasks to heap, greedily pop and process

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Kth Largest Element in a Stream | Easy | ⬜ | Min-heap of size K |
| 2 | Last Stone Weight | Easy | ⬜ | Max-heap simulation |
| 3 | K Closest Points to Origin | Medium | ⬜ | Top-K |
| 4 | Kth Largest Element in Array | Medium | ⬜ | Top-K or Quickselect |
| 5 | Task Scheduler | Medium | ⬜ | Greedy + Heap |
| 6 | Design Twitter | Medium | ⬜ | Merge K + Heap |
| 7 | Find Median from Data Stream | Hard | ⬜ | Two-heap |

## ⚡ Python heapq Cheat Sheet
```python
import heapq
heapq.heappush(heap, val)      # push — O(log n)
heapq.heappop(heap)             # pop min — O(log n)
heap[0]                          # peek min — O(1)
heapq.heapify(lst)              # build heap in-place — O(n)
heapq.nlargest(k, lst)          # K largest — O(n log k)
heapq.nsmallest(k, lst)         # K smallest — O(n log k)
# Max-heap trick: push -val, pop gives -max
```

## 💡 Interview Tips
- ALWAYS mention: "Python heapq is a min-heap, I'll negate for max-heap"
- Heapify is O(n), NOT O(n log n) — know why (interview favorite question)
- For "top K" problems: heap of size K = O(n log k) which is better than sorting O(n log n)
- Kth largest = (n-k+1)th smallest

## 🔗 Connections to Other Patterns
- Merge K sorted → connects to **Linked List** merge
- Heap with greedy → foundation for **Greedy** problems
- Priority queue → used in **Graph** algorithms (Dijkstra, Prim's)
