# Copy List with Random Pointer
# Link: https://leetcode.com/problems/copy-list-with-random-pointer/
#
# A linked list of length n is given such that each node contains an additional
# random pointer which could point to any node in the list, or null.
#
# Construct a deep copy of the list. The deep copy should consist of exactly n
# brand new nodes, where each new node has its value set to the value of its
# corresponding original node. Both the next and random pointer of the new nodes
# should point to new nodes in the copied list (not the original nodes).
#
# Example 1:
#   Input:  head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
#   Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
#   (same structure, all new nodes)
#
# Example 2:
#   Input:  head = [[1,1],[2,1]]
#   Output: [[1,1],[2,1]]
#
# Constraints:
# - 0 <= n <= 1000
# - -10^4 <= Node.val <= 10^4
# - Node.random is null or points to a node in the linked list
#
# Key insight: You can't just copy next pointers first — the random pointer can
# point forward in the list to a node you haven't created yet.
# Solution: Two-pass with a HashMap { original_node → copied_node }

from typing import Optional


class Node:
    def __init__(self, x: int, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


def copyRandomList(head: Optional[Node]) -> Optional[Node]:
    pass


if __name__ == "__main__":
    # Test 1: empty list
    assert copyRandomList(None) is None

    # Test 2: single node, random points to itself
    n1 = Node(1)
    n1.random = n1
    copy = copyRandomList(n1)
    assert copy is not n1, "Should be a new node"
    assert copy.val == 1
    assert copy.random is copy, "Random should point to the copy itself, not original"

    # Test 3: two nodes
    n1 = Node(1)
    n2 = Node(2)
    n1.next = n2
    n1.random = n2   # 1's random → 2
    n2.random = n2   # 2's random → itself
    copy = copyRandomList(n1)
    assert copy.val == 1
    assert copy.next.val == 2
    assert copy.random is copy.next, "1's copy random should point to 2's copy"
    assert copy.next.random is copy.next, "2's copy random should point to itself copy"
    assert copy is not n1 and copy.next is not n2, "Should be entirely new nodes"

    print("✅ All tests passed!")
