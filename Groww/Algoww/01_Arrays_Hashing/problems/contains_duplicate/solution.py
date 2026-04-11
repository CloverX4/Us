# Contains Duplicate
# https://leetcode.com/problems/contains-duplicate/
#
# Given an integer array nums, return true if any value appears
# at least twice, and false if every element is distinct.
#
# Write your solution below:

def containsDuplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False
