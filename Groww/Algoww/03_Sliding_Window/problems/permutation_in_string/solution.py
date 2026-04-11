# Permutation in String
# LeetCode 567
# Fixed-Size Sliding Window + Frequency Map

from collections import defaultdict,Counter

def checkInclusion(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    
    s1_freq_map = Counter(s1)
    # initialize the frequency map for the first window (size of s1 - 1) in s2
    curr_window_freq_map = Counter(s2[:len(s1)-1])

    matches_count = sum(1 for c in "abcdefghijklmnopqrstuvwxyz" if s1_freq_map[c] == curr_window_freq_map[c])
    window_size = len(s1)

    for r in range(window_size-1, len(s2)):
        if curr_window_freq_map[s2[r]] == s1_freq_map[s2[r]]:
            matches_count -= 1

        # expand 1 on right
        curr_window_freq_map[s2[r]] += 1

        if curr_window_freq_map[s2[r]] == s1_freq_map[s2[r]]:
            matches_count += 1

        # if frequency maps mathc, early return true
        if matches_count == 26:
            return True
        
        #shrink l by 1, so the r expands in next iteration and result in window size as len(s1)
        curr_window_freq_map[s2[r-window_size+1]] -= 1

        # mhmm remember this deatil, counter directly ignored 0 counts in the comparison, 
        # No need to handle it here, but yep a point to remember 
        # if curr_window_freq_map[s2[r-window_size+1]] == 0:
        #     del curr_window_freq_map[s2[r-window_size+1]]
        
    return False

def checkInclusion_v2(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    
    s1_freq_map = Counter(s1)
    # initialize the frequency map for the first window (size of s1 - 1) in s2
    curr_window_freq_map = Counter(s2[:len(s1)-1])

    for r in range(len(s1)-1, len(s2)):
        # expand 1 on right
        curr_window_freq_map[s2[r]] += 1

        # if frequency maps mathc, early return true
        if s1_freq_map == curr_window_freq_map:
            return True
        
        #shrink l by 1, so the r expands in next iteration and result in window size as len(s1)
        curr_window_freq_map[s2[r-len(s1)+1]] -= 1

        # mhmm remember this deatil, counter directly ignored 0 counts in the comparison, 
        # No need to handle it here, but yep a point to remember 
        if curr_window_freq_map[s2[r-len(s1)+1]] == 0:
            del curr_window_freq_map[s2[r-len(s1)+1]]
        
    return False

def checkInclusion_v1(s1: str, s2: str) -> bool:
    if len(s1) > len(s2):
        return False
    
    s1_freq_map = Counter(s1)
    for r in range(len(s1)-1, len(s2)):
        curr_window_freq_map = Counter(s2[r-len(s1)+1:r+1])
        if curr_window_freq_map == s1_freq_map:
            return True
        
    return False

# Test cases
def test():
    assert checkInclusion("ab", "eidbaooo") == True
    assert checkInclusion("ab", "eidboaoo") == False
    assert checkInclusion("a", "a") == True
    assert checkInclusion("ab", "a") == False       # s1 longer than s2
    assert checkInclusion("adc", "dcda") == True     # permutation at end
    assert checkInclusion("ab", "ab") == True        # exact match
    print("All test cases pass.")

if __name__ == "__main__":
    test()
