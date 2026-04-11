# How Many Numbers Are Smaller Than the Current Number
# https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/
#
# Given an array nums, for each nums[i] find out how many numbers
# in the array are smaller than it. Return the counts as an array.
#
# Example 1: nums = [8,1,2,2,3] → [4,0,1,1,3]
#   For 8: there are 4 smaller (1,2,2,3)
#   For 1: there are 0 smaller
#   For 2: there is 1 smaller (1)
#   For 3: there are 3 smaller (1,2,2)
#
# Example 2: nums = [6,5,4,8] → [2,1,0,3]
# Example 3: nums = [7,7,7,7] → [0,0,0,0]
#
# Constraints:
# - 2 <= nums.length <= 500
# - 0 <= nums[i] <= 100
#
# Hint: nums[i] <= 100 — how does that help?
#
# Write your solution below:

def smallerNumbersThanCurrent(nums: list[int]) -> list[int]:
    count_map = [0] * 101
    for num in nums:
        count_map[num] += 1

    prefix_arr = [0] * 101
    prefix = 0
    for i in range(len(count_map)):
        prefix_arr[i] += prefix
        prefix += count_map[i]
    
    res = []
    for num in nums:
        res.append(prefix_arr[num])
    return res


# ---- Test Cases ----
if __name__ == "__main__":
    assert smallerNumbersThanCurrent([8,1,2,2,3]) == [4,0,1,1,3],  "Test 1 Failed"
    assert smallerNumbersThanCurrent([6,5,4,8]) == [2,1,0,3],      "Test 2 Failed"
    assert smallerNumbersThanCurrent([7,7,7,7]) == [0,0,0,0],      "Test 3 Failed"
    assert smallerNumbersThanCurrent([1,2]) == [0,1],               "Test 4 Failed"
    assert smallerNumbersThanCurrent([0,0]) == [0,0],               "Test 5 Failed"
    assert smallerNumbersThanCurrent([5,0,10,0,10,6]) == [2,0,4,0,4,3], "Test 6 Failed"

    print("✅ All tests passed!")
