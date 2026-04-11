# Longest Substring Without Repeating Characters
# https://leetcode.com/problems/longest-substring-without-repeating-characters/
#
# Given a string s, find the length of the longest substring
# without repeating characters.
#
# Example 1: Input: s = "abcabcbb" → Output: 3 ("abc")
# Example 2: Input: s = "bbbbb" → Output: 1 ("b")
# Example 3: Input: s = "pwwkew" → Output: 3 ("wke")
#
# Constraints:
# - 0 <= s.length <= 5 * 10^4
# - s consists of English letters, digits, symbols and spaces


def length_of_longest_substring(s: str) -> int:
    current_window_chars = set()
    l = 0
    max_length = 0

    for r in range(len(s)):
        while s[r] in current_window_chars:
            current_window_chars.remove(s[l])
            l += 1

        current_window_chars.add(s[r])
        max_length = max(max_length, r - l + 1)

    return max_length


# --- OLD ATTEMPT (Day 6, March 10 — before learning sliding window template) ---
# Bug: l was the outer loop driver instead of r, causing r to get stuck.
# Kept for tracking growth.
def length_of_longest_substring_old(s: str) -> int:
    has_char = set()
    global_max = 0
    l, r = 0, 1

    while l<r and r < len(s):
        if s[l] not in has_char:
            has_char.add(s[l])
        while s[r] not in has_char and r < len(s):
            has_char.add(s[r])
            r += 1

        global_max = max(global_max, r-l)
        has_char.remove(s[l])
        l += 1
        
    return global_max


if __name__ == "__main__":
    # Basic examples
    assert length_of_longest_substring("abcabcbb") == 3, "abc is longest"
    assert length_of_longest_substring("bbbbb") == 1, "all same char"
    assert length_of_longest_substring("pwwkew") == 3, "wke is longest"

    # Edge cases
    assert length_of_longest_substring("") == 0, "empty string"
    assert length_of_longest_substring(" ") == 1, "single space"
    assert length_of_longest_substring("a") == 1, "single char"

    # Tricky cases
    assert length_of_longest_substring("abcdef") == 6, "all unique"
    assert length_of_longest_substring("aab") == 2, "duplicate at start, 'ab' is longest"
    assert length_of_longest_substring("dvdf") == 3, "tricky — 'vdf' not 'dv', must shrink past first d"
    assert length_of_longest_substring("tmmzuxt") == 5, "mzuxt — window resets mid-string"
    assert length_of_longest_substring("aa") == 1, "two same chars"

    print("✅ All tests passed!")
