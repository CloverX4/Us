# 🐍 Python Fluency — Interview Quick Reference

> Scan this before every session. These are the landmines that trip you up repeatedly.
> Not algorithm theory — pure Python gotchas and tricks.

---

## ⚠️ The Landmines (Things That Have Bitten You)

| Gotcha | Wrong | Right | Why |
|--------|-------|-------|-----|
| `.sort()` / `.reverse()` return None | `a = lst.sort()` → a is None | `lst.sort()` (in-place, discard return) OR `a = sorted(lst)` | In-place methods return None. Always. |
| String `.append()` doesn't exist | `s.append('x')` | `s += 'x'` or build a list then `''.join(lst)` | Strings are immutable. No in-place mutation. |
| `str.join()` call order | `lst.join(',')` | `','.join(lst)` | Separator is the object. List is the argument. |
| Lists can't be dict keys | `d[['a','b']] = 1` | `d[('a','b')] = 1` | Only hashable types as keys. Lists → tuples. |
| `while` loop needs manual increment | `while i < n: do_thing()` → infinite | `while i < n: do_thing(); i += 1` | `for` manages it. `while` doesn't. |
| Dict missing key KeyError | `d[key] += 1` on new key | `d.get(key, 0) + 1` or `defaultdict(int)` | Always guard against missing keys. |
| `while i in range(n)` is wrong | `while i in range(n)` | `while i < n` | `in range()` is a membership check, not iteration. |
| Mutating function parameter | `k = k // 2` when k is a param | Use a new variable: `size = k // 2` | Mutating params is confusing. Don't. |

---

## 🔧 The Toolkit (Reach for These Automatically)

### Collections
```python
from collections import defaultdict, Counter, deque

defaultdict(int)      # dict where missing keys default to 0
defaultdict(list)     # dict where missing keys default to []
Counter(iterable)     # frequency map, e.g. Counter("aabbc") → {'a':2,'b':2,'c':1}
deque()               # O(1) append and popleft (use instead of list for queues)
```

### Heap
```python
import heapq

heapq.heapify(lst)          # min-heap in-place, O(n)
heapq.heappush(heap, val)   # push, O(log n)
heapq.heappop(heap)         # pop min, O(log n)

# Max-heap trick: negate values
heapq.heappush(heap, -val)
max_val = -heapq.heappop(heap)

# k largest elements
heapq.nlargest(k, lst)      # O(n log k)
```

### Sorting
```python
sorted(lst)                        # returns new list, original unchanged
sorted(lst, reverse=True)          # descending
sorted(lst, key=lambda x: x[1])    # sort by second element
lst.sort()                         # in-place, returns None
```

### Strings
```python
s.isalnum()     # True if alphanumeric
s.isalpha()     # True if all letters
s.isdigit()     # True if all digits
s.lower()       # new string (doesn't mutate)
s.upper()       # new string
s.split()       # split on whitespace
s.split(',')    # split on delimiter
''.join(lst)    # join list of chars into string — use this to build strings
ord('a')        # → 97
chr(97)         # → 'a'
ord(ch) - ord('a')  # 0-indexed alphabet position
```

### Useful Builtins
```python
float('inf')     # positive infinity (use for min tracking init)
float('-inf')    # negative infinity (use for max tracking init)
math.inf         # same thing (need import math)

all(iterable)    # True if all elements are truthy
any(iterable)    # True if any element is truthy

enumerate(lst)         # (index, value) pairs
enumerate(lst, start=1)  # start index at 1

zip(lst1, lst2)        # pair elements together
zip(*matrix)           # transpose a matrix

abs(x)           # absolute value
divmod(a, b)     # returns (quotient, remainder) — replaces a//b and a%b

# Swap without temp
a, b = b, a
```

### List / Array Tricks
```python
lst[::-1]           # reverse (new list)
lst[i:j]            # slice [i, j)
[0] * n             # list of n zeros
[[0]*cols for _ in range(rows)]   # 2D array (NOT [[0]*cols]*rows — shared refs!)

# Range patterns
range(n)            # 0 to n-1
range(a, b)         # a to b-1
range(a, b, step)   # a to b-1 with step
range(n-1, -1, -1)  # n-1 down to 0 (reverse)
range(0, n, 3)      # 0, 3, 6, 9... (tiled iteration)
```

### Dict / Set
```python
d = {}
d.get(key, default)           # safe get with fallback
d.setdefault(key, []).append  # get or create

s = set()
s.add(x)
s.discard(x)    # remove if present, no error if not (vs .remove() which raises)
x in s          # O(1) lookup

# Set operations
a | b    # union
a & b    # intersection
a - b    # difference (in a but not b)
a ^ b    # symmetric difference
```

---

## 🎯 Interview-Specific Patterns

### Initializing tracking variables
```python
min_val = float('inf')    # tracking minimum → init to infinity
max_val = float('-inf')   # tracking maximum → init to negative infinity
result = []               # collecting results → init to empty list
count = 0                 # counting → init to 0
```

### Two Sum / Complement pattern
```python
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i          # store AFTER check (handles target=0, same element)
```

### Frequency map boilerplate
```python
freq = Counter(s)          # shorthand
# OR manual:
freq = defaultdict(int)
for ch in s:
    freq[ch] += 1
```

### Sliding window (variable) boilerplate
```python
l = 0
for r in range(len(s)):    # r is ALWAYS the outer loop driver
    # expand: add s[r] to window state
    while window_is_invalid():
        # shrink: remove s[l] from window state
        l += 1
    # update result with current window [l..r]
```

### Sliding window (fixed size k) boilerplate
```python
# Build first window
for i in range(k):
    # add nums[i] to window

for i in range(k, len(nums)):
    # add nums[i] (new right)
    # remove nums[i-k] (old left)
    # update result
```

---

## 🔢 Complexity Cheat (when asked in interview)

| n ≤ | Max complexity | Think |
|-----|---------------|-------|
| 20 | O(2ⁿ) or O(n!) | Backtracking, bitmask |
| 100 | O(n³) | Triple nested loop |
| 1,000 | O(n²) | Double nested loop |
| 10⁵ | O(n log n) | Sort, heap, binary search |
| 10⁶+ | O(n) | Single pass, sliding window, hashing |

---

*Updated as new gotchas are discovered during sessions*
