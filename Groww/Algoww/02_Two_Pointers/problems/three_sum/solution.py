# 3Sum
# https://leetcode.com/problems/3sum/
#
# Given an integer array nums, return all the triplets that sum to 0.
# No duplicate triplets in the result.
#
# Pattern: Sort + Fix one + Two Pointers
# Time: O(n^2) | Space: O(1) extra (O(n) for sort depending on implementation)


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        res = []
        i = 0
        while i < len(nums)-2:
            if nums[i] > 0:  # Since array is sorted, no triplet can sum to 0 beyond this point
                break

            while 0 < i < len(nums)-2 and nums[i] == nums[i-1]:
                i += 1

            l, r = i+1, len(nums)-1
            while l<r:
                curr = nums[l] + nums[r]
                if curr < -nums[i]:
                    l += 1
                elif curr > -nums[i]:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                # NOTE: Duplicate-skip loops placed OUTSIDE else block intentionally.
                # Standard approach puts them inside else (only after a match), but
                # outside also works for 3Sum because after a non-match move (l++ or r--),
                # the skip just avoids re-checking the same value from the same direction,
                # which wouldn't produce a new result anyway. The key guard is
                # `l < r < len(nums) - 1` to prevent IndexError on nums[r+1].
                while l < r < len(nums) - 1 and nums[l] == nums[l-1]:
                    l += 1
                while l < r < len(nums) - 1 and nums[r] == nums[r+1]:
                    r -= 1
            i += 1
        return res


# ─── Test Cases ───
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),                          # extra zeros, still one triplet
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),         # two valid triplets
        ([1, 2, 3], []),                                        # all positive
        ([-1, -1, -1, 2], [[-1, -1, 2]]),                      # duplicates in input, one triplet
    ]
    for i, (nums, expected) in enumerate(tests):
        result = sol.threeSum(nums)
        # Sort inner lists and outer list for comparison
        result_sorted = sorted([sorted(t) for t in result])
        expected_sorted = sorted([sorted(t) for t in expected])
        status = "✅" if result_sorted == expected_sorted else "❌"
        print(f"{status} Test {i+1}: threeSum({nums}) = {result} (expected {expected})")
