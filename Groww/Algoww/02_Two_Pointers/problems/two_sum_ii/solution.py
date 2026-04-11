# Two Sum II - Input Array Is Sorted
# https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
#
# Given a 1-indexed sorted array, find two numbers that add up to target.
# Return their 1-indexed positions.
#
# Pattern: Two Pointers — Opposite End
# Time: O(n) | Space: O(1)


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        l, r = 0, len(numbers) - 1
        while l<r:
            curr  = numbers[l] + numbers[r]
            if curr < target:
                l += 1
            elif curr > target:
                r -= 1
            else:
                return [l+1, r+1]  # Return 1-indexed positions


# ─── Test Cases ───
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([2, 7, 11, 15], 9, [1, 2]),
        ([2, 3, 4], 6, [1, 3]),
        ([-1, 0], -1, [1, 2]),
        ([-3, -1, 0, 2, 4], 3, [2, 5]),          # negatives
        ([1, 1, 3, 5], 2, [1, 2]),                # duplicate values
        ([1, 2, 3, 4, 5, 6], 11, [5, 6]),         # answer at the end
        ([-1000, -1, 0, 1, 1000], 0, [1, 5]),     # extreme values
    ]
    for i, (nums, target, expected) in enumerate(tests):
        result = sol.twoSum(nums, target)
        status = "✅" if result == expected else "❌"
        print(f"{status} Test {i+1}: twoSum({nums}, {target}) = {result} (expected {expected})")
