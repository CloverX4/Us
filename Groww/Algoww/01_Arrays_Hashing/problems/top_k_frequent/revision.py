# Top K Frequent Elements — REVISION (Day 5 blind re-solve)
# Bucket sort approach. Code from memory, no peeking!
#
# Given an integer array nums and an integer k, return the k most
# frequent elements. You may return the answer in any order.
#
# Write your solution below:

from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    # extract frequncy map
    freq_map = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]

    # assign arrays into the frequncy buckets
    for ki, val in freq_map.items():
        buckets[val].append(ki)

    res = []
    # start collecting top k from the end of the buckets
    for bkt in reversed(buckets):
        res.extend(bkt)
        if len(res) >= k:
            break

    return res[:k]


# ---- Test Cases ----
if __name__ == "__main__":
    assert sorted(topKFrequent([1,1,1,2,2,3], 2)) == [1,2],     "Test 1 Failed"
    assert topKFrequent([1], 1) == [1],                           "Test 2 Failed"
    assert sorted(topKFrequent([1,2], 2)) == [1,2],              "Test 3 Failed"
    assert sorted(topKFrequent([4,4,1,1,1,2,2,3], 3)) == [1,2,4], "Test 4 Failed"
    assert sorted(topKFrequent([-1,-1,2,2,3], 2)) == [-1,2],    "Test 5 Failed"

    print("✅ All revision tests passed!")
