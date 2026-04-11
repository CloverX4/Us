# Longest Repeating Character Replacement
# LeetCode 424
# Sliding Window (variable size) + Frequency Map

from collections import defaultdict

def characterReplacement(s: str, k: int) -> int:
    # TODO: Implement sliding window solution
    curr_window_freq_map = defaultdict(int)
    l = 0
    curr_window_max_freq = 0
    global_max_len = 0

    for r in range(len(s)):
        # increment the char frequency in the frequency map
        curr_window_freq_map[s[r]] += 1

        # check if current char's frequency beats current max frequency 
        curr_window_max_freq = max(curr_window_max_freq, curr_window_freq_map[s[r]])

        # if #characters to replace are more thank k - shrink the window
        # #chars to replace = window size - current window's max frequncy 
        while (r-l+1) - curr_window_max_freq > k:
            curr_window_freq_map[s[l]] -= 1
            l += 1

        # update the max globally if current window is bigger than that
        global_max_len = max(global_max_len, r-l+1)

    return global_max_len

# Example test cases
def test():
    assert characterReplacement("ABAB", 2) == 4
    assert characterReplacement("AABABBA", 1) == 4
    print("All test cases pass.")

if __name__ == "__main__":
    test()
