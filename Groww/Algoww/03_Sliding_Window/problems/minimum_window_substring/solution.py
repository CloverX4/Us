# Minimum Window Substring
# LeetCode 76
# Variable-Size Sliding Window + Frequency Map

from collections import Counter, defaultdict

def minWindow(s: str, t: str) -> str:
    # TODO: Implement solution
    if len(t) > len(s):
        return ""
    
    curr_window = s[:len(t)-1]
    t_freq_map = Counter(t)
    curr_window_freq_map = Counter(curr_window)

    matches_count = sum(1 for c in t_freq_map.keys() if t_freq_map[c] == curr_window_freq_map[c])
    l = 0
    best_l, best_r = 0, len(s)

    min_window_length = len(s)+1
    t_set_len = len(t_freq_map)

    for r in range(len(t)-1, len(s)):
        # increment the freq map count for the char
        curr_window_freq_map[s[r]] += 1

        # if the current char frequecy matches that of t, increment matches count
        if curr_window_freq_map[s[r]] == t_freq_map[s[r]]:
            matches_count += 1

                # track min window lenght at the end of the iteration
        if matches_count == t_set_len:   
            # once matches count is met, try minimizing the window until the 
            # window is invalid?? -- how do i decrement matches_count?? 
            # - check if decremented map effectd the mismatch to og map?
            while matches_count == t_set_len:
                if r-l+1 < min_window_length:
                    best_l, best_r = l, r
                    min_window_length = r-l+1
                    
                curr_window_freq_map[s[l]] -= 1
                if curr_window_freq_map[s[l]] < t_freq_map[s[l]]:
                    matches_count -= 1
                l += 1

    return s[best_l:best_r+1] if min_window_length <= len(s) else ""

            

# Test cases
def test():
    assert minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert minWindow("a", "a") == "a"
    assert minWindow("a", "aa") == ""
    assert minWindow("ab", "b") == "b"               # single char match
    assert minWindow("bba", "ab") == "ba"             # minimal at end
    assert minWindow("abc", "cba") == "abc"           # full string is the window
    print("All test cases pass.")

if __name__ == "__main__":
    test()
