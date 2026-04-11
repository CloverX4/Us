# Valid Anagram
# https://leetcode.com/problems/valid-anagram/
#
# Given two strings s and t, return true if t is an anagram of s,
# and false otherwise.
#
# An anagram uses the exact same characters the exact same number
# of times, just rearranged.
#
# Example 1: s = "anagram", t = "nagaram" → true
# Example 2: s = "rat", t = "car" → false
#
# Constraints:
# - 1 <= s.length, t.length <= 5 * 10^4
# - s and t consist of lowercase English letters
#
# Write your solution below:

def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    if s == t:
        return True
    
    res = {}

    for i in range(len(s)):
        res[s[i]] = res.get(s[i], 0) + 1
        res[t[i]] = res.get(t[i], 0) - 1

    for ltr in res:
        if (res[ltr] != 0):
            return False
        
    return True


# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert isAnagram("anagram", "nagaram") == True,  "Test 1 Failed: basic anagram"
    assert isAnagram("rat", "car") == False,          "Test 2 Failed: not anagram"

    # Edge cases
    assert isAnagram("a", "a") == True,               "Test 3 Failed: single char, same"
    assert isAnagram("a", "b") == False,              "Test 4 Failed: single char, different"
    assert isAnagram("ab", "a") == False,             "Test 5 Failed: different lengths"
    assert isAnagram("", "") == True,                 "Test 6 Failed: empty strings"

    # Tricky cases
    assert isAnagram("aacc", "ccac") == False,        "Test 7 Failed: same chars, wrong counts"
    assert isAnagram("aabbcc", "abcabc") == True,     "Test 8 Failed: multi-char anagram"
    assert isAnagram("ab", "ba") == True,             "Test 9 Failed: simple swap"

    print("✅ All tests passed!")
