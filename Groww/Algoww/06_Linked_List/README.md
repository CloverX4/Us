# 06 — Linked Lists

## 🧠 Core Intuition
Linked lists test your **pointer manipulation** skills. The core challenge: you can't go backwards (singly linked), and you can't jump to index i.

**The key skills**: Drawing out pointer changes on paper, handling edge cases (empty list, single node, head changes), and knowing the classic tricks.

## 🔑 Key Patterns

### 1. Two-Pointer (Fast & Slow)
- **When**: Cycle detection, find middle, find nth from end
- **Floyd's Cycle Detection**:
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # cycle!
```

### 2. Reverse a Linked List
- **When**: Reverse all or part of a list — THE most fundamental operation
```python
def reverse(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev  # new head
```

### 3. Dummy Head Technique
- **When**: The head might change (merge, remove, partition)
- **How**: Create `dummy = ListNode(0); dummy.next = head` — return `dummy.next`
- Eliminates all head-is-None edge cases!

### 4. Merge Technique
- **When**: Merge two sorted lists, merge K lists
```python
dummy = ListNode(0)
curr = dummy
while l1 and l2:
    if l1.val <= l2.val:
        curr.next = l1
        l1 = l1.next
    else:
        curr.next = l2
        l2 = l2.next
    curr = curr.next
curr.next = l1 or l2
```

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Reverse Linked List | Easy | ⬜ | Reverse |
| 2 | Merge Two Sorted Lists | Easy | ⬜ | Merge + Dummy |
| 3 | Linked List Cycle | Easy | ⬜ | Fast & Slow |
| 4 | Reorder List | Medium | ⬜ | Find mid + Reverse + Merge |
| 5 | Copy List with Random Pointer | Medium | ⬜ | HashMap (old node → new node) |
| 6 | Remove Nth Node From End | Medium | ⬜ | Two pointers with gap |
| 7 | Add Two Numbers | Medium | ⬜ | Carry tracking |
| 8 | LRU Cache | Medium | ⬜ | HashMap + Doubly Linked List |
| 9 | Merge K Sorted Lists | Hard | ⬜ | Heap + Merge |

## 💡 Interview Tips
- ALWAYS use a dummy head when the head could change
- Draw the pointers on paper — linked list bugs are almost always pointer issues
- Remember: in Python, `node = node.next` doesn't modify the list, it just moves your reference
- For "reverse a portion": identify `prev_to_start`, `start`, `end`, `after_end`

## 🔗 Connections to Other Patterns
- Fast & slow → same as **Two Pointers** pattern
- Merge K lists uses a **Heap**
- LRU Cache = HashMap + Linked List — classic **Design** problem
