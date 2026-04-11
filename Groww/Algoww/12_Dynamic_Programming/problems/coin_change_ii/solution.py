# Coin Change II
# Link: https://leetcode.com/problems/coin-change-ii/
#
# You are given an integer array coins representing coins of different denominations
# and an integer amount representing a total amount of money.
#
# Return the number of combinations that make up that amount.
# If that amount of money cannot be made up by any combination of the coins, return 0.
# You may assume that you have an infinite number of each kind of coin.
# The answer is guaranteed to fit in a signed 32-bit integer.
#
# Example 1: Input: amount = 5, coins = [1,2,5] → Output: 4
#   (5=5, 5=2+2+1, 5=2+1+1+1, 5=1+1+1+1+1)
#
# Example 2: Input: amount = 3, coins = [2] → Output: 0
#
# Example 3: Input: amount = 10, coins = [10] → Output: 1
#
# Constraints:
# - 1 <= coins.length <= 300
# - 1 <= coins[i] <= 5000
# - All values of coins are unique
# - 0 <= amount <= 5000
#
# Key insight: Contrast with Coin Change I (minimum coins = optimization).
# This is COUNT THE WAYS = unbounded knapsack counting variant.
# dp[i] = number of ways to make amount i
# For each coin, for each amount from coin to target: dp[a] += dp[a - coin]
# ORDER MATTERS: iterate coins in outer loop, amounts in inner loop
# (this avoids counting [1,2] and [2,1] as different combinations)

from typing import List


def change(amount: int, coins: List[int]) -> int:
    pass


if __name__ == "__main__":
    # Test 1: basic
    assert change(5, [1, 2, 5]) == 4, f"Got {change(5, [1,2,5])}"

    # Test 2: impossible
    assert change(3, [2]) == 0, f"Got {change(3, [2])}"

    # Test 3: exact match
    assert change(10, [10]) == 1, f"Got {change(10, [10])}"

    # Test 4: amount = 0 (empty combination always works)
    assert change(0, [1, 2, 3]) == 1, f"Got {change(0, [1,2,3])}"

    # Test 5: larger case
    assert change(5, [1, 2, 5]) == 4

    print("✅ All tests passed!")
