# Container With Most Water
# https://leetcode.com/problems/container-with-most-water/
#
# Given n vertical lines, find two that form a container holding the most water.
# Area = width * min(height[l], height[r])
#
# Pattern: Two Pointers — Opposite End + Greedy
# Time: O(n) | Space: O(1)


class Solution:
    def maxArea(self, height: list[int]) -> int:
        glob = 0
        l, r = 0, len(height) - 1

        while l < r:
            curr = (r-l) * min(height[l], height[r])
            glob = max(glob, curr)
            if height[l] < height[r]:
                l += 1
            else:
                r-=1

        return glob


# ─── Test Cases ───
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([0, 0], 0),                              # zero height
        ([4, 3, 2, 1, 4], 16),                    # best pair is outermost
        ([1, 2, 1], 2),                            # short array
        ([10000, 0, 0, 0, 10000], 40000),          # tall lines far apart
        ([1, 2, 4, 3], 4),                         # not always the tallest lines
    ]
    for i, (height, expected) in enumerate(tests):
        result = sol.maxArea(height)
        status = "✅" if result == expected else "❌"
        print(f"{status} Test {i+1}: maxArea({height}) = {result} (expected {expected})")
