# Contains Duplicate — Notes

## Pattern Used
**Set for O(1) existence checking**

## Key Insight
Before adding each element to the set, check if it already exists. If yes → duplicate found.

## Approaches Discussed
| # | Approach | Time | Space | Notes |
|---|---------|------|-------|-------|
| 1 | Brute force (two loops) | O(n²) | O(1) | Check every pair |
| 2 | Sort + adjacent check | O(n log n) | O(1)* | *Modifies input |
| 3 | Hash set (optimal) | O(n) | O(n) | Early exit on first dup |
| 4 | One-liner: `len(nums) != len(set(nums))` | O(n) | O(n) | No early exit |

## Things to Remember
- Always mention **both time AND space** complexity
- Loop version has early exit advantage over the one-liner
- Same set-for-existence pattern shows up in: BFS/DFS visited tracking, Longest Consecutive Sequence
- Edge cases: empty array → false, single element → false

## Complexity
- **Time**: O(n) worst, O(1) best (early exit)
- **Space**: O(n)
