# Encode and Decode Strings
# https://leetcode.com/problems/encode-and-decode-strings/ (Premium)
#
# Design an algorithm to encode a list of strings to a single string,
# and decode that single string back to the original list.
#
# encode(["hello","world"]) → "5#hello5#world"
# decode("5#hello5#world")  → ["hello","world"]
#
# The strings can contain ANY character, including your delimiter.
# Format: length + '#' + string for each entry.
#
# Constraints:
# - 0 <= strs.length <= 200
# - 0 <= strs[i].length <= 200
# - strs[i] contains any possible character (unicode, special chars, etc.)
#
# Write your solution below:

def encode(strs: list[str]) -> str:
    res = ""
    for  st in strs:
        res += f"{len(st)}#{st}"

    return res

def decode(s: str) -> list[str]:
    res = []
    i = 0
    while i < len(s):
        curr_str_len = ""
        # nxt_hash_after_i = s.find("#", i)
        while s[i] != '#':
            curr_str_len += s[i]
            i += 1
        curr_str_len = int(curr_str_len)
        curr_str = s[i+1:i+1+curr_str_len]
        res.append(curr_str)
        i += curr_str_len + 1

    return res


# ---- Test Cases ----
if __name__ == "__main__":
    # Basic cases
    assert decode(encode(["hello","world"])) == ["hello","world"],   "Test 1 Failed: basic"
    assert decode(encode([""])) == [""],                              "Test 2 Failed: single empty string"
    assert decode(encode([])) == [],                                  "Test 3 Failed: empty list"

    # Tricky cases — delimiter inside string
    assert decode(encode(["he#lo","wor#ld"])) == ["he#lo","wor#ld"], "Test 4 Failed: delimiter in string"
    assert decode(encode(["5#hello"])) == ["5#hello"],               "Test 5 Failed: looks like encoding"
    assert decode(encode(["","",""])) == ["","",""],                  "Test 6 Failed: multiple empty strings"

    # Edge cases
    assert decode(encode(["a"])) == ["a"],                           "Test 7 Failed: single char"
    assert decode(encode(["abc","","def"])) == ["abc","","def"],     "Test 8 Failed: empty in middle"
    assert decode(encode(["12#abc"])) == ["12#abc"],                 "Test 9 Failed: number + delimiter in string"

    print("✅ All tests passed!")
