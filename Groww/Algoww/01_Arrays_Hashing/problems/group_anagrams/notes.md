# Group Anagrams — Notes

## Pattern Used
**Sorted Key HashMap** — use a canonical form of each string as the grouping key

## Key Insight
All anagrams, when sorted, produce the same string. Use that sorted string as a dictionary key to group them.

## Two Approaches
| # | Approach | Key | Time | Space |
|---|---------|-----|------|-------|
| 1 | Sorted string key | `"".join(sorted(word))` | O(n × k log k) | O(n × k) |
| 2 | Frequency tuple key | `tuple(count_array)` | O(n × k) | O(n × k) |

Where n = number of strings, k = max string length.

## Things to Remember
- Lists can't be dict keys (unhashable/mutable) → use `tuple()` or `"".join()`
- `defaultdict(list)` — auto-creates empty list for new keys, cleaner than manual checking
- `ord(ch) - ord('a')` — maps letters to 0-25 indices. Memorize this.
- When problem has two dimensions (n items, k size each) — use **two variables** in complexity, not just "O(n)"
- Sorted approach works universally (any characters). Frequency tuple assumes known alphabet (26 lowercase).
- Constraints say lowercase English letters → both approaches valid here

## Complexity (sorted approach — implemented)
- **Time**: O(n × k log k) — n strings, each sorted in k log k
- **Space**: O(n × k) — storing all strings + sorted keys in hashmap
