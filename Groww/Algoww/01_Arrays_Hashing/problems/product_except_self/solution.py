# Product of Array Except Self
# https://leetcode.com/problems/product-of-array-except-self/
#
# Given an integer array nums, return an array answer such that
# answer[i] is equal to the product of all elements of nums except nums[i].
#
# You must write an algorithm that runs in O(n) time and without
# using the division operator.
#
# Example 1: nums = [1,2,3,4]       → [24,12,8,6]
# Example 2: nums = [-1,1,0,-3,3]   → [0,0,9,0,0]
#
# Constraints:
# - 2 <= nums.length <= 10^5
# - -30 <= nums[i] <= 30
# - The product of any prefix or suffix of nums fits in a 32-bit integer
#
# Follow up: Can you solve it in O(1) extra space? (output array doesn't count)
#
# Write your solution below:

def productExceptSelf(nums: list[int]) -> list[int]:
    res = []
    curr_fix = 1

    for i in range(len(nums)):
        res.append(curr_fix)
        curr_fix *= nums[i]

    curr_fix = 1
    for i in range(len(nums)-1, -1, -1):
        res[i] *= curr_fix
        curr_fix *= nums[i]

    return res    


# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert productExceptSelf([1,2,3,4]) == [24,12,8,6],         "Test 1 Failed: basic"
    assert productExceptSelf([-1,1,0,-3,3]) == [0,0,9,0,0],     "Test 2 Failed: with zero"

    # Edge cases
    assert productExceptSelf([0,0]) == [0,0],                    "Test 3 Failed: two zeros"
    assert productExceptSelf([1,1]) == [1,1],                    "Test 4 Failed: two ones"
    assert productExceptSelf([2,3]) == [3,2],                    "Test 5 Failed: two elements"

    # Tricky cases
    assert productExceptSelf([-1,-1]) == [-1,-1],                "Test 6 Failed: negatives"
    assert productExceptSelf([1,0,3,0,5]) == [0,0,0,0,0],       "Test 7 Failed: multiple zeros"
    assert productExceptSelf([1,2,3,4,5]) == [120,60,40,30,24], "Test 8 Failed: ascending"

    print("✅ All tests passed!")
