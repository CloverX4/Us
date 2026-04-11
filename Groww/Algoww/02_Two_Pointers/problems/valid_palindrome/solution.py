# Valid Palindrome
# https://leetcode.com/problems/valid-palindrome/
#
# Given a string s, return true if it is a palindrome after
# converting to lowercase and removing non-alphanumeric characters.
#
# Pattern: Two Pointers — Opposite End
# Time: O(n) | Space: O(1)


class Solution:
    def isPalindrome(self, s: str) -> bool:
        # YOUR CODE HERE
        l, r = 0, len(s) - 1
        s = s.lower()  # Convert to lowercase for case-insensitive comparison
        while l<r:
            while l<r and not s[l].isalnum():
                l+=1
            while l<r and not s[r].isalnum():
                r-=1
            if s[l] != s[r]:
                return False
            l+=1
            r-=1
        return True


# ─── Test Cases ───
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("A man, a plan, a canal: Panama", True),   # classic palindrome
        ("race a car", False),                       # not a palindrome
        (" ", True),                                 # empty after cleaning
        ("a a", True),                               # single char repeated
        ("0P", False),                               # mixed digit + letter
        ("!!!", True),                               # all non-alnum → empty
        ("a", True),                                 # single character
        ("abba", True),                              # even-length palindrome
        ("abcba", True),                             # odd-length palindrome
        ("Nasan", True),                             # case-insensitive palindrome
    ]
    for i, (s, expected) in enumerate(tests):
        result = sol.isPalindrome(s)
        status = "✅" if result == expected else "❌"
        print(f"{status} Test {i+1}: isPalindrome({s!r}) = {result} (expected {expected})")
