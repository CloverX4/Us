# Sliding Window Maximum
# LeetCode 239
# Fixed-Size Sliding Window + ???

from collections import deque
from typing import List

def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    # TODO: Implement solution
    pass

# Test cases
def test():
    assert maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]
    assert maxSlidingWindow([1], 1) == [1]
    assert maxSlidingWindow([1,-1], 1) == [1,-1]
    assert maxSlidingWindow([9,11], 2) == [11]
    assert maxSlidingWindow([4,3,2,1], 2) == [4,3,2]      # decreasing array
    assert maxSlidingWindow([1,2,3,4], 2) == [2,3,4]      # increasing array
    print("All test cases pass.")

if __name__ == "__main__":
    test()
