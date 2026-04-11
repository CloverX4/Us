# Generate Parentheses
# Link: https://leetcode.com/problems/generate-parentheses/
#
# Given n pairs of parentheses, write a function to generate all combinations
# of well-formed parentheses.
#
# Example 1: Input: n = 3
#   Output: ["((()))","(()())","(())()","()(())","()()()"]
#
# Example 2: Input: n = 1
#   Output: ["()"]
#
# Constraints:
# - 1 <= n <= 8
#
# Key insight: This LOOKS like it needs a stack, but it's pure backtracking.
# At each step, you have two choices: add '(' or add ')'.
# Constraints: open count <= n, close count <= open count.
# When both reach n, you have a valid combination.
# The constraint is what makes it backtracking (not just "try everything" — prune invalid states).

from typing import List


def generateParenthesis(n: int) -> List[str]:
    pass


if __name__ == "__main__":
    # Test 1: n=1
    result = generateParenthesis(1)
    assert sorted(result) == sorted(["()"]), f"Got {result}"

    # Test 2: n=2
    result = generateParenthesis(2)
    assert sorted(result) == sorted(["(())", "()()"]), f"Got {result}"

    # Test 3: n=3
    result = generateParenthesis(3)
    expected = ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert sorted(result) == sorted(expected), f"Got {result}"

    # Test 4: count check — n=4 should have 14 combinations (Catalan number)
    result = generateParenthesis(4)
    assert len(result) == 14, f"Expected 14, got {len(result)}"

    print("✅ All tests passed!")
