# Top K Frequent Elements
# https://leetcode.com/problems/top-k-frequent-elements/
#
# Given an integer array nums and an integer k, return the k most
# frequent elements. You may return the answer in any order.
#
# Example 1: nums = [1,1,1,2,2,3], k = 2 → [1,2]
# Example 2: nums = [1], k = 1            → [1]
#
# Constraints:
# - 1 <= nums.length <= 10^5
# - -10^4 <= nums[i] <= 10^4
# - k is in the range [1, number of unique elements]
# - It is guaranteed that the answer is unique.
#
# Follow up: Your algorithm's time complexity must be better than
# O(n log n), where n is the array's size.
#
# Write your solution below:
from collections import defaultdict

def topKFrequent(nums: list[int], k: int) -> list[int]:
    freq_map = defaultdict(int)
    for num in nums:
        freq_map[num] += 1
    
    buckets = [ [ ] for _ in range(len(nums) + 1) ] 

    for num, freq in freq_map.items():
        buckets[freq].append(num)

    res = []

    for i in reversed(buckets):
        res.extend(i)
        if len(res) >= k:
            break

    return res[:k]

# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert sorted(topKFrequent([1,1,1,2,2,3], 2)) == [1,2],     "Test 1 Failed: basic top 2"
    assert topKFrequent([1], 1) == [1],                           "Test 2 Failed: single element"

    # Edge cases
    assert sorted(topKFrequent([1,2], 2)) == [1,2],              "Test 3 Failed: k equals unique count"
    assert sorted(topKFrequent([3,3,3,3], 1)) == [3],            "Test 4 Failed: all same element"

    # Tricky cases
    assert sorted(topKFrequent([1,1,2,2,3], 2)) == [1,2],       "Test 5 Failed: tied frequencies"
    assert sorted(topKFrequent([-1,-1,2,2,3], 2)) == [-1,2],    "Test 6 Failed: negatives"
    assert sorted(topKFrequent([4,4,1,1,1,2,2,3], 3)) == [1,2,4], "Test 7 Failed: top 3"

    print("✅ All tests passed!")
