# Group Anagrams
# https://leetcode.com/problems/group-anagrams/
#
# Given an array of strings strs, group the anagrams together.
# You can return the answer in any order.
#
# Example 1: strs = ["eat","tea","tan","ate","nat","bat"]
#            → [["bat"],["nat","tan"],["ate","eat","tea"]]
# Example 2: strs = [""]  → [[""]]
# Example 3: strs = ["a"] → [["a"]]
#
# Constraints:
# - 1 <= strs.length <= 10^4
# - 0 <= strs[i].length <= 100
# - strs[i] consists of lowercase English letters
#
# Write your solution below:
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    sorted_map = defaultdict(list)
    for st in strs:
        sorted_st = "".join(sorted(st))
        sorted_map[sorted_st].append(st)
    
    return list(sorted_map.values())

# ---- Test Cases ----
if __name__ == "__main__":
    # Helper: sort inner lists and outer list for comparison
    def normalize(groups):
        return sorted([sorted(g) for g in groups])

    # Basic case
    result = groupAnagrams(["eat","tea","tan","ate","nat","bat"])
    assert normalize(result) == normalize([["bat"],["nat","tan"],["ate","eat","tea"]]), \
        "Test 1 Failed: basic grouping"

    # Edge cases
    assert groupAnagrams([""]) == [[""]], \
        "Test 2 Failed: empty string"
    assert groupAnagrams(["a"]) == [["a"]], \
        "Test 3 Failed: single char"

    # No anagrams
    result = groupAnagrams(["abc", "def", "ghi"])
    assert normalize(result) == normalize([["abc"], ["def"], ["ghi"]]), \
        "Test 4 Failed: no anagrams"

    # All same anagram
    result = groupAnagrams(["ab", "ba", "ab", "ba"])
    assert normalize(result) == normalize([["ab", "ba", "ab", "ba"]]), \
        "Test 5 Failed: all same anagram"

    # Different lengths
    result = groupAnagrams(["a", "ab", "ba", "abc"])
    assert normalize(result) == normalize([["a"], ["ab", "ba"], ["abc"]]), \
        "Test 6 Failed: mixed lengths"

    print("✅ All tests passed!")
