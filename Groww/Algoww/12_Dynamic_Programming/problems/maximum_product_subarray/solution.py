# Maximum Product Subarray
# Link: https://leetcode.com/problems/maximum-product-subarray/
#
# Given an integer array nums, find a subarray that has the largest product,
# and return the product.
# The test cases are generated so that the answer will fit in a 32-bit integer.
#
# Example 1: Input: nums = [2,3,-2,4] → Output: 6  ([2,3])
# Example 2: Input: nums = [-2,0,-1]  → Output: 0  ([] or [0])
#
# Constraints:
# - 1 <= nums.length <= 2 * 10^4
# - -10 <= nums[i] <= 10
# - The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer
#
# Key insight: Unlike Maximum Subarray (Kadane's), you CANNOT just reset when things go negative.
# A large negative number multiplied by another negative = large positive.
# So you need to track BOTH the current maximum AND current minimum at each position.
# When you hit a negative number, min and max SWAP roles.
#
# This is the "dual-state DP" pattern — two running values evolve together.

from typing import List


def maxProduct(nums: List[int]) -> int:
    pass


if __name__ == "__main__":
    # Test 1: basic — product of first two
    assert maxProduct([2, 3, -2, 4]) == 6, f"Got {maxProduct([2,3,-2,4])}"

    # Test 2: zeros break products
    assert maxProduct([-2, 0, -1]) == 0, f"Got {maxProduct([-2,0,-1])}"

    # Test 3: two negatives make a positive
    assert maxProduct([-2, 3, -4]) == 24, f"Got {maxProduct([-2,3,-4])}"

    # Test 4: single element
    assert maxProduct([-2]) == -2, f"Got {maxProduct([-2])}"

    # Test 5: all negative — odd count means max is a subarray
    assert maxProduct([-1, -2, -3]) == 6, f"Got {maxProduct([-1,-2,-3])}"

    # Test 6: single negative surrounded by large positives
    assert maxProduct([2, -1, 2]) == 2, f"Got {maxProduct([2,-1,2])}"

    print("✅ All tests passed!")
