# Two Sum
# https://leetcode.com/problems/two-sum/
#
# Given an array of integers nums and an integer target, return
# indices of the two numbers such that they add up to target.
#
# You may assume that each input would have exactly one solution,
# and you may not use the same element twice.
#
# Example 1: nums = [2,7,11,15], target = 9  → [0,1]
# Example 2: nums = [3,2,4], target = 6      → [1,2]
# Example 3: nums = [3,3], target = 6        → [0,1]
#
# Constraints:
# - 2 <= nums.length <= 10^4
# - -10^9 <= nums[i] <= 10^9
# - Only one valid answer exists.
#
# Write your solution below:

def twoSum(nums: list[int], target: int) -> list[int]:
    idx_map = {}
    for i in range(len(nums)):
        x = target - nums[i]
        if x in idx_map:
            return [idx_map[x], i]
        if nums[i] not in idx_map: # keep the first occurence of the element
            idx_map[nums[i]] = i


# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert twoSum([2, 7, 11, 15], 9) == [0, 1],       "Test 1 Failed: basic pair"
    assert twoSum([3, 2, 4], 6) == [1, 2],             "Test 2 Failed: not first two"
    assert twoSum([3, 3], 6) == [0, 1],                "Test 3 Failed: duplicate values"

    # Edge cases
    assert twoSum([0, 0], 0) == [0, 1],                "Test 4 Failed: zeros"
    assert twoSum([-1, -2, -3, -4, -5], -8) == [2, 4], "Test 5 Failed: negatives"
    assert twoSum([1, 2], 3) == [0, 1],                "Test 6 Failed: minimum length"

    # Tricky case
    assert twoSum([5, 75, 25], 100) == [1, 2],         "Test 7 Failed: answer not at start"

    print("✅ All tests passed!")
