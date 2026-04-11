# Subarray Sum Equals K
# https://leetcode.com/problems/subarray-sum-equals-k/
#
# Given an array of integers nums and an integer k, return the total
# number of subarrays whose sum equals to k.
#
# A subarray is a contiguous non-empty sequence of elements.
#
# Example 1: nums = [1,1,1], k = 2  → 2
# Example 2: nums = [1,2,3], k = 3  → 2
#
# Constraints:
# - 1 <= nums.length <= 2 * 10^4
# - -1000 <= nums[i] <= 1000
# - -10^7 <= k <= 10^7
#
# Note: Elements can be NEGATIVE — sliding window won't work here.
#
# Write your solution below:

def subarraySum(nums: list[int], k: int) -> int:
    prefix_freq_map = {0:1}
    prefix_sum = 0
    subarray_count = 0
    
    for num in nums:
        prefix_sum += num
        compliment = prefix_sum - k
        if compliment in prefix_freq_map:
            subarray_count += prefix_freq_map[compliment]
        prefix_freq_map[prefix_sum] = prefix_freq_map.get(prefix_sum, 0) + 1

    return subarray_count


# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert subarraySum([1,1,1], 2) == 2,                "Test 1 Failed: basic"
    assert subarraySum([1,2,3], 3) == 2,                "Test 2 Failed: two subarrays"

    # Edge cases
    assert subarraySum([1], 1) == 1,                     "Test 3 Failed: single element match"
    assert subarraySum([1], 0) == 0,                     "Test 4 Failed: single element no match"

    # Negatives
    assert subarraySum([1,-1,0], 0) == 3,               "Test 5 Failed: negatives, k=0"
    assert subarraySum([-1,-1,1], 0) == 1,              "Test 6 Failed: negative prefix"

    # Tricky
    assert subarraySum([3,4,7,2,-3,1,4,2], 7) == 4,    "Test 7 Failed: multiple ways"
    assert subarraySum([0,0,0], 0) == 6,                "Test 8 Failed: all zeros"

    print("✅ All tests passed!")
