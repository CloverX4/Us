# Longest Consecutive Sequence
# https://leetcode.com/problems/longest-consecutive-sequence/
#
# Given an unsorted array of integers nums, return the length of
# the longest consecutive elements sequence.
#
# You must write an algorithm that runs in O(n) time.
#
# Example 1: nums = [100,4,200,1,3,2]        → 4  (sequence: 1,2,3,4)
# Example 2: nums = [0,3,7,2,5,8,4,6,0,1]    → 9  (sequence: 0-8)
#
# Constraints:
# - 0 <= nums.length <= 10^5
# - -10^9 <= nums[i] <= 10^9
#
# Write your solution below:

def longestConsecutive(nums: list[int]) -> int:
    nums = set(nums)
    longest = 0

    for num in nums:
        if num - 1 not in nums:
            curr_streak = 1
            while (num + 1) in nums:
                num += 1
                curr_streak += 1
            longest = max(longest, curr_streak)

    return longest


# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert longestConsecutive([100,4,200,1,3,2]) == 4,            "Test 1 Failed: basic"
    assert longestConsecutive([0,3,7,2,5,8,4,6,0,1]) == 9,       "Test 2 Failed: 0-8 sequence"

    # Edge cases
    assert longestConsecutive([]) == 0,                            "Test 3 Failed: empty"
    assert longestConsecutive([1]) == 1,                           "Test 4 Failed: single element"
    assert longestConsecutive([1,2,3,4,5]) == 5,                  "Test 5 Failed: already consecutive"

    # Tricky cases
    assert longestConsecutive([1,1,1,1]) == 1,                    "Test 6 Failed: all duplicates"
    assert longestConsecutive([9,1,4,7,3,-1,0,5,8,-1,6]) == 7,   "Test 7 Failed: negatives"
    assert longestConsecutive([1,3,5,7]) == 1,                    "Test 8 Failed: no consecutive pairs"

    print("✅ All tests passed!")
