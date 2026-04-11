# Sort Colors
# Link: https://leetcode.com/problems/sort-colors/
#
# Given an array nums with n objects colored red (0), white (1), or blue (2),
# sort them in-place so that objects of the same color are adjacent, in order 0, 1, 2.
# You must solve this without using the library's sort function.
#
# Example 1: Input: nums = [2,0,2,1,1,0] → Output: [0,0,1,1,2,2]
# Example 2: Input: nums = [2,0,1]       → Output: [0,1,2]
#
# Constraints:
# - n == nums.length
# - 1 <= n <= 300
# - nums[i] is either 0, 1, or 2
#
# Follow-up: Could you come up with a one-pass algorithm using only constant extra space?
# (Hint: Dutch National Flag algorithm — 3 pointers)

from typing import List


def sortColors(nums: List[int]) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    pass


if __name__ == "__main__":
    # Test 1: basic case
    nums = [2, 0, 2, 1, 1, 0]
    sortColors(nums)
    assert nums == [0, 0, 1, 1, 2, 2], f"Expected [0,0,1,1,2,2], got {nums}"

    # Test 2: already sorted
    nums = [0, 1, 2]
    sortColors(nums)
    assert nums == [0, 1, 2], f"Expected [0,1,2], got {nums}"

    # Test 3: reverse sorted
    nums = [2, 1, 0]
    sortColors(nums)
    assert nums == [0, 1, 2], f"Expected [0,1,2], got {nums}"

    # Test 4: all same color
    nums = [1, 1, 1]
    sortColors(nums)
    assert nums == [1, 1, 1], f"Expected [1,1,1], got {nums}"

    # Test 5: single element
    nums = [0]
    sortColors(nums)
    assert nums == [0], f"Expected [0], got {nums}"

    # Test 6: no 1s (only 0s and 2s)
    nums = [2, 0, 2, 0]
    sortColors(nums)
    assert nums == [0, 0, 2, 2], f"Expected [0,0,2,2], got {nums}"

    print("✅ All tests passed!")
