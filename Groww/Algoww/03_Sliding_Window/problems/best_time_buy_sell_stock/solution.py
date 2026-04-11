# Best Time to Buy and Sell Stock
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
#
# You are given an array prices where prices[i] is the price of a
# given stock on the ith day.
#
# You want to maximize your profit by choosing a single day to buy
# and a single day to sell in the future.
# Return the maximum profit. If no profit is possible, return 0.
#
# Example 1: Input: prices = [7,1,5,3,6,4] → Output: 5
# Example 2: Input: prices = [7,6,4,3,1] → Output: 0
#
# Constraints:
# - 1 <= prices.length <= 10^5
# - 0 <= prices[i] <= 10^4


def max_profit(prices: list[int]) -> int:
    max_profit = 0
    min_so_far = float('inf')

    for i in range(len(prices)):
        min_so_far = min(min_so_far, prices[i])
        max_profit = max(max_profit, prices[i] - min_so_far)

    return max_profit


if __name__ == "__main__":
    # Basic examples
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5, "Example 1: buy at 1, sell at 6"
    assert max_profit([7, 6, 4, 3, 1]) == 0, "Example 2: decreasing prices, no profit"

    # Edge cases
    assert max_profit([10]) == 0, "Single element — can't sell"
    assert max_profit([9, 9, 9]) == 0, "All same prices — no profit"
    assert max_profit([1, 2]) == 1, "Two elements — simple profit"
    assert max_profit([2, 1]) == 0, "Two elements — can't profit"

    # Tricky cases
    assert max_profit([2, 4, 1, 7]) == 6, "Min is NOT at index 0 — buy at 1, sell at 7"
    assert max_profit([3, 1, 4, 8, 2, 10]) == 9, "Multiple valleys — buy at 1, sell at 10 = 9"
    assert max_profit([1, 2, 3, 4, 5]) == 4, "Monotonically increasing — buy first, sell last"

    print("✅ All tests passed!")
