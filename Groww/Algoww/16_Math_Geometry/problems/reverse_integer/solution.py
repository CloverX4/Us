# Reverse Integer
# Link: https://leetcode.com/problems/reverse-integer/
#
# Given a signed 32-bit integer x, return x with its digits reversed.
# If reversing x causes the value to go outside the signed 32-bit integer range
# [-2^31, 2^31 - 1], return 0.
#
# Assume the environment does not allow you to store 64-bit integers (signed or unsigned).
#
# Example 1: Input: x = 123   → Output: 321
# Example 2: Input: x = -123  → Output: -321
# Example 3: Input: x = 120   → Output: 21
#
# Constraints:
# - -2^31 <= x <= 2^31 - 1
#
# Key insight: Extract digits one by one using % and //.
# Handle sign separately (or let % handle it naturally in Python — careful: Python's %
# behaves differently from C/Java for negative numbers).
# The overflow check is the real interview question here: check BEFORE multiplying.
# INT_MAX = 2^31 - 1 = 2147483647, INT_MIN = -2^31 = -2147483648


def reverse(x: int) -> int:
    pass


if __name__ == "__main__":
    # Test 1: positive
    assert reverse(123) == 321, f"Got {reverse(123)}"

    # Test 2: negative
    assert reverse(-123) == -321, f"Got {reverse(-123)}"

    # Test 3: trailing zero
    assert reverse(120) == 21, f"Got {reverse(120)}"

    # Test 4: single digit
    assert reverse(5) == 5, f"Got {reverse(5)}"

    # Test 5: overflow — reversed exceeds 32-bit range
    assert reverse(1534236469) == 0, f"Got {reverse(1534236469)}"

    # Test 6: zero
    assert reverse(0) == 0, f"Got {reverse(0)}"

    print("✅ All tests passed!")
