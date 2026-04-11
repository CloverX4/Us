# Valid Anagram — Notes

## Pattern Used
**Frequency Counting** — single-pass with +1/-1 in a shared map

## Key Insight
Instead of two separate frequency maps, use ONE map: increment for `s`, decrement for `t`. If all values are 0 at the end → anagram.

## Approaches Discussed
| # | Approach | Time | Space | Notes |
|---|---------|------|-------|-------|
| 1 | Sort both, compare | O(n log n) | O(n)* | Simple but slower |
| 2 | Two Counters, compare with == | O(n) | O(n) | Pythonic, `Counter(s) == Counter(t)` |
| 3 | Single map +1/-1 (implemented) | O(n) | O(n) | Shows understanding, single pass |

*Depends on sort implementation

## Things to Remember
- **Early exit**: Check `len(s) != len(t)` first — O(1) elimination
- `dict.get(key, 0)` to avoid KeyError on missing keys
- `defaultdict(int)` is another option — auto-initializes to 0
- `all(v == 0 for v in res.values())` — Pythonic alternative to loop check
- Space is technically O(1) since only 26 lowercase letters (bounded alphabet) — mention in interview!
- `all()` returns True if all elements truthy, `any()` if any truthy — useful everywhere

## Bugs Caught During Session
- Initial version used `res[s[i]] + 1` without handling missing keys → KeyError
- Fixed with `.get(key, 0)`
 
## Complexity
- **Time**: O(n)
- **Space**: O(1) if bounded alphabet (26 letters), O(n) in general
